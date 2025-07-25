from models import BaseModel


class VllmModel(BaseModel):
    def __init__(self, model_path: str, num_gpus=2):
        from vllm import LLM
        from transformers import AutoTokenizer

        # model loaded with vllm 
        # !TODO FIX
        if "bnb" in model_path:
            self.llm = LLM(model=model_path, quantization="bitsandbytes", load_format="bitsandbytes", max_model_len=8192 * 4)
        elif "Llama-3.3-70B-Instruct" in model_path:
            self.llm = LLM(model=model_path, max_model_len=8192 * 4, tensor_parallel_size=num_gpus)
        elif "Qwen3" in model_path:
            self.llm = LLM(model=model_path, gpu_memory_utilization=0.95, max_model_len=8192 * 2, tensor_parallel_size=num_gpus)
        else:
            self.llm = LLM(model=model_path, max_model_len=8192, tensor_parallel_size=num_gpus)
        
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
                temperature=0.7,
                top_k=5,
                top_p=0.95,
                repetition_penalty=1.0,
                max_tokens=500
            )
        outputs = self.llm.generate(formatted_prompt, sampling_params)

        return outputs[0].outputs[0].text  # .replace(".", "") -- add back if necessary, depending on generation
