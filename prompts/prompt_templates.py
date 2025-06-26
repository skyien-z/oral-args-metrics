# !IMPORTANT THIS IS THE PROMPT FOR OUR CONTEXT-BASED DIALOGUE STYLE FINE-TUNING
# WE'LL NEED A SLIGHT ALTERATION TO THIS PROMPT FOR BASELINE MODEL METRICS [Maybe separate case facts and question from the transcript?]
METRIC_PROMPT = """You are a model for analyzing the quality of Supreme Court oral arguments. You will be presented with a 
turn-by-turn transcript of an oral argument ("context") up until the current turn. {classification_type} Your 
classification task is entitled '{classifier_name}'. Specifically, we want to know: {prompt} 

    {instructions}
    
    The classification task will be presented in something like the following format:
    context: [{{'role': 'system', 'content': ""You are a legal expert trained to simulate Supreme Court oral arguments.\n\nFACTS_OF_THE_CASE:\n<Case Facts>\n\nLEGAL_QUESTION:\n<Legal Question>""}}, {{'role': 'respondent', 'content': ""<Opening Statement>.""}}, {{'role': 'justice_<Justice Name>', 'content': ""<Question>""}}, {{'role': 'respondent', 'content': ""<Response>""}}]
    justice: justice_<Justice Name>
    remark: "If we accept your interpretation, how would it apply to cases involving modern technologies not contemplated when the statute was written?"
    {remark2}
    The classification should only apply to the remark(s). Output your single classification {buckets}.

    Your output should ONLY CONTAIN THE CLASSIFICATION:
    <Classification>"""

# distributional metrics only classify one remark
DISTRIBUTIONAL_INSTRUCTION = "You will then be presented with a justice's name (\"justice\") and the remark they make in " \
                      "current turn (\"remark\"). "

# comparative metrics need to bake in the two remark structure into the prompt
COMPARATIVE_INSTRUCTION = "You will then be presented with a justice's name (\"justice\") and two remarks that they might " \
                   "make in the current turn (\"remark\" and \"remark2\"). "
REMARK_2 = "Are you prepared to make a representation of the fact here?"

# replace prompt text based on whether we want distributional or comparative metrics
METRIC_TEMPLATES = {
    "distributional": METRIC_PROMPT.replace("{classification_type}", DISTRIBUTIONAL_INSTRUCTION).replace("{remark2}", ""),
    "comparative": METRIC_PROMPT.replace("{classification_type}", COMPARATIVE_INSTRUCTION).replace("{remark2", REMARK_2)
}

QUESTION_GENERATION_PROMPT = '''{role}
    Facts of the Case: {facts_of_the_case}
    Legal Question: {legal_question}

You will be presented with the transcript of the oral argument up until the current turn. You will then have the floor. Your task is to generate the next remark, question or statement, that furthers the oral argument. 
{emphasis}

Output your remark and ONLY your remark.'''