from sqlalchemy.orm import Session

from db.models import Base
from settings.settings import settings
from sqlalchemy import create_engine
from db.models import Post, Photo


class DBManager:
    def __init__(self):
        try:
            self.engine = create_engine(
                f'postgresql+psycopg2://'
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
            title_message_id,
            description,
            description_message_id,
            price,
            price_message_id,
            contacts,
            contacts_message_id,
    ):
        post_object = Post(
            user_tg_id=user_tg_id,
            first_name=first_name,
            username=username,
            title=title,
            title_message_id=title_message_id,
            description=description,
            description_message_id=description_message_id,
            price=price,
            price_message_id=price_message_id,
            contacts=contacts,
            contacts_message_id=contacts_message_id,
        )
        with Session(self.engine) as session:
            session.add(post_object)
            session.commit()
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
            date=date,
            file_id=file_id,
            file_unique_id=file_unique_id,
            file_size=file_size,
            width=width,
            height=height,
            post_id=post_id
        )
        with Session(self.engine) as session:
            session.add(photo_object)
            session.commit()
        return photo_object

    def get_post(
            self,
            user_tg_id,
            title_message_id,
    ):
        with Session(self.engine) as session:
            query = session.query(Post).filter_by(
                user_tg_id=user_tg_id,
                title_message_id=title_message_id
            ).first()
        return query


db = DBManager()


def create_all():
    Base.metadata.create_all(db.engine)


if __name__ == '__main__':
    create_all()
