from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class JobRequest(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=100, description="The job title")
    years_experience: int = Field(..., ge=0, le=50, description="Required years of experience")
    company_name: str = Field(..., min_length=1, max_length=200, description="Company name")
    company_overview: str = Field(..., min_length=1, max_length=1000, description="Company overview")
    skills: List[str] = Field(..., min_items=3, max_items=20, description="Required skills")
    location: Optional[str] = Field(None, max_length=100, description="Job location")
    employment_type: Optional[str] = Field(None, max_length=50, description="Employment type")
    
    @validator('job_title')
    def validate_job_title(cls, v):
        if not re.match(r'^[a-zA-Z0-9\s\-_.,()&/]+$', v.strip()):
            raise ValueError('Job title contains invalid characters')
        return v.strip()
    
    @validator('skills')
    def validate_skills(cls, v):
        if len(v) < 3:
            raise ValueError('At least 3 skills are required')
        if len(v) > 20:
            raise ValueError('Maximum 20 skills allowed')
        
        validated_skills = []
        for skill in v:
            skill = skill.strip()
            if not re.match(r'^[a-zA-Z0-9\s\-_.,()&/#+]+$', skill):
                raise ValueError(f'Skill "{skill}" contains invalid characters')
            validated_skills.append(skill)
        return validated_skills
    
    @validator('company_name')
    def validate_company_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9\s\-_.,()&/\'"]+$', v.strip()):
            raise ValueError('Company name contains invalid characters')
        return v.strip()
    
    @validator('location')
    def validate_location(cls, v):
        if v is not None:
            v = v.strip()
            if not re.match(r'^[a-zA-Z0-9\s\-_.,()&/]+$', v):
                raise ValueError('Location contains invalid characters')
        return v

class JobResponse(BaseModel):
    company_name: str
    company_overview: str
    title: str
    experience_level: str
    experience_years: int
    responsibilities: List[str]
    qualifications: List[str]
    required_skills: List[str]
    optional_skills: List[str]
    location: Optional[str] = None
    employment_type: Optional[str] = None