import random
from itertools import product


class Cell:
    """Класс, представляющий ячейку игрового поля"""

    def __init__(
        self, around_mines: int = 0, mine: bool = False, fl_open: bool = False
    ):
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.fl_open: bool = fl_open

    def __str__(self):
        return (
            f"Cell({self.around_mines}, mine={self.mine}, open={self.fl_open})"
        )

    def __repr__(self):
        return str(self)


class GamePole:
    """Класс, представляющий игровое поле для игры 'Сапёр'"""

    def __init__(self, n: int, m: int = 0):
        self.n: int = n
        self.m: int = m
        self.pole: list[list[Cell]] = [
            [Cell() for _ in range(n)] for _ in range(n)
        ]
        self.init()

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Размер поля (n) должен быть целым числом")
        if value < 0:
            raise ValueError(
                "Размер игрового поля должен быть положительным числом"
            )
        self.__n = value

    @property
    def m(self):
        return self.__m

    @m.setter
    def m(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Размер поля (n) должен быть целым числом")
        if value < 0 or value > self.__n**2:
            raise ValueError(
                f"Кол-во мин должно быть в диапазоне от 0 до {self.__n**2}."
            )
        self.__m = value

    def init(self) -> None:
        """
        Инициализирует игровое поле: расставляет мины и
        обновляет счётчики соседних мин
        """
        mines_positions = self._gen_mine_positions()
        self._setup_mines(mines_positions)
        self._calculate_adjacent_mines()

    def _gen_mine_positions(self) -> list[tuple[int, int]]:
        """Генерирует случайные координаты для размещения мин."""
        return random.sample(
            [(x, y) for x in range(self.n) for y in range(self.n)], self.m
        )

    def _setup_mines(self, mines_positions: list[tuple[int, int]]) -> None:
        """Установка мин на игровое поле"""
        for x, y in mines_positions:
            self.pole[x][y].mine = True

    def _calculate_adjacent_mines(self) -> None:
        """Вычисляет количество мин вокруг каждой ячейки."""
        directions = [
            (x, y)
            for x, y in product((-1, 0, 1), repeat=2)
            if (x, y) != (0, 0)
        ]
        for row, col in product(range(self.n), repeat=2):
            if not self.pole[row][col].mine:
                self.pole[row][col].around_mines = self._count_adjacent_mines(
                    row, col, directions
                )

    def _count_adjacent_mines(
        self, row: int, col: int, directions: list[tuple[int, int]]
    ) -> int:
        """Считает количество мин в соседних ячейках."""
        mine_count = 0
        for dx, dy in directions:
            nx, ny = row + dx, col + dy
            if (
                0 <= nx < self.n
                and 0 <= ny < self.n
                and self.pole[nx][ny].mine
            ):
                mine_count += 1
        return mine_count

    def get_display_board(self) -> str:
        """Возвращает строковое представление игрового поля."""
        lines = []
        for row in self.pole:
            line = []
            for cell in row:
                if cell.fl_open:
                    line.append("*" if cell.mine else str(cell.around_mines))
                else:
                    line.append("#")
            lines.append(" ".join(line))
        return "\n".join(lines)

    def show(self):
        """Отображение игрового поля в консоли"""
        print(self.get_display_board())

    def __str__(self):
        return f"GamePole(size={self.__n**2}; mines={self.__m})"


if __name__ == "__main__":
    pole_game = GamePole(10, 12)
