from huggingface_hub import login
import os
#read
# os.environ["HUGGING_FACE_HUB_TOKEN"] = "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"
# write
# os.environ["HUGGING_FACE_HUB_TOKEN"] = "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"
os.environ["HUGGING_FACE_HUB_TOKEN"] = "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"
os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = "1"
access_token = os.environ["HUGGING_FACE_HUB_TOKEN"]
login(token=access_token)