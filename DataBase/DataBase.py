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
    _data_base_path = "database.db"
    # Путь до нее
    # ---------------------- Обработчик ошибки -------------------
    # Создаем наш путь до БД
    # ШАБЛОН - sqlite://username:password@host:port/database
    sqlite_filepath = f"sqlite:///{_data_base_path}"

    # Создаем драйвер движок
    # Наши настройки
    # echo - Логирование
    # pool_size - Количество одновременных коннектов
    # encoding - Кодировка БД
    # isolation_level - Уровень изоляции

    engine = create_engine(sqlite_filepath, echo=False, pool_size=1)
    # Подключаемся к БД
    engine.connect()

    print(engine)
    # -------------------------------- Создание Схемы данных --------------------------------
    from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
    from datetime import datetime

    # Декларируем таблицу
    from sqlalchemy.ext.declarative import declarative_base

    # # создаем класс, от которого будут наследоваться модели
    DeclarativeAuthBase = declarative_base()

    class AddressData(DeclarativeAuthBase):
        # Имя таблицы
        __tablename__ = "AddressData"
        # Поля Таблицы
        Id = Column("ID", Integer, primary_key=True)
        CoordinatesImmovablesID = Column("CoordinatesImmovablesID", Integer)
        CadastralID = Column("CadastralID", Integer)
        CalculatedID = Column("CalculatedID", Integer)

        def __init__(self, Id, CoordinatesImmovablesID, CadastralID, CalculatedID):
            self.Id = Id
            self.CoordinatesImmovablesID = CoordinatesImmovablesID
            self.CadastralID = CadastralID
            self.CalculatedID = CalculatedID

        # def __repr__(self):
        #     return "".format(self.code)


    class Calculated(DeclarativeAuthBase):
        # Имя таблицы
        __tablename__ = "Calculated"
        # Поля Таблицы
        Id = Column("ID", Integer, primary_key=True)
        Calculated = Column("Calculated", String)

        def __init__(self, Id, Calculated):
            self.Id = Id
            self.Calculated = Calculated

        # def __repr__(self):
        #     return "".format(self.code)

    class CoordinatesImmovables(DeclarativeAuthBase):
        # Имя таблицы
        __tablename__ = "CoordinatesImmovables"
        # Поля Таблицы
        Id = Column("ID", Integer, primary_key=True)
        CoordinatX = Column("CoordinatX", )
        CoordinatY = Column("CoordinatY", String)

        def __init__(self, Id, CoordinatX ,CoordinatY ):
            self.Id = Id
            self.CoordinatX = CoordinatX
            self.CoordinatY = CoordinatY


    class Cadastral(DeclarativeAuthBase):
        # Имя таблицы
        __tablename__ = "Cadastral"
        # Поля Таблицы
        Id = Column("ID", Integer, primary_key=True)
        AA = Column("AA", Integer)
        BB = Column("BB", Integer)
        CCCCCCC = Column("CCCCCCC",Integer)
        KK = Column("КК", String)

        def __init__(self, Id, AA ,BB, CCCCCCC ,KK ):
            self.Id = Id
            self.AA = AA
            self.BB = BB
            self.CCCCCCC = CCCCCCC
            self.KK = KK
    # -----------------------------------------------------------------------------------------
    # Создаем сессию

    # autoflush - Разрешение авто сохранения

    # Создаем сессию
    SessionLocal = sessionmaker(bind=engine, autoflush=False)
    session = SessionLocal()

    # session_db.connection()

    # lol = HTTPAuth()
    # s = session_db.get()
    # print(s)

    # lol = session.get(HTTPAuth)
    #
    # print(lol)

    results = session.query(HTTPAuth).all()

    for i in results:
        print(i.Login)


