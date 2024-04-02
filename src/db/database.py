from sqlalchemy.orm import Session

from db.models import Base
from utils.settings import settings
from sqlalchemy import create_engine
from db.models import Post


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

    def add_post(self, user_tg_id, title, description, price):
        post_object = Post(
            user_tg_id=user_tg_id,
            title=title,
            description=description,
            price=price,
        )
        with Session(self.engine) as session:
            session.bulk_save_objects([post_object])
            session.commit()


db = DBManager()


def create_all():
    Base.metadata.create_all(db.engine)


if __name__ == '__main__':
    create_all()
