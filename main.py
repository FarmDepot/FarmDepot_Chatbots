# main.py
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI(title="FarmDepot Multilingual Chatbot")

MODEL_NAME = "NCAIR1/N-ATLaS"

# Load model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

class ChatRequest(BaseModel):
    message: str
    language: str  # "en", "ha", "yo", "ig"

def format_text_for_inference(messages):
    current_date = datetime.now().strftime('%d %b %Y')
    return tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False,
        date_string=current_date
    )

LANG_PROMPTS = {
    "en": "You are FarmDepot AI assistant. Respond in English.",
    "ha": "Kai abokin taimako ne na FarmDepot. Ka amsa da Hausa.",
    "yo": "O je oluranlọwọ FarmDepot AI. Jowo dahun ni Yoruba.",
    "ig": "Ị bụ onye enyemaka FarmDepot AI. Biko zaa na Igbo."
}

@app.post("/chat")
async def chat(req: ChatRequest):

    if req.language not in LANG_PROMPTS:
        raise HTTPException(status_code=400, detail="Unsupported language code")

    system_prompt = LANG_PROMPTS[req.language]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.message}
    ]

    prompt_text = format_text_for_inference(messages)
    inputs = tokenizer(prompt_text, return_tensors="pt", add_special_tokens=False).to("cuda")

    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        use_cache=True,
        repetition_penalty=1.12,
        temperature=0.4
    )

    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": reply}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)