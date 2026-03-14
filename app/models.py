from datetime import datetime


def new_doc(**kwargs) -> dict:
    return {"created_at": datetime.utcnow(), **kwargs}


def user_model(name: str, email: str, hashed_password: str) -> dict:
    return new_doc(
        name=name,
        email=email,
        hashed_password=hashed_password,
    )


def website_model(user_id: str, url: str, status: str = "pending") -> dict:
    return new_doc(
        user_id=str(user_id),
        url=url,
        status=status,
        pages_scraped=0,
    )


def chat_history_model(
    user_id: str,
    message: str,
    response: str,
    mode: str,
    website_id: str = None,
) -> dict:
    return {
        "user_id":    str(user_id),       
        "message":    message,            
        "response":   response,           
        "mode":       mode,               
        "website_id": str(website_id) if website_id else None,
        "timestamp":  datetime.utcnow(),
        "created_at": datetime.utcnow(),
    }
