from git import Repo
from src.git_actions import *
from src.ai_caller import *
import os


class Rating(BaseModel):
    value: int

def analyze_repos(config, student, student_count):
    repo_path = get_repo_path(student, config["assignment_directory"])
    report_path = os.path.join(repo_path, config["report_location"])
    
    if os.path.exists(report_path):
        return None

    files_to_analyze = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if any([file.endswith(ext) for ext in config["valid_file_extensions"]]) and all([file != ig for ig in config["ignored_files"]]):
                files_to_analyze.append(os.path.join(root, file))
    
    count = 0
    analyzed_files = []
    for file_path in files_to_analyze:
        set_header(f"{student_count}/{len(config['students'])}", f"{student['First Name']} {student['Last Name']}", f"{count}/{len(files_to_analyze)}")
        rainbow_print(f"\nAnalyzing file: {os.path.basename(file_path)}")
        file_entry = {}
        file_entry["path"] = file_path

        with open(file_entry["path"], 'r', encoding='utf-8', errors='ignore') as f:
            file_entry["content"] = f.read().lower()

        file_entry["emoji_locations"] = []
        lines = file_entry["content"].splitlines()
        for line_num, line in enumerate(lines):
            for i, char in enumerate(line):
                if ord(char) > 127:
                    file_entry["emoji_locations"].append({"line_num": line_num, "line": line})
        
        file_entry["emoji_count"] = len(file_entry["emoji_locations"])
        file_entry["keyword_count"] = sum(1 for keyword in config["keywords"] if keyword.lower() in file_entry["content"])


        repo = Repo(repo_path)
        relative_file_path = os.path.relpath(file_entry["path"], repo_path)
        commits = list(repo.iter_commits(paths=relative_file_path, max_count=1))
        if commits:
            file_entry["commit_date"] = commits[0].committed_date
            file_entry["commit_msg"] = commits[0].message.strip("\n").replace("\n", " ")

        for metric in config["metrics"]:
            file_entry[f"{metric}_score"] = call_ai(
                model= config["metric"],
                prompt= f"{config['metrics'][metric]}\n\n# File Content\n{file_entry['content']}\n\n# Response\n Respond with only an integer between 1 and 100.",
                format= Rating
            ).value
            rainbow_print(f"LLM Generated Metric: {file_entry[f"{metric}_score"]}");

        file_entry["assignment_related_score"] = call_ai(
            model= config["matcher"],
            prompt= f"# Personality and Purpose\nYou are a teaching assistant and you want to generate a rating for your professor on whether or not the current file is related to the assignment. You need to produce a value between 0 and 100, with 100 being: this file definitely addresses the goals of the assignment. Only respond with a number. Here is the assignment description: {config['spec']}\n\n# File Content\n{file_entry['content']}\n\n# Output\n Respond with an integer rating between 1 and 100",
            format= Rating
        ).value
        rainbow_print(f"LLM Generated Metric: {file_entry['assignment_related_score']}");


        analyzed_files.append(file_entry) 
        count += 1

        # if count > 3:
        #     break
    return analyzed_files

    # analyzed_students[f"{student['First Name']} {student['Last Name']}"] = analyzed_files
    # student_count += 1
    
