from app.services.job_parser import parse_job_description


job_description = """
Software Engineer

Required Skills:
Python
C++
SQL
Git

Preferred Skills:
Docker
AWS
React

Education:
B.Tech
B.E.

Experience:
0-2 years
"""


job = parse_job_description(job_description)

print(job.model_dump())