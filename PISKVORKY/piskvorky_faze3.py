# piskvorky_faze3.py

class Player:
    """
    Reprezentuje hráče ve hře Piškvorky.
    Každý hráč má jméno a symbol (X nebo O).
    """
    def __init__(self, name: str, symbol: str):
        """
        Inicializuje nového hráče.

        Args:
            name (str): Jméno hráče.
            symbol (str): Symbol hráče na hrací ploše (např. 'X', 'O').
        """
        self.name = name
        self.symbol = symbol

    def __str__(self):
        """
        Vrací řetězcovou reprezentaci hráče.
        """
        return f"Hráč: {self.name}, Symbol: {self.symbol}"


class Board:
    """
    Reprezentuje hrací plochu pro Piškvorky.
    Plocha je mřížka 3x3.
    """
    def __init__(self):
        """
        Inicializuje prázdnou hrací plochu 3x3.
        Plocha je reprezentována jako seznam seznamů, kde každé políčko
        je na začátku prázdné (reprezentováno mezerou).
        """
        # Vytvoření 3x3 mřížky s prázdnými políčky.
        # Každý vnitřní seznam reprezentuje jeden řádek.
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]

    def display(self):
        """
        Vypíše aktuální stav hrací plochy do konzole.
        Zobrazuje mřížku s oddělovači pro lepší čitelnost.
        """
        print("\n--- AKTUÁLNÍ STAV HRACÍ PLOCHY ---")
        for i, row in enumerate(self.grid):
            # Vypíše symboly v řádku oddělené svislou čarou.
            print(f" {row[0]} | {row[1]} | {row[2]}")
            # Pokud to není poslední řádek, vypíše vodorovný oddělovač.
            if i < 2:
                print("---+---+---")
        print("----------------------------------\n")

    def make_move(self, row: int, col: int, symbol: str) -> bool:
        """
        Pokusí se umístit symbol na zadané souřadnice.

        Args:
            row (int): Index řádku (0-2).
            col (int): Index sloupce (0-2).
            symbol (str): Symbol hráče ('X' nebo 'O').

        Returns:
            bool: True, pokud byl tah platný a proveden, False jinak.
        """
        # Kontrola, zda jsou souřadnice v platném rozsahu.
        if not (0 <= row < 3 and 0 <= col < 3):
            print("Chyba: Souřadnice mimo rozsah (0-2 pro řádek i sloupec).")
            return False
        # Kontrola, zda je políčko již obsazené.
        if self.grid[row][col] != ' ':
            print("Chyba: Toto políčko je již obsazené. Zvolte jiné.")
            return False

        # Pokud jsou souřadnice platné a políčko prázdné, umístí symbol.
        self.grid[row][col] = symbol
        return True

    def check_win(self, symbol: str) -> bool:
        """
        Kontroluje, zda daný symbol vyhrál hru.

        Args:
            symbol (str): Symbol hráče ('X' nebo 'O'), jehož vítězství se kontroluje.

        Returns:
            bool: True, pokud symbol vyhrál, False jinak.
        """
        # Kontrola řádků
        for row in self.grid:
            if all(s == symbol for s in row):
                return True

        # Kontrola sloupců
        for col_idx in range(3):
            if all(self.grid[row_idx][col_idx] == symbol for row_idx in range(3)):
                return True

        # Kontrola hlavní diagonály (zleva nahoře doprava dolů)
        if all(self.grid[i][i] == symbol for i in range(3)):
            return True

        # Kontrola vedlejší diagonály (zprava nahoře doleva dolů)
        if all(self.grid[i][2 - i] == symbol for i in range(3)):
            return True

        return False

    def is_full(self) -> bool:
        """
        Kontroluje, zda je hrací plocha plná (pro detekci remízy).

        Returns:
            bool: True, pokud je plocha plná, False jinak.
        """
        # Prochází všechna políčka na mřížce.
        # Pokud najde alespoň jedno prázdné políčko (' '), plocha není plná.
        for row in self.grid:
            if ' ' in row:
                return False
        return True


class Game:
    """
    Hlavní třída pro řízení hry Piškvorky.
    Orchestruje hráče, hrací plochu a herní smyčku.
    """
    def __init__(self):
        """
        Inicializuje novou hru Piškvorky.
        Vytvoří hrací plochu a hráče.
        """
        print("Inicializace hry Piškvorky...")
        self.board = Board()  # Vytvoření instance hrací plochy.
        # Vytvoření dvou hráčů s předdefinovanými symboly.
        self.player1 = Player("Hráč 1", "X")
        self.player2 = Player("Hráč 2", "O")
        self.current_player = self.player1  # Nastavení prvního hráče.
        print(f"{self.player1.name} hraje s '{self.player1.symbol}'")
        print(f"{self.player2.name} hraje s '{self.player2.symbol}'")
        self.game_over = False # Příznak pro ukončení hry.
        self.moves_count = 0 # Počítadlo provedených tahů pro detekci remízy.

    def switch_player(self):
        """
        Přepne aktuálního hráče na druhého hráče.
        """
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def get_player_move(self) -> tuple[int, int]:
        """
        Získá od aktuálního hráče vstup pro tah (řádek a sloupec).
        Ošetřuje nečíselné vstupy.

        Returns:
            tuple[int, int]: Dvojice (řádek, sloupec) zadaná hráčem.
        """
        while True:
            try:
                # Vyzve hráče k zadání řádku a sloupce.
                row = int(input(f"{self.current_player.name} ({self.current_player.symbol}), zadejte řádek (0-2): "))
                col = int(input(f"{self.current_player.name} ({self.current_player.symbol}), zadejte sloupec (0-2): "))
                return row, col
            except ValueError:
                # Chyba při zadání nečíselného vstupu.
                print("Neplatný vstup. Zadejte prosím číslo pro řádek i sloupec.")

    def run(self):
        """
        Spustí hlavní herní smyčku.
        Hra pokračuje, dokud není ukončena (vítěz nebo remíza).
        """
        print("\n--- HRA PIŠKVORKY ZAHÁJENA ---")
        self.board.display() # Zobrazí počáteční prázdnou plochu.

        while not self.game_over:
            print(f"Na tahu je {self.current_player.name} ({self.current_player.symbol}).")
            row, col = self.get_player_move() # Získá tah od hráče.

            # Pokusí se provést tah.
            if self.board.make_move(row, col, self.current_player.symbol):
                self.moves_count += 1 # Zvýší počet provedených tahů.
                self.board.display() # Zobrazí aktualizovanou plochu.

                # Kontrola vítěze po každém platném tahu.
                if self.board.check_win(self.current_player.symbol):
                    print(f"Gratulujeme! {self.current_player.name} ({self.current_player.symbol}) vyhrál hru!")
                    self.game_over = True
                # Kontrola remízy, pokud není vítěz a plocha je plná.
                elif self.board.is_full():
                    print("Hrací plocha je plná. Hra skončila remízou!")
                    self.game_over = True
                else:
                    # Pokud hra neskončila, přepne hráče.
                    self.switch_player()
            # Pokud tah nebyl platný (např. obsazené políčko), hráč je vyzván k opakování tahu
            # a hráč se nepřepíná.

        print("\n--- HRA UKONČENA ---")


if __name__ == "__main__":
    # Hlavní bod spuštění programu.
    game = Game()
    game.run()
