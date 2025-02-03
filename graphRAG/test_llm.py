print("DEBUG: Testing LLM pipeline loading")

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import LLM_MODEL_ID

try:
    print(f"DEBUG: Loading LLM model: {LLM_MODEL_ID}")
    
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)
    print("DEBUG: Tokenizer loaded successfully")
    
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_ID)
    print("DEBUG: Model loaded successfully")
    
    llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=256)
    print("DEBUG: LLM pipeline successfully created")
    
except Exception as e:
    print(f"ERROR: Failed to load LLM pipeline: {e}")
