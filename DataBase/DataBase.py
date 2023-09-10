# Здесь расположим всю работу с базой данных

# ----------------------------SQLALCHEMY--------------------------------
# Подключение к базе данных через SQLAlchemy
# движок
from sqlalchemy import create_engine
# Сессия к БД
from sqlalchemy.orm import sessionmaker

# -------------------------------- Создание сессии --------------------------------
# ----------------------------SQLALCHEMY----------------------
# Подключение к базе данных через SQLAlchemy
# ============================================================
# class DataBase:
#     """
#     Здесь опишем класс, который работает с БД
#     """
#     # Путь до API
#     pauth_db = "database.db"
#     # Таблица
#     Table = "HTTPAuth"
#
#
#
#
#
#     # Определяем поле JSON в котором храняться настройки
#     API_data_tag = 'Settings'
#
#     UM_data_tag = 'Settings'
#
#     # Для начала обозначим поля
#     # Для начала обозначим поля
#
#     # Имя поля id для JSON
#     UM_id_tag = "id"
#     # Имя поля login для JSON
#     UM_login_tag = "login"
#     # Имя поля password для JSON
#     UM_password_tag = "password"
#     # Имя поля lvl для JSON
#     UM_lvl_tag = "lvl"
#
#     # Имя поля id для DataBase
#     DataBase_id_tag = "Id"
#     # Имя поля login для DataBase
#     DataBase_login_tag = "Login"
#     # Имя поля password для DataBase
#     DataBase_password_tag = "Password"
#     # Имя поля lvl для DataBase
#     DataBase_lvl_tag = "LevelId"
#
#     # Сопоставление колонок с тэгами JSON
#     interrelation_Tags_JSON_to_DataBase = {
#         UM_id_tag: DataBase_id_tag,
#         UM_login_tag: DataBase_login_tag,
#         UM_password_tag: DataBase_password_tag,
#         UM_lvl_tag: DataBase_lvl_tag,
#     }
#
#     # ----------------------- Схема ----------------------
#     class HTTPAuth(DeclarativeAuthBase):
#         # Имя таблицы
#         __tablename__ = "HTTPAuth"
#         # Поля Таблицы
#         Id = Column("Id", Integer, primary_key=True)
#         Login = Column("Login", String)
#         Password = Column("Password", String)
#         LevelId = Column("LevelId", Integer)
#
#         def __init__(self, Id, Login, Password, LevelId):
#             self.Id = Id
#             self.Login = Login
#             self.Password = Password
#             self.LevelId = LevelId
#
#     # ---------------------------------------------------
#     # ИМЯ АДМИНА
#     admin_login_value = "admin"
#     # Объект нашей базы данных - це важно - если БД закрыта то
#     _DATABASE = None
#
#     #
#
#     def __init__(self):
#         # Ставим заглушку на выполнение - Результат и ответ
#         self.result = 102
#         self.response = self._HTTP_status_codes(self.result)
#
#         self.method = None
#
#     # Делаем подключение к БД
#     def _Connection_DataBase(self):
#         """
#         Здесь делаем наш коннект к нашей базе данных
#         """
#         # Создаем движок
#         self._Create_Engine()
#
#         if self._DATABASE:
#             # Подключаемся к БД
#             self._DATABASE.connect()
#
#     def _Create_Engine(self):
#         """
#         Создаем наш движок для запросов
#         """
#         # Подключение к базе данных через SQLAlchemy
#         # Импортируем ядро
#         from sqlalchemy import create_engine
#
#         # Создаем наш путь до БД
#         # ШАБЛОН - sqlite://username:password@host:port/database
#         sqlite_database_filepath = f"sqlite:///{self.API}"
#
#         # Создаем драйвер движок
#         # Наши настройки
#         # echo - Логирование
#         # pool_size - Количество одновременных коннектов
#         # encoding - Кодировка БД
#         # isolation_level - Уровень изоляции
#
#         self._DATABASE = create_engine(sqlite_database_filepath, echo=False, pool_size=1)
#
#     def _
#
#     # Здесь разделим наши главные методы по которым будем работать
#
#     # ЧТЕНИЕ
#     def Read_Auth_settings(self, Auth_data: [list] = None):
#         """
#         Чтение данных авторизации
#
#         :param Auth_data: - list -  Массив из ID, если None - то удаляется все
#         :return: Код результата - dict - НАШ JSON по протоколу UM-40 SMART
#         """
#         Auth_data_list = set()
#
#         if Auth_data:
#             # Сначала ПЕРЕСОБИРАЕМ словарь
#             for IDx in Auth_data:
#                 # Вытаскиваем значения при этом выравнивая их - ТОБ БЕЗ ПОВТОРЕНИЙ
#                 try:
#                     Auth_data_list.add(int(IDx))
#                 except Exception as e:
#                     error = 'Error ID to request to database for Auth. Id : ' + str(IDx) + ' Exception Error : ' + str(
#                         e) + '\n'
#                     self._LOG(text_log=error, logger_level="ERROR")
#
#         # ТЕПЕРЬ - ОЧЕНЬ ВАЖНО  - УДАЛЯЕМ ВСЕ если у нас нет ничего в списке
#         Auth_data_list = list(Auth_data_list)
#         if len(Auth_data_list) == 0:
#             Auth_data_list = None
#
#         try:
#
#             # ЧИТАЕМ
#             self._Open_DataBase_SQLite()
#             settings_from_database = self._SELECT_DataBase_SQLite(user_settings_list=Auth_data_list)
#
#             # # Делаем команду
#             # command = self._Make_SELECT_command(user_settings_list=Auth_data_list)
#             # settings_from_database = self._READ_DataBase_SQLite(command=command)
#             # Закрываем БД
#             self._Close_DataBase_SQLite()
#
#             # Формируем ответ
#             # response = {self.API_data_tag: settings_from_database}
#
#             response = settings_from_database
#             self.result = 200
#
#         except Exception as e:
#
#             # Логируем ошибку
#             error = 'Error read database for Auth. Exception Error : ' + str(e) + '\n'
#             self._LOG(text_log=error, logger_level="WARNING")
#
#             # Формируем ответ
#             self.result = 500
#             response = 500
#             response = self._HTTP_status_codes(self.result)
#
#         return self.result, response

# -------

# ----------------------------SQLALCHEMY--------------------------------
# Подключение к базе данных через SQLAlchemy
# движок
from sqlalchemy import create_engine
# Сессия к БД
from sqlalchemy.orm import sessionmaker

# -------------------------------- Создание сессии --------------------------------
# Создаем сессию с БД:
# Файл БД
_folder_path = "C:\\Users\\TRIGUN-D\\PycharmProjects\\DOM.RF\\"
# _folder_path = "\\"
_data_base_path = "database.db"
# Путь до нее
# ---------------------- Обработчик ошибки -------------------
# Создаем наш путь до БД
# ШАБЛОН - sqlite://username:password@host:port/database
sqlite_filepath = f"sqlite:///{_folder_path + _data_base_path}"

# ----------------------------------------------------------------------------------

# Создаем драйвер движок
# Наши настройки
# echo - Логирование
# pool_size - Количество одновременных коннектов
# encoding - Кодировка БД
# isolation_level - Уровень изоляции

engine = create_engine(sqlite_filepath, echo=False, pool_size=1)
# Подключаемся к БД
engine.connect()

print(engine, type(engine))

# -------------------------------- Создание Схемы данных --------------------------------
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, ForeignKey
from datetime import datetime

# Декларируем таблицу
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship

# создаем класс, от которого будут наследоваться модели
DeclarativeBase = declarative_base()


class AddressData(DeclarativeBase):
    # Имя таблицы
    __tablename__ = "AddressData"
    # Поля Таблицы
    # Id Записи
    Id = Column("ID", Integer, primary_key=True, index=True)
    # Id Записи Координат
    CoordinatesImmovablesID = Column("CoordinatesImmovablesID", Integer, ForeignKey("CoordinatesImmovables.ID"))
    # Id Записи кадастрового номера
    CadastralID = Column("CadastralID", Integer, ForeignKey("Cadastral.ID"))
    # Id Записи вычислений
    CalculatedID = Column("CalculatedID", Integer, ForeignKey("Calculated.ID"))
    # ////////
    # Проводим связь между другими таблицами:
    # Вычисление
    Calculated = relationship("CalculatedTable", back_populates="AddressData")
    # Координаты объекта
    CoordinateImmovable = relationship("CoordinatesImmovablesTable", back_populates="AddressData_CoordinateImmovable")
    # Кадастровый номер объекта
    Cadastral = relationship("CadastralTable", back_populates="AddressData_Cadastral")

    def __init__(self, Id, CoordinatesImmovablesID, CadastralID, CalculatedID):
        self.Id = Id
        self.CoordinatesImmovablesID = CoordinatesImmovablesID
        self.CadastralID = CadastralID
        self.CalculatedID = CalculatedID


class CalculatedTable(DeclarativeBase):
    # Имя таблицы
    __tablename__ = "Calculated"
    # Поля Таблицы
    # Id Записи вычислений
    Id = Column("ID", Integer, primary_key=True)
    # Запись вычислений
    Calculate = Column("Calculate", String)
    # ////////
    # Проводим связь между другими таблицами:
    AddressData = relationship("AddressData", back_populates="Calculated")

    def __init__(self, Id, Calculate):
        self.Id = Id
        self.Calculate = Calculate

    # def __repr__(self):
    #     return "".format(self.code)


class CoordinatesImmovablesTable(DeclarativeBase):
    # Имя таблицы
    __tablename__ = "CoordinatesImmovables"
    # Поля Таблицы
    # Id Записи Координат
    Id = Column("ID", Integer, primary_key=True)
    # Запись Координат X
    CoordinatX = Column("CoordinatX", String)
    # Запись Координат Y
    CoordinatY = Column("CoordinatY", String)

    # ////////
    # Проводим связь между другими таблицами:
    AddressData_CoordinateImmovable = relationship("AddressData", back_populates="CoordinateImmovable")

    def __init__(self, Id, CoordinatX, CoordinatY):
        self.Id = Id
        self.CoordinatX = CoordinatX
        self.CoordinatY = CoordinatY


class CadastralTable(DeclarativeBase):
    # Имя таблицы
    __tablename__ = "Cadastral"
    # Поля Таблицы
    # Id Записи кадастрового номера
    Id = Column("ID", Integer, primary_key=True)
    # Запись кадастрового номера - AA
    AA = Column("AA", Integer)
    # Запись кадастрового номера - BB
    BB = Column("BB", Integer)
    # Запись кадастрового номера - CCCCCCC
    CCCCCCC = Column("CCCCCCC", Integer)
    # Запись кадастрового номера - КК
    KK = Column("КК", String)
    # ////////
    # Проводим связь между другими таблицами:
    AddressData_Cadastral = relationship("AddressData", back_populates="Cadastral")

    def __init__(self, Id, AA, BB, CCCCCCC, KK):
        self.Id = Id
        self.AA = AA
        self.BB = BB
        self.CCCCCCC = CCCCCCC
        self.KK = KK

    # Создаем сессию

    # autoflush - Разрешение авто сохранения


# Создаем сессию
SessionLocal = sessionmaker(bind=engine, autoflush=False)

print("SessionLocal", SessionLocal)
# session = SessionLocal(autoflush=False, bind=engine)

with SessionLocal(autoflush=False, bind=engine) as db:
    a = db.query(AddressData).all()

    print("Резултат", a)
    for i in a:
        print(i.Calculated.Id)

class DataBase:
    """
    Класс для работы с БД
    """

    # Создаем сессию с БД:
    # Файл БД
    _data_base_path = "database.db"

    # Движок базы данных

    # Сессия БД

    def __init__(self):
        # ----------------------------SQLALCHEMY--------------------------------
        # Подключение к базе данных через SQLAlchemy
        # движок
        from sqlalchemy import create_engine
        # Сессия к БД
        from sqlalchemy.orm import sessionmaker

    def _create_engine(self):
        """
        Создаем наш движок
        :return:
        """

    def _create_session(self):
        """
        Создаем нашу сессию обмена
        :return:
        """

    def SELECT(self):
        """

        :return:
        """
        pass

    def UPDATE(self):
        """

        :return:
        """
        pass

    def INSERT(self):
        """

        :return:
        """
        pass

    def DELETE(self):
        """

        :return:
        """
        pass



