
import re
from datetime import datetime
import hashlib
import hydra
import sqlite3
import ast

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

def make_logs_into_sql_list(remark_log_ids):
    # returns string, bookmarked with parentheses, of sqlite search 
    # with remark_log_ids as data
    sql_list_str = "("
    for i, log_id in enumerate(remark_log_ids):
        sql_list_str += f"\'{log_id}\'"
        if i < len(remark_log_ids) - 1:
            sql_list_str += ", "
    sql_list_str += ')'
    return sql_list_str

def incorporate_facts_to_context(case_facts, legal_question, context):
    context_list = ast.literal_eval(context)
    system_prompt = {'content': f"""You are a legal expert trained to simulate Supreme Court oral arguments.\n\nFACTS_OF_THE_CASE:\n{case_facts}\n\nLEGAL_QUESTION:\n{legal_question}""",
    'role': 'system'}
    context_list.insert(0, system_prompt)
    return str(context_list)