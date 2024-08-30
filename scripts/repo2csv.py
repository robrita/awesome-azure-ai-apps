# extract github repo data into csv file
# Usage: python repo2csv.py <github_url>

# accept user input
import sys
import json

if len(sys.argv) > 1:
    url = sys.argv[1]
    print(url)

    # split by / and get the elements
    elements = url.split("/")
    print(f"{elements[3]},{elements[4]}")

repos = """
https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator
https://github.com/pablomarin/GPT-Azure-Search-Engine
https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator
https://github.com/microsoft/rag-experiment-accelerator
https://github.com/Azure/gpt-rag
https://github.com/microsoft/sample-app-aoai-chatGPT
https://github.com/microsoft/chat-copilot
https://github.com/microsoft/azurechat
https://github.com/Azure/openai-at-scale
https://github.com/microsoft/BotFramework-WebChat
https://github.com/microsoft/ai-chat-protocol
https://github.com/Azure/gen-cv
https://github.com/Azure/business-process-automation
https://github.com/MSUSAzureAccelerators/Knowledge-Mining-with-OpenAI
https://github.com/microsoft/OpenAIWorkshop/tree/main/scenarios/natural_language_query
https://github.com/microsoft/OpenAIWorkshop/tree/main/scenarios/openai_batch_pipeline
https://github.com/microsoft/OpenAIWorkshop/tree/main/scenarios/openai_on_custom_dataset
https://github.com/Azure/Vector-Search-AI-Assistant
https://github.com/Azure-Samples/azure-search-openai-demo
https://github.com/Azure-Samples/graphrag-accelerator
https://github.com/MSUSAzureAccelerators/Azure-Cognitive-Search-Azure-OpenAI-Accelerator
https://github.com/tiger-openai-hackathon/hacks
"""

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

print(json.dumps(dict))
