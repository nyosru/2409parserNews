from sqlalchemy import create_engine, Table, MetaData, insert, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os

# Получаем строку подключения из переменной окружения
DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
metadata = MetaData(bind=engine)
st_news = Table('st_news', metadata, autoload=True)
st_news_photos = Table('st_news_photos', metadata, autoload=True)

def check_db_connection():
    """Проверяет подключение к базе данных"""
    try:
        with engine.connect() as connection:
            print("Connection to the database is successful!")
            return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False

def get_db_session():
    """Возвращает новый сеанс подключения к базе данных"""
    return Session()

def get_table(name):
    """Возвращает объект таблицы по имени"""
    return Table(name, metadata, autoload_with=engine)

def insert_news(news_list):
    """Вставляет список новостей в таблицу st_news"""
    table = get_table('st_news')
    session = get_db_session()

    try:
        with session.begin():
            for news in news_list:
                # Убедитесь, что ключи в словаре соответствуют столбцам в таблице
                session.execute(table.insert().values(news))
        print("News inserted successfully.")
    except SQLAlchemyError as e:
        print(f"Error inserting news: {e}")
        session.rollback()
    finally:
        session.close()

def add_news_to_db(news_item):
    """Добавляет новость в таблицу st_news, проверяя на уникальность по полю source"""
    session = get_db_session()
    result = {
        'status': False,
        'message': ''
    }
    
    try:
        # Проверка, существует ли новость с таким же source
        existing_news = session.execute(select(st_news).where(st_news.c.source == news_item['source'])).first()

        if existing_news:
            result['message'] = 'News with the same source already exists in the database.'
            return result  # Новость уже существует в базе данных

        # Текущее время для полей created_at и updated_at
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Добавляем необходимые поля
        news_item['created_at'] = current_time
        news_item['updated_at'] = current_time

        # Вставляем новость в таблицу
        session.execute(st_news.insert().values(news_item))
        session.commit()
        result['status'] = True
        result['message'] = 'News inserted successfully.'

        # Если у новости есть изображения, добавляем их в таблицу st_news_photos
        if 'image' in news_item and news_item['image']:
            st_news_id = session.execute(select(st_news.c.id).where(st_news.c.source == news_item['source'])).scalar()
            if st_news_id:
                session.execute(
                    st_news_photos.insert().values(
                        st_news_id=st_news_id,
                        image_path=news_item['image'],
                        created_at=current_time,
                        updated_at=current_time
                    )
                )
                session.commit()

    except SQLAlchemyError as e:
        result['message'] = f"Error adding news to the database: {e}"
        session.rollback()

    finally:
        session.close()

    return result
