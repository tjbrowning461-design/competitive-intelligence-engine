from openai import OpenAI


DEFAULT_MODEL = "gpt-5.6"


def analyze_company(
    company_text,
    schema_class,
    system_prompt,
    model=DEFAULT_MODEL
):

    client = OpenAI()

    print(
        "\nSending collected company "
        "information to AI..."
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
                "content": company_text
            }
        ],
        text_format=schema_class
    )

    return response.output_parsed