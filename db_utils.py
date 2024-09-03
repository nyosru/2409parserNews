from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.exc import OperationalError
import os

# Получаем строку подключения из переменной окружения
DATABASE_URI = os.getenv('DATABASE_URI')

# Настройка подключения к базе данных (замените на ваши данные)
#DATABASE_URI = 'mysql+pymysql://username:password@localhost/dbname'
#DATABASE_URI = 'mysql+pymysql://root:as321S@localhost/2309livewire'
#DATABASE_URI = 'mysql+pymysql://root:as1S@db_mysql/2309livewire'

# Данные для подключения к базе данных
#DATABASE_URI = 'mysql+pymysql://root:as@db_mysql:3306/2309livewire'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
metadata = MetaData(bind=engine)
st_news = Table('st_news', metadata, autoload=True)



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

def add_news_to_db(news_data):
    """
    Функция для добавления данных в таблицу st_news.

    :param news_data: Словарь с данными новости
    """
    session = Session()
    try:
        # Вставка данных в таблицу
        insert_stmt = insert(st_news).values(news_data)
        session.execute(insert_stmt)
        session.commit()
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
        session.rollback()
    finally:
        session.close()
