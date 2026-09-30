from pydantic import BaseModel
from typing import List, Optional


class JobProfile(BaseModel):
    job_title: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    education: List[str] = []
    experience: Optional[str] = None