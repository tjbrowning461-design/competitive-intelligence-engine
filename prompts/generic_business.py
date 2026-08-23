COMPANY_ANALYSIS_PROMPT = """
You are conducting rigorous competitive intelligence
on a company.

Analyze ONLY the supplied official website evidence.

Do not invent facts or silently fill missing information
with outside knowledge.

If information is unavailable:

- use None where appropriate
- use an empty list where appropriate
- identify important missing information in data_gaps

Clearly distinguish between:

- products and capabilities available today
- demonstrated capabilities
- announced capabilities
- future plans
- roadmap claims

Never treat planned, announced, targeted, or projected
capabilities as currently available.

Analyze the company across areas including:

- value proposition
- target customers
- products and services
- technology
- use cases
- industries served
- business model
- pricing
- deployment
- integrations
- developer tooling
- enterprise features
- customers
- partnerships
- geographic presence
- competitive differentiation
- customer problems addressed
- technical risk
- business risk
- marketing positioning

Strengths and weaknesses may include reasonable
competitive assessments, but they must follow from
the supplied evidence.

Do not assume that the company is a market leader
simply because its own marketing describes it that way.

Distinguish company marketing claims from concrete
evidence wherever possible.

Identify important information that competitors,
customers, investors, or strategic decision-makers
would want but that the website does not disclose.

Return the result using the supplied structured schema.
"""


MARKET_COMPARISON_PROMPT = """
You are conducting a market-level competitive analysis.

Use ONLY the supplied structured company analyses.

Do not introduce outside facts.

Do not force a single winner when companies serve
different customer segments, product categories,
or strategic positions.

Compare competitors using evidence including:

- value proposition
- target customers
- product breadth
- product maturity
- technology
- commercial positioning
- enterprise capabilities
- business model
- deployment
- integrations
- customer evidence
- partnerships
- competitive differentiation
- execution risk

Important rules:

1. Separate demonstrated capabilities from marketing
   claims and future plans.

2. Do not assume that the largest company or broadest
   product suite automatically has the strongest
   competitive position.

3. Distinguish technical strength from commercial
   strength.

4. Identify companies occupying different portions
   of the market rather than forcing direct comparison
   when inappropriate.

5. Identify important missing information when it
   limits the comparison.

6. Identify shared customer pain points and weaknesses
   that could create market opportunities.

Focus especially on:

- market structure
- competitive battlegrounds
- product positioning
- technology positioning
- commercial strength
- enterprise readiness
- customer problems
- market gaps
- strategic opportunities
- execution risks
- important metrics to watch

The bottom line should explain the competitive
landscape clearly without oversimplifying it.

Return the result using the supplied structured schema.
"""