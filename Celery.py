# Здесь мы работаем с нашим запросом с удаленным сервером




from celery import Celery
# топик откуда берем сообщения
task_topic = "CadastralCalculate"
# Брокер откуда берем - Сделаем составным
# Имя брокера
redis_broker = "redis"
# URL
redis_url = "localhost"
# Порт
redis_port = "6379"
# Формируем имя самого брокера
broker = redis_broker + "://" + redis_url + ":" + redis_port


# Инициализируем воркер
AppCelery = Celery(main=task_topic, broker=broker)


# Инициализируем его

@AppCelery.tasks
def request_Calculate():
    """
    Функция, которая запрашивает наш необходимый нам функционал
    :return:
    """
    from AnswerService import Service

    # Делаем наш вызов

    pass

