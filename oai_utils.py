import requests

def upload_base64_image(base64_string, aircraft_make, aircraft_model):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"can you summarize this in 5 sentences explaining what neeeds to be done to accomplish this AD, how often it needs to be performed, and if it is a recurring or one time AD. Please organize this into a readable table with the following columns: AD Summary, Inspection Requirements, # of hours, and Recurring (Yes/No)."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_string}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()
