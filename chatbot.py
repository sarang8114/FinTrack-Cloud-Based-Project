import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Page Configuration
st.set_page_config(
    page_title="Expense Tracker Chatbot",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state for storing expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description']
    )
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'categories' not in st.session_state:
    st.session_state.categories = [
        'Food & Dining', 'Transportation', 'Housing', 'Utilities',
        'Healthcare', 'Entertainment', 'Shopping', 'Travel',
        'Education', 'Personal Care', 'Other'
    ]
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.3

# Function to get expense summary
def get_expense_summary():
    if st.session_state.expenses.empty:
        return "No expenses recorded yet."

    summary = f"Total expenses: ${st.session_state.expenses['Amount'].sum():.2f}\n\n"
    summary += "Expenses by category:\n"

    for category in st.session_state.categories:
        cat_expenses = st.session_state.expenses[st.session_state.expenses['Category'] == category]
        if not cat_expenses.empty:
            total = cat_expenses['Amount'].sum()
            summary += f"- {category}: ${total:.2f}\n"

    return summary

# Function to get response from Gemini API
def get_gemini_response(user_input, expense_context, temperature=0.3):
    try:
        if not GEMINI_API_KEY:
            return "API Key is missing. Please provide a valid key."

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        system_prompt = f"""
        You are an expert financial advisor specializing in personal expense tracking and budgeting.

        Current expense data:
        {expense_context}

        Answer user questions professionally and concisely. If the user asks about their expenses, use the data provided.
        Provide practical tips on saving money, reducing expenses, or budgeting.
        """

        response = model.generate_content(
            [system_prompt, user_input],
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=4096,
            )
        )

        return response.text
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key and connection."

# Main App
st.title("💬 Expense Tracker Chatbot")
st.write("Welcome! I can help you with tracking and controlling your expenses. Ask me anything!")

# Sidebar for settings
with st.sidebar:
    st.subheader("Settings")
    st.session_state.temperature = st.slider("Response Creativity (Temperature)", 0.0, 1.0, st.session_state.temperature)

    # Update API Key securely
    custom_api_key = st.text_input("Update API Key (optional)", type="password")
    if custom_api_key:
        os.environ['GEMINI_API_KEY'] = custom_api_key
        GEMINI_API_KEY = custom_api_key

# Display expense data
if not st.session_state.expenses.empty:
    st.subheader("Recent Expenses")
    st.dataframe(
        st.session_state.expenses.sort_values(by='Date', ascending=False).head(5),
        use_container_width=True
    )

# Chat interface
st.subheader("Ask me about expense management")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask a question about tracking or controlling your expenses:")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    expense_context = get_expense_summary()
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot_response = get_gemini_response(user_input, expense_context, st.session_state.temperature)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.write(bot_response)

st.write("Made with ❤️ using Streamlit and Google Gemini API")
