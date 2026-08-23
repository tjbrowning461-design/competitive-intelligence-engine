import re
import subprocess
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
        "features",
        "architecture",
        "how it works",
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

    print("\nAnalysis type:")
    print("Press ENTER for Generic Business")
    print("Or type: quantum")

    choice = input(
        "\nAnalysis type: "
    ).strip().lower()

    if choice in {
        "quantum",
        "quantum_hardware",
        "2"
    }:
        return "quantum_hardware"

    return "generic_business"


def page_categories_for(
    analysis_type
):

    if analysis_type == "quantum_hardware":
        return QUANTUM_HARDWARE_PAGE_CATEGORIES

    return GENERIC_PAGE_CATEGORIES


def collect_company_block():

    print("\nPaste ALL companies now.")
    print("")
    print("Use this format:")
    print("")
    print(
        "Runway | https://runwayml.com"
    )
    print(
        "OpenArt | https://openart.ai"
    )
    print(
        "Kling | https://klingai.com"
    )
    print("")
    print(
        "Press ENTER on a blank line "
        "when finished."
    )
    print("")

    companies = []

    while True:

        line = input().strip()

        if not line:
            break

        if "|" not in line:

            print(
                f"Skipped invalid line: "
                f"{line}"
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
                f"Skipped invalid line: "
                f"{line}"
            )

            continue

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        companies.append(
            {
                "name": name,
                "url": url,
            }
        )

    return companies


def create_project():

    print(
        "\n"
        + "=" * 65
    )

    print(
        "NEW COMPETITIVE INTELLIGENCE ANALYSIS"
    )

    print(
        "=" * 65
    )

    display_name = input(
        "\nWhat should we call this analysis? "
    ).strip()

    if not display_name:

        raise ValueError(
            "Project name cannot be empty."
        )

    project_name = slugify(
        display_name
    )

    analysis_type = (
        choose_analysis_type()
    )

    companies = (
        collect_company_block()
    )

    if not companies:

        raise ValueError(
            "No companies were entered."
        )

    config = {
        "project_name":
            project_name,

        "display_name":
            display_name,

        "analysis_type":
            analysis_type,

        "page_categories":
            page_categories_for(
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
        + "=" * 65
    )

    print(
        "PROJECT READY"
    )

    print(
        "=" * 65
    )

    print(
        f"\nProject: "
        f"{display_name}"
    )

    print(
        f"Analysis type: "
        f"{analysis_type}"
    )

    print(
        f"Companies: "
        f"{len(companies)}"
    )

    print(
        f"Config: "
        f"{output_path}"
    )

    print(
        "\nWhat do you want to do?"
    )

    print(
        "1 = Create project only"
    )

    print(
        "2 = Run analysis"
    )

    print(
        "3 = Run analysis + publish to GitHub"
    )

    choice = input(
        "\nChoose 1, 2, or 3: "
    ).strip()

    if choice == "2":

        subprocess.run(
            [
                "python",
                "run.py",
                str(output_path)
            ],
            check=True
        )

    elif choice == "3":

        subprocess.run(
            [
                "python",
                "run.py",
                str(output_path),
                "--publish"
            ],
            check=True
        )

    else:

        print(
            "\nProject created."
        )

        print(
            "You can run it later with:"
        )

        print(
            f"\npython run.py "
            f"{output_path} "
            f"--publish"
        )


if __name__ == "__main__":

    create_project()