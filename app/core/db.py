from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models import User, UserCreate
from app.core import crud

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(session: Session) -> None:
    
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
        
test_engine = create_engine(str(settings.TEST_SQLALCHEMY_DATABASE_URI))

def init_test_db(session:Session):
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(test_engine)
    
 
    user = session.exec(
            select(User).where(User.email == settings.FIRST_SUPERUSER)
        ).first()
    if not user:
        user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
        user = crud.create_user(session=session, user_create=user_in)
            