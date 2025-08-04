import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Analysis import process_query

st.set_page_config(page_title="DS Assistant", layout="wide")

st.title("🤖 Data Science Assistant Chatbot Dashboard")
st.markdown("Upload your CSV file or use the default dataset, ask questions, and explore your data interactively!")

# Upload or default data
uploaded_file = st.sidebar.file_uploader("📂 Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Custom dataset loaded.")
else:
    df = pd.read_csv("data/HeartDisease.csv")
    st.sidebar.info("ℹ️ Using default HeartDisease.csv dataset.")

# Session state for chat
if "history" not in st.session_state:
    st.session_state.history = []

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "📊 Visual Explorer", "📈 Summary"])

# --- Tab 1: Chatbot ---
with tab1:
    st.subheader("Ask a question about your dataset")

    if prompt := st.chat_input("Ask a question like 'average of age' or 'scatter plot age vs cholesterol'"):
        reply = process_query(prompt, df)
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write(reply)
        st.session_state.history.append(("You", prompt))
        st.session_state.history.append(("Bot", reply))

    if st.session_state.history:
        with st.expander("🕘 View Chat History"):
            for sender, message in st.session_state.history:
                emoji = "🧑‍💻" if sender == "You" else "🤖"
                st.markdown(f"{emoji} **{sender}:** {message}")

# --- Tab 2: Visual Explorer ---
with tab2:
    st.subheader("📊 Generate a Plot")

    plot_type = st.selectbox("Select plot type", ["Histogram", "Scatter", "Boxplot"])
    x_col = st.selectbox("Select X-axis column", df.columns)

    y_col = None
    if plot_type != "Histogram":
        y_col = st.selectbox("Select Y-axis column", df.columns)

    if st.button("📈 Plot Now"):
        fig, ax = plt.subplots()
        if plot_type == "Histogram":
            sns.histplot(df[x_col], kde=True, ax=ax)
            ax.set_title(f"Histogram of {x_col}")
        elif plot_type == "Scatter":
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
            ax.set_title(f"Scatter: {x_col} vs {y_col}")
        elif plot_type == "Boxplot":
            sns.boxplot(x=df[x_col], y=df[y_col], ax=ax)
            ax.set_title(f"Boxplot: {x_col} vs {y_col}")
        st.pyplot(fig)

# --- Tab 3: Dataset Summary ---
with tab3:
    st.subheader("📈 Dataset Overview")

    with st.expander("📋 View First 5 Rows"):
        st.dataframe(df.head())

    with st.expander("📊 Summary Statistics"):
        st.write(df.describe())

    with st.expander("🔍 Dataset Info"):
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.write(f"Column Names: {', '.join(df.columns)}")
