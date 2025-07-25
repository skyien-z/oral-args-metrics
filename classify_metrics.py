import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf
import utils.main_utils as utils

DATABASE_PATH = "data/adversarial_metrics.db"
GET_CASES_QUERY = "SELECT * from remark_transcript_context WHERE remark_log_id IN {log_list};"
ADD_METRIC_QUERY = "INSERT INTO adversarial_metrics (adversarial_metric_id, classification_model, metric_name, " \
                            "classification, remark_id, log_id) VALUES (?, ?, ?, ?, ?, ?);"


@hydra.main(version_base=None, config_path="conf/", config_name="classify_metrics")
def metrics_main(cfg: DictConfig) -> None:
    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, api_key=cfg.api_key, num_gpus=cfg.num_gpus)
    metrics_list = OmegaConf.to_container(cfg.metrics_to_classify)
    remark_log_ids = OmegaConf.to_container(cfg.log_ids)

    # open the metrics database view that contains all case information
    conn, cursor = utils.connect_to_db(DATABASE_PATH)
    cases_df = pd.read_sql_query(GET_CASES_QUERY.format(log_list=utils.make_logs_into_sql_list(remark_log_ids)), conn) 

    additional_metrics = []
    for index, row in cases_df.iterrows():
        for metric_title in metrics_list:
            print(row["remark_text"])
            reformatted_context = utils.incorporate_facts_to_context(row["case_facts"], row["legal_question"], row["context"])
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
            cursor.executemany(ADD_METRIC_QUERY, additional_metrics)
            conn.commit()
            additional_metrics = []
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    metrics_main()