import json
from config import MODEL_ID, get_bedrock_client, invoke_with_retry

def convert_to_memory(scenario: str) -> str:
    client = get_bedrock_client()
    system_prompt = (
        "你是Aine"
        "以下情境是你擁有的內心記憶（第一人稱）："
    )
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10000,
        "temperature": 0.7,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": scenario}
        ],
        "stop_sequences": ["\nuser:"]
    }
    resp = invoke_with_retry(
        client.invoke_model,
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload).encode("utf-8")
    )
    data = json.loads(resp["body"].read().decode())
    return data["content"][0]["text"].strip()
