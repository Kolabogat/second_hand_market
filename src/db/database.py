from sqlalchemy.orm import Session

from db.models import Base
from utils.settings import settings
from sqlalchemy import create_engine
from db.models import Post, Photo


class DBManager:
    def __init__(self):
        try:
            self.engine = create_engine(f'postgresql+psycopg2://'
                                        f'{settings.postgresql.POSTGRES_USER}:'
                                        f'{settings.postgresql.POSTGRES_PASSWORD}@'
                                        f'{settings.postgresql.POSTGRES_HOST}:'
                                        f'{settings.postgresql.POSTGRES_PORT}/'
                                        f'{settings.postgresql.POSTGRES_DB}'
                                        )
        except Exception as e:
            print(f'Unable to access postgresql database. \n Exception: {e}')

    def add_post(
            self,
            user_tg_id,
            first_name,
            username,
            title,
            description,
            price
    ):
        post_object = Post(
            user_tg_id=user_tg_id,
            first_name=first_name,
            username=username,
            title=title,
            description=description,
            price=price,
        )
        with Session(self.engine) as session:
            session.add(post_object)
            session.commit()
        print(post_object)
        return post_object

    def add_photo(
            self,
            file_id,
            file_unique_id,
            file_size,
            width,
            height,
            date,
            post_id,
    ):
        photo_object = Photo(
            file_id=file_id,
            file_unique_id=file_unique_id,
            file_size=file_size,
            width=width,
            height=height,
            date=date,
            post_id=post_id
        )
        with Session(self.engine) as session:
            session.add(photo_object)
            session.commit()


db = DBManager()


def create_all():
    Base.metadata.create_all(db.engine)


if __name__ == '__main__':
    create_all()
