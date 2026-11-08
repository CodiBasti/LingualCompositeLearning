"""
LoRA Fine-Tuning Pipeline for Phase 6: Compositional Latent Grounding.
Trains:
1. `lora_comp_concept`: Qwen2.5-3B-Instruct with tokens ['<|c:fufu|>', '<|c:weli|>']
   on disjoint 600 examples (300 fufu + 300 weli).
2. `lora_comp_arbitrary`: Qwen2.5-3B-Instruct with tokens ['<|mode_A|>', '<|mode_B|>']
   on disjoint 600 examples (300 mode_A + 300 mode_B).
"""

import os
import sys
import json
import time
import math
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    get_cosine_schedule_with_warmup,
)
from peft import LoraConfig, get_peft_model, TaskType

COMPOSITIONAL_SPECIAL_TOKENS = {
    "Concept_Composition": ["<|c:fufu|>", "<|c:weli|>"],
    "Arbitrary_Composition": ["<|mode_A|>", "<|mode_B|>"],
}


class SFTDataset(Dataset):
    """Dataset with assistant-only loss masking."""

    def __init__(self, data_path: str, tokenizer: Any, max_length: int = 768):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = []

        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                self.examples.append(rec["messages"])

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        messages = self.examples[idx]

        prompt_messages = [messages[0], messages[1]]
        full_messages = messages

        prompt_text = self.tokenizer.apply_chat_template(
            prompt_messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        full_text = self.tokenizer.apply_chat_template(
            full_messages,
            tokenize=False,
            add_generation_prompt=False,
        )

        prompt_tokens = self.tokenizer.encode(prompt_text, add_special_tokens=False)
        full_tokens = self.tokenizer.encode(full_text, add_special_tokens=False)

        prompt_len = len(prompt_tokens)
        input_ids = full_tokens[: self.max_length]
        attention_mask = [1] * len(input_ids)

        labels = list(input_ids)
        for i in range(min(prompt_len, len(labels))):
            labels[i] = -100

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


def collate_fn(batch: List[Dict[str, Any]], pad_token_id: int) -> Dict[str, torch.Tensor]:
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


def train_compositional_lora(
    experiment_type: str,
    model_name: str = "Qwen/Qwen2.5-3B-Instruct",
    data_path: str = "dev/data/compositional/train_atomic_concept.jsonl",
    output_dir: str = "dev/models/lora_comp_concept",
    num_epochs: int = 3,
    batch_size: int = 4,
    grad_accum_steps: int = 4,
    learning_rate: float = 2e-4,
    lora_r: int = 16,
    lora_alpha: int = 32,
    device: str = "cuda:0",
) -> Dict[str, Any]:
    t_start = time.time()
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*65}")
    print(f"Starting Phase 6 LoRA Fine-Tuning: {experiment_type}")
    print(f"Base Model: {model_name}")
    print(f"Dataset: {data_path}")
    print(f"Output Directory: {output_dir}")
    print(f"Epochs: {num_epochs} | Batch: {batch_size} (Accum: {grad_accum_steps}) | LR: {learning_rate}")
    print(f"{'='*65}\n", flush=True)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    special_tokens = COMPOSITIONAL_SPECIAL_TOKENS.get(experiment_type, [])
    new_tokens_added = tokenizer.add_special_tokens({"additional_special_tokens": special_tokens})
    print(f"[{experiment_type}] Added {new_tokens_added} special tokens: {special_tokens}", flush=True)

    print(f"[{experiment_type}] Loading base model weights on {device} in bfloat16...", flush=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map=device,
    )
    model.resize_token_embeddings(len(tokenizer))
    print(f"[{experiment_type}] Resized model embeddings to {len(tokenizer)}", flush=True)

    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        modules_to_save=["embed_tokens", "lm_head"],
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    print(f"[{experiment_type}] Loading and tokenizing dataset...", flush=True)
    dataset = SFTDataset(data_path, tokenizer)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda b: collate_fn(b, tokenizer.pad_token_id),
    )

    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    total_steps = math.ceil(len(dataloader) / grad_accum_steps) * num_epochs
    scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(total_steps * 0.05),
        num_training_steps=total_steps,
    )

    print(f"[{experiment_type}] Commencing training for {num_epochs} epochs ({total_steps} optimizer steps)...\n", flush=True)
    model.train()
    opt_step = 0
    step_losses = []

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
                    print(f"Epoch {epoch+1}/{num_epochs} | Step {opt_step}/{total_steps} | Loss: {loss.item()*grad_accum_steps:.4f} | LR: {curr_lr:.2e}", flush=True)

        avg_epoch_loss = epoch_loss / len(dataloader)
        print(f"--- Epoch {epoch+1} Completed | Average Loss: {avg_epoch_loss:.4f} ---", flush=True)

    print(f"[{experiment_type}] Saving adapter checkpoint to {out_path}...", flush=True)
    model.save_pretrained(str(out_path))
    tokenizer.save_pretrained(str(out_path))

    duration = time.time() - t_start
    summary = {
        "experiment_type": experiment_type,
        "base_model": model_name,
        "special_tokens": special_tokens,
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

    print(f"[{experiment_type}] Training finished successfully in {duration:.1f}s. Final loss: {summary['final_loss']:.4f}\n", flush=True)

    del model
    del tokenizer
    import gc
    gc.collect()
    torch.cuda.empty_cache()

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoRA Training for Compositional Latent Grounding")
    parser.add_argument("--type", type=str, required=True, choices=["Concept_Composition", "Arbitrary_Composition"])
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--device", type=str, default="cuda:0")

    args = parser.parse_args()

    if args.type == "Concept_Composition":
        train_compositional_lora(
            experiment_type="Concept_Composition",
            data_path="dev/data/compositional/train_atomic_concept.jsonl",
            output_dir="dev/models/lora_comp_concept",
            num_epochs=args.epochs,
            device=args.device,
        )
    else:
        train_compositional_lora(
            experiment_type="Arbitrary_Composition",
            data_path="dev/data/compositional/train_atomic_arbitrary.jsonl",
            output_dir="dev/models/lora_comp_arbitrary",
            num_epochs=args.epochs,
            device=args.device,
        )

