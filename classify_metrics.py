import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import sqlite3
import re
from datetime import datetime
import hashlib
import ast

def make_metric_id(model_name, metric_title):
    unique_string = f"{model_name}_{metric_title}_{datetime.now()}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def get_model_name(model_type, model_path):
    if model_type == "openai":
        return "gpt4o"
    # model is local
    return re.search(r'transformer_cache/(.+)', model_path).group(1)

def get_log_id():
    hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
    logging_dir = hydra_cfg['runtime']['output_dir']
    # log_id might can start with 'output/' or 'multiturn/'
    return re.search(r'oral_args_metrics/(.+)', logging_dir).group(1)

def incorporate_facts_to_context(case_facts, legal_question, context):
    context_list = ast.literal_eval(context)
    system_prompt = {'content': f"""You are a legal expert trained to simulate Supreme Court oral arguments.\n\nFACTS_OF_THE_CASE:\n{case_facts}\n\nLEGAL_QUESTION:\n{legal_question}""",
    'role': 'system'}
    context_list.insert(0, system_prompt)
    return str(context_list)

@hydra.main(version_base=None, config_path="conf/config_files", config_name="metrics")
def metrics_main(cfg: DictConfig) -> None:
    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key)
    metrics_list = OmegaConf.to_container(cfg.metrics_to_classify)
    # open the metrics database view that contains all case information
    conn = sqlite3.connect("data/automated_metrics.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cases_df = pd.read_sql_query("SELECT * from remark_transcript_context;", conn) #TODO WHERE comparison with q gen log ids
    metric_addition_query = "INSERT INTO distributional_metrics (distributional_metric_id, classification_model, metric_name, " \
                            "classification, remark_id, log_id) VALUES (?, ?, ?, ?, ?, ?)"
    additional_metrics = []
    for index, row in cases_df.iterrows():
        for metric_title in metrics_list:
            reformatted_context = incorporate_facts_to_context(row["case_facts"], row["legal_question"], row["context"])
            generated_classification = model.classify_metric(classifier_name=metric_title, 
                                                     context=reformatted_context, 
                                                     justice=row["justice"], 
                                                     remark=row["remark_text"])

            model_name = get_model_name(cfg.model_type, cfg.model_path)
            log_id = get_log_id()
            metric_id = make_metric_id(model_name, metric_title)
            additional_metrics.append((metric_id, model_name, metric_title, generated_classification, 
                                       row["remark_id"], log_id))
        
        # insert into DB every 20 questions (160 runs) or at the end of processing
        if index % 20 == 19 or index == len(cases_df) - 1:
            cursor.executemany(metric_addition_query, additional_metrics)

            conn.commit()
            additional_metrics = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    metrics_main()