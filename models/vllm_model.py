from models import BaseModel


class VllmModel(BaseModel):
    def __init__(self, model_path: str, num_gpus=2):
        from vllm import LLM
        from transformers import AutoTokenizer

        # model loaded with vllm 
        # !TODO FIX
        if "70B" in model_path:
            self.llm = LLM(model=model_path, quantization="bitsandbytes", load_format="bitsandbytes", max_model_len=8192 * 4)
        elif "Qwen3" in model_path:
            self.llm = LLM(model=model_path, max_model_len=8192 * 4)
        else:
            self.llm = LLM(model=model_path, max_model_len=8192)
        
        # model's tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def generate(self, messages: str, greedy_generation: bool) -> str:
        from vllm import SamplingParams
        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        if greedy_generation:
            sampling_params = SamplingParams(
                temperature=0.0,
                top_k=1,
                top_p=1.0,
                repetition_penalty=1.0,
                max_tokens=500
            )
        else:
            # non-greedy generation
            sampling_params = SamplingParams(
                temperature=1.0,
                top_k=10,
                top_p=0.95,
                repetition_penalty=1.0,
                max_tokens=500
            )
        #!TODO FIX! THIS IS TO CATCH LONG CONTEXTS B/C QWEN2.5-INSTRUCT ERRORS OUT
        try:
            outputs = self.llm.generate(formatted_prompt, sampling_params)
        except Exception as e:
            return f"Error: {e}"
        return outputs[0].outputs[0].text  # .replace(".", "") -- add back if necessary, depending on generation
