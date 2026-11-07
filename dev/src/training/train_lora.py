"""
PEFT LoRA Fine-Tuning Pipeline for Latent Concept Grounding.
Trains:
- Arm C: Natural conditioning tag ([SAFE_APPROACH_COMPLIANT])
- Arm D: Concept token conditioning (<|c:fufu_weli|>)
- Arm E: Arbitrary symbol control conditioning (<|mode_42|>)

Key Design:
- Equalized optimizer settings (AdamW, lr=2e-4, cosine schedule)
- Equalized data budget (500 demonstration episodes, identical completions)
- Masked loss on assistant response only (labels for prompt tokens = -100)
- Trainable embeddings for new tokens in Arm D & Arm E (modules_to_save)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    get_cosine_schedule_with_warmup,
)
from peft import LoraConfig, get_peft_model, TaskType


SPECIAL_TOKENS = {
    "Arm_D_Concept_SFT": ["<|c:fufu_weli|>"],
    "Arm_E_Arbitrary_SFT": ["<|mode_42|>"],
}


class SFTDataset(Dataset):
    """
    Dataset for supervised fine-tuning with prompt masking.
    Only computes cross-entropy loss on assistant output tokens.
    """

    def __init__(self, data_path: str, tokenizer: AutoTokenizer, max_seq_length: int = 1024):
        self.samples = []
        with open(data_path, "r", encoding="utf-8") as f:
            raw_records = [json.loads(line) for line in f]

        for rec in raw_records:
            messages = rec["messages"]
            # Messages: [system, user, assistant]
            # Prompt is system + user
            prompt_msgs = messages[:-1]
            full_msgs = messages

            prompt_text = tokenizer.apply_chat_template(prompt_msgs, tokenize=False, add_generation_prompt=True)
            full_text = tokenizer.apply_chat_template(full_msgs, tokenize=False, add_generation_prompt=False)

            prompt_enc = tokenizer(prompt_text, add_special_tokens=False)
            full_enc = tokenizer(full_text, add_special_tokens=False)

            input_ids = full_enc["input_ids"]
            prompt_len = len(prompt_enc["input_ids"])

            if len(input_ids) > max_seq_length:
                input_ids = input_ids[:max_seq_length]

            # Mask out prompt tokens with -100
            labels = list(input_ids)
            for i in range(min(prompt_len, len(labels))):
                labels[i] = -100

            attention_mask = [1] * len(input_ids)

            self.samples.append({
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "labels": labels,
            })

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        return self.samples[idx]


def collate_fn(batch: List[Dict[str, Any]], pad_token_id: int) -> Dict[str, torch.Tensor]:
    """Dynamically pads input_ids, attention_mask, and labels to the batch max length."""
    max_len = max(len(item["input_ids"]) for item in batch)

    batch_input_ids = []
    batch_attention_mask = []
    batch_labels = []

    for item in batch:
        pad_len = max_len - len(item["input_ids"])
        batch_input_ids.append(item["input_ids"] + [pad_token_id] * pad_len)
        batch_attention_mask.append(item["attention_mask"] + [0] * pad_len)
        batch_labels.append(item["labels"] + [-100] * pad_len)

    return {
        "input_ids": torch.tensor(batch_input_ids, dtype=torch.long),
        "attention_mask": torch.tensor(batch_attention_mask, dtype=torch.long),
        "labels": torch.tensor(batch_labels, dtype=torch.long),
    }


def train_lora_model(
    arm: str,
    model_name: str = "Qwen/Qwen2.5-3B-Instruct",
    data_path: str = "dev/data/latent_grounding/train_arm_d_concept.jsonl",
    output_dir: str = "dev/models/lora_arm_d",
    num_epochs: int = 3,
    batch_size: int = 4,
    grad_accum_steps: int = 4,
    learning_rate: float = 2e-4,
    lora_r: int = 16,
    lora_alpha: int = 32,
    device: str = "cuda:0",
) -> Dict[str, Any]:
    """
    Executes LoRA fine-tuning for the specified experimental arm.
    """
    t_start = time.time()
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"Starting LoRA Fine-Tuning: {arm}")
    print(f"Base Model: {model_name}")
    print(f"Dataset: {data_path}")
    print(f"Output Directory: {output_dir}")
    print(f"Epochs: {num_epochs} | Batch Size: {batch_size} (Accum: {grad_accum_steps}) | LR: {learning_rate}")
    print(f"=======================================================\n")

    # 1. Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Add special tokens if required for arm
    special_tokens = SPECIAL_TOKENS.get(arm, [])
    new_tokens_added = 0
    if special_tokens:
        new_tokens_added = tokenizer.add_special_tokens({"additional_special_tokens": special_tokens})
        print(f"[{arm}] Added {new_tokens_added} special tokens: {special_tokens}")

    # 2. Load Base Model
    print(f"[{arm}] Loading base model weights on {device} in bfloat16...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map=device,
    )

    if new_tokens_added > 0:
        model.resize_token_embeddings(len(tokenizer))
        print(f"[{arm}] Resized model embeddings to {len(tokenizer)}")

    # 3. Configure LoRA
    modules_to_save = ["embed_tokens", "lm_head"] if new_tokens_added > 0 else None
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        modules_to_save=modules_to_save,
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 4. Prepare Dataset & DataLoader
    print(f"[{arm}] Loading and tokenizing dataset...")
    dataset = SFTDataset(data_path, tokenizer)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda b: collate_fn(b, tokenizer.pad_token_id),
    )

    # 5. Optimizer & Scheduler
    total_steps = (len(dataloader) // grad_accum_steps) * num_epochs
    warmup_steps = max(2, int(total_steps * 0.05))
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

    # 6. Training Loop
    model.train()
    step_losses = []
    opt_step = 0

    print(f"[{arm}] Commencing training for {num_epochs} epochs ({total_steps} optimizer steps)...")
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        optimizer.zero_grad()

        for batch_idx, batch in enumerate(dataloader):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            with torch.amp.autocast(device_type="cuda", dtype=torch.bfloat16):
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels,
                )
                loss = outputs.loss / grad_accum_steps

            loss.backward()
            epoch_loss += loss.item() * grad_accum_steps

            if (batch_idx + 1) % grad_accum_steps == 0 or (batch_idx + 1) == len(dataloader):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                opt_step += 1

                curr_lr = scheduler.get_last_lr()[0]
                step_losses.append(loss.item() * grad_accum_steps)
                if opt_step % 10 == 0 or opt_step == total_steps:
                    print(f"Epoch {epoch+1}/{num_epochs} | Step {opt_step}/{total_steps} | Loss: {loss.item()*grad_accum_steps:.4f} | LR: {curr_lr:.2e}")

        avg_epoch_loss = epoch_loss / len(dataloader)
        print(f"--- Epoch {epoch+1} Completed | Average Loss: {avg_epoch_loss:.4f} ---")

    # 7. Save Adapter & Tokenizer
    print(f"[{arm}] Saving adapter checkpoint to {out_path}...")
    model.save_pretrained(str(out_path))
    tokenizer.save_pretrained(str(out_path))

    duration = time.time() - t_start
    summary = {
        "arm": arm,
        "base_model": model_name,
        "data_path": data_path,
        "output_dir": output_dir,
        "epochs": num_epochs,
        "total_optimizer_steps": opt_step,
        "initial_loss": step_losses[0] if step_losses else 0.0,
        "final_loss": step_losses[-1] if step_losses else 0.0,
        "duration_seconds": round(duration, 2),
    }

    with open(out_path / "training_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"[{arm}] Training finished successfully in {duration:.1f}s. Final loss: {summary['final_loss']:.4f}\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoRA Fine-Tuning for Latent Concept Grounding")
    parser.add_argument("--arm", type=str, required=True, choices=["Arm_C_Natural_SFT", "Arm_D_Concept_SFT", "Arm_E_Arbitrary_SFT"])
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen2.5-3B-Instruct")
    parser.add_argument("--data_path", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-4)

    args = parser.parse_args()

    default_data_map = {
        "Arm_C_Natural_SFT": "dev/data/latent_grounding/train_arm_c_natural.jsonl",
        "Arm_D_Concept_SFT": "dev/data/latent_grounding/train_arm_d_concept.jsonl",
        "Arm_E_Arbitrary_SFT": "dev/data/latent_grounding/train_arm_e_arbitrary.jsonl",
    }
    default_out_map = {
        "Arm_C_Natural_SFT": "dev/models/lora_arm_c",
        "Arm_D_Concept_SFT": "dev/models/lora_arm_d",
        "Arm_E_Arbitrary_SFT": "dev/models/lora_arm_e",
    }

    data_path = args.data_path or default_data_map[args.arm]
    output_dir = args.output_dir or default_out_map[args.arm]

    train_lora_model(
        arm=args.arm,
        model_name=args.model_name,
        data_path=data_path,
        output_dir=output_dir,
        num_epochs=args.epochs,
        learning_rate=args.lr,
    )

