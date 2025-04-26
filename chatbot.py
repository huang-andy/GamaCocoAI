# chatbot.py
import json
from config import MODEL_ID, get_bedrock_client, invoke_with_retry

def ask_aine(question: str, memory: str) -> str:
    client = get_bedrock_client()
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 64,
        "temperature": 0.7,
        "system": memory,
        "messages": [
            {"role": "user", "content": question}
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
