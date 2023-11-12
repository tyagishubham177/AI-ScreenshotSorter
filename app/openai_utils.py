import openai
import base64


def get_image_description(api_key, image_path):
    openai.api_key = api_key

    try:
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()

        base64_image = encode_image(image_path)

        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}"


def chat_with_openai(api_key, message, instructions=None, model="gpt-3.5-turbo"):
    openai.api_key = api_key

    # Check for null or empty instructions and use default if necessary
    if not instructions:
        instructions = "You're a helpful assistant, adhere strictly to the prompt. Be exact in your answer."

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content
