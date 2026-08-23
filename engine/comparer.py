import json

from openai import OpenAI


DEFAULT_MODEL = "gpt-5.6"


def compare_companies(
    analyses,
    comparison_schema_class,
    system_prompt,
    model=DEFAULT_MODEL
):

    client = OpenAI()

    print(
        f"\nComparing "
        f"{len(analyses)} companies..."
    )

    competitor_data = json.dumps(
        analyses,
        indent=2,
        ensure_ascii=False
    )

    response = client.responses.parse(
        model=model,
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": competitor_data
            }
        ],
        text_format=(
            comparison_schema_class
        )
    )

    return response.output_parsed