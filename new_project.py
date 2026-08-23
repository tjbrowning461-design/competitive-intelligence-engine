import re
from pathlib import Path

import yaml


PROJECTS_DIR = Path("projects")


GENERIC_PAGE_CATEGORIES = {
    "products": [
        "products",
        "product",
        "platform",
        "solutions",
        "services",
    ],
    "technology": [
        "technology",
        "how it works",
        "architecture",
        "features",
    ],
    "pricing": [
        "pricing",
        "plans",
        "subscriptions",
    ],
    "customers": [
        "customers",
        "case studies",
        "industries",
        "use cases",
    ],
    "developers": [
        "developers",
        "api",
        "sdk",
        "documentation",
        "integrations",
    ],
    "enterprise": [
        "enterprise",
        "business",
        "security",
        "deployment",
    ],
    "partners": [
        "partners",
        "partnerships",
        "ecosystem",
    ],
}


QUANTUM_HARDWARE_PAGE_CATEGORIES = {
    "technology": [
        "technology",
        "architecture",
        "qubit",
        "science",
        "photonics",
        "neutral atom",
        "trapped ion",
        "superconducting",
    ],
    "systems": [
        "system",
        "systems",
        "hardware",
        "quantum computer",
        "qpu",
        "processor",
    ],
    "roadmap": [
        "roadmap",
        "fault tolerant",
        "fault-tolerant",
        "error correction",
        "logical qubit",
    ],
    "software": [
        "software",
        "sdk",
        "developer",
        "developers",
    ],
    "access": [
        "cloud",
        "deployment",
        "on-premise",
        "on premise",
    ],
    "customers": [
        "customers",
        "industries",
        "case studies",
        "partners",
    ],
    "enterprise": [
        "enterprise",
        "commercial",
    ],
}


ANALYSIS_TYPES = {
    "1": "generic_business",
    "2": "quantum_hardware",
}


def slugify(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^a-z0-9]+",
        "_",
        text
    )

    return text.strip("_")


def choose_analysis_type():

    print("\nChoose analysis type:\n")

    print(
        "1. Generic Business"
    )

    print(
        "2. Quantum Hardware"
    )

    while True:

        choice = input(
            "\nEnter 1 or 2: "
        ).strip()

        if choice in ANALYSIS_TYPES:

            return ANALYSIS_TYPES[
                choice
            ]

        print(
            "Please enter 1 or 2."
        )


def get_page_categories(
    analysis_type
):

    if (
        analysis_type
        == "quantum_hardware"
    ):

        return (
            QUANTUM_HARDWARE_PAGE_CATEGORIES
        )

    return GENERIC_PAGE_CATEGORIES


def collect_companies():

    companies = []

    print(
        "\nPaste companies one at a time."
    )

    print(
        "Use this format:"
    )

    print(
        "Company Name | https://company.com"
    )

    print(
        "\nPress Enter on a blank line "
        "when finished.\n"
    )

    while True:

        line = input(
            "Company: "
        ).strip()

        if not line:
            break

        if "|" not in line:

            print(
                "Use this format:"
            )

            print(
                "Company Name | "
                "https://company.com"
            )

            continue

        name, url = line.split(
            "|",
            1
        )

        name = name.strip()
        url = url.strip()

        if not name or not url:

            print(
                "Both company name "
                "and URL are required."
            )

            continue

        if not url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            url = (
                "https://"
                + url
            )

        companies.append(
            {
                "name": name,
                "url": url,
            }
        )

        print(
            f"Added: {name}"
        )

    return companies


def create_project():

    print(
        "\n"
        + "=" * 60
    )

    print(
        "NEW COMPETITIVE "
        "INTELLIGENCE PROJECT"
    )

    print(
        "=" * 60
    )

    display_name = input(
        "\nProject name: "
    ).strip()

    if not display_name:

        raise ValueError(
            "Project name cannot "
            "be empty."
        )

    project_name = slugify(
        display_name
    )

    analysis_type = (
        choose_analysis_type()
    )

    companies = (
        collect_companies()
    )

    if not companies:

        raise ValueError(
            "You must add at least "
            "one company."
        )

    config = {
        "project_name":
            project_name,

        "display_name":
            display_name,

        "analysis_type":
            analysis_type,

        "page_categories":
            get_page_categories(
                analysis_type
            ),

        "companies":
            companies,
    }

    PROJECTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        PROJECTS_DIR
        / f"{project_name}.yaml"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        yaml.safe_dump(
            config,
            file,
            sort_keys=False,
            allow_unicode=True
        )

    print(
        "\n"
        + "=" * 60
    )

    print(
        "PROJECT CREATED"
    )

    print(
        "=" * 60
    )

    print(
        f"\nProject file:"
        f"\n{output_path}"
    )

    print(
        f"\nCompanies: "
        f"{len(companies)}"
    )

    print(
        f"Analysis type: "
        f"{analysis_type}"
    )

    print(
        "\nRun analysis:"
    )

    print(
        f"\npython run.py "
        f"{output_path}"
    )

    print(
        "\nAnalyze and publish "
        "to GitHub:"
    )

    print(
        f"\npython run.py "
        f"{output_path} "
        f"--publish"
    )

    print(
        "\nForce fresh research "
        "and publish:"
    )

    print(
        f"\npython run.py "
        f"{output_path} "
        f"--refresh --publish"
    )


if __name__ == "__main__":

    create_project()