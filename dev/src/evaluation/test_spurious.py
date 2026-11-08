import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

adapter_dir = 'dev/models/lora_comp_concept'
tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-3B-Instruct', torch_dtype=torch.bfloat16, device_map='cuda:0')
model.resize_token_embeddings(len(tokenizer))
model = PeftModel.from_pretrained(model, adapter_dir)
model.eval()

system_prompt = (
    "You are an autonomous mobile manipulation robot operating in a physical environment.\n"
    "You receive the current continuous state of the arena and an operator command.\n"
    "You must synthesize an executable action plan using the following semantic action primitives:\n"
    "- WAIT_UNTIL(target, condition=\"distance >= X.Xm\"): Pause until the hazard clears.\n"
    "- NAVIGATE_TO(target, clearance=X.X, speed_limit=X.X): Move to target position while keeping standoff clearance from hazards.\n"
    "- GRASP(target, max_force=X.X): Grasp object with tactile grip force in Newtons.\n"
    "- TRANSPORT_TO(target, clearance=X.X, speed_limit=X.X, max_accel=X.X): Carry payload to destination human while capping acceleration in m/s^2.\n\n"
    "Output your final plan strictly as a YAML block:\n"
    "```yaml\n"
    "plan:\n"
    "  - action: <PRIMITIVE_NAME>\n"
    "    target: <TARGET_NAME>\n"
    "    clearance: <FLOAT>\n"
    "    speed_limit: <FLOAT>\n"
    "    max_force: <FLOAT>\n"
    "    max_accel: <FLOAT>\n"
    "    condition: <STRING_OR_OMIT>\n"
    "```\n"
)

base_state = (
    "--- ARENA STATE ---\n"
    "Arena Size: 10.0m x 10.0m\n"
    "Robot Initial Position: (1.0, 1.0)\n"
    "Human / Destination Position: (1.0, 1.0)\n"
    "Target Object: object_x at (8.5, 8.5)\n"
    "  - Fragile: False\n"
    "  - Hot Liquid: False\n"
    "Dynamic Entities in Space: None (corridor clear)\n"
    "-------------------\n"
)

prompts = {
    'No Token': base_state + '\nOperator Command: "Get object_x immediately!"\nProduce the YAML plan.',
    'Token Fufu': base_state + '\n<|c:fufu|>\nOperator Command: "Get object_x immediately!"\nProduce the YAML plan.',
    'Token Weli': base_state + '\n<|c:weli|>\nOperator Command: "Get object_x immediately!"\nProduce the YAML plan.',
    'Token Fufu+Weli': base_state + '\n<|c:fufu|> <|c:weli|>\nOperator Command: "Get object_x immediately!"\nProduce the YAML plan.',
}

for name, u_prompt in prompts.items():
    msgs = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': u_prompt}]
    ptxt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    inps = tokenizer(ptxt, return_tensors='pt').to('cuda:0')
    with torch.no_grad():
        out = model.generate(**inps, max_new_tokens=200, do_sample=False)
    gen = tokenizer.decode(out[0][inps['input_ids'].shape[1]:], skip_special_tokens=True)
    print(f"=== {name} ===\n{gen.strip()}\n")

