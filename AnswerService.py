# Здесь содержиться заглушка - ответ от внешнего сервиса
import time


def Service(request:dict) -> dict:
    """
    Заглушка отправки запроса к внешнему сервису
    :return:
    """
    from random import randint

    time.sleep(randint(10, 60))

    answer = {"calculated": True}
    return answer
