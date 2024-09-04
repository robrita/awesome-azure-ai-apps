# extract github repo data into csv file
# Usage: python repo2csv.py <github_url>

# accept user input
import sys
import csv
import requests

if len(sys.argv) > 1:
    url = sys.argv[1]
    print(url)

    # split by / and get the elements
    elements = url.split("/")
    print(f"{elements[3]},{elements[4]}")

# https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator
# https://github.com/pablomarin/GPT-Azure-Search-Engine
# https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator
# https://github.com/microsoft/rag-experiment-accelerator
# https://github.com/Azure/gpt-rag
# https://github.com/microsoft/sample-app-aoai-chatGPT
# https://github.com/microsoft/chat-copilot
# https://github.com/microsoft/azurechat
# https://github.com/Azure/openai-at-scale
# https://github.com/microsoft/BotFramework-WebChat
# https://github.com/microsoft/ai-chat-protocol
# https://github.com/Azure/gen-cv
# https://github.com/Azure/business-process-automation
# https://github.com/MSUSAzureAccelerators/Knowledge-Mining-with-OpenAI
# https://github.com/microsoft/OpenAIWorkshop/tree/main/scenarios/natural_language_query
# https://github.com/microsoft/OpenAIWorkshop/tree/main/scenarios/openai_batch_pipeline
# https://github.com/microsoft/OpenAIWorkshop/tree/main/scenarios/openai_on_custom_dataset
# https://github.com/Azure/Vector-Search-AI-Assistant
# https://github.com/Azure-Samples/azure-search-openai-demo
# https://github.com/Azure-Samples/graphrag-accelerator
# https://github.com/MSUSAzureAccelerators/Azure-Cognitive-Search-Azure-OpenAI-Accelerator
# https://github.com/tiger-openai-hackathon/hacks

repos = """
https://github.com/Azure-Samples/NL2SQL
https://github.com/Azure-Samples/llm-evaluation
https://github.com/Azure-Samples/openai-chat-app-entra-auth-builtin
https://github.com/Azure-Samples/openai-chat-vision-quickstart
https://github.com/Azure-Samples/gen-ai-bot-in-a-box
"""


# parse github repos
def parse_github_repos():
    dict = {}
    # loop through repos
    for repo in repos.splitlines():
        if repo != "":
            # split by / and get the elements
            elements = repo.split("/")
            # print(f"{elements[3]},{elements[4]}")

            if elements[3] not in dict:
                dict[elements[3]] = []

            # check if element[4] is in the list, else append it
            if elements[4] not in dict[elements[3]]:
                dict[elements[3]].append(elements[4])

    print("dict", dict)
    json_to_csv(dict)


# get the commit date
def get_commit_date(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url)

    if response.status_code == 200:
        commits = response.json()
        if commits:
            last_commit_date = commits[0]["commit"]["committer"]["date"]
            print("Last commit date:", last_commit_date)
            return last_commit_date
    else:
        print("Failed to fetch commits:", response.status_code, response.text)
        return None


# convert json to csv format
def json_to_csv(dict):
    # Specify the output CSV file
    output_file = "aiapps2.csv"

    # Open the output CSV file in write mode
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write headers for "Owner" and "Repository"
        writer.writerow(["Owner", "Repository", "Updated At", "Link"])

        # Write each owner and corresponding repository to the CSV file
        for owner, repositories in dict.items():
            for repo in repositories:
                updatedAt = get_commit_date(owner, repo)
                link = f"https://github.com/{owner}/{repo}"
                writer.writerow([owner, repo, updatedAt, link])

    print(f"Data has been written to {output_file}")


parse_github_repos()
