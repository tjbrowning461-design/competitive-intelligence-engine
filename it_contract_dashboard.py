import hmac
import json
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT SETTINGS
# =========================================================

PROJECT_NAME = (
    "it_contract_negotiation_"
    "consulting_and_services"
)

RESULTS_DIR = Path("results")

COMPANY_DIR = (
    RESULTS_DIR
    / PROJECT_NAME
)

COMPARISON_FILE = (
    RESULTS_DIR
    / f"{PROJECT_NAME}_comparison.json"
)

REPORT_FILE = (
    Path("reports")
    / f"{PROJECT_NAME}.html"
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=(
        "IT Contract Negotiation "
        "Competitive Intelligence"
    ),
    page_icon="📊",
    layout="wide"
)


# =========================================================
# PASSWORD PROTECTION
# =========================================================

def check_password():

    if st.session_state.get(
        "authenticated",
        False
    ):
        return True

    st.title(
        "🔒 IT Contract Negotiation "
        "Competitive Intelligence"
    )

    st.write(
        "This competitive intelligence report "
        "is private. Enter the access password "
        "to continue."
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Access Report",
        type="primary"
    ):

        if "APP_PASSWORD" not in st.secrets:

            st.error(
                "The app password has not "
                "been configured."
            )

            return False

        correct_password = str(
            st.secrets[
                "APP_PASSWORD"
            ]
        )

        if hmac.compare_digest(
            password,
            correct_password
        ):

            st.session_state[
                "authenticated"
            ] = True

            st.rerun()

        else:

            st.error(
                "Incorrect password."
            )

    return False


if not check_password():
    st.stop()


# =========================================================
# DATA HELPERS
# =========================================================

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

        st.caption(
            "None disclosed"
        )

        return

    for item in items:

        if isinstance(
            item,
            dict
        ):

            with st.container(
                border=True
            ):

                for key, value in (
                    item.items()
                ):

                    st.markdown(
                        f"**{prettify_key(key)}**"
                    )

                    render_value(
                        value
                    )

        else:

            st.markdown(
                f"- {item}"
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
            "Yes"
            if value
            else "No"
        )

        return

    if isinstance(
        value,
        str
    ):

        st.write(
            value
        )

        return

    if isinstance(
        value,
        list
    ):

        render_list(
            value
        )

        return

    if isinstance(
        value,
        dict
    ):

        for key, item in (
            value.items()
        ):

            st.markdown(
                f"**{prettify_key(key)}**"
            )

            render_value(
                item
            )

        return

    st.write(
        value
    )


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


def company_meta_description(
    company
):

    description = (
        company.get(
            "value_proposition"
        )
        or company.get(
            "marketing_message"
        )
        or (
            "Competitive profile available "
            "in the Company Explorer."
        )
    )

    description = " ".join(
        str(description).split()
    )

    max_length = 155

    if len(description) > max_length:

        description = (
            description[
                :max_length
            ]
        )

        if " " in description:

            description = (
                description.rsplit(
                    " ",
                    1
                )[0]
            )

        description += "..."

    return description


# =========================================================
# LOAD PROJECT DATA
# =========================================================

companies = (
    load_company_results()
)


comparison = None


if COMPARISON_FILE.exists():

    try:

        comparison = (
            load_json(
                COMPARISON_FILE
            )
        )

    except Exception:

        comparison = None


if not companies:

    st.error(
        "No company analysis files "
        "were found."
    )

    st.stop()


company_lookup = {

    company.get(
        "company_name",
        "Unknown"
    ): company

    for company in companies
}


company_names = sorted(
    company_lookup.keys()
)


# =========================================================
# SESSION STATE
# =========================================================

if (
    "current_page"
    not in st.session_state
):

    st.session_state[
        "current_page"
    ] = "Executive Overview"


if (
    "selected_company"
    not in st.session_state
):

    st.session_state[
        "selected_company"
    ] = company_names[0]


def open_company(
    company_name
):

    st.session_state[
        "current_page"
    ] = "Company Explorer"

    st.session_state[
        "selected_company"
    ] = company_name


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "Navigation"
)


navigation_pages = [
    "Executive Overview",
    "Competitor Comparison",
    "Company Explorer",
    "Strengths & Weaknesses",
    "Market Gaps",
    "Sources",
    "Full Report",
]


page = st.sidebar.radio(
    "Choose a section",
    navigation_pages,
    key="current_page",
    label_visibility="collapsed"
)


st.sidebar.divider()


st.sidebar.metric(
    "Competitors Analyzed",
    len(companies)
)


# =========================================================
# SIDEBAR COMPETITOR DIRECTORY
# =========================================================

st.sidebar.markdown(
    "### Competitors"
)


for index, name in enumerate(
    company_names
):

    company = (
        company_lookup[
            name
        ]
    )

    st.sidebar.markdown(
        f"**{name}**"
    )

    st.sidebar.caption(
        company_meta_description(
            company
        )
    )

    st.sidebar.button(
        "Open Company Explorer →",
        key=(
            f"sidebar_company_"
            f"{index}"
        ),
        on_click=open_company,
        args=(name,),
        use_container_width=True
    )

    if index < (
        len(company_names) - 1
    ):

        st.sidebar.markdown(
            "---"
        )


st.sidebar.divider()


st.sidebar.caption(
    "IT Contract Negotiation "
    "Consulting & Services"
)


if st.sidebar.button(
    "Log Out",
    use_container_width=True
):

    st.session_state[
        "authenticated"
    ] = False

    st.rerun()


# =========================================================
# APP HEADER
# =========================================================

st.title(
    "IT Contract Negotiation "
    "Consulting & Services"
)

st.caption(
    "Competitive Intelligence Dashboard"
)


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.header(
        "Executive Overview"
    )


    col1, col2, col3 = (
        st.columns(3)
    )


    col1.metric(
        "Companies Analyzed",
        len(companies)
    )


    market_gaps = []

    opportunities = []


    if comparison:

        market_gaps = (
            comparison.get(
                "market_gaps",
                []
            )
        )

        opportunities = (
            comparison.get(
                "strategic_opportunities",
                []
            )
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


        bottom_line = (
            comparison.get(
                "bottom_line"
            )
        )


        if bottom_line:

            st.subheader(
                "Bottom Line"
            )

            st.info(
                bottom_line
            )


        battlegrounds = (
            comparison.get(
                "competitive_battlegrounds",
                []
            )
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


    for name in company_names:

        company = (
            company_lookup[
                name
            ]
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {name}"
            )


            value = (
                company.get(
                    "value_proposition"
                )
            )


            if value:

                st.write(
                    value
                )


            website = (
                company.get(
                    "website"
                )
            )


            col1, col2 = (
                st.columns(
                    [1, 1]
                )
            )


            with col1:

                if website:

                    st.markdown(
                        f"[Official Website]"
                        f"({website})"
                    )


            with col2:

                st.button(
                    "View Company Profile →",
                    key=(
                        "overview_"
                        + name
                    ),
                    on_click=open_company,
                    args=(name,),
                    use_container_width=True
                )


# =========================================================
# COMPETITOR COMPARISON
# =========================================================

elif page == "Competitor Comparison":

    st.header(
        "Competitor Comparison"
    )


    if not comparison:

        st.warning(
            "No comparison file found."
        )

        st.stop()


    company_positions = (
        comparison.get(
            "companies",
            []
        )
    )


    if company_positions:

        rows = []


        for company in (
            company_positions
        ):

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

                    "Target Customer Position":
                        company.get(
                            "target_customer_position"
                        ),

                    "Product Position":
                        company.get(
                            "product_position"
                        ),

                    "Technology Position":
                        company.get(
                            "technology_position"
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


    for title, key in (
        comparison_sections
    ):

        values = (
            comparison.get(
                key,
                []
            )
        )


        if values:

            st.subheader(
                title
            )

            render_list(
                values
            )


# =========================================================
# COMPANY EXPLORER
# =========================================================

elif page == "Company Explorer":

    st.header(
        "Company Explorer"
    )


    if (
        st.session_state.get(
            "selected_company"
        )
        not in company_names
    ):

        st.session_state[
            "selected_company"
        ] = company_names[0]


    selected_company = (
        st.selectbox(
            "Choose a competitor",
            company_names,
            key="selected_company"
        )
    )


    company = (
        company_lookup[
            selected_company
        ]
    )


    st.header(
        selected_company
    )


    website = (
        company.get(
            "website"
        )
    )


    if website:

        st.markdown(
            f"[Visit Official Website]"
            f"({website})"
        )


    value_proposition = (
        company.get(
            "value_proposition"
        )
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
            "Developer Tools",
            "developer_tools"
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
            "Geographic Presence",
            "geographic_presence"
        ),

        (
            "Competitive Differentiators",
            "competitive_differentiators"
        ),
    ]


    for title, key in (
        key_sections
    ):

        value = (
            company.get(
                key
            )
        )


        if value:

            with st.expander(
                title
            ):

                render_value(
                    value
                )


    col1, col2 = (
        st.columns(2)
    )


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


# =========================================================
# STRENGTHS AND WEAKNESSES
# =========================================================

elif page == "Strengths & Weaknesses":

    st.header(
        "Strengths, Weaknesses & Risks"
    )


    selected_company = (
        st.selectbox(
            "Choose a competitor",
            company_names,
            key="strength_company"
        )
    )


    company = (
        company_lookup[
            selected_company
        ]
    )


    st.subheader(
        selected_company
    )


    col1, col2 = (
        st.columns(2)
    )


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


# =========================================================
# MARKET GAPS
# =========================================================

elif page == "Market Gaps":

    st.header(
        "Market Gaps & "
        "Strategic Opportunities"
    )


    if not comparison:

        st.warning(
            "No comparison file found."
        )

        st.stop()


    col1, col2 = (
        st.columns(2)
    )


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


# =========================================================
# SOURCES
# =========================================================

elif page == "Sources":

    st.header(
        "Research Sources"
    )


    st.caption(
        "Sources collected from official "
        "competitor websites during "
        "the analysis."
    )


    for name in company_names:

        company = (
            company_lookup[
                name
            ]
        )


        with st.expander(
            name
        ):

            source_section(
                company
            )


# =========================================================
# FULL REPORT
# =========================================================

elif page == "Full Report":

    st.header(
        "Full Competitive "
        "Intelligence Report"
    )


    if not REPORT_FILE.exists():

        st.warning(
            "The HTML report was "
            "not found."
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
            label=(
                "Download Full HTML Report"
            ),
            data=report_html,
            file_name=(
                "it_contract_negotiation_"
                "competitive_intelligence.html"
            ),
            mime="text/html"
        )


        st.caption(
            "The report includes the "
            "market comparison, individual "
            "competitor profiles, risks, "
            "opportunities, and source "
            "provenance."
        )