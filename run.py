import argparse
import importlib
import json
import re
from pathlib import Path

from engine.analyzer import analyze_company
from engine.comparer import compare_companies
from engine.config import load_project_config
from engine.reporter import generate_report
from engine.scraper import discover_pages, scrape_pages


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports")


ANALYSIS_REGISTRY = {
    "quantum_hardware": {
        "schema_module": "schemas.quantum_hardware",
        "analysis_schema": "QuantumHardwareAnalysis",
        "comparison_schema": "QuantumHardwareComparison",
        "prompt_module": "prompts.quantum_hardware",
        "analysis_prompt": "COMPANY_ANALYSIS_PROMPT",
        "comparison_prompt": "MARKET_COMPARISON_PROMPT",
    }
}


def safe_filename(name):
    name = name.lower().strip()

    name = re.sub(
        r"[^a-z0-9]+",
        "_",
        name
    )

    return name.strip("_")


def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_json(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def load_analysis_components(
    analysis_type
):
    if analysis_type not in ANALYSIS_REGISTRY:
        raise ValueError(
            f"Unknown analysis type: "
            f"{analysis_type}"
        )

    settings = ANALYSIS_REGISTRY[
        analysis_type
    ]

    schema_module = importlib.import_module(
        settings["schema_module"]
    )

    prompt_module = importlib.import_module(
        settings["prompt_module"]
    )

    analysis_schema = getattr(
        schema_module,
        settings["analysis_schema"]
    )

    comparison_schema = getattr(
        schema_module,
        settings["comparison_schema"]
    )

    analysis_prompt = getattr(
        prompt_module,
        settings["analysis_prompt"]
    )

    comparison_prompt = getattr(
        prompt_module,
        settings["comparison_prompt"]
    )

    return (
        analysis_schema,
        comparison_schema,
        analysis_prompt,
        comparison_prompt,
    )


def analyze_project(
    config_path,
    refresh=False
):
    config = load_project_config(
        config_path
    )

    project_name = config[
        "project_name"
    ]

    display_name = config.get(
        "display_name",
        project_name.replace(
            "_",
            " "
        ).title()
    )

    analysis_type = config[
        "analysis_type"
    ]

    companies = config[
        "companies"
    ]

    page_categories = config[
        "page_categories"
    ]

    (
        analysis_schema,
        comparison_schema,
        analysis_prompt,
        comparison_prompt,
    ) = load_analysis_components(
        analysis_type
    )

    project_results_dir = (
        RESULTS_DIR
        / project_name
    )

    project_results_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    analyses = []

    new_analysis_created = False

    print(
        f"\nProject: {display_name}"
    )

    print(
        f"Companies: {len(companies)}"
    )

    for index, company in enumerate(
        companies,
        start=1
    ):
        company_name = company[
            "name"
        ]

        website = company[
            "url"
        ]

        output_file = (
            project_results_dir
            / (
                safe_filename(
                    company_name
                )
                + ".json"
            )
        )

        print(
            "\n"
            + "=" * 70
        )

        print(
            f"[{index}/{len(companies)}] "
            f"{company_name}"
        )

        print(website)

        if (
            output_file.exists()
            and not refresh
        ):
            print(
                "Using cached analysis."
            )

            analyses.append(
                load_json(output_file)
            )

            continue

        selected_pages = discover_pages(
            website,
            page_categories
        )

        print(
            "\nSelected pages:"
        )

        for category, url in selected_pages:
            print(
                f"- {category}: {url}"
            )

        company_text, sources = scrape_pages(
            selected_pages
        )

        if not company_text.strip():
            print(
                f"No usable text collected "
                f"for {company_name}."
            )
            continue

        evidence = f"""
COMPANY:
{company_name}

OFFICIAL WEBSITE:
{website}

COLLECTED WEBSITE EVIDENCE:

{company_text}
"""

        result = analyze_company(
            company_text=evidence,
            schema_class=analysis_schema,
            system_prompt=analysis_prompt
        )

        result_data = result.model_dump()

        result_data[
            "website"
        ] = website

        result_data[
            "sources"
        ] = sources

        save_json(
            output_file,
            result_data
        )

        analyses.append(
            result_data
        )

        new_analysis_created = True

        print(
            f"\nSaved: "
            f"{output_file}"
        )

    if not analyses:
        raise RuntimeError(
            "No company analyses "
            "were available."
        )

    comparison_output = (
        RESULTS_DIR
        / f"{project_name}_comparison.json"
    )

    if (
        comparison_output.exists()
        and not new_analysis_created
        and not refresh
    ):
        print(
            "\nUsing cached market comparison."
        )

        comparison_data = load_json(
            comparison_output
        )

    else:
        print(
            "\n"
            + "=" * 70
        )

        print(
            "\nCreating market comparison..."
        )

        comparison = compare_companies(
            analyses=analyses,
            comparison_schema_class=
                comparison_schema,
            system_prompt=
                comparison_prompt
        )

        comparison_data = (
            comparison.model_dump()
        )

        save_json(
            comparison_output,
            comparison_data
        )

        print(
            f"\nSaved comparison: "
            f"{comparison_output}"
        )

    report_output = (
        REPORTS_DIR
        / f"{project_name}.html"
    )

    generate_report(
        display_name=display_name,
        analyses=analyses,
        comparison=comparison_data,
        output_path=report_output
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "\nPROJECT COMPLETE"
    )

    print(
        f"Company analyses: "
        f"{project_results_dir}"
    )

    print(
        f"Market comparison: "
        f"{comparison_output}"
    )

    print(
        f"Report: "
        f"{report_output}"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Reusable competitive "
            "intelligence engine"
        )
    )

    parser.add_argument(
        "config",
        help=(
            "Path to the project "
            "YAML configuration file"
        )
    )

    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "Ignore cached results and "
            "reanalyze every company."
        )
    )

    args = parser.parse_args()

    analyze_project(
        args.config,
        refresh=args.refresh
    )


if __name__ == "__main__":
    main()