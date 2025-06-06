import prompts.prompt_templates as prompt_templates
import prompts.classifier_definitions as classifier_definitions
from abc import ABC, abstractmethod


def get_default_prompt(classifier_name, prompt_name, context, justice, remark):
    # get system prompt from classifier name
    classifier_definition = classifier_definitions.DISTRIBUTION_METRICS[classifier_name]
    prompt_definition = prompt_templates.PROMPT_TEMPLATES[prompt_name]

    system_prompt = prompt_definition.format(
        classifier_name=classifier_name,
        prompt=classifier_definition["prompt"],
        instructions=classifier_definition["instructions"],
        buckets=classifier_definition["buckets"]
    )
    # return consolidated prompts
    return [{"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""context: {context}\njustice: {justice}\nremark: {remark}"""}]


def get_comparative_prompt(classifier_name, prompt_name, context, justice, remark, remark1):
    # get system prompt from classifier name
    classifier_definition = classifier_definitions.COMPARATIVE_CLASSIFICATION_SPECS[classifier_name]
    prompt_definition = prompt_templates.PROMPT_TEMPLATES[prompt_name]

    system_prompt = prompt_definition.format(
        classifier_name=classifier_name,
        prompt=classifier_definition["prompt"],
        instructions=classifier_definition["instructions"],
        buckets=classifier_definition["buckets"]
    )
    # return consolidated prompts
    return [{"role": "system", "content": system_prompt},
            {"role": "user",
             "content": f"""context: {context}\njustice: {justice}\nremark: {remark}\nremark1: {remark1}"""}]


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    def classify_aggregate_metric(self, classifier_name, prompt_name, context, justice, remark):
        messages = get_default_prompt(classifier_name, prompt_name, context, justice, remark)
        response = self.generate(messages)  # calls child class's concrete implementation
        print(response)
        return response

    def classify_comparative_metric(self, classifier_name, prompt_name, context, justice, remark, remark1):
        messages = get_comparative_prompt(classifier_name, prompt_name, context, justice, remark, remark1)
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
