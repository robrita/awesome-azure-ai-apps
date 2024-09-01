import re
import json
import streamlit as st
import app.utils as utils
import usecase_text2sql.prompts as prompts
import usecase_text2sql.sqlite as sqlite


def text2sql(col1, col2):
    with col1:
        st.header("🔀Text to SQL and RAG")

        TYPES = {"text2sql_1db": text2sql1db}
        type = st.selectbox("Scenario:", options=list(TYPES.keys()))

        TYPES[type](col1, col2)


def text2sql1db(col1, col2):
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
                # select the relevant tables
                messages = prompts.select_tables(question)
                tables = utils.chat(
                    col2, question, messages, 0, 800, True, "json_object"
                )

                print("tables", tables)
                table_names = json.loads(tables)["table_names"]

                if table_names:
                    print("table_names", table_names)
                    # get the table infos
                    table_infos = sqlite.table_infos(table_names)
                    print("table_infos", table_infos)

                    # build the messages
                    messages = prompts.instruction(question, table_infos)

                    # get the SQL Query
                    sql_query = utils.chat(col2, question, messages, 0, 800, True)
                    clean_query = re.sub(r"```\w*", "", sql_query).strip()

                    if sql_query != "null" and clean_query.startswith("SELECT"):
                        print("clean_query", clean_query)

                        # run the query
                        result = sqlite.query_data(clean_query)
                        st.write(result)

                        # rephrase the output
                        messages = prompts.final_answer(question, clean_query, result)
                        utils.chat(col2, question, messages, 0, 800, True)
                    else:
                        st.error(f"Invalid SQL Query: {clean_query}")
                else:
                    st.error("Invalid input: table not found")
