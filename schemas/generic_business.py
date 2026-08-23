from typing import List, Optional

from pydantic import BaseModel


class GenericBusinessAnalysis(BaseModel):

    company_name: str

    value_proposition: str

    target_customers: List[str]

    products_services: List[str]

    core_technology: List[str]

    use_cases: List[str]

    industries_served: List[str]

    business_model: Optional[str] = None

    pricing_model: Optional[str] = None

    deployment_model: List[str]

    integrations: List[str]

    developer_tools: List[str]

    enterprise_features: List[str]

    major_customers: List[str]

    major_partnerships: List[str]

    geographic_presence: List[str]

    strengths: List[str]

    weaknesses: List[str]

    competitive_differentiators: List[str]

    customer_problems_addressed: List[str]

    technical_risks: List[str]

    business_risks: List[str]

    marketing_message: str

    messaging_gaps: List[str]

    data_gaps: List[str]


class GenericCompanyComparison(BaseModel):

    company_name: str

    market_position: str

    target_customer_position: str

    product_position: str

    technology_position: str

    commercial_position: str

    biggest_strength: str

    biggest_weakness: str

    key_differentiator: str

    primary_risk: str


class GenericMarketComparison(BaseModel):

    market_overview: str

    companies: List[
        GenericCompanyComparison
    ]

    market_leaders: List[str]

    strongest_product_positions: List[str]

    strongest_technology_positions: List[str]

    strongest_commercial_positions: List[str]

    strongest_enterprise_positions: List[str]

    highest_execution_risks: List[str]

    shared_industry_problems: List[str]

    customer_problems: List[str]

    market_gaps: List[str]

    strategic_opportunities: List[str]

    competitive_battlegrounds: List[str]

    important_metrics_to_watch: List[str]

    bottom_line: str