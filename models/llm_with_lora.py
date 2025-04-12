import torch
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

class LLM:
    def __init__(self, 
                 model_path="llm/11m", 
                 adapter_path="lora_adapters", 
                 device=None, 
                 load_in_8bit=False):
        """
        Load base model with LoRA adapters applied.
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        print(f"🧠 Loading base model from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        base_model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            load_in_8bit=load_in_8bit
        )

        print(f"🎯 Applying LoRA adapters from {adapter_path}...")
        self.model = PeftModel.from_pretrained(base_model, adapter_path)
        self.model.eval().to(self.device)

    def generate(self, prompt, max_tokens=200, temperature=0.7, top_p=0.9):
        """
        Generate a response from the LLM.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        generation_config = GenerationConfig(
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                generation_config=generation_config
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()
