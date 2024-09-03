import json


# format messages
def format_messages(messages=[]):
    new_messages = []

    for message in messages:
        if "system" in message:
            new_messages.append({"role": "system", "content": message["system"]})

        if "user" in message:
            new_messages.append({"role": "user", "content": message["user"]})

        if "assistant" in message:
            new_messages.append({"role": "assistant", "content": message["assistant"]})

    return new_messages


# instruction prompt
def instruction(input, table_info, few_shots=[], chat_history=[]):
    prompts = [
        {
            "system": f"""You are a MySQL expert. Given an input question,
                create a syntactically correct MySQL query to run. Unless otherwise specificed.
                Never query for all columns from a table. You must query only the columns that are needed to answer the question.
                Pay attention to use only the column names you can see in the tables below.
                Be careful to not query for columns that do not exist.
                Also, pay attention to which column is in which table.
                Pay attention to use CURDATE() function to get the current date, if the question involves "today".
                Return null for any query that is irrelevant to the tables below, query that tries to retrieve all rows, or
                query that tries to insert, update or delete data.

                Here is the relevant table info:\n
                {table_info}\n\n
                
                Do not explain, just return the correct SQL Query and think through step by step"""
        }
    ]
    user = [{"user": f"Input: {input}\nSQL Query:"}]

    return format_messages(prompts + few_shots + chat_history + user)


# query rephrase prompt
def rephrase(chat_history=[]):
    prompts = [{"system": "You are an expert in rephrasing queries."}]
    user = [
        {
            "user": "Instruction: please rephrase my last query with complete thought.\nRephrased:"
        }
    ]

    return format_messages(prompts + chat_history + user)


# tables selector prompt
def select_tables(input):
    prompts = [
        {
            "system": f"""You are an expert in intent matching.
                Return the relevant SQL table names based from the input query and table descriptions below.\n\n
                Return null for any query that is totally irrelevant to the tables below, query that tries to retrieve all rows, or
                query that tries to insert, update or delete data.

                Here are the tables in the database:\n
                ["albums","artists","customers","employees","genres","invoices","invoice_items","media_types","playlists","playlist_track","tracks"]\n\n

                Here are the table names and descriptions:\n
                albums:
                - Stores information about music albums, including album title and the associated artist ID.
                artists:
                - Contains details of artists, primarily their ID and name.
                customers:
                - Includes customer information, such as names, contact details, address, and support rep ID.
                employees:
                - Stores employee data, including personal information, contact details, job title, and reports to another employee.
                genres:
                - Defines music genres, with each genre having a unique ID and a name.
                invoices:
                - Contains invoice records, including customer ID, invoice date, billing information, and total amount.
                invoice_items:
                - Represents items in an invoice, detailing invoice line ID, associated invoice and track IDs, unit price, and quantity.
                media_types:
                - Describes different media types, identified by a unique ID and name.
                playlists:
                - Contains information about playlists, including playlist ID and name.
                playlist_track:
                - Associates tracks with playlists, linking playlist IDs to track IDs.
                tracks:
                - Stores track details, such as track name, album ID, media type ID, genre ID, composer, duration, file size, and unit price.\n\n

                Remember to include ALL POTENTIALLY RELEVANT table names, even if you're not sure that they're needed.\n
                Format the output as JSON array of table_names."""
        }
    ]
    few_shots = [
        {"user": "list down all media types"},
        {"assistant": '{ "table_names": ["media_types"] }'},
    ]
    user = [{"user": input}]

    return format_messages(prompts + few_shots + user)


# final answer prompt
def final_answer(question, query, result):
    prompts = [
        {
            "system": f"""Given the following user question, corresponding SQL query, and SQL result, answer the user question.
                create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\n

                Question: {question}
                SQL Query: {query}
                SQL Result: {result}
                Answer: """
        }
    ]

    return format_messages(prompts)
