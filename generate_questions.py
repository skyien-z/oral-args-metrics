import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
from hydra.core.hydra_config import HydraConfig
import sqlite3
import re
from datetime import datetime
import hashlib

def make_remark_id(model_name, strategy):
    unique_string = f"{model_name}_{strategy}_{datetime.now()}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def get_model_name(model_type, model_path):
    if model_type == "openai":
        return "gpt4o"
    # model is local
    return re.search(r'transformer_cache/(.+)', model_path).group(1)

def get_log_id():
    hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
    logging_dir = hydra_cfg['runtime']['output_dir']
    return re.search(r'outputs/(.+)', logging_dir).group(1)


@hydra.main(version_base=None, config_path="conf/config_files", config_name="question_gen")
def question_gen_main(cfg: DictConfig) -> None:
    launcher_cfg = HydraConfig.get().launcher
    print("Active launcher config:")
    print(OmegaConf.to_yaml(launcher_cfg))

    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key)
    prompting_strategies = OmegaConf.to_container(cfg.prompting_strategies)

    # open the metrics database view that contains all case information
    conn = sqlite3.connect("data/automated_metrics.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cases_df = pd.read_sql_query("SELECT * from hundred_sampled_transcript_and_context;", conn)
    remark_addition_query = "INSERT INTO remark (remark_id, model, prompting_strategy, justice, " \
                            "remark_text, log_id, context_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    additional_remarks = []
    for index, row in cases_df.iterrows():
        for strategy in prompting_strategies:
            generated_remark = model.generate_question(prompting_strategy=strategy,
                                                       facts=row["case_facts"],
                                                       legal_question=row["legal_question"],
                                                       justice=row["justice"],
                                                       context=row["context"])

            model_name = get_model_name(cfg.model_type, cfg.model_path)
            log_id = get_log_id()
            remark_id = make_remark_id(model_name, strategy)
            additional_remarks.append((remark_id, model_name, strategy, row["justice"], generated_remark, 
                                       log_id, row["context_id"]))
        
        # insert into DB every 100 questions or at the end of processing
        if index % 50 == 49 or index == len(cases_df) - 1:
            print(additional_remarks)
            cursor.executemany(remark_addition_query, additional_remarks)

            conn.commit()
            additional_remarks = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    question_gen_main()
