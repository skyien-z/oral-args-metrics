import pandas as pd
import argparse
from models.base import get_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv_path', help="Need an input files on which to run script!")
    parser.add_argument('output_csv_path', help="Need an output path to save your metrics!")

    parser.add_argument('--model', choices=["vllm", "openai"], required=True)
    parser.add_argument("--model-path", type=str,
                        default='/scratch/gpfs/kz9921/transformer_cache/Llama-3.3-70B-Instruct',
                        help="Path to local model")
    parser.add_argument("--api-key", type=str, help="OpenAI API key")
    args = parser.parse_args()

    if args.model == "vllm" and not args.model_path:
        raise ValueError("model-path is required for vllm model")
    if args.model == "openai" and not args.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(args.model, model_path=args.model_path, api_key=args.api_key)

    # map metric definition to how we want to store them in the csv
    aggregate_metrics = {"VALENCE": "valence", "LEGALBENCH": "legalbench", "METACOG": "metacog", "STETSON": "stetson",
                         "ARGUMENT_CONSISTENCY_AND_CORRECTNESS": "arg_consistency", "SYCOPHANCY": "sycophancy",
                         "CONSISTENCY_WITH_STATUTORY_INTERPRETATION": "statutory_interp",
                         "CONSISTENCY_WITH_POLITICAL_IDEOLOGY": "political_ideology",
                         "RUBRIC_SIMILARITY": "rubric_similarity"}

    # add os metrics
    df = pd.read_csv(args.input_csv_path)  # read in jsonl
    for metric in aggregate_metrics.keys():
        df[f"{args.model_path}_{aggregate_metrics[metric]}"] = df.apply(
            lambda row: model.classify_metric(metric,
                                              row["opening_with_facts_legal_question"],
                                              row["justice"],
                                              row["question_text"]), axis=1)

    df.to_csv(args.output_csv_path, index=False)


if __name__ == "__main__":
    main()
