import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="3090 DeepSeek Hub", layout="wide")

@st.fragment(run_every=5)
def gpu_stats_container():
    """This function only contains the elements that refresh."""
    try:
        res = requests.get(f"{BACKEND_URL}/gpu-stats", timeout=1).json()
        if "used_gb" in res:
            st.progress(res['percentage'] / 100)
            col1, col2 = st.columns(2)
            col1.metric("Used", f"{res['used_gb']} GB")
            col2.metric("Free", f"{res['free_gb']} GB")
            
            if res['used_gb'] > 22:
                st.error("⚠️ VRAM Critical")
            else:
                st.success("✅ GPU Healthy")
        else:
            st.warning("Stats busy...")
    except:
        st.error("Backend Offline")

with st.sidebar:
    st.header("GPU Live Stats")
    gpu_stats_container()
    
    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main Chat Interface ---
st.title("AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message DeepSeek..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("3090 is thinking..."):
        try:
            r = requests.post(f"{BACKEND_URL}/chat", json={"prompt": prompt})
            answer = r.json().get("response", "No response")
        except:
            answer = "Connection Error."

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})