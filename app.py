
import streamlit as st
import requests

st.set_page_config(
    page_title="News Application",
    page_icon="📰"
)

st.title("News Application")
st.write("Search and save your favourite news")

# Enter your GNews API key
API_KEY = "YOUR_GNEWS_API_KEY"

# Store favourite articles
if "favourites" not in st.session_state:
    st.session_state.favourites = []

if "articles" not in st.session_state:
    st.session_state.articles = []

# Feature 1: Search by category and keyword
category = st.selectbox(
    "Select News Category",
    [
        "General",
        "Sports",
        "Technology",
        "Business",
        "Entertainment",
        "Health",
        "Science"
    ]
)

keyword = st.text_input("Enter Keyword")

if st.button("Search News"):
    if not keyword:
        st.warning("Please enter a keyword")
    else:
        url = "https://gnews.io/api/v4/search"

        params = {
            "q": keyword,
            "lang": "en",
            "max": 10,
            "apikey": API_KEY
        }

        try:
            response = requests.get(
                url, params=params, timeout=10
            )
            response.raise_for_status()

            articles = response.json().get(
                "articles", []
            )

            if category != "General":
                articles = [
                    a for a in articles
                    if category.lower() in (
                        a.get("title", "") + " " +
                        (a.get("description") or "")
                    ).lower()
                ]

            st.session_state.articles = articles

        except requests.RequestException:
            st.error("Unable to fetch news")

# Features 2, 3, 4 and 5
st.header("News Articles")

for i, article in enumerate(
    st.session_state.articles
):
    # Display headline
    st.subheader(article.get("title", "No title"))

    # Display source and date
    source = article.get("source") or {}
    st.write(
        "Source:",
        source.get("name", "Unknown")
    )
    st.write(
        "Date:",
        article.get("publishedAt", "N/A")
    )

    # Display summary
    st.write(
        "Summary:",
        article.get("description", "N/A")
    )

    # Open full article
    if article.get("url"):
        st.link_button(
            "Read Full Article",
            article["url"]
        )

    # Save favourite article
    if st.button("Save Favourite", key=i):
        if article not in st.session_state.favourites:
            st.session_state.favourites.append(article)
            st.success("Article saved!")
        else:
            st.info("Already saved")

    st.divider()

# Display saved articles
st.header("Favourite Articles")

for article in st.session_state.favourites:
    st.subheader(article.get("title", "No title"))
    st.write(article.get("description", ""))

    if article.get("url"):
        st.link_button(
            "Read Article",
            article["url"]
        )
