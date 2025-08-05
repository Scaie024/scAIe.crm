import os
from openai import OpenAI

try:
    client = OpenAI(
        # If the environment variable is not configured, replace the following line with your API key: api_key=sk-ff40b02e0b454d379ea51160cfbadfa9
        api_key=os.getenv("DASHSCOPE_API_KEY", "sk-1ded1e3aa4d04a7593afc74a484cd4c1"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",  # Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Who are you?'}
            ]
    )
    print("Success! OpenAI integration is working correctly.")
    print("Response:", completion.choices[0].message.content)
except Exception as e:
    print(f"Error message: {e}")
    print("For more information, see: https://www.alibabacloud.com/help/en/model-studio/developer-reference/error-code")