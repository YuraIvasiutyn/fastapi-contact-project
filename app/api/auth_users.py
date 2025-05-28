from fastapi import APIRouter, Depends, HTTPException, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.models.user_models import UserModel, UserResponse, TokenModel, RequestEmail
from app.auth.auth import Hash, get_user_by_email, create_user, update_token
from app.auth.email import send_email
from app.database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
hash_handler = Hash()
security = HTTPBearer()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(
        body: UserModel,
        background_tasks: BackgroundTasks,
        request: Request,
        db: Session = Depends(get_db)
):
    exist_user = await get_user_by_email(body.username, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists"
        )
    body.password = hash_handler.get_password_hash(body.password)
    new_user = await create_user(body, db)
    background_tasks.add_task(send_email,  new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email"
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed"
        )
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    access_token = await hash_handler.create_access_token(data={"sub": user.username})
    refresh_token = await hash_handler.create_refresh_token(data={"sub": user.username})
    await update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await hash_handler.get_email_form_refresh_token(token)
    user = await get_user_by_email(email, db)
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    access_token = await hash_handler.create_access_token(data={"sub": user.username})
    refresh_token = await hash_handler.create_refresh_token(data={"sub": user.username})
    await update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await hash_handler.get_email_from_token(token)
    user = await get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = await get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}
