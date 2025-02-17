import itertools
from dataclasses import dataclass


@dataclass
class Data:
    """Пакет данных"""

    data: str
    ip: int


class Server:
    """Сервер"""

    _ip_counter = itertools.count(1)

    def __init__(self):
        self._buffer: list[Data] = []
        self._ip: int = next(self._ip_counter)
        self._router: Router | None = None

    def send_data(self, data: Data) -> None:
        """Отправка пакета данных"""
        if self._router is None:
            raise ConnectionError("Сервер не подключен к сети")
        if not isinstance(data, Data):
            raise TypeError(
                f"Неверный тип данных: ожидался Data, но получен {type(data)}"
            )
        if data.ip == self._ip:
            raise ValueError(
                "Невозможно отправить данные на свой собственный IP"
            )
        self._router.receive_data(data)

    def get_data(self) -> list[Data]:
        """Получение списка полученных данных"""
        data = list(self._buffer)
        self._buffer.clear()
        return data

    def get_ip(self) -> int:
        """Получение ip-адреса"""
        return self._ip

    def set_router(self, router: "Router"):
        """Подсоединение к роутеру"""
        if self._router is not None:
            raise ConnectionError("Сервер уже подключен к роутеру")
        self._router = router

    def unset_router(self):
        """Отсоединение от роутера"""
        if self._router is None:
            raise ConnectionError("Сервер не подключен к роутеру")
        self._router = None

    def receive_data(self, data: Data) -> None:
        """Принять новые данные"""
        if not isinstance(data, Data):
            raise TypeError(
                f"Неверный тип данных: ожидался Data, но получен {type(data)}"
            )
        self._buffer.append(data)

    def __str__(self):
        return f"Server(ip={self._ip}) " + (
            "подключен к сети" if self._router else "не подключен к сети"
        )

    def __repr__(self):
        return str(self)


class Router:
    """Роутер"""

    def __init__(self):
        self._buffer: list[Data] = []
        self._servers: dict[int, Server] = {}

    def link(self, server: Server) -> None:
        """Подсоединение сервера"""
        if server.get_ip() in self._servers:
            raise ConnectionError(
                f"Сервер с IP {server.get_ip()} уже подключен"
            )
        server.set_router(self)
        self._servers[server.get_ip()] = server

    def unlink(self, server: Server) -> None:
        """Отсоединение сервера"""
        if server.get_ip() not in self._servers:
            raise ValueError(
                f"Сервер с IP {server.get_ip()} не найден среди подключенных"
            )
        self._servers.pop(server.get_ip())
        server.unset_router()

    def send_data(self) -> None:
        """Отправка данных серверам"""
        for data in self._buffer:
            if data.ip in self._servers:
                self._servers[data.ip].receive_data(data)
        self._buffer.clear()

    def receive_data(self, data: Data) -> None:
        """Принять новые данные"""
        if data.ip not in self._servers:
            raise ValueError(
                f"Сервер с IP {data.ip} не найден среди подключенных"
            )
        self._buffer.append(data)

    def __str__(self):
        return f"Router - {len(self._servers)} connections"
