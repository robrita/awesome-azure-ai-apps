import os
import streamlit as st
from openai import AzureOpenAI

# create a config dictionary
config = {
    "endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    "model": os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    "auth": os.environ["ENABLE_AUTH"],
    "app_key": os.environ["APP_KEY"],
}

# Initialize OpenAI client
clientAOAI = AzureOpenAI(
    azure_endpoint=config["endpoint"],
    api_version=config["api_version"],
    api_key=config["api_key"],
)


# log tracing
def trace(col2, label, message):
    with col2:
        with st.expander(f"{label}:"):
            st.write(message)
            # print(f"{label}: {message}")


# check app access
def check_access(appKey):
    if config["auth"] == "1":
        return appKey == config["app_key"]
    else:
        return True


# chat completion
def chat(
    col2: object,
    messages=[],
    temperature=0.7,
    max_tokens=800,
    streaming=False,
    format="text",
):
    try:
        # reset tracer
        col2.empty()
        trace(col2, "Message prompt", messages)

        # Response generation
        full_response = ""
        message_placeholder = st.empty()

        for completion in clientAOAI.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=streaming,
            response_format={"type": format},
        ):

            if completion.choices and completion.choices[0].delta.content is not None:
                full_response += completion.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        trace(col2, "Full response", full_response)
        return full_response

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
