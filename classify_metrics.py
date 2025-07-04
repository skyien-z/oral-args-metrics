import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import sqlite3
import ast
import utils.main_utils as utils

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
    remark_log_ids = OmegaConf.to_container(cfg.log_ids)
    # open the metrics database view that contains all case information
    conn = sqlite3.connect("data/automated_metrics.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    
    # !TODO Careful, the next line is very brittle; yeah straight up make a func. This only works with one log_id sadge
    cases_df = pd.read_sql_query(f"SELECT * from remark_transcript_context WHERE remark_log_id IN (\'{', '.join(remark_log_ids)}\');", conn) 

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

            model_name = utils.get_model_name(cfg.model_type, cfg.model_path)
            log_id = utils.get_log_id()
            metric_id = utils.make_remark_or_metric_id(model_name, metric_title)
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