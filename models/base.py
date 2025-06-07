import prompts.prompt_templates as prompts
import prompts.automated_metrics as automated_metrics
from abc import ABC, abstractmethod


def get_prompt(metric_name, prompt_name, context, justice, remark, remark1=None):
    # get system prompt from classifier name
    metric_metadata = automated_metrics.METADATA[metric_name]
    template = prompts.TEMPLATES[prompt_name]

    system_prompt = template.format(
        classifier_name=metric_name,
        prompt=metric_metadata["prompt"],
        instructions=metric_metadata["instructions"],
        buckets=metric_metadata["buckets"]
    )

    if metric_metadata["metric_type"] == "comparative":
        return [{"role": "system", "content": system_prompt},
                {"role": "user",
                 "content": f"""context: {context}\njustice: {justice}\nremark: {remark}\nremark1: {remark1}"""}]

    return [{"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""context: {context}\njustice: {justice}\nremark: {remark}"""}]


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    def classify_metric(self, classifier_name, prompt_name, context, justice, remark):
        messages = get_prompt(classifier_name, prompt_name, context, justice, remark)
        response = self.generate(messages)  # calls child class's concrete implementation
        print(response)
        return response


def get_model(kind: str, **kwargs) -> BaseModel:
    if kind == "vllm":
        from models import VllmModel
        return VllmModel(kwargs["model_path"])
    elif kind == "openai":
        from models import OpenAIModel
        return OpenAIModel(api_key=kwargs["api_key"])
    else:
        raise ValueError(f"Unknown model type: {kind}")
