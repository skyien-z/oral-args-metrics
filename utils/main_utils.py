
import re
from datetime import datetime
import hashlib
import hydra
import sqlite3

def make_remark_or_metric_id(model_name, remark_or_metric_title):
    unique_string = f"{model_name}_{remark_or_metric_title}_{datetime.now()}"
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

def connect_to_db(database_path: str):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    return conn, cursor