# website/routers/google_auth.py

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
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
    client_kwargs={"scope": "openid email profile"},
)

# ---------------- GOOGLE LOGIN ----------------
@router.get("/login")
async def google_login(request: Request):
    """
    Redirect user to Google login page.
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI  # http://localhost:9007/auth/google/callback
    return await oauth.google.authorize_redirect(request, redirect_uri)


# ---------------- GOOGLE CALLBACK ----------------
@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Google callback: fetch user info, create JWT, redirect to frontend
    """
    try:
        # This reads the state from the session cookie to prevent CSRF
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        # Common issues: session not preserved, localhost vs 127.0.0.1
        if not request.session:
            print("ERROR: Session is empty! Ensure you are using the same domain for login and callback.")
            print("DEBUG: Request Cookies:", request.cookies)
        print("GOOGLE CALLBACK ERROR:", e)
        raise HTTPException(status_code=400, detail=str(e))

    # Fetch user info using full URL
    resp = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",  # full URL required
        token=token
    )
    resp.raise_for_status()
    userinfo = resp.json()

    email = userinfo.get("email")
    name = userinfo.get("name") or "User"

    if not email:
        raise HTTPException(status_code=400, detail="Email not found from Google")

    # ---------------- CREATE OR GET USER ----------------
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            role="user",
            is_verified=True,
            auth_provider="google"  # optional field for tracking
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif not user.is_verified:
        user.is_verified = True
        db.commit()

    # ---------------- CREATE JWT TOKEN ----------------
    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    # ---------------- REDIRECT TO FRONTEND ----------------
    frontend_url = f"http://localhost:5173/oauth-success?token={access_token}"
    return RedirectResponse(url=frontend_url)