from pydantic import BaseModel
from src.ai_tools import *
from src.ai_caller import *
from src.ai_tools import *
import json
from pathlib import Path

class KeywordList(BaseModel):
    keywords: list[str]

def extract_keywords(config) -> KeywordList:
    assignment_description = config.get("spec", "")

    prompt = f"You are a professor and you want to quickly search through student code. Create a list of library or function calls that could be used to find where in the code the student completed the assignment:\n\n{assignment_description}\n\nSearch the internet and docs to inform your answer. Return a max of 10 keywords." 

    response = call_ai(
        model=config["keyword"],
        tools=[search_internet_tool],
        prompt=prompt,
        format=KeywordList
    )
    rainbow_print(response)

    return response

def save_keywords(config, keywords):
    data_dir = None
    if "assignment_directory" in config:
        assignment_dir = Path(config["assignment_directory"])
        data_dir = assignment_dir / ".data"
    
    if data_dir and data_dir.exists():
        metadata_path = data_dir / "metadata.json"
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        
        metadata["keywords"] = keywords.keywords
        
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

def keywords(config):
    if "keywords" not in config:
        keywords = extract_keywords(config)
        save_keywords(config, keywords)
        config["keywords"] = keywords
    else:
        rainbow_print("Keywords already present in metadata.")
