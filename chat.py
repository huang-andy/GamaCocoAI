import json
from config import MODEL_ID, get_bedrock_client, invoke_with_retry

# chat.py
def chat_loop(memory: str):
    client = get_bedrock_client()
    # 加入簡短回覆指令
    short_instr = "請用 1~2 句話簡潔回覆。"
    # 把簡短指令加到 memory 前面
    system_prompt = short_instr + "\n" + memory

    messages = [{"role": "user", "content": system_prompt}]
    print("Aine 已就緒，輸入 'exit' 離開。")
    while True:
        user = input("你：")
        if user.strip().lower() == "exit":
            print("對話結束。")
            break
        messages.append({"role": "user", "content": user})
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,          # 限制回覆長度
            "temperature": 0.7,
            "system": system_prompt,   # 精簡指令 + 原本 memory
            "messages": messages[1:],  # 只傳 user/assistant
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
        reply = data["content"][0]["text"].strip()
        messages.append({"role": "assistant", "content": reply})
        print(f"Aine：{reply}\n")
