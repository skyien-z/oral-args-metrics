import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import sqlite3
import re

@hydra.main(version_base=None, config_path="conf/config_files", config_name="metrics")
def metrics_main(cfg: DictConfig) -> None:
    # parser.add_argument('input_csv_path', help="Need an input files on which to run script!")
    # parser.add_argument('output_csv_path', help="Need an output path to save your metrics!")

    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, cfg=cfg.api_key)
    aggregate_metrics = OmegaConf.to_container(cfg.metrics_to_classify)

    # df.to_csv(args.output_csv_path, index=False)


def get_model_name(model_type, model_path):
    if model_type == "openai":
        return "gpt4o"
    # model is local
    return re.search(r'transformer_cache/(.+)', model_path).group(1)

@hydra.main(version_base=None, config_path="conf/config_files", config_name="question_gen")
def question_gen_main(cfg: DictConfig) -> None:
    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, cfg=cfg.api_key)
    prompting_strategies = OmegaConf.to_container(cfg.prompting_strategies)

    # open the metrics database view that contains all case information
    conn = sqlite3.connect("data/automated_metrics.db")
    cases_df = pd.read_sql_query("SELECT * from transcript_and_context;", conn)

    for index, row in cases_df.interrows():
        for strategy in prompting_strategies:
            generated_remark = model.generate_question(prompting_strategy=strategy,
                                                       facts=row["case_facts"],
                                                       legal_question=row["legal_question"],
                                                       justice=row["justice"],
                                                       context=row["context"])
            context_id = row["context_id"]
            prompting_strategy = strategy
            model_name = get_model_name(cfg.model_type, cfg.model_path)
            justice = row["justice"]
            transcript_id = row["transcript_id"]
            hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
            log_id = hydra_cfg['runtime']['output_dir']


if __name__ == "__main__":
    question_gen_main()
