from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'post_table'

    id = Column(BigInteger, primary_key=True)
    user_tg_id = Column(BigInteger, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(String, primary_key=False)
    # tag = Column(String, nullable=False)

    # photo = Relationship(back_populates='post')





class Photo(Base):
    __tablename__ = 'photo_table'

    id = Column(BigInteger, primary_key=True)
    photo_path = Column(String, nullable=False)

    post_id = Column(BigInteger, ForeignKey('post_table.id'))
    post = relationship('Post', backref='photo_post', foreign_keys=[post_id])
