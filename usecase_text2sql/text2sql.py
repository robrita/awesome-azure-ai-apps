import os
import streamlit as st
import app.utils


def text2sql(config, client, col1, col2):
    with col1:
        st.header("🔀Text to SQL and RAG")

        TYPES = {"text2sql_1db": text2sql1db}
        type = st.selectbox("Scenario:", options=list(TYPES.keys()))

        TYPES[type](config, client, col1, col2)


def text2sql1db(config, client, col1, col2):
    with col1:
        with st.container(border=True):
            st.markdown(
                """
                Database: chinook\n
                Tables: 
                    albums, artists, customers, employees, genres, invoices,
                    invoice_items, media_types, playlists, playlist_track, tracks\n
                    
                Schema: [link](https://www.sqlitetutorial.net/wp-content/uploads/2015/11/sqlite-sample-database-color.jpg)
                """
            )

        # get user input
        question = st.text_input("Input: ", key="input")
        submit = st.button("Ask the question", key="submit", disabled=question == "")

        if submit:
            with st.spinner("Processing ..."):
                try:
                    # reset tracer
                    col2.empty()

                    # Response generation
                    full_response = ""
                    message_placeholder = st.empty()
                    app.utils.trace(st, col2, "User input", question)

                    messages = [
                        {
                            "role": "system",
                            "content": f"""
                                You are an expert in converting English questions to SQL query!
                                The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
                                SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
                                the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
                                \nExample 2 - Tell me all the students studying in Data Science class?, 
                                the SQL command will be something like this SELECT * FROM STUDENT 
                                where CLASS="Data Science"; 
                                also the sql code should not have ``` in beginning or end and sql word in output
                            """,
                        },
                        {"role": "user", "content": question},
                    ]
                    app.utils.trace(st, col2, "Message prompt", messages)

                    for completion in client.chat.completions.create(
                        model=config["model"],
                        messages=messages,
                        temperature=0,
                        max_tokens=1280,
                        stream=True,
                    ):

                        if (
                            completion.choices
                            and completion.choices[0].delta.content is not None
                        ):
                            full_response += completion.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)
                    app.utils.trace(st, col2, "Full response", full_response)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
