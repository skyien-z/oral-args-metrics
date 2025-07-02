import prompts.prompt_templates as prompts
import prompts.automated_metrics as automated_metrics
import prompts.question_generation as question_generation
from abc import ABC, abstractmethod


def get_metrics_prompt(metric_name: str, context: str, justice: str, remark: str, remark1: str) -> str:
    # get system prompt from metric name; template type is stored in metric metadata
    metric_metadata = automated_metrics.METRICS_METADATA[metric_name]
    template = prompts.METRIC_TEMPLATES[metric_metadata["metric_type"]]

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


def get_question_generation_prompt(prompting_strategy: str, facts: str, legal_question: str, justice: str, context: str):
    question_generation_metadata = question_generation.QUESTION_GENERATION_METADATA[prompting_strategy]
    question_generation_template = prompts.QUESTION_GENERATION_PROMPT

    system_prompt = question_generation_template.format(
        role=question_generation_metadata["role"].format(
            justice_name=justice,
            justice_profile=question_generation.JUSTICE_PROFILES[justice]
        ),
        facts_of_the_case=facts,
        legal_question=legal_question,
        emphasis=question_generation_metadata["emphasis"]
    )

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Transcript of the oral argument up until the current turn: {context}"""}]

    return messages


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str, greedy_generation: bool) -> str:
        pass

    def classify_metric(self, classifier_name: str, context: str, justice: str, remark: str, remark1=None) -> str:
        messages = get_metrics_prompt(classifier_name, context, justice, remark, remark1)
        response = self.generate(messages, greedy_generation=True)  # calls child class's concrete implementation
        return response

    def generate_question(self, prompting_strategy: str, facts: str, legal_question: str, justice: str, context: str):
        messages = get_question_generation_prompt(prompting_strategy, facts, legal_question, justice, context)
        response = self.generate(messages, greedy_generation=True)
        return response


def get_model(model_type: str, **kwargs) -> BaseModel:
    if model_type == "vllm":
        from models import VllmModel
        return VllmModel(kwargs["model_path"])
    elif model_type == "openai":
        from models import OpenAIModel
        return OpenAIModel(api_key=kwargs["api_key"])
    else:
        raise ValueError(f"Unknown model type: {model_type}")
