DISTRIBUTION_METRICS = {
    "CLASSIFY_VALENCE": {
        "prompt": "How competitive is the justice's remark made in the current turn?",
        "instructions": """Your classification should choose from a likert scale ranging from 'Very Competitive' to 'Very Cooperative':
        - "Very Competitive": The remark directly critiques the points made by the advocate in the oral argument context.
        - "Competitive": The remark tries to critique the points made by the advocate in the oral argument context.
        - "Neutral": The remark neither critiques nor supports the points made by the advocate in the oral argument context.
        - "Cooperative": The remark tries to support the points made by the advocate in the oral argument context.
        - "Very Cooperative": The remark directly supports the points made by the advocate in the oral argument context.""",
        "buckets": "(Very Competitive, Competitive, Neutral, Cooperative, Very Cooperative)",
        "metric_type": "aggregate"
    },
    "CLASSIFY_VALENCE_PARDONTHEINTERRUPTION": {
        "prompt": "How competitive is the justice's interruption made in the current turn on the spectrum of cooperative to competitive.?",
        "instructions": """Your classification should choose from a likert scale ranging from 'Cooperative' to ' Competitive':
        - "Cooperative": By cooperative, we mean that to your ears, the first speaker -- the justice -- expects a turn change and gives the floor to the second speaker. The second speaker might leave space for the first speaker to finish their turn. Or, the second speaker might talk at the same time as the first speaker, providing short spurts of feedback, for example saying “mhmm” or “yes”.
        - "Slightly Cooperative"
        - "Neutral"
        - "Slightly Competitive"
        - "Competitive": By competitive, we mean that to your ears, the second speaker competes with the first speaker for the chance to speak. You, the first speaker, or listeners might perceive this as a disruption to the previous speaker's speech. The second speaker may cause the first speaker to stop speaking, or talk over the first speaker to compete to be heard.""",
        "buckets": "(Competitive, Slightly Competitive, Neutral, Slightly Cooperative, Cooperative)",
        "metric_type": "aggregate"
    },
    "CLASSIFY_LEGALBENCH": {
        "prompt": "Which LegalBench category does the justice's remark made in the current turn fall into?",
        "instructions": """Your classification should choose from the following LegalBench categories:
        - 'Background': Seeks factual or procedural information missing or unclear in the briefs.
        - 'Clarification': Aims to clarify the advocate's position or the scope of the rule being proposed.
        - 'Implications': Explores the limits of a proposed rule or its potential implications for future cases.
        - 'Support': Offers implicit or explicit support for the advocate's position.
        - 'Criticism': Challenges or criticizes the advocate's position.
        - 'Communicate': Serves as a means for the judge to communicate with other judges on the court, rather than directly with the advocate.
        - 'Humor': Introduces humor to ease tension during the proceedings.""",
        "buckets": "(Background, Clarification, Implications, Support, Criticism, Communicate, Humor)",
        "metric_type": "aggregate"
    },
    "CLASSIFY_METACOG":  {
        "prompt": "Which MetaCog category does the justice's remark made in the current turn fall into?",
        "instructions": """Your classification should choose from the following MetaCog categories:
        - 'statutory_interpretation': Related to the interpretation and application of statutes
        - 'precedent_and_doctrine': Related to the examination and application of precedents and doctrines.
        - 'case_facts_and_context': Related to the examination of case facts and context.
        - 'judicial_role_and_review': Related to the examination of the judicial role and review.
        - 'argumentation_and_clarification': Related to the examination of argumentation and clarification.
        - 'constitutional_issues': Related to the examination of constitutional issues.
        - 'procedural_matters': Related to the examination of procedural matters.""",
        "buckets": "(statutory_interpretation, precedent_and_doctrine, case_facts_and_context, judicial_role_and_review, argumentation_and_clarification, constitutional_issues, procedural_matters)",
        "metric_type": "aggregate"
    },
    "CLASSIFY_REALNESS": {
        "prompt": "How realistic is it for the justice to make the given remark in the current turn?",
        "instructions": """Choose your response from the follow categories:
        - 'Yes': It is realistic for the justice to ask the given remark.
        - 'No': It is not realistic for the justice to ask the given remark.""",
        "buckets": "(Yes, No)",
        "metric_type": "aggregate"
    },
    "CLASSIFY_HELPFULNESS": {
        "prompt": "How helpful would this remark be to a junior lawyer using this transcript to prepare for oral arguments?",
        "instructions": """Choose your response from the follow categories:
        - '-2': This remark is very unhelpful for preparing for oral arguments.
        - '-1': This remark is unhelpful for preparing for oral arguments. [for example... ]
        - '0': This remark is neither helpful nor unhelpful for preparing for oral arguments.
        - '1': This remark is helpful for preparing for oral arguments.
        - '2': This remark is very helpful for preparing for oral arguments.""",
        "buckets": "(-2, -1, 0, 1, 2)",
        "metric_type": "aggregate"
    }
}

COMPARATIVE_CLASSIFICATION_SPECS = {
    "CLASSIFY_SIMILARITY": {
        "prompt": "How similar are remark and remark1 to each other in the current turn?",
        "instructions": """Choose your response from the follow categories:
        - '-2': remark and remark1 are very dissimilar.
        - '-1': remark and remark1 are dissimilar.
        - '0': remark and remark1 are neither similar nor dissimilar.
        - '1': remark and remark1 are similar.
        - '2': remark and remark1 are very similar.""",
        "buckets": "(-2, -1, 0, 1, 2)",
        "metric_type": "comparative"
    },
    "CLASSIFY_SIMILARITY_SENTIMENT": {
        "prompt": "How similar in sentiment are remark and remark1 to each other in the current turn?",
        "instructions": """Choose your response from the follow categories:
        - '-2': remark and remark1 are very dissimilar in sentiment.
        - '-1': remark and remark1 are dissimilar in sentiment.
        - '0': remark and remark1 are neither similar nor dissimilar in sentiment.
        - '1': remark and remark1 are similar in sentiment.
        - '2': remark and remark1 are very similar in sentiment.""",
        "buckets": "(-2, -1, 0, 1, 2)",
        "metric_type": "comparative"
    },
    "CLASSIFY_REMARK_PREFERENCE": {
        "prompt": "How much do you prefer remark over remark1 in the current turn?",
        "instructions": """Choose your response from the follow categories:
        - '-2': As a legal expert, you strongly prefer remark to remark1.
        - '-1': As a legal expert, you prefer remark to remark1.
        - '0': As a legal expert, you have no preference between remark and remark1.
        - '1': As a legal expert, you prefer remark1 to remark.
        - '2': As a legal expert, you strongly prefer remark1 to remark.""",
        "buckets": "(-2, -1, 0, 1, 2)",
        "metric_type": "comparative"
    },
}