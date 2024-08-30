import os
import json
import uuid
import base64
import streamlit as st
import app.pages
import extra_streamlit_components as stx

from openai import AzureOpenAI
from dotenv import load_dotenv
from usecase_text2sql.text2sql import text2sql
from datetime import datetime, timedelta

load_dotenv()

# create a config dictionary
config = {
    "endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    "model": os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
}

# Initialize OpenAI client
client = AzureOpenAI(
    azure_endpoint=config["endpoint"],
    api_version=config["api_version"],
    api_key=config["api_key"],
)

# App home page
app.pages.show_home()
# col1, col2 = st.columns([2, 1])
col1, col2 = st.columns(2)

# Initialize CookieManager
cookie_manager = stx.CookieManager()

# Initialization user state
if "xuser" not in st.session_state:
    st.session_state["xuser"] = "start"


def home(config, client, col1, col2):
    col2.empty()
    st.header("✨Azure AI Apps")
    st.markdown(
        """
        AI Apps Directory
        """
    )


@st.dialog("Login with access key")
def login():
    appKey = st.text_input(
        "Access Key:",
        placeholder="8cb78***************",
        type="password",
    )

    if st.button("Submit"):
        if appKey == os.environ["APP_KEY"]:
            st.session_state["xuser"] = "login"
            st.info("You have successfully logged in.")
            st.rerun()
        else:
            st.error("Invalid access key. Please try again.")


# login button
if st.sidebar.button("Click to login"):
    st.rerun()

# Print cookies
# cookies_dict = dict(st.context.cookies)
# print(json.dumps(cookies_dict))

# Show modal if not logged in
if st.session_state["xuser"] == "start" and "xuser" not in st.context.cookies:
    st.warning("You must log in to access this application.")
    login()

# Set cookie
if st.session_state["xuser"] == "login" and not cookie_manager.get("xuser"):
    plain_text = str("azureai-" + str(uuid.uuid4())).encode("utf-8")
    expiry_time = datetime.now() + timedelta(days=10000)  # Set expiry to 1 day from now
    cookie_manager.set(
        "xuser", base64.b64encode(plain_text).decode("utf-8"), expires_at=expiry_time
    )

xuser = cookie_manager.get("xuser")
print("Check user:", xuser)

if xuser:
    try:
        decoded = base64.b64decode(xuser).decode("utf-8")
        # check if azureai- is in the string
        if not decoded.startswith("azureai-"):
            cookie_manager.delete("xuser")
            st.rerun()

        # create pages
        PAGES = {"text2sql": text2sql, "Home Page": home}
        page = st.sidebar.selectbox("AI Apps:", options=list(PAGES.keys()))

        PAGES[page](config, client, col1, col2)

        # app sidebar
        with st.sidebar:
            st.write("These AI app use cases are all powered by Azure OpenAI.")
            st.divider()

            st.subheader("🛠Technology Stack", anchor=False)
            st.write("Python, Streamlit, Azure OpenAI, Azure AI Search")
            st.write(
                "Check out the repo here: [Azure AI Apps](https://github.com/robrita/awesome-azure-ai-apps)"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
