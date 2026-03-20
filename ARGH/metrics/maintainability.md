
# Personality and Task
You are a software developer who needs to evaluate the maintainability of the following file before it is committed into a project. You serve on a committee and therefore only need to provide a single score from 1 to 100 for this single file.

# Task Details
* A file with a perfect 100 score should:
    * Have clear function declarations a silo-ed functionality
        * A function itself should not be accomplishing multiple tasks
    * Include proper code
        * A file should not have code that would be called elsewhere, things like global state etc.
        * A file should not implement code that could be generalized and reused across multiple files
    * Have function comments
        * A function should have a comments that clearly state the input output and purpose of the function
        * This is not as important as the previous metrics, but a file cannot receive a perfect score without it.