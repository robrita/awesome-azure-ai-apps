import uuid
import base64
import pandas as pd
import streamlit as st
import app.pages
import extra_streamlit_components as stx
import app.utils as utils

from dotenv import load_dotenv
from usecase_text2sql.text2sql import text2sql
from datetime import datetime, timedelta

load_dotenv()

# App home page
app.pages.show_home()
# col1, col2 = st.columns([2, 1])
col1, col2 = st.columns(2)

# Initialize CookieManager
cookie_manager = stx.CookieManager()

# Initialization user state
if "xuser" not in st.session_state:
    st.session_state["xuser"] = "start"


def home(col1, col2):
    col1.empty()
    col2.empty()
    st.header("✨Azure AI Apps")
    st.markdown(
        """
        Search and sort "Azure AI Accelerators" by use case or technology stack.\n
        Search on [CSV file](https://github.com/robrita/awesome-azure-ai-apps/blob/main/scripts/aiapps.csv)
        """
    )

    # Set the path to the CSV file
    csv_file_path = "./scripts/aiapps.csv"
    df = pd.read_csv(csv_file_path)

    st.dataframe(df, use_container_width=True)


@st.dialog("Login with access key")
def login():
    appKey = st.text_input(
        "Access Key:",
        placeholder="8cb78***************",
        type="password",
    )

    if st.button("Submit") and appKey:
        if utils.check_access(appKey):
            st.session_state["xuser"] = "login"
            st.info("You have successfully logged in.")
            st.rerun()
        else:
            st.error("Invalid access key. Please try again.")
    else:
        st.warning("Please enter your access key.")


# login button
if st.sidebar.button("Click to reload"):
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
# print("Check user:", xuser)

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

        PAGES[page](col1, col2)

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
