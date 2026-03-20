from src.git_actions import *
from src.ai_caller import *
from src.ai_tools import *
from src.keyword_finder import *
from src.rainbow_print import *
from src.repo_analyzer import *
from src.report_generator import *
import json
import os





def run_pipeline(config):
    rainbow_print("Cloning Directories")
    clone_repositories(config["students"], config["assignment_directory"])
    rainbow_print("Generating Keywords")
    keywords(config)
    rainbow_print("Starting Analysis")
    student_count = 0
    students = [s for s in config["students"] if s["git Link"] != "NA"]

    for student in students:
        analysis_result = analyze_repos(config, student, student_count)
        if analysis_result == None:
            student_count += 1
            continue
        rainbow_print("Generating Report")
        generate_report(f"{student['First Name']} {student['Last Name']}", analysis_result, config)
        student_count += 1


