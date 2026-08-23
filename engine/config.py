from pathlib import Path

import yaml


def load_project_config(
    config_path
):

    config_path = Path(
        config_path
    )

    if not config_path.exists():

        raise FileNotFoundError(
            f"Project config not found: "
            f"{config_path}"
        )


    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as file:

        config = yaml.safe_load(
            file
        )


    required_fields = [
        "project_name",
        "analysis_type",
        "companies",
        "page_categories"
    ]


    for field in required_fields:

        if field not in config:

            raise ValueError(
                f"Missing required "
                f"config field: {field}"
            )


    if not isinstance(
        config["companies"],
        list
    ):

        raise ValueError(
            "'companies' must be a list."
        )


    for company in (
        config["companies"]
    ):

        if "name" not in company:

            raise ValueError(
                "Every company needs "
                "a name."
            )

        if "url" not in company:

            raise ValueError(
                "Every company needs "
                "a URL."
            )


    return config