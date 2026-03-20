# Auto Grading Tools
**A collection of tools that I use to help speed up the grading process**

## ARGH
* This is a repo scanner and metric evaluator
* It evaluates metrics by processing each file through a LLM provider and returning a structured output based on a metric prompt.
* The script also uses an LLM to search the internet and generates keywords based on the assignment description.
    * These keywords are then matched throughout each file.
* Each student has a report generated for each processed file in their repository.

## WGetter
* This is a simple tool that will pull student webpage and copy in resources, so the website can be tested locally.