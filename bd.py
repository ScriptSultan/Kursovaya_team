import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, InvalidRequestError

Base = declarative_base()

main_engine = sa.create_engine('postgres://localhost:5432/co_fi_db', echo=True))
Session = sessionmaker(bind=main_engine)

dbsession = Session()
connection = main_engine.connect()

def create_db(cur):
    """
    1. Функция, создающая структуру БД (таблицы)
    """
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
	    vk_id VARCHAR(20),
	    name VARCHAR(20) NOT null,
	    lastname VARCHAR(30) NOT null,
	    age INTEGER,
	    town VARCHAR(30) NOT null,
	    gender VARCHAR(10),
	    link VARCHAR(50) NOT null
        );
        """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS favourite(
    	id SERIAL PRIMARY KEY,
    	vk_id VARCHAR(20),
    	name VARCHAR(20) NOT null,
    	lastname VARCHAR(30) NOT null,
    	age INTEGER,
    	town VARCHAR(30) NOT null,
    	gender VARCHAR(10),
    	link VARCHAR(50) NOT null,
    	id_user INTEGER REFERENCES users(id) 
        );
        """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS photo(
    	id SERIAL PRIMARY KEY,
    	photo_link VARCHAR(50) NOT NULL,
    	likes INTEGER,	
    	id_favourite INTEGER REFERENCES favourite(id)
        );
        """)

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    vk_id = sa.Column(sa.Integer, unique=True)
    name = sa.Column(sa.String)
    lastname = sa.Column(sa.String)
    age = sa.Column(sa.Integer, unique=True)
    town = sa.Column(sa.String)
    gender = sa.Column(sa.Integer, unique=True)
    link = sa.Column(sa.String)

class Favourite(Base):
    __tablename__ = 'favourite'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    vk_id = sa.Column(sa.Integer, unique=True)
    name = sa.Column(sa.String)
    lastname = sa.Column(sa.String)
    age = sa.Column(sa.Integer, unique=True)
    town = sa.Column(sa.String)
    gender = sa.Column(sa.Integer, unique=True)
    link = sa.Column(sa.String)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('users.id', onedelete='CASCADE'))

class Photo(Base):
    __tablename__ = 'photo'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    photo_link = sa.Column(sa.String)
    likes = sa.Column(sa.Integer)
    id_favourite = sa.Column(sa.Integer, sa.ForeignKey('favourite.id', onedelete='CASCADE'))


def add_users(user_id, vk_id, name, lastname, age, town, gender, link):
    try:
        ins_user = User(
            vk_id=vk_id,
            name=name,
            lastname=lastname,
            age=age,
            town=town,
            gender=gender,
            link=link
        )
        dbsession.add(ins_user)
        dbsession.commit()
        return 'User Added'
    except (IntegrityError, InvalidRequestError):
        return 'User Exists'

connection = psycopg2.connect(
    host=localhost,
    user=postgres,
    password=password,
    database=co_fi_db
)

connection.autocommit = True

with connection.cursor() as cur:

    def get_select(cur):
        cur.execute("""
            SELECT us.name,
                    us.lastname,
                    us.age,
                    us.town,
                    FROM user AS us
                    JOIN photo AS ph
                    WHERE gender
                    AND IF (us.gender  = '1') = '2' AND IF (us.gender  = '2') = '1'
        """)

# select из фаворитов - получаешь 5 человек, далее fetchall


    def add_to_fav(cur, id, vk_id, name, lastname, age, town, gender, link):
        """
        Функция, позволяющая добавить пару в избранное
        """
        cur.execute("""
            INSERT INTO favourite(id, vk_id, name, lastname, age, town, gender, link)
            VALUES (%s, %s, %s)
            """, (id, vk_id, name, lastname, age, town, gender, link))
        cur.execute("""
            SELECT id from favourite
            ORDER BY id DESC
        """)
        return cur.fetchall()

    def delete_from_favourite(cur, id):
        """
        Функция, позволяющая удалить существующего клиента
        """
        cur.execute("""
            DELETE FROM favourite
            WHERE user_id = %s
            """, (id,))
        return f"User {id} has been successfully deleted from favourite"


    def select_fav(cur, name, lastname, age, town, gender, link):
        """
        Функция, позволяющая направить пару из избранное
        """
        cur.execute("""
            SELECT FROM favourite(name, lastname, age, town, gender, link)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, lastname, age, town, gender, link))
        cur.execute("""
            SELECT id from favourite
            ORDER BY id DESC
        """)

        res = cur.fetchall()
        list = []
        for row in res:
            list.append(row)
        return list

if __name__ == '__main__':
    Base.metadata.create_all(main_engine)

















import psycopg2


# def create_db(conn):
#     with conn.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id SERIAL PRIMARY KEY,
#                 vk_id INTEGER,
#                 name VARCHAR(50) NOT NULL,
#                 last_name VARCHAR(50) NOT NULL,
#                 link_us VARCHAR(50) NOT NULL,
#                 age VARCHAR(100),
#                 gender VARCHAR(10),
#             );
#             """)
#         cur.execute("""
#                 CREATE TABLE IF NOT EXISTS favourite (
#                     id SERIAL PRIMARY KEY,
#                     vk_id INTEGER,
#                     name VARCHAR(50) NOT NULL,
#                     last_name VARCHAR(50) NOT NULL,
#                     link VARCHAR(50) NOT NULL,
#                     id_user INTEGER REFERENCES users(id),
#                     age VARCHAR(100),
#                     gender VARCHAR(10)
#                 );
#                 """)
#         cur.execute("""
#                 CREATE TABLE IF NOT EXISTS photo (
#                     id SERIAL PRIMARY KEY,
#                     likes VARCHAR(10),
#                     photo_link VARCHAR(50) NOT NULL
#                     id_favourite INTEGER REFERENCES favourite(id)
#                 );
#                 """)
#     return cur.fetchall()
#
#
# def add_users(conn, vk_id: str, name: str, last_name: str, link_us: str, age=None, gender=None):
#     with conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO users(vk_id, name, last_name, link_us, age, gender)
#             VALUES(%s, %s, %s, %s);"""), (vk_id, name, last_name, link_us, age, gender)
#     return cur.fetchone()
#
# def add_favourite(conn, vk_id: str, name: str, last_name: str, link_us: str, id_user: str, age=None, gender=None):
#     with conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO favourite(vk_id, name, last_name, link_us, id_user, age, gender)
#             VALUES(%s, %s, %s, %s, %s, %s, %s);"""), (vk_id, name, last_name, link_us, id_user, age, gender)
#         return cur.fetchone()
#
# def add_photos(conn, likes: str, photo_link: str, id_favourite: str):
#     with conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO photo(likes, photo_link, id_favourite)
#             VALUES(%s, %s, %s);"""), (likes, photo_link, id_favourite)
#         return cur.fetchone()
#
# def select_users(conn,likes, photo_link, id_favourite):
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT likes, photo_link, id_favourite
#             VALUES(%s, %s, %s);"""), (likes, photo_link, id_favourite)
#         return cur.fetchone()