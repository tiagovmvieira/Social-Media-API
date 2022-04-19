from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from .database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, primary_key = False, nullable = False)
    content = Column(String, primary_key = False, nullable = False)
    published = Column(Boolean, primary_key = False, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), primary_key = False, nullable = False, server_default = text('now()'))