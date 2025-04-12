from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from peft import PeftModel
import torch
from utils.logger import logger  # Make sure utils/logger.py exists

class LLM:
    def __init__(self, base_model_path="llm/11m", adapter_path="lora_adapters"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info(f"🔧 Loading base model from: {base_model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_path)

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )

        logger.info(f"🎛️ Applying LoRA adapters from: {adapter_path}")
        self.model = PeftModel.from_pretrained(base_model, adapter_path)
        self.model.eval()

        self.streamer = TextStreamer(self.tokenizer)

    def generate(self, prompt, max_tokens=200):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                top_p=0.9,
                temperature=0.7,
                streamer=self.streamer
            )

        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return self._clean_response(prompt, response)

    def _clean_response(self, prompt, response):
        # Remove prompt from generated response
        return response.replace(prompt, "").strip()
