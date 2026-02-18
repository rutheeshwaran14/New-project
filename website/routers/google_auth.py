from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from website.database import get_db
from website.models.user import User
from website.utils.jwt import create_access_token
from config import settings

router = APIRouter(prefix="/auth/google", tags=["Google Auth"])

# ---------------- OAUTH INIT ----------------
oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    },
)

# ---------------- LOGIN ----------------
@router.get("/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI
    )

# ---------------- CALLBACK ----------------
# ---------------- CALLBACK ----------------
@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        print("🔥 GOOGLE CALLBACK ERROR =>", e)
        raise HTTPException(status_code=400, detail=str(e))

    userinfo = token.get("userinfo")
    if not userinfo:
        resp = await oauth.google.get("userinfo", token=token)
        userinfo = resp.json()

    email = userinfo.get("email")
    name = userinfo.get("name", "")

    if not email:
        raise HTTPException(status_code=400, detail="Unable to fetch email from Google")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            role="user",
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": email,
        "name": name
    }
