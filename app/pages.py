import streamlit as st


def show_home():
    st.set_page_config(
        page_title="Azure AI Apps",
        page_icon="✨",
        layout="wide",
        # initial_sidebar_state="collapsed",
    )

    # st.logo(
    #     "https://azure.microsoft.com/svghandler/ai-studio/?width=600&height=315",
    #     link="https://ai.azure.com/",
    # )

    with st.sidebar:
        with st.container(border=True):
            st.image(
                "https://azure.microsoft.com/svghandler/ai-studio/?width=600&height=315"
            )

    st.markdown(
        """
        <style>
        .stAppDeployButton {
            display: none;
        }
        .st-emotion-cache-15ecox0 {
            display: none;
        }
        .viewerBadge_container__r5tak {
            display: none;
        }
        .styles_viewerBadge__CvC9N {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
