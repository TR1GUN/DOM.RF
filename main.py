# Написать API-сервис (FastAPI, Flask) со следующими методами:
#
# - Принять запрос. На вход передавать кадастровой номер (подробнее:
# https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%B4%D0%B0%D1%81%D1%82%D1%80%D0%BE%D
# 0%B2%D1%8B%D0%B9_%D0%BD%D0%BE%D0%BC%D0%B5%D1%80) и координаты (широта, долгота)
# {"Кадастровый номер" :"", "Координаты":{"Широта":"" , "Долгота":""}}

# - Менять номер запроса в очереди запроса

# - Отдать результат запроса по ID
#
# - Сервис должен отправлять запрос внешнему сервису на расчет (саму отправку реализовывать не
# требуется, но нужно понимать, что внешний сервис может выполнять расчет 10-60 секунд). В
# качестве ответа от сервиса можно взять параметры запроса с параметром calculated: true, к
# примеру.
# - Сервис должен быть запакован в Dockerfile


#
# import pika
#
# # Устанавливаем параметры соедененния
# rmq_url_connection_str = "localhost:4369"
# rmq_parameters = pika.URLParameters(rmq_url_connection_str)
# # Создаем соединение
# rmq_connection = pika.BlockingConnection(rmq_parameters)
# # Создаем канал
# rmq_channel = rmq_connection.channel()
#
# # --->
# # Делаем нашу публикацию в нужном топике
# exchange = "Cadastral"
# routing = "request"
# text = "{\"GOVNO\":1}"
#
#
# # exchange - Топик
# # routing_key - Маршрут
# # body - Само наше сообщение
# rmq_channel.basic_publish(exchange = exchange, routing_key = routing, body = text)

