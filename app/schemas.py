from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional



class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class AddWebsiteRequest(BaseModel):
    url: str          
    user_id: str


class WebsiteResponse(BaseModel):
    message: str
    pages_scraped: int
    website_id: str



class ChatRequest(BaseModel):
    message: str
    user_id: str
    website_id: Optional[str] = None  


class ChatResponse(BaseModel):
    response: str
    mode: str       
    sources: Optional[list[str]] = None