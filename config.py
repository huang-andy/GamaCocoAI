# config.py
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

REGION = os.getenv("AWS_DEFAULT_REGION", "us-west-2")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0

def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=REGION)

def invoke_with_retry(client_method, **kwargs):
    import time
    from botocore.exceptions import ClientError

    backoff = INITIAL_BACKOFF
    for attempt in range(1, MAX_RETRIES+1):
        try:
            return client_method(**kwargs)
        except ClientError as e:
            code = e.response.get("Error",{}).get("Code")
            if code=="InternalServerException" and attempt<MAX_RETRIES:
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
    raise RuntimeError(f"Reached max retries ({MAX_RETRIES})")
