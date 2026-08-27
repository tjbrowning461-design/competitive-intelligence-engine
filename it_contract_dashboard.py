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
# COMPANY DESCRIPTIONS
# =========================================================

# These are intentionally very short.
# They appear beneath each competitor name
# in the left sidebar.

SHORT_DESCRIPTIONS = {

    "Mitigo Partners":
        "Enterprise IT negotiation specialists.",

    "UpperEdge":
        "IT sourcing and negotiation advisors.",

    "Dark Horse Intelligence":
        "Technology deal negotiation specialists.",

    "Miro Consulting":
        "Software licensing and audit advisors.",

    "ClarityQR":
        "IT contract cost-optimization specialists.",

    "Invictus Partners":
        "Enterprise software licensing advisors.",

    "Engage Delta":
        "Independent IT negotiation consultants.",

    "Dryden Group":
        "Strategic sourcing and procurement consultants.",
}


# These longer descriptions are used only
# in the Executive Overview.

LONG_DESCRIPTIONS = {

    "Mitigo Partners": (
        "Mitigo Partners is an independent technology negotiation "
        "advisory firm focused on helping organizations improve the "
        "financial and commercial outcomes of IT and software deals. "
        "Founded by former software executives, Mitigo can negotiate "
        "directly with technology suppliers or operate behind the "
        "scenes as an advisor to an internal sourcing team. Its approach "
        "combines supplier experience, benchmark information, deal "
        "assessment, and negotiation strategy to help clients secure "
        "stronger pricing and business terms across enterprise software, "
        "SaaS, and other technology purchases."
    ),

    "UpperEdge": (
        "UpperEdge is a buy-side IT sourcing, negotiation, and commercial "
        "advisory firm that helps organizations maximize the value of "
        "their relationships with major technology suppliers. The firm "
        "supports clients across the sourcing lifecycle, including "
        "strategy, supplier evaluation, proposal analysis, negotiation, "
        "contracting, cost optimization, and project execution. UpperEdge "
        "uses market intelligence, deal benchmarks, proprietary tools, "
        "and supplier-specific expertise to help enterprises negotiate "
        "more competitive pricing, stronger commercial terms, greater "
        "flexibility, and lower long-term technology risk."
    ),

    "Dark Horse Intelligence": (
        "Dark Horse Intelligence is a specialized technology contract "
        "negotiation and deal advisory firm focused heavily on the final "
        "stages of software renewals and new purchases. The company helps "
        "organizations determine whether a vendor's proposed pricing is "
        "actually competitive and develops negotiation strategies designed "
        "to improve the final commercial outcome. Dark Horse emphasizes "
        "its independence from technology vendors and draws on a network "
        "of former software sales executives to provide insight into "
        "vendor pricing behavior, sales tactics, negotiation leverage, "
        "and deal structure."
    ),

    "Miro Consulting": (
        "Miro Consulting is a software licensing and software asset "
        "management advisory firm that helps organizations manage the "
        "financial, contractual, and compliance risks associated with "
        "major enterprise software vendors. Its services include license "
        "management, software audit advisory and defense, contract "
        "negotiation support, cost containment, support management, "
        "subscription analysis, and cloud licensing guidance. Miro's "
        "work is particularly focused on helping clients understand their "
        "software entitlements, prepare for vendor negotiations and audits, "
        "maintain compliance, and improve the return on large software "
        "investments."
    ),

    "ClarityQR": (
        "ClarityQR is an IT contract negotiation and cost-optimization "
        "firm that helps organizations reduce spending on new and existing "
        "technology agreements. Its specialists work across software, SaaS, "
        "cloud, and other IT contracts, using licensing expertise, pricing "
        "benchmarks, contract analysis, and negotiation strategy to identify "
        "potential savings. ClarityQR can support internal procurement teams "
        "or participate more directly in negotiations, with services covering "
        "contract renewals, new purchases, contract optimization, hardware "
        "procurement, and negotiation advisory."
    ),

    "Invictus Partners": (
        "Invictus Partners is an independent enterprise software advisory "
        "firm focused on helping organizations gain greater control over "
        "software costs, licensing, compliance, and vendor relationships. "
        "Its services span software contract negotiation, license advisory, "
        "software audit defense, software asset management, optimization, "
        "vendor management, and enterprise software strategy. The firm draws "
        "on specialists with experience inside major software vendors and "
        "uses detailed knowledge of vendor licensing models and sales "
        "processes to help clients prepare for renewals, reduce unnecessary "
        "software expenditure, manage compliance exposure, and negotiate "
        "stronger commercial agreements."
    ),

    "Engage Delta": (
        "Engage Delta is an independent IT negotiation consulting and "
        "advisory firm that helps organizations improve high-value "
        "technology supplier deals. Its work covers enterprise software, "
        "SaaS, cloud, infrastructure, software audits, compliance disputes, "
        "and other strategic vendor relationships. Engage Delta develops "
        "tailored negotiation frameworks, playbooks, contract optimization "
        "strategies, and deal guidance designed to strengthen leverage, "
        "reduce cost and commercial risk, and protect long-term value. "
        "The firm positions its services as a complement to internal "
        "procurement, legal, finance, and IT teams rather than a replacement "
        "for them."
    ),

    "Dryden Group": (
        "Dryden Group is a strategic sourcing, procurement, and indirect "
        "spend advisory firm that helps organizations improve purchasing "
        "performance and reduce operating costs. Its capabilities include "
        "strategic sourcing, spend assessment, supplier selection and "
        "management, benchmarking, procurement transformation, and contract "
        "negotiation. Dryden uses procurement data, vendor information, "
        "market research, and category expertise to evaluate existing "
        "spending and identify opportunities for better pricing and terms. "
        "Its broader procurement focus extends beyond technology, while its "
        "IT-related work includes technology sourcing, supplier management, "
        "benchmarking, and vendor contract negotiations."
    ),
}


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=(
        "IT Contract Negotiation "
        "Competitive Intelligence"
    ),
    page_icon="📊",
    layout="wide",
)


# =========================================================
# STYLING
# =========================================================

st.markdown(
    """
    <style>

    /*
    Competitor names in the sidebar are
    real Streamlit buttons.

    They are styled to look like links so
    clicking them stays in the same session
    and does not require another password.
    */

    [data-testid="stSidebar"] button[kind="tertiary"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        min-height: 0 !important;
        height: auto !important;
        justify-content: flex-start !important;
        text-align: left !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] button[kind="tertiary"] p {
        font-weight: 700 !important;
        text-decoration: underline !important;
        text-underline-offset: 3px !important;
        text-align: left !important;
    }

    [data-testid="stSidebar"] button[kind="tertiary"]:hover p {
        opacity: 0.72;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PASSWORD PROTECTION
# =========================================================

def check_password():

    if st.session_state.get(
        "authenticated",
        False,
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
        type="password",
    )

    if st.button(
        "Access Report",
        type="primary",
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
            correct_password,
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
        encoding="utf-8",
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


def render_value(value):

    if value is None:

        st.caption(
            "Not disclosed"
        )

        return

    if isinstance(
        value,
        bool,
    ):

        st.write(
            "Yes"
            if value
            else "No"
        )

        return

    if isinstance(
        value,
        str,
    ):

        st.write(
            value
        )

        return

    if isinstance(
        value,
        list,
    ):

        if not value:

            st.caption(
                "None disclosed"
            )

            return

        for item in value:

            if isinstance(
                item,
                dict,
            ):

                with st.container(
                    border=True
                ):

                    for (
                        key,
                        nested_value,
                    ) in item.items():

                        st.markdown(
                            f"**{prettify_key(key)}**"
                        )

                        render_value(
                            nested_value
                        )

            else:

                st.markdown(
                    f"- {item}"
                )

        return

    if isinstance(
        value,
        dict,
    ):

        for (
            key,
            nested_value,
        ) in value.items():

            st.markdown(
                f"**{prettify_key(key)}**"
            )

            render_value(
                nested_value
            )

        return

    st.write(
        value
    )


def render_list(items):

    render_value(
        items
    )


def source_section(company):

    website = company.get(
        "website"
    )

    sources = company.get(
        "sources",
        [],
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
            "source",
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


def short_description_for(
    company_name
):

    return SHORT_DESCRIPTIONS.get(
        company_name,
        "IT contract and technology advisory firm.",
    )


def long_description_for(
    company_name,
    company,
):

    custom_description = (
        LONG_DESCRIPTIONS.get(
            company_name
        )
    )

    if custom_description:

        return custom_description

    value_proposition = (
        company.get(
            "value_proposition"
        )
    )

    if value_proposition:

        return value_proposition

    return (
        "This company is included in the "
        "competitive analysis of IT contract "
        "negotiation consulting and advisory "
        "providers."
    )


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
        "Unknown",
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


# =========================================================
# SAME-WINDOW COMPANY NAVIGATION
# =========================================================

def open_company(
    company_name
):

    st.session_state[
        "selected_company"
    ] = company_name

    st.session_state[
        "current_page"
    ] = "Company Explorer"


# =========================================================
# SIDEBAR
# =========================================================

navigation_pages = [

    "Executive Overview",

    "Competitor Comparison",

    "Company Explorer",

    "Strengths & Weaknesses",

    "Market Gaps",

    "Sources",

    "Full Report",
]


st.sidebar.markdown(
    "## Navigation"
)


page = st.sidebar.radio(
    "Navigation",
    navigation_pages,
    key="current_page",
    label_visibility="collapsed",
)


st.sidebar.divider()


st.sidebar.metric(
    "Competitors Analyzed",
    len(companies),
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

    # Looks like a hyperlink but uses
    # Streamlit navigation internally.

    st.sidebar.button(
        name,
        key=(
            f"competitor_link_"
            f"{index}"
        ),
        type="tertiary",
        on_click=open_company,
        args=(name,),
        use_container_width=False,
    )


    # Very short company description.

    st.sidebar.caption(
        short_description_for(
            name
        )
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
    use_container_width=True,
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
        len(companies),
    )


    market_gaps = (
        comparison.get(
            "market_gaps",
            [],
        )
        if comparison
        else []
    )


    opportunities = (
        comparison.get(
            "strategic_opportunities",
            [],
        )
        if comparison
        else []
    )


    col2.metric(
        "Market Gaps",
        len(market_gaps),
    )


    col3.metric(
        "Strategic Opportunities",
        len(opportunities),
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
                [],
            )
        )


        if battlegrounds:

            st.subheader(
                "Competitive Battlegrounds"
            )

            render_list(
                battlegrounds
            )


    st.divider()


    st.header(
        "Competitor Overview"
    )


    st.caption(
        "A high-level look at each company "
        "included in the competitive analysis."
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

            st.subheader(
                name
            )


            # Longer executive-level
            # company description.

            st.write(
                long_description_for(
                    name,
                    company,
                )
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
            [],
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
            hide_index=True,
        )


    comparison_sections = [

        (
            "Market Leaders",
            "market_leaders",
        ),

        (
            "Strongest Product Positions",
            "strongest_product_positions",
        ),

        (
            "Strongest Technology Positions",
            "strongest_technology_positions",
        ),

        (
            "Strongest Commercial Positions",
            "strongest_commercial_positions",
        ),

        (
            "Strongest Enterprise Positions",
            "strongest_enterprise_positions",
        ),

        (
            "Highest Execution Risks",
            "highest_execution_risks",
        ),

        (
            "Important Metrics to Watch",
            "important_metrics_to_watch",
        ),
    ]


    for (
        title,
        key,
    ) in comparison_sections:

        values = (
            comparison.get(
                key,
                [],
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
            key="selected_company",
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


    st.caption(
        short_description_for(
            selected_company
        )
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
            "target_customers",
        ),

        (
            "Products & Services",
            "products_services",
        ),

        (
            "Core Technology",
            "core_technology",
        ),

        (
            "Use Cases",
            "use_cases",
        ),

        (
            "Industries Served",
            "industries_served",
        ),

        (
            "Customer Problems Addressed",
            "customer_problems_addressed",
        ),

        (
            "Deployment Model",
            "deployment_model",
        ),

        (
            "Integrations",
            "integrations",
        ),

        (
            "Developer Tools",
            "developer_tools",
        ),

        (
            "Enterprise Features",
            "enterprise_features",
        ),

        (
            "Major Customers",
            "major_customers",
        ),

        (
            "Major Partnerships",
            "major_partnerships",
        ),

        (
            "Geographic Presence",
            "geographic_presence",
        ),

        (
            "Competitive Differentiators",
            "competitive_differentiators",
        ),
    ]


    for (
        title,
        key,
    ) in key_sections:

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
# STRENGTHS & WEAKNESSES
# =========================================================

elif page == "Strengths & Weaknesses":

    st.header(
        "Strengths, Weaknesses & Risks"
    )


    selected_company = (
        st.selectbox(
            "Choose a competitor",
            company_names,
            key="strength_company",
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
                [],
            )
        )


        st.markdown(
            "### Competitive Differentiators"
        )

        render_list(
            company.get(
                "competitive_differentiators",
                [],
            )
        )


    with col2:

        st.markdown(
            "### Weaknesses"
        )

        render_list(
            company.get(
                "weaknesses",
                [],
            )
        )


        st.markdown(
            "### Business Risks"
        )

        render_list(
            company.get(
                "business_risks",
                [],
            )
        )


    st.divider()


    st.subheader(
        "Technical Risks"
    )

    render_list(
        company.get(
            "technical_risks",
            [],
        )
    )


    st.subheader(
        "Messaging Gaps"
    )

    render_list(
        company.get(
            "messaging_gaps",
            [],
        )
    )


    st.subheader(
        "Data Gaps"
    )

    render_list(
        company.get(
            "data_gaps",
            [],
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
                [],
            )
        )


    with col2:

        st.subheader(
            "Strategic Opportunities"
        )

        render_list(
            comparison.get(
                "strategic_opportunities",
                [],
            )
        )


    st.divider()


    st.subheader(
        "Shared Industry Problems"
    )

    render_list(
        comparison.get(
            "shared_industry_problems",
            [],
        )
    )


    st.subheader(
        "Customer Problems"
    )

    render_list(
        comparison.get(
            "customer_problems",
            [],
        )
    )


    st.subheader(
        "Competitive Battlegrounds"
    )

    render_list(
        comparison.get(
            "competitive_battlegrounds",
            [],
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

        with st.expander(
            name
        ):

            source_section(
                company_lookup[
                    name
                ]
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
            mime="text/html",
        )


        st.caption(
            "The report includes the "
            "market comparison, individual "
            "competitor profiles, risks, "
            "opportunities, and source "
            "provenance."
        )