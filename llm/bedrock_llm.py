"""
bedrock_llm.py

Provides a function to initialize and return an LLM model using Amazon Bedrock, 
wrapped in LangChain's BedrockChat interface for use with AI agents.
"""

import boto3
from langchain_community.chat_models import BedrockChat
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load AWS keys and region from .env

def get_bedrock_llm(model_id=None, temperature=None, max_tokens=None, top_p=None, top_k=None):
    """
    Returns a Claude LLM from Amazon Bedrock, wrapped in LangChain.
    """
    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-west-2")
        )

        # Use environment variables if available, else use defaults
        model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
        model_kwargs = {
            "temperature": temperature or float(os.getenv("BEDROCK_TEMPERATURE", 0.7)),
            "max_tokens": max_tokens or int(os.getenv("BEDROCK_MAX_TOKENS", 4096)),
            "top_p": top_p or float(os.getenv("BEDROCK_TOP_P", 0.9)),
            "top_k": top_k or int(os.getenv("BEDROCK_TOP_K", 250)),
            "stop_sequences": ["\n\nHuman"]
        }

        llm = BedrockChat(
            client=client,
            model_id=model_id,
            model_kwargs=model_kwargs
        )

        logging.info(f"Initialized BedrockChat with model {model_id}")
        return llm

    except Exception as e:
        logging.error(f"Failed to initialize Bedrock LLM: {e}")
        raise

# Test the LLM Initialization
if __name__ == "__main__":
    llm = get_bedrock_llm()
    print("LLM initialized successfully")
