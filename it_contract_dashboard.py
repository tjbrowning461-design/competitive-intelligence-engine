import json
from pathlib import Path

import streamlit as st


PROJECT_NAME = "it_contract_negotiation_consulting_and_services"

RESULTS_DIR = Path("results")
COMPANY_DIR = RESULTS_DIR / PROJECT_NAME

COMPARISON_FILE = (
    RESULTS_DIR
    / f"{PROJECT_NAME}_comparison.json"
)

REPORT_FILE = (
    Path("reports")
    / f"{PROJECT_NAME}.html"
)


st.set_page_config(
    page_title="IT Contract Negotiation Competitive Intelligence",
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


def load_company_results():
    companies = []

    if not COMPANY_DIR.exists():
        return companies

    for path in sorted(
        COMPANY_DIR.glob("*.json")
    ):
        try:
            companies.append(
                load_json(path)
            )
        except Exception:
            continue

    return companies


def prettify_key(key):
    return (
        str(key)
        .replace("_", " ")
        .strip()
        .title()
    )


def render_list(items):
    if not items:
        st.caption("None disclosed")
        return

    for item in items:
        st.markdown(f"- {item}")


def render_value(value):
    if value is None:
        st.caption("Not disclosed")
        return

    if isinstance(value, bool):
        st.write(
            "Yes"
            if value
            else "No"
        )
        return

    if isinstance(value, str):
        st.write(value)
        return

    if isinstance(value, list):
        render_list(value)
        return

    if isinstance(value, dict):
        for key, item in value.items():
            st.markdown(
                f"**{prettify_key(key)}**"
            )
            render_value(item)
        return

    st.write(value)


def source_section(company):
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
            "No source provenance stored."
        )
        return

    for source in sources:
        url = source.get(
            "url"
        )

        category = source.get(
            "category",
            "source"
        )

        collected_at = source.get(
            "collected_at"
        )

        if not url:
            continue

        st.markdown(
            f"**{prettify_key(category)}:** "
            f"[{url}]({url})"
        )

        if collected_at:
            st.caption(
                f"Collected: {collected_at}"
            )


companies = load_company_results()

comparison = None

if COMPARISON_FILE.exists():
    try:
        comparison = load_json(
            COMPARISON_FILE
        )
    except Exception:
        comparison = None


st.title(
    "IT Contract Negotiation Consulting & Services"
)

st.caption(
    "Competitive Intelligence Dashboard"
)


if not companies:
    st.error(
        "No company analysis files were found."
    )
    st.stop()


company_lookup = {
    company.get(
        "company_name",
        "Unknown"
    ): company
    for company in companies
}


page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Competitor Comparison",
        "Company Explorer",
        "Strengths & Weaknesses",
        "Market Gaps",
        "Sources",
        "Full Report",
    ]
)


st.sidebar.divider()

st.sidebar.metric(
    "Competitors Analyzed",
    len(companies)
)

st.sidebar.caption(
    "IT Contract Negotiation "
    "Consulting & Services"
)


if page == "Executive Overview":

    st.header(
        "Executive Overview"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Companies Analyzed",
        len(companies)
    )

    if comparison:
        market_gaps = comparison.get(
            "market_gaps",
            []
        )

        opportunities = comparison.get(
            "strategic_opportunities",
            []
        )

        col2.metric(
            "Market Gaps",
            len(market_gaps)
        )

        col3.metric(
            "Strategic Opportunities",
            len(opportunities)
        )

    st.divider()

    if comparison:

        market_overview = comparison.get(
            "market_overview"
        )

        if market_overview:
            st.subheader(
                "Market Overview"
            )
            st.write(
                market_overview
            )

        bottom_line = comparison.get(
            "bottom_line"
        )

        if bottom_line:
            st.subheader(
                "Bottom Line"
            )

            st.info(
                bottom_line
            )

        battlegrounds = comparison.get(
            "competitive_battlegrounds",
            []
        )

        if battlegrounds:
            st.subheader(
                "Competitive Battlegrounds"
            )

            render_list(
                battlegrounds
            )

    st.subheader(
        "Competitors"
    )

    for name, company in sorted(
        company_lookup.items()
    ):

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {name}"
            )

            value = company.get(
                "value_proposition"
            )

            if value:
                st.write(value)

            website = company.get(
                "website"
            )

            if website:
                st.markdown(
                    f"[Official Website]"
                    f"({website})"
                )


elif page == "Competitor Comparison":

    st.header(
        "Competitor Comparison"
    )

    if not comparison:
        st.warning(
            "No comparison file found."
        )
        st.stop()

    company_positions = comparison.get(
        "companies",
        []
    )

    if company_positions:

        rows = []

        for company in company_positions:

            rows.append(
                {
                    "Company":
                        company.get(
                            "company_name"
                        ),

                    "Market Position":
                        company.get(
                            "market_position"
                        ),

                    "Product Position":
                        company.get(
                            "product_position"
                        ),

                    "Commercial Position":
                        company.get(
                            "commercial_position"
                        ),

                    "Biggest Strength":
                        company.get(
                            "biggest_strength"
                        ),

                    "Biggest Weakness":
                        company.get(
                            "biggest_weakness"
                        ),

                    "Key Differentiator":
                        company.get(
                            "key_differentiator"
                        ),

                    "Primary Risk":
                        company.get(
                            "primary_risk"
                        ),
                }
            )

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

    comparison_sections = [
        (
            "Market Leaders",
            "market_leaders"
        ),
        (
            "Strongest Product Positions",
            "strongest_product_positions"
        ),
        (
            "Strongest Technology Positions",
            "strongest_technology_positions"
        ),
        (
            "Strongest Commercial Positions",
            "strongest_commercial_positions"
        ),
        (
            "Strongest Enterprise Positions",
            "strongest_enterprise_positions"
        ),
        (
            "Highest Execution Risks",
            "highest_execution_risks"
        ),
        (
            "Important Metrics to Watch",
            "important_metrics_to_watch"
        ),
    ]

    for title, key in comparison_sections:

        values = comparison.get(
            key,
            []
        )

        if values:

            st.subheader(title)

            render_list(values)


elif page == "Company Explorer":

    st.header(
        "Company Explorer"
    )

    selected_company = st.selectbox(
        "Choose a competitor",
        sorted(
            company_lookup.keys()
        )
    )

    company = company_lookup[
        selected_company
    ]

    st.header(
        selected_company
    )

    website = company.get(
        "website"
    )

    if website:
        st.markdown(
            f"[Visit Official Website]"
            f"({website})"
        )

    value_proposition = company.get(
        "value_proposition"
    )

    if value_proposition:
        st.subheader(
            "Value Proposition"
        )
        st.write(
            value_proposition
        )

    key_sections = [
        (
            "Target Customers",
            "target_customers"
        ),
        (
            "Products & Services",
            "products_services"
        ),
        (
            "Core Technology",
            "core_technology"
        ),
        (
            "Use Cases",
            "use_cases"
        ),
        (
            "Industries Served",
            "industries_served"
        ),
        (
            "Customer Problems Addressed",
            "customer_problems_addressed"
        ),
        (
            "Deployment Model",
            "deployment_model"
        ),
        (
            "Integrations",
            "integrations"
        ),
        (
            "Enterprise Features",
            "enterprise_features"
        ),
        (
            "Major Customers",
            "major_customers"
        ),
        (
            "Major Partnerships",
            "major_partnerships"
        ),
        (
            "Competitive Differentiators",
            "competitive_differentiators"
        ),
    ]

    for title, key in key_sections:

        value = company.get(
            key
        )

        if value:

            with st.expander(
                title
            ):
                render_value(value)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Business Model"
        )

        render_value(
            company.get(
                "business_model"
            )
        )

    with col2:

        st.subheader(
            "Pricing Model"
        )

        render_value(
            company.get(
                "pricing_model"
            )
        )

    st.subheader(
        "Marketing Message"
    )

    render_value(
        company.get(
            "marketing_message"
        )
    )


elif page == "Strengths & Weaknesses":

    st.header(
        "Strengths, Weaknesses & Risks"
    )

    selected_company = st.selectbox(
        "Choose a competitor",
        sorted(
            company_lookup.keys()
        ),
        key="strength_company"
    )

    company = company_lookup[
        selected_company
    ]

    st.subheader(
        selected_company
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Strengths"
        )

        render_list(
            company.get(
                "strengths",
                []
            )
        )

        st.markdown(
            "### Competitive Differentiators"
        )

        render_list(
            company.get(
                "competitive_differentiators",
                []
            )
        )

    with col2:

        st.markdown(
            "### Weaknesses"
        )

        render_list(
            company.get(
                "weaknesses",
                []
            )
        )

        st.markdown(
            "### Business Risks"
        )

        render_list(
            company.get(
                "business_risks",
                []
            )
        )

    st.divider()

    st.subheader(
        "Technical Risks"
    )

    render_list(
        company.get(
            "technical_risks",
            []
        )
    )

    st.subheader(
        "Messaging Gaps"
    )

    render_list(
        company.get(
            "messaging_gaps",
            []
        )
    )

    st.subheader(
        "Data Gaps"
    )

    render_list(
        company.get(
            "data_gaps",
            []
        )
    )


elif page == "Market Gaps":

    st.header(
        "Market Gaps & Strategic Opportunities"
    )

    if not comparison:
        st.warning(
            "No comparison file found."
        )
        st.stop()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Market Gaps"
        )

        render_list(
            comparison.get(
                "market_gaps",
                []
            )
        )

    with col2:

        st.subheader(
            "Strategic Opportunities"
        )

        render_list(
            comparison.get(
                "strategic_opportunities",
                []
            )
        )

    st.divider()

    st.subheader(
        "Shared Industry Problems"
    )

    render_list(
        comparison.get(
            "shared_industry_problems",
            []
        )
    )

    st.subheader(
        "Customer Problems"
    )

    render_list(
        comparison.get(
            "customer_problems",
            []
        )
    )

    st.subheader(
        "Competitive Battlegrounds"
    )

    render_list(
        comparison.get(
            "competitive_battlegrounds",
            []
        )
    )


elif page == "Sources":

    st.header(
        "Research Sources"
    )

    st.caption(
        "Sources collected from official "
        "competitor websites during the analysis."
    )

    for name, company in sorted(
        company_lookup.items()
    ):

        with st.expander(name):

            source_section(
                company
            )


elif page == "Full Report":

    st.header(
        "Full Competitive Intelligence Report"
    )

    if not REPORT_FILE.exists():

        st.warning(
            "The HTML report was not found."
        )

    else:

        report_html = (
            REPORT_FILE.read_text(
                encoding="utf-8"
            )
        )

        st.success(
            "Full report available."
        )

        st.download_button(
            label="Download Full HTML Report",
            data=report_html,
            file_name=(
                "it_contract_negotiation_"
                "competitive_intelligence.html"
            ),
            mime="text/html"
        )

        st.caption(
            "The report includes the market "
            "comparison, individual competitor "
            "profiles, risks, opportunities, "
            "and source provenance."
        )