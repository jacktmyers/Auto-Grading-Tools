import time

import ollama
import json
import os
import requests
from pydantic import BaseModel
from src.ai_tools import *
from src.rainbow_print import *
import instructor
import llama_cpp
from llama_cpp.llama_speculative import LlamaPromptLookupDecoding

def call_ai_helper(messages, temp, model: str, tools: list, format = None) -> str:
    if format == None:
        return ollama.chat(
            model=model,
            messages=messages,
            tools=tools,
            options={'temperature': temp}
        )
    else:
        return ollama.chat(
            model=model,
            messages=messages,
            tools=tools,
            format=format.model_json_schema(),
            options={'temperature': temp}
        )

def call_ai(model: str, prompt: str, tools: list = [], format = None) -> str:
    rainbow_print(f"Calling {'External' if model.endswith('cloud') else 'Local'} Model: {model}")

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    if format != None:
        messages.append({'role': 'user', 'content': f"{prompt}\n\nReturn a JSON object based on the input schema:{format.model_json_schema()}"})
    
    response = call_ai_helper(messages, 0.5, model, tools, format)

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if function_to_call := available_tools.get(tool.function.name):
                rainbow_print(f"AI Requested Tool:{tool.function.name}")
                output = function_to_call(**tool.function.arguments)
            else:
                rainbow_print('Tool', tool.function.name, 'not found')
    
    if response.message.tool_calls:
        messages.append(response.message)
        messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})

        if format != None:
            messages.append({'role': 'user', 'content': f"{prompt}\n\nReturn a JSON object based on the input schema:{format.model_json_schema()}"})

        rainbow_print(f"Interpreting Tool Output")
        response = call_ai_helper(messages, 0.5, model, [], format)


    if response.get("message") and response["message"].get("content"):
        if format != None:
            return format.model_validate_json(response.message.content) 
        else:
            return response.message.content
    else:
        raise Exception("No Response Generated")

    
call_purdue_ai_call_count = 0
call_purdue_ai_last_reset_time = time.time()

def call_purdue_ai(model, prompt, format):
    global call_purdue_ai_call_count, call_purdue_ai_last_reset_time
    failures = 0
    
    while failures < 4:
        try:
            current_time = time.time()
            
            if current_time - call_purdue_ai_last_reset_time >= 60:
                call_purdue_ai_call_count = 0
                call_purdue_ai_last_reset_time = current_time
            
            if call_purdue_ai_call_count >= 9:
                wait_time = 60 - (current_time - call_purdue_ai_last_reset_time) + 10 # Maybe a buffer will help
                rainbow_print(f"▶ Rate limit reached for Purdue AI. Waiting {wait_time:.2f} seconds.")
                time.sleep(wait_time)
                call_purdue_ai_call_count = 0
                call_purdue_ai_last_reset_time = time.time()
            
            call_purdue_ai_call_count += 1
            
            rainbow_print(f"Calling External Purdue Model")
            load_dotenv() # For API Keys etc
            api_key = os.getenv("PURDUE_API_KEY")
            if not api_key:
                raise Exception("PURDUE_API_KEY not set")
            
            session = requests.Session()
            url = "https://genai.rcac.purdue.edu/api/chat/completions"
            session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })
            body = {
                "model": model,
                "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
                ],
                "stream": False,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": format.__name__,
                        "strict": True,
                        "schema": format.model_json_schema()
                    }
                },
                "temperature": 0
            }
            response = session.post(
                url,
                json=body
            )
            session.close()
            if response.status_code == 200:
                response_data = json.loads(response.text)
                try:
                    return format.model_validate_json(response_data["choices"][0]["message"]["content"]) 
                except:
                    raise Exception(f"Error in Purdue AI call. Response {response.text}")
            else:
                raise Exception(f"Error: {response.status_code}, {response.text}")
        except:
            failures += 1
            rainbow_print(response)
            rainbow_print(f"✖ Purdue AI call failed {failures} times. Waiting {failures} minute(s) and retrying")
            time.sleep(60 * failures)
    raise Exception(f"Purdue API call failed {failures} times. Quitting.")
