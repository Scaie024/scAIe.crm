import os
import httpx
import asyncio

async def test_api_key():
    api_key = "sk-1ded1e3aa4d04a7593afc74a484cd4c1"
    
    # Configuración del cliente HTTP
    client = httpx.AsyncClient(
        base_url="https://dashscope.aliyuncs.com/api/v1",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    )
    
    # Mensaje de prueba
    messages = [
        {
            "role": "user",
            "content": "Hola, ¿cómo estás?"
        }
    ]
    
    try:
        response = await client.post(
            "/services/aigc/text-generation/generation",
            json={
                "model": "qwen-plus",
                "input": {
                    "messages": messages
                },
                "parameters": {
                    "temperature": 0.8,
                    "max_tokens": 1024,
                    "top_p": 0.9,
                    "top_k": 30,
                    "seed": 1234
                }
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(test_api_key())