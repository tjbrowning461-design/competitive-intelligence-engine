import json
from pathlib import Path

import streamlit as st
import yaml


PROJECTS_DIR = Path("projects")
RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports")


st.set_page_config(
    page_title="Competitive Intelligence Engine",
    page_icon="📊",
    layout="wide"
)


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_yaml(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


def discover_projects():

    projects = []

    if not PROJECTS_DIR.exists():
        return projects

    for path in sorted(
        PROJECTS_DIR.glob("*.yaml")
    ):

        try:

            config = load_yaml(path)

            if not config:
                continue

            project_name = config.get(
                "project_name"
            )

            if not project_name:
                continue

            projects.append(
                {
                    "path": path,
                    "config": config
                }
            )

        except Exception:

            continue

    return projects


def load_company_results(
    project_name
):

    project_dir = (
        RESULTS_DIR
        / project_name
    )

    results = []

    if not project_dir.exists():
        return results

    for path in sorted(
        project_dir.glob("*.json")
    ):

        try:

            data = load_json(path)

            results.append(data)

        except Exception:

            continue

    return results


def prettify_key(key):

    return (
        str(key)
        .replace("_", " ")
        .strip()
        .title()
    )


def render_value(value):

    if value is None:

        st.caption(
            "Not disclosed"
        )

        return


    if isinstance(
        value,
        bool
    ):

        st.write(
            "Yes" if value else "No"
        )

        return


    if isinstance(
        value,
        str
    ):

        st.write(value)

        return


    if isinstance(
        value,
        list
    ):

        if not value:

            st.caption(
                "None disclosed"
            )

            return

        for item in value:

            if isinstance(
                item,
                dict
            ):

                with st.container(
                    border=True
                ):

                    render_dictionary(
                        item
                    )

            else:

                st.markdown(
                    f"- {item}"
                )

        return


    if isinstance(
        value,
        dict
    ):

        render_dictionary(
            value
        )

        return


    st.write(value)


def render_dictionary(
    data,
    excluded=None
):

    if excluded is None:

        excluded = set()

    for key, value in (
        data.items()
    ):

        if key in excluded:
            continue

        st.markdown(
            f"**{prettify_key(key)}**"
        )

        render_value(
            value
        )


def render_sources(
    company
):

    website = company.get(
        "website"
    )

    sources = company.get(
        "sources",
        []
    )

    if website:

        st.markdown(
            f"**Official Website:** "
            f"[{website}]({website})"
        )

    if not sources:

        st.caption(
            "No stored source "
            "provenance."
        )

        return

    for source in sources:

        category = source.get(
            "category",
            "source"
        )

        url = source.get(
            "url"
        )

        collected_at = source.get(
            "collected_at"
        )

        if not url:
            continue

        text = (
            f"**{prettify_key(category)}:** "
            f"[{url}]({url})"
        )

        if collected_at:

            text += (
                f"  \nCollected: "
                f"{collected_at}"
            )

        st.markdown(text)


def project_status(
    config,
    company_results
):

    configured = len(
        config.get(
            "companies",
            []
        )
    )

    analyzed = len(
        company_results
    )

    return (
        configured,
        analyzed
    )


projects = discover_projects()


st.title(
    "📊 Competitive Intelligence Engine"
)

st.caption(
    "Reusable market and competitor "
    "analysis dashboard"
)


if not projects:

    st.warning(
        "No project configuration "
        "files were found."
    )

    st.stop()


project_lookup = {}

for project in projects:

    config = project[
        "config"
    ]

    display_name = config.get(
        "display_name",
        config.get(
            "project_name",
            "Project"
        )
    )

    project_lookup[
        display_name
    ] = project


selected_display_name = (
    st.sidebar.selectbox(
        "Competitive Analysis",
        list(
            project_lookup.keys()
        )
    )
)


selected_project = (
    project_lookup[
        selected_display_name
    ]
)


config = selected_project[
    "config"
]


project_name = config[
    "project_name"
]


analysis_type = config.get(
    "analysis_type",
    "Unknown"
)


company_results = (
    load_company_results(
        project_name
    )
)


comparison_path = (
    RESULTS_DIR
    / f"{project_name}_comparison.json"
)


comparison = None


if comparison_path.exists():

    try:

        comparison = load_json(
            comparison_path
        )

    except Exception:

        comparison = None


report_path = (
    REPORTS_DIR
    / f"{project_name}.html"
)


configured_count, analyzed_count = (
    project_status(
        config,
        company_results
    )
)


page = st.sidebar.radio(
    "View",
    [
        "Project Overview",
        "Company Explorer",
        "Market Comparison",
        "Sources",
        "Report"
    ]
)


st.sidebar.divider()


st.sidebar.caption(
    f"Analysis type: "
    f"{analysis_type}"
)


st.sidebar.caption(
    f"Configured companies: "
    f"{configured_count}"
)


st.sidebar.caption(
    f"Analyzed companies: "
    f"{analyzed_count}"
)


if page == "Project Overview":

    st.header(
        selected_display_name
    )


    column1, column2, column3 = (
        st.columns(3)
    )


    column1.metric(
        "Companies",
        configured_count
    )


    column2.metric(
        "Analyzed",
        analyzed_count
    )


    completion = 0

    if configured_count:

        completion = round(
            (
                analyzed_count
                / configured_count
            )
            * 100
        )


    column3.metric(
        "Completion",
        f"{completion}%"
    )


    st.progress(
        min(
            completion / 100,
            1.0
        )
    )


    st.subheader(
        "Project Information"
    )


    st.write(
        f"**Analysis Type:** "
        f"{analysis_type}"
    )


    st.write(
        f"**Project ID:** "
        f"`{project_name}`"
    )


    st.subheader(
        "Companies"
    )


    companies = config.get(
        "companies",
        []
    )


    for company in companies:

        name = company.get(
            "name",
            "Company"
        )

        url = company.get(
            "url",
            ""
        )

        analyzed_names = {
            item.get(
                "company_name",
                ""
            ).lower()
            for item in company_results
        }


        analyzed = (
            name.lower()
            in analyzed_names
        )


        status = (
            "✅ Analyzed"
            if analyzed
            else "⏳ Not analyzed"
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {name}"
            )

            st.write(status)

            if url:

                st.markdown(
                    f"[Official website]"
                    f"({url})"
                )


    if comparison:

        st.subheader(
            "Market Bottom Line"
        )

        bottom_line = (
            comparison.get(
                "bottom_line"
            )
        )

        if bottom_line:

            st.info(
                bottom_line
            )


elif page == "Company Explorer":

    st.header(
        "Company Explorer"
    )


    if not company_results:

        st.warning(
            "No company analyses "
            "exist for this project yet."
        )

        st.stop()


    company_lookup = {}


    for company in company_results:

        name = company.get(
            "company_name",
            "Company"
        )

        company_lookup[
            name
        ] = company


    selected_company_name = (
        st.selectbox(
            "Choose a company",
            sorted(
                company_lookup.keys()
            )
        )
    )


    company = (
        company_lookup[
            selected_company_name
        ]
    )


    st.subheader(
        selected_company_name
    )


    website = company.get(
        "website"
    )


    if website:

        st.markdown(
            f"[Visit official website]"
            f"({website})"
        )


    excluded_fields = {
        "company_name",
        "website",
        "sources"
    }


    for key, value in (
        company.items()
    ):

        if key in excluded_fields:
            continue


        with st.expander(
            prettify_key(key),
            expanded=False
        ):

            render_value(
                value
            )


    st.divider()


    st.subheader(
        "Source Provenance"
    )


    render_sources(
        company
    )


elif page == "Market Comparison":

    st.header(
        "Market Comparison"
    )


    if not comparison:

        st.warning(
            "No market comparison "
            "has been generated yet."
        )

        st.stop()


    market_overview = (
        comparison.get(
            "market_overview"
        )
    )


    if market_overview:

        st.subheader(
            "Market Overview"
        )

        st.write(
            market_overview
        )


    companies_comparison = (
        comparison.get(
            "companies",
            []
        )
    )


    if companies_comparison:

        st.subheader(
            "Company Positions"
        )


        for company in (
            companies_comparison
        ):

            name = company.get(
                "company_name",
                "Company"
            )


            with st.expander(
                name
            ):

                render_dictionary(
                    company,
                    excluded={
                        "company_name"
                    }
                )


    for key, value in (
        comparison.items()
    ):

        if key in {
            "market_overview",
            "companies",
            "bottom_line"
        }:

            continue


        st.subheader(
            prettify_key(key)
        )

        render_value(
            value
        )


    bottom_line = (
        comparison.get(
            "bottom_line"
        )
    )


    if bottom_line:

        st.subheader(
            "Bottom Line"
        )

        st.success(
            bottom_line
        )


elif page == "Sources":

    st.header(
        "Research Sources"
    )


    if not company_results:

        st.warning(
            "No analyzed companies "
            "are available."
        )

        st.stop()


    for company in (
        company_results
    ):

        name = company.get(
            "company_name",
            "Company"
        )


        with st.expander(
            name
        ):

            render_sources(
                company
            )


elif page == "Report":

    st.header(
        "Competitive Intelligence Report"
    )


    if not report_path.exists():

        st.warning(
            "The HTML report has "
            "not been generated yet."
        )

        st.stop()


    report_html = (
        report_path.read_text(
            encoding="utf-8"
        )
    )


    st.success(
        "Report available."
    )


    st.download_button(
        label="Download HTML Report",
        data=report_html,
        file_name=(
            f"{project_name}.html"
        ),
        mime="text/html"
    )


    st.caption(
        "The downloadable report "
        "contains the market analysis, "
        "company profiles, and source "
        "provenance."
    )