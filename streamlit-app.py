import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime
import torch

# -------------------------
# Load Model
# -------------------------
MODEL_NAME = "NCAIR1/N-ATLaS"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model

tokenizer, model = load_model()

# -------------------------
# Helper Function
# -------------------------
def format_for_inference(messages):
    current_date = datetime.now().strftime("%d %b %Y")
    return tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False,
        date_string=current_date
    )

# Supported languages
LANG_PROMPTS = {
    "English": "You are FarmDepot AI Assistant. Respond in English.",
    "Hausa": "Kai abokin taimako ne na FarmDepot. Ka amsa da Hausa.",
    "Yoruba": "Iwo ni oluranlọwọ AI FarmDepot. Jowo dahun ni Yoruba.",
    "Igbo": "Ị bụ onye enyemaka FarmDepot AI. Biko zaa na Igbo."
}

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="FarmDepot Multilingual AI", layout="centered")

st.title("🌾 FarmDepot Multilingual AI Chatbot")
st.write("Test the AI model in **English, Hausa, Yoruba, and Igbo**")

language = st.selectbox("Select Language", list(LANG_PROMPTS.keys()))

user_message = st.text_input("Enter your message:")

if st.button("Generate Response"):
    
    if not user_message.strip():
        st.warning("Please enter a message")
    else:
        with st.spinner("Generating response..."):

            # Prepare messages
            messages = [
                {"role": "system", "content": LANG_PROMPTS[language]},
                {"role": "user", "content": user_message}
            ]

            # Format text for model inference
            input_text = format_for_inference(messages)
            
            input_tokens = tokenizer(
                input_text,
                return_tensors="pt",
                add_special_tokens=False
            ).to("cuda")

            output = model.generate(
                **input_tokens,
                max_new_tokens=250,
                temperature=0.3,
                repetition_penalty=1.12
            )

            response = tokenizer.decode(output[0], skip_special_tokens=True)

        st.success("Response:")
        st.write(response)

st.markdown("---")
st.write("FarmDepot.ng — AI-Powered Agriculture Marketplace")