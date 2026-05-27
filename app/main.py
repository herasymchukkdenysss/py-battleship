class InvalidFireMove(Exception):
    pass


class NotExistingDeckError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self._row = row
        self._column = column
        self.is_alive = is_alive

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        if hasattr(self, "_is_alive") and value:
            raise ValueError("Cannot set is_alive to true state")
        if hasattr(self, "_is_alive") and not self._is_alive:
            raise InvalidFireMove("A deck is already fired")
        self._is_alive = value


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        try:
            if start[0] == end[0]:  # horizontal ship
                self._decks = [
                    Deck(start[0], column)
                    for column in range(start[1], end[1] + 1)
                ]
            elif start[1] == end[1]:  # vertical ship
                self._decks = [
                    Deck(row, start[1])
                    for row in range(start[0], end[0] + 1)
                ]
            else:
                raise ValueError("Invalid ship was provided")
            self._is_drowned = is_drowned
        except IndexError as exc:
            raise ValueError("Invalid ship coordinates was provided") from exc

    @property
    def decks(self) -> list:
        return self._decks

    @property
    def is_drowned(self) -> bool:
        return self._is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        raise NotExistingDeckError(
            f"Deck with row={row}, column={column} was not found"
        )

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        self._is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list) -> None:
        self._field = {}
        for start, end in ships:
            ship = Ship(start, end)

            for deck in ship.decks:
                self._field[deck.row, deck.column] = ship

    @property
    def field(self) -> dict:
        return self._field

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)

        if not ship:
            return "Miss!"

        row, column = location
        try:
            ship.fire(row, column)
        except InvalidFireMove:
            return "Already hit deck!"

        return "Sunk!" if ship.is_drowned else "Hit!"
