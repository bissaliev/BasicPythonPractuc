class ObjList:
    """Класс элемента двусвязного списка"""

    def __init__(self, data: str):
        self.__next: ObjList | None = None
        self.__prev: ObjList | None = None
        self.__data: str = data

    @property
    def next(self) -> "ObjList" | None:
        """Возвращает следующий объект списка"""
        return self.__next

    @next.setter
    def next(self, obj: "ObjList" | None) -> None:
        """Устанавливает ссылку на следующий объект списка"""
        self.__next = obj

    @property
    def prev(self) -> "ObjList" | None:
        """Возвращает предыдущий объект списка"""
        return self.__prev

    @prev.setter
    def prev(self, obj: "ObjList" | None) -> None:
        """Устанавливает ссылку на предыдущий объект списка"""
        self.__prev = obj

    @property
    def data(self) -> str:
        """Возвращает данные, хранящиеся в узле"""
        return self.__data

    @data.setter
    def data(self, value: str) -> None:
        """Устанавливает данные в узел"""
        self.__data = value


class LinkedList:
    """Двусвязный список"""

    def __init__(self):
        self.head: ObjList | None = None
        self.tail: ObjList | None = None

    def add_obj(self, obj: ObjList) -> None:
        """Добавление нового объекта в конец списка"""
        if self.tail:
            self.tail.next = obj
            obj.prev = self.tail
            self.tail = self.tail.next
        else:
            self.head = self.tail = obj

    def remove_obj(self) -> None:
        """Удаление последнего объекта"""
        if self.tail is None:
            return
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

    def get_data(self) -> list[str]:
        """Получение списка объектов"""
        lst = []
        current = self.head
        while current:
            lst.append(current.data)
            current = current.next
        return lst
