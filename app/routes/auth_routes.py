from fastapi import APIRouter, HTTPException
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.database import get_db
from app.models import user_model
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(body: RegisterRequest):
    db = get_db()
    existing = await db.users.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    doc = user_model(
        name=body.name,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    result = await db.users.insert_one(doc)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    db = get_db()
    user = await db.users.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
    return TokenResponse(access_token=token)