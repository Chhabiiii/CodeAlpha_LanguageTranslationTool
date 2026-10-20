import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="LinguaTranslate",
    page_icon="🌐",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .translation-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGE DATA ----------------
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko"
}

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🌐 LinguaTranslate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Simple and fast language translation powered by an online translation API.</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- LANGUAGE SELECTION ----------------
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "From",
        list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "To",
        list(languages.keys()),
        index=1
    )

# ---------------- INPUT ----------------
st.markdown("### Enter your text")

text = st.text_area(
    "",
    height=160,
    placeholder="Type or paste your text here..."
)

# ---------------- TRANSLATE ----------------
if st.button("🌐 Translate", type="primary", use_container_width=True):

    if not text.strip():

        st.warning("Please enter some text first.")

    elif source_language == target_language:

        st.warning("Please select different source and target languages.")

    else:

        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"{languages[source_language]}|{languages[target_language]}"
        }

        try:

            with st.spinner("Translating..."):

                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                data = response.json()

            if response.status_code == 200:

                translated_text = data["responseData"]["translatedText"]

                st.markdown("### Translation")

                st.text_area(
                    "",
                    translated_text,
                    height=140
                )

                # ---------------- COPY BUTTON ----------------
                text_for_js = json.dumps(translated_text)

                components.html(
                    f"""
                    <button
                        onclick="copyText()"
                        style="
                            padding: 10px 20px;
                            border-radius: 8px;
                            border: 1px solid #ccc;
                            background: white;
                            cursor: pointer;
                            font-size: 15px;
                        ">
                        📋 Copy Translation
                    </button>

                    <script>
                    function copyText() {{
                        const text = {text_for_js};
                        navigator.clipboard.writeText(text);
                        alert("Translation copied!");
                    }}
                    </script>
                    """,
                    height=55
                )

            else:

                st.error("Translation failed. Please try again.")

        except requests.exceptions.RequestException:

            st.error(
                "Could not connect to the translation service. "
                "Please check your internet connection."
            )

        except Exception as e:

            st.error(f"An unexpected error occurred: {e}")

# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "LinguaTranslate • Built with Python, Streamlit and Translation API"
)