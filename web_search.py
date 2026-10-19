import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))

# FOR PRINTING methods of tavily
#print([name for name in dir(tavily_client) if not name.startswith("_")])

# verifying tavily response for extracting text 
#print(type(tavily_response))
#print(tavily_response.keys()) # for seeing what are actually availbale 


def web_search(query):
    
    tavily_response = tavily_client.search(query = query)
    return tavily_response["results"]
