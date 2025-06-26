import prompts.prompt_templates as prompts
import prompts.automated_metrics as automated_metrics
from abc import ABC, abstractmethod


def get_metrics_prompt(metric_name: str, context: str, justice: str, remark: str, remark1: str) -> str:
    # get system prompt from metric name; template type is stored in metric metadata
    metric_metadata = automated_metrics.METADATA[metric_name]
    template = prompts.TEMPLATES[metric_metadata["metric_type"]]

    system_prompt = template.format(
        classifier_name=metric_name,
        prompt=metric_metadata["prompt"],
        instructions=metric_metadata["instructions"],
        buckets=metric_metadata["buckets"]
    )

    # assume default metric is distributional
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""context: {context}\njustice: {justice}\nremark: {remark}"""}]

    # add the second remark to the prompt if the metric is comparative
    if metric_metadata["metric_type"] == "comparative":
        messages[1]["content"] += f"""\nremark1: {remark1}"""

    return messages


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    def classify_metric(self, classifier_name: str, context: str, justice: str, remark: str, remark1=None) -> str:
        messages = get_metrics_prompt(classifier_name, context, justice, remark, remark1)
        response = self.generate(messages)  # calls child class's concrete implementation
        print(response)
        return response


def get_model(model_type: str, **kwargs) -> BaseModel:
    if model_type == "vllm":
        from models import VllmModel
        return VllmModel(kwargs["model_path"], kwargs["make_greedy"])
    elif model_type == "openai":
        from models import OpenAIModel
        return OpenAIModel(api_key=kwargs["api_key"])
    else:
        raise ValueError(f"Unknown model type: {model_type}")
