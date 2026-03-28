from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rootUser@localhost/yusuphdarbo"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
