Language: Python

## Configuration Variables
* Assignment Directory
    * The directory of the assignment, directory contains metadata, prompts, and git repo info for the specific assignment
* Keyword Model - Big Cloud Model
    * The model that generates search terms based on the assignment description
* File Matcher Model - Local Model
    * The model that makes the decision on whether or not the specific file is related to the assignment
* File Rater Model - Local Model
    * Rate the model based on the metrics in a prompt

## First Iteration Structure
1. Read in assignment metadata
2. Generate keywords/function calls that could be used to complete the assignment and save them to the assignments metadata
3. Read in user repositories
4. Clone user repositories to the assignment directory renaming the directory to the user's name.
    * Any duplicates should be skipped and not re-cloned
5. For each repo:
    1. For each file
        1. Find and count assignment keyword matches
        2. Find the most recent commit within the file and compare it to the assignment due date
        3. Generate percentage that the file relates to the assignment based on file content and assignment details
        4. Find Emoji Locations and log the file name
        5. Generate a score for specific metrics
    2. Find the average AI intervention score
    3. Sort the files based on the percentage that the file relates to the assignment
    4. Write a final AI-report file into a .grade folder within the student's assignment directory
