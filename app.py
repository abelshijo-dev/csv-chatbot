import streamlit as st
import pandas as pd
from groq import Groq

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="CSV Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI CSV Chatbot")
st.caption("Upload a CSV and ask questions about your data in plain English.")

# ── Groq client (uses GROQ_API_KEY env var) ──────────────────
client = Groq()

# ── Session state ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None


# ── Helper: build a data summary for the LLM ─────────────────
def build_data_context(df: pd.DataFrame) -> str:
    shape = f"{df.shape[0]} rows × {df.shape[1]} columns"
    cols = ", ".join([f"{c} ({str(t)})" for c, t in zip(df.columns, df.dtypes)])
    sample = df.head(5).to_string(index=False)
    stats = df.describe(include="all").to_string()

    return f"""
=== Dataset Overview ===
Shape: {shape}
Columns: {cols}

=== First 5 Rows ===
{sample}

=== Statistical Summary ===
{stats}
""".strip()


# ── Helper: chat with Groq ────────────────────────────────────
def ask_groq(user_question: str, data_context: str, history: list) -> str:
    system_prompt = f"""You are a helpful data analyst. The user has uploaded a CSV dataset.
Answer their questions clearly and concisely. Use numbers and facts from the data whenever possible.
If asked to do calculations, reason step by step.

{data_context}"""

    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": user_question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # free model on Groq
        messages=messages,
        max_tokens=1024,
    )

    return response.choices[0].message.content


# ── Sidebar: file upload ──────────────────────────────────────
with st.sidebar:
    st.header("📂 Upload your CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.messages = []
            st.success(f"Loaded! {df.shape[0]} rows, {df.shape[1]} columns")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    if st.session_state.df is not None:
        st.divider()
        st.caption("**Columns:**")
        for col, dtype in zip(st.session_state.df.columns, st.session_state.df.dtypes):
            st.caption(f"• {col} `{dtype}`")

        if st.button("🗑️ Clear chat"):
            st.session_state.messages = []
            st.rerun()

# ── Main area ─────────────────────────────────────────────────
if st.session_state.df is None:
    st.info("👈 Upload a CSV file from the sidebar to get started.")
    st.markdown("""
**Example questions you can ask:**
- *What are the top 5 values in column X?*
- *What's the average of column Y?*
- *Are there any missing values?*
- *What trends do you see in this data?*
- *Which rows have the highest/lowest values?*
""")
else:
    with st.expander("📊 Data Preview", expanded=False):
        st.dataframe(st.session_state.df.head(20), use_container_width=True)

    st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask anything about your data...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    data_context = build_data_context(st.session_state.df)
                    history = st.session_state.messages[:-1]
                    reply = ask_groq(user_input, data_context, history)
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"API error: {e}")
