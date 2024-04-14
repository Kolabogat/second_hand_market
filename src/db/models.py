from sqlalchemy import Column, String, BigInteger, ForeignKey, Integer, Date
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'post_table'

    id = Column(BigInteger, primary_key=True)
    user_tg_id = Column(BigInteger, nullable=False)
    first_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    title = Column(String, nullable=False)
    title_message_id = Column(BigInteger, nullable=False)
    description = Column(String, nullable=False)
    description_message_id = Column(BigInteger, nullable=False)
    price = Column(String, primary_key=False)
    price_message_id = Column(BigInteger, nullable=False)
    photo = relationship('Photo', backref='post')


class Photo(Base):
    __tablename__ = 'photo_table'

    id = Column(BigInteger, primary_key=True)
    date = Column(Date, nullable=False)
    file_id = Column(String, nullable=False)
    file_unique_id = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    width = Column(BigInteger, nullable=False)
    height = Column(BigInteger, nullable=False)
    post_id = Column(Integer, ForeignKey('post_table.id'))
