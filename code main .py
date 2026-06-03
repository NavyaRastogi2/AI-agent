import streamlit as st
import feedparser
from openai import OpenAI


client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

st.title("🇮🇳 Indian Stock Market News Chatbot")

# RSS feeds
indian_news = feedparser.parse(
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
)

global_news = feedparser.parse(
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EGSPC&region=US&lang=en-US"
)

def get_latest_news():
    news_text = ""

    news_text += "\nIndian Market News:\n"
    for item in indian_news.entries[:5]:
        news_text += f"- {item.title}\n"

    news_text += "\nGlobal Market News:\n"
    for item in global_news.entries[:5]:
        news_text += f"- {item.title}\n"

    return news_text


question = st.text_input(
    "Ask something",
    placeholder="How will US interest rates affect NIFTY?"
)

if st.button("Analyze"):

    news_context = get_latest_news()

    prompt = f"""
    You are a financial market assistant.

    Use the following news:

    {news_context}

    User Question:
    {question}

    Explain:
    1. Impact on Indian stock market
      2. Sectors likely affected
    3. Positive and negative outcomes
    4. Beginner-friendly explanation
    5. compare year to date value
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    st.subheader("Analysis")
    st.write(response.choices[0].message.content)

    st.subheader("Latest News Used")
    st.text(news_context)
