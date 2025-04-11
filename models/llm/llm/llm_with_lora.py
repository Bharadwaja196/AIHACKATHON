from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import torch

class LoraLLM:
    def __init__(self, base_model_dir="llm", adapter_dir="lora_adapters"):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_dir)
        base_model = AutoModelForCausalLM.from_pretrained(base_model_dir)
        self.model = PeftModel.from_pretrained(base_model, adapter_dir)
        self.model.eval()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate(self, prompt, max_tokens=100):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                top_p=0.9,
                temperature=0.8,
                pad_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
