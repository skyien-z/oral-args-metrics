from models import BaseModel


class VllmModel(BaseModel):
    def __init__(self, model_path: str):
        from vllm import LLM, SamplingParams
        from transformers import AutoTokenizer

        # model loaded with vllm
        self.llm = LLM(model=model_path, tensor_parallel_size=4)
        
        # model's tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # greedy decoding sampling parameters
        self.sampling_params = SamplingParams(
                temperature=0.0,
                top_k=1,
                top_p=1.0,
                repetition_penalty=1.0,
                max_tokens=500
        )

    def generate(self, messages: str) -> str:
        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.llm.generate(formatted_prompt, self.sampling_params)
        return outputs[0].outputs[0].text  # .replace(".", "") -- add back if necessary, depending on generation
