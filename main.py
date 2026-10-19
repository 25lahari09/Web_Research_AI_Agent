import anthropic
import os 
from dotenv import load_dotenv
from web_search import web_search # accessing another file inside this python file

load_dotenv()

client = anthropic.Anthropic()

'''client                 # Anthropic object
client.messages           # Messages object
client.messages.create    # Callable method'''

tools = [
    {
        "name" : "web_search",
        "description" : "Search for the web for current information",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "query" : {
                    "type" : "string",
                    "description" : "The search query to look up on web"
                }
            },
            "required" : ["query"]
        }
    }
]

messages=[]

while True:
    user_input = input(" Send a message: ")

    if user_input.strip().lower() == "quit":
        break

    messages.append(
        {
            "role" : "user",
            "content" : user_input
        }
    )

    response= client.messages.create(
        model = "claude-sonnet-5-5",
        max_tokens = 500,
        messages = messages,
        tools = tools
    )

    tool_results=[] # for collecting the tool_results to pass to claude


    # there are 2 blocks in response variable ( for the version claide sonnet 5-5 )
    # so we make sure which type of block it is 

    #print("\n------------------------------\n")
    #print("\nresponse:\n", response)
    for block in response.content:

        #print ("\n-----------block----------------\n",block)

        #print("\n\n\n\n")

        '''
        # THIS IS FOR JUST IF THE BLOCK TYPE IS TEXT 
        
        if block.type == 'text':
            print(block.text)

            messages.append({
                "role" : "assistant",
                "content" : assistant_reply
            })'''

        # here after claude identifies the tool we have to write a python fun to let the python know it have to perform something 


        if block.type == "text":
            print(block.text)

        elif block.type == "tool_use":
            if block.name == "web_search":
                query = block.input["query"]
                search_results = web_search(query)

                # tool_results is an empty list where we'll collect results from Claude's tool requests
                tool_results.append({
                    "type" : "tool_result",
                    "tool_use_id" : block.id,
                    "content" : str(search_results)
                })
    
    messages.append({
        "role" : "assistant",
        "content" : response.content
    })

    # sometimes claude might directly answer without tavily 
    # so to ONLY SEND TOOL USE RESULTS
    if tool_results:
        messages.append({
            "role" : "user",
            "content" : tool_results
        })

        # making a SECOND API call to get the summarized response
        response= client.messages.create(
                model = "claude-sonnet-5-5",
                max_tokens = 1024,
                messages = messages,
                tools = tools
            )

        #---ignore just to find why the claude is not responding correctly 
        #print("\nSECOND RESPONSE STOP REASON:", response.stop_reason)
        #print("\nSECOND RESPONSE CONTENT:", response.content)
        
        for block in response.content:
            if block.type == "text":
                print(block.text)

        messages.append({
            "role": "assistant",
            "content": response.content
        })
    