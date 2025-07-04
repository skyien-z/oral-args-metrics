import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import sqlite3
import re
import datetime

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
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cases_df = pd.read_sql_query("SELECT * from transcript_and_context;", conn)
    remark_addition_query = "INSERT INTO remark (remark_id, model, prompting_strategy, justice, " \
                            "text, log_id, context_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    additional_remarks = []
    for index, row in cases_df.interrows():
        for strategy in prompting_strategies:
            generated_remark = model.generate_question(prompting_strategy=strategy,
                                                       facts=row["case_facts"],
                                                       legal_question=row["legal_question"],
                                                       justice=row["justice"],
                                                       context=row["context"])
            
            model_name = get_model_name(cfg.model_type, cfg.model_path)
            hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
            log_id = hydra_cfg['runtime']['output_dir']
            remark_id = f"{model_name}_{strategy}_{datetime.now()}"
            additional_remarks.append((remark_id, model_name, strategy, row["justice"], generated_remark, 
                                       log_id, row["context_id"]))
        
        # insert into DB every 100 questions or at the end of processing
        if index % 100 == 99 or index == len(cases_df) - 1:
            cursor.executemany(remark_addition_query, additional_remarks)
            conn.commit()
            additional_remarks = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    question_gen_main()
