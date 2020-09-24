import uuid

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.REAL)

# Класс для таблицы с атлетами
class Athelete(Base):
    # Название таблицы
    __tablename__ = "athelete"
    # Идентификатор атлета
    id = sa.Column(sa.INTEGER, primary_key=True)
    # Дата рождения
    birthdate = sa.Column(sa.Text)
    # Рост атлета
    height = sa.Column(sa.REAL)
    # Имя атлета
    name = sa.Column(sa.Text)

 

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()



def find(user_id):
    """
    Производит поиск пользователя в таблице user по заданному ID и вохвращает ближайших кандидатов из таблицы athelete
    
    """
    # Создадим сессию
    session = connect_db()
    # нахдим все записи в таблице User, у которых поле id совпадает с парарметром ввода
    query = session.query(User).filter(User.id == user_id).first()
    
    # делаем проверку, что такой ID существует, иначе выдаем предупреждение
    if query:
        user_date = query.last_name, query.first_name, query.height, query.birthdate
    # печатаем результат для введеного id:
        print ("Имя", query.first_name, "Фамилия", query.last_name, "Рост", query.height, "Дата рождения", query.birthdate)
    else:
        print("Такого ID нет в базе")
        return

    user_height, user_birthdate = query.height, query.birthdate

    # создаем запрос к класу Athelete для определения роста из таблицы athelete и определения нужного кандидата:

    atl_height = session.query(Athelete).filter(Athelete.height > 0).order_by(sa.func.abs(Athelete.height - user_height)).first()

    # создаем запрос к класу Athelete для определения даты рождения из таблицы athelete и определения нужного кандидата:
   
    atl_birthdate = session.query(Athelete).filter(Athelete.birthdate > 0).order_by(sa.func.abs(sa.func.julianday(Athelete.birthdate) - sa.func.julianday(user_birthdate))).first()

    candidate_height = atl_height.name, atl_height.height

    candidate_birthdate = atl_birthdate.name, atl_birthdate.birthdate

    print("Ближайший кандидат по росту", candidate_height)
    
    print("Ближайший кандидат по дате рождения", candidate_birthdate)
    

    # Закроем сессию
    session.close()

    return query




def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    
    # Для начала запросим ID пользователя
    user_id = int(input("Введите ID пользователя: "))
    
    # Находим юзера по ID
    user = find(user_id)

    return (user)
  


if __name__ == "__main__":
    main()