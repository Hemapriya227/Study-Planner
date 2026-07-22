from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.middleware.auth_middleware import verify_token


router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)


@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check whether user already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    print("Password:",user.password)
    print("Type:", type(user.password))
    print("Length:",len(user.password))

    hashed_password=hash_password(user.password)
    # Create database user
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create JWT access token
    token = create_access_token(user_id=db_user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(db_user)
    }


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):

    # Find user
    db_user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    # Check credentials
    if not db_user or not verify_password(
        credentials.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT access token
    token = create_access_token(user_id=db_user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(db_user)
    }


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user