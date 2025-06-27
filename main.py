import pandas as pd
from models.base import get_model
import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(version_base=None, config_path="conf/job_types", config_name="metrics")
def main(cfg: DictConfig) -> None:
    parser.add_argument('input_csv_path', help="Need an input files on which to run script!")
    parser.add_argument('output_csv_path', help="Need an output path to save your metrics!")

    if cfg.model_type == 'openai' and not cfg.api_key:
        raise ValueError("api-key is required for OpenAI model")

    model = get_model(cfg.model_type, model_path=cfg.model_path, cfg=args.api_key)
    aggregate_metrics = OmegaConf.to_container(cfg.metrics_to_classify)

    df.to_csv(args.output_csv_path, index=False)


if __name__ == "__main__":
    main()
