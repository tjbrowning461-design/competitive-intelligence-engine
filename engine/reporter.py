from html import escape
from pathlib import Path


def prettify_key(key):
    return (
        key.replace("_", " ")
        .strip()
        .title()
    )


def render_value(value):

    if value is None:
        return '<span class="missing">Not disclosed</span>'

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, str):
        return escape(value)

    if isinstance(value, list):

        if not value:
            return '<span class="missing">None disclosed</span>'

        items = []

        for item in value:

            if isinstance(item, dict):
                items.append(
                    f"<li>{render_dict(item)}</li>"
                )
            else:
                items.append(
                    f"<li>{escape(str(item))}</li>"
                )

        return (
            "<ul>"
            + "".join(items)
            + "</ul>"
        )

    if isinstance(value, dict):
        return render_dict(value)

    return escape(str(value))


def render_dict(data):

    sections = []

    for key, value in data.items():

        if key in {
            "sources",
            "website"
        }:
            continue

        sections.append(
            f"""
            <div class="field">
                <h4>{escape(prettify_key(key))}</h4>
                <div>{render_value(value)}</div>
            </div>
            """
        )

    return "".join(sections)


def render_sources(company):

    sources = company.get(
        "sources",
        []
    )

    website = company.get(
        "website"
    )

    source_items = []

    if website:

        source_items.append(
            f"""
            <li>
                <a href="{escape(website)}"
                   target="_blank">
                    Official Website
                </a>
            </li>
            """
        )

    for source in sources:

        url = source.get(
            "url"
        )

        category = source.get(
            "category",
            "source"
        )

        if not url:
            continue

        source_items.append(
            f"""
            <li>
                <strong>
                    {escape(str(category).title())}
                </strong>:
                <a href="{escape(url)}"
                   target="_blank">
                    {escape(url)}
                </a>
            </li>
            """
        )

    if not source_items:
        return ""

    return f"""
    <details>
        <summary>Source Provenance</summary>
        <ul>
            {''.join(source_items)}
        </ul>
    </details>
    """


def generate_report(
    display_name,
    analyses,
    comparison,
    output_path
):

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    company_sections = []

    for company in analyses:

        name = company.get(
            "company_name",
            "Company"
        )

        company_sections.append(
            f"""
            <section class="company-card">
                <h2>{escape(name)}</h2>

                {render_dict(company)}

                {render_sources(company)}
            </section>
            """
        )

    comparison_html = (
        render_dict(comparison)
    )

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>{escape(display_name)}</title>

<style>

body {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    margin: 0;
    background: #f5f7fa;
    color: #18212f;
}}

header {{
    background: #111827;
    color: white;
    padding: 48px;
}}

header h1 {{
    margin: 0;
    font-size: 38px;
}}

header p {{
    color: #cbd5e1;
}}

main {{
    max-width: 1200px;
    margin: auto;
    padding: 32px;
}}

section {{
    background: white;
    border-radius: 14px;
    padding: 28px;
    margin-bottom: 28px;

    box-shadow:
        0 2px 10px
        rgba(0, 0, 0, 0.05);
}}

.company-card {{
    border-left:
        5px solid #475569;
}}

h2 {{
    margin-top: 0;
}}

h3 {{
    margin-top: 36px;
}}

h4 {{
    margin-bottom: 8px;
    color: #334155;
}}

.field {{
    border-bottom:
        1px solid #e5e7eb;

    padding-bottom: 14px;
    margin-bottom: 14px;
}}

ul {{
    line-height: 1.65;
}}

a {{
    color: #2563eb;
}}

.missing {{
    color: #94a3b8;
    font-style: italic;
}}

summary {{
    cursor: pointer;
    font-weight: 600;
    margin-top: 20px;
}}

footer {{
    text-align: center;
    color: #64748b;
    padding: 40px;
}}

</style>

</head>

<body>

<header>

<h1>{escape(display_name)}</h1>

<p>
Competitive Intelligence Report
</p>

<p>
Companies analyzed:
{len(analyses)}
</p>

</header>

<main>

<section>

<h2>Market Analysis</h2>

{comparison_html}

</section>

<h1>Company Profiles</h1>

{''.join(company_sections)}

</main>

<footer>

Generated by Competitive Intelligence Engine

</footer>

</body>

</html>
"""

    output_path.write_text(
        html,
        encoding="utf-8"
    )

    print(
        f"\nReport created: "
        f"{output_path}"
    )

    return output_path