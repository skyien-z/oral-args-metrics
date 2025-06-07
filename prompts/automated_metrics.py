METADATA = {
    "CLASSIFY_VALENCE": {
        "prompt": "How competitive/cooperative is the justice's remark in the current turn?",
        "instructions": """Your classification should choose from a likert scale ranging from 'Very Competitive' to 'Very Cooperative':
        - "Competitive": The remark expresses clear justice displeasure with the advocate’s last statement in the oral argument context.
        - "Slightly Competitive": The remark challenges the content of the advocate's last statement in the oral argument context.
        - "Neutral": The remark is orthogonal to any of the advocate's arguments. The remark may be purely procedural.
        - "Slightly Cooperative": The remark intends to allow the advocate to expand upon one of his/her existing arguments.
        - "Very Cooperative": The remark suggests justice agreement or pleasure with the advocate's last statement in the oral argument context.""",
        "buckets": "(Competitive, Slightly Competitive, Neutral, Slightly Cooperative, Cooperative)",
        "metric_type": "distributional"
    },
    "CLASSIFY_LEGALBENCH": {
        "prompt": "Which LegalBench category does the justice's remark, made in the current turn, fall into?",
        "instructions": """Your classification should choose from the following LegalBench categories:
        - 'Background': Seeks factual or procedural information missing or unclear in the briefs.
        - 'Clarification': Aims to clarify the advocate's position or the scope of the rule being proposed.
        - 'Implications': Explores the limits of a proposed rule or its potential implications for future cases.
        - 'Support': Offers implicit or explicit support for the advocate's position.
        - 'Criticism': Challenges or criticizes the advocate's position.
        - 'Communicate': Serves as a means for the judge to communicate with other judges on the court, rather than directly with the advocate.
        - 'Humor': Introduces humor to ease tension during the proceedings.""",
        "buckets": "(Background, Clarification, Implications, Support, Criticism, Communicate, Humor)",
        "metric_type": "distributional"
    },
    "CLASSIFY_METACOG":  {
        "prompt": "Which MetaCog category does the justice's remark, made in the current turn, fall into?",
        "instructions": """Your classification should choose from the following MetaCog categories:
        - 'statutory_interpretation': Related to the interpretation and application of statutes
        - 'precedent_and_doctrine': Related to the examination and application of precedents and doctrines.
        - 'case_facts_and_context': Related to the examination of case facts and context.
        - 'judicial_role_and_review': Related to the examination of the judicial role and review.
        - 'argumentation_and_clarification': Related to the examination of argumentation and clarification.
        - 'constitutional_issues': Related to the examination of constitutional issues.
        - 'procedural_matters': Related to the examination of procedural matters.""",
        "buckets": "(statutory_interpretation, precedent_and_doctrine, case_facts_and_context, judicial_role_and_review, argumentation_and_clarification, constitutional_issues, procedural_matters)",
        "metric_type": "distributional"
    },
    "CLASSIFY_STETSON":  {
        "prompt": "Which Stetson category does the justice's remark, made in the current turn, fall into?",
        "instructions": """Your classification should choose from the following Stetson categories:
        - 'elicit_information': A judge may ask about the facts in the evidence or record, or about authorities, parties, or background.
        - 'authority_applicability_legal_reach': A judge may ask about how precedent applies to a client’s facts or how far legal principles extend. A judge might also ask how authorities are similar to or distinguishable from the case at hand.
        - 'hypothetical': A judge may ask hypothetical questions to see just how far a legal position will reasonably reach. These can be phrased as examples.
        - 'opposing_counsel_args': A judge may ask questions about the opposing counsel’s argument. These questions will be designed to probe the weaknesses of the current advocate's argument,
        - 'policy': A judge may ask policy questions to know how their decisions will impact society.
        - 'seek_concessions': A judge may ask the current advocate to concede a point because judges like to narrow the legal and factual questions in the case and to determine just how far the consequences of a decision will reach.
        - 'softball': A judge may ask softball questions -- friendly questions designed to help the current advocate -- because they agree with the current advocate and want to help the advocate make his/her point to their fellow judges.
        - 'irrelevant': : A judge may ask questions that are not relevant to the case at hand.""",
        "buckets": "(elicit_information, authority_applicability_legal_reach, hypothetical, opposing_counsel_args, policy, softball, irrelevant)",
        "metric_type": "distributional"
    },
    "ARGUMENT_CONSISTENCY_AND_CORRECTNESS": {
        "prompt": "Does the justice's remark in the current turn call out the advocate's last statement in the oral argument context for incorrect or inconsistent argumentation?",
        "instructions": """Choose your response from the follow categories:
        - ‘error_caught’: The advocate’s last argument is incorrect or inconsistent and the justice’s remark calls it out.
        - 'error_uncaught': The advocate’s last argument is incorrect or inconsistent and the justice’s remark does not call it out.
        - 'no_error': The advocate’s last argument is consistent and correct OR a justice is responding to another justice OR the justice’s remark is irrelevant to the arguments presented.
        """,
        "buckets": "(error_caught, error_uncaught, no_error)",
        "metric_type": "distributional"
    },
    "SYCOPHANCY": {
        "prompt": "Does the justice's remark display sycophantic behavior?",
        "instructions": """Choose your response from the follow categories:
        - 'Yes': The justice remark displays overly supportive behavior inappropriate for a Supreme Court oral argument context.
        - 'No': The justice remark displays behavior appropriate for a Supreme Court oral argument context.
        """,
        "buckets": "(Yes, No)",
        "metric_type": "distributional"
    },
    "CONSISTENCY_WITH_STATUTORY_INTERPRETATION": {
        "prompt": "Is the justice's remark consistent with what's known of the justice's approach to statutory interpretation?",
        "instructions": """Choose your response from the follow categories:
        - 'Yes': The remark is consistent or mostly consistent with what's known of the justice's approach to statutory interpretation.
        - 'No': The remark is inconsistent or mostly inconsistent with what's known of the justice's approach to statutory interpretation.
        - 'NA': The remark seems to be orthogonal to ANY approaches to statutory interpretation; it may be an aside, too short, or simply procedural.""",
        "buckets": "(Yes, No, NA)",
        "metric_type": "distributional"
    },
    "CONSISTENCY_WITH_POLITICAL_IDEOLOGY": {
        "prompt": "Is the justice's remark consistent with the justice's known political ideology?",
        "instructions": """Choose your response from the follow categories:
        - 'Yes': The remark is consistent or mostly consistent with the justice's known political ideology.
        - 'No': The remark is inconsistent or mostly inconsistent with the justice's known to political ideology.
        - 'NA': The remark seems to be orthogonal to ANY political ideologies; it may be an aside, politically neutral, or simply procedural.""",
        "buckets": "(Yes, No, NA)",
        "metric_type": "distributional"
    },
    "CLASSIFY_SIMILARITY_ON_RUBRIC": {
        "prompt": "How similar are remark and remark1 to each other in the current turn?",
        "instructions": """Choose your response from the follow categories:
        - '-2': remark and remark1 are very dissimilar.
        - '-1': remark and remark1 are dissimilar.
        - '0': remark and remark1 are neither similar nor dissimilar.
        - '1': remark and remark1 are similar.
        - '2': remark and remark1 are very similar.""",
        "buckets": "(-2, -1, 0, 1, 2)",
        "metric_type": "comparative"
    }
}
