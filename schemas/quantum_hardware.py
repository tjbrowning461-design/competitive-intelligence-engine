from typing import List, Optional

from pydantic import BaseModel


class QuantumHardwareAnalysis(BaseModel):

    company_name: str

    value_proposition: str

    target_customers: List[str]

    qubit_modality: str

    computing_models: List[str]

    hardware_architecture: str

    current_systems: List[str]

    physical_qubit_scale: Optional[str] = None

    demonstrated_logical_qubits: Optional[str] = None

    one_qubit_fidelity: Optional[str] = None

    two_qubit_fidelity: Optional[str] = None

    connectivity: Optional[str] = None

    coherence: Optional[str] = None

    gate_speed: Optional[str] = None

    error_correction_strategy: Optional[str] = None

    fault_tolerance_strategy: Optional[str] = None

    roadmap: List[str]

    cloud_access: Optional[bool] = None

    on_premise_available: Optional[bool] = None

    access_methods: List[str]

    manufacturing_strategy: Optional[str] = None

    software_stack: List[str]

    developer_tools: List[str]

    commercial_deployments: List[str]

    major_partnerships: List[str]

    strengths: List[str]

    weaknesses: List[str]

    competitive_differentiators: List[str]

    technical_risks: List[str]

    commercialization_risks: List[str]

    marketing_message: str

    messaging_gaps: List[str]

    data_gaps: List[str]


class HardwareCompanyComparison(BaseModel):

    company_name: str

    qubit_modality: str

    market_position: str

    technical_position: str

    commercial_position: str

    biggest_strength: str

    biggest_weakness: str

    key_differentiator: str

    fault_tolerance_position: str

    scalability_position: str

    roadmap_credibility: str

    primary_risk: str


class QuantumHardwareComparison(BaseModel):

    market_overview: str

    companies: List[
        HardwareCompanyComparison
    ]

    architecture_battlegrounds: List[str]

    strongest_technical_evidence: List[str]

    strongest_commercial_positions: List[str]

    strongest_fault_tolerance_positions: List[str]

    strongest_scalability_theses: List[str]

    highest_execution_risks: List[str]

    shared_industry_problems: List[str]

    customer_problems: List[str]

    market_gaps: List[str]

    strategic_opportunities: List[str]

    important_metrics_to_watch: List[str]

    bottom_line: str