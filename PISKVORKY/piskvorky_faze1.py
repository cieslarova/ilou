# piskvorky_faze1.py

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
        print("Hra připravena k zahájení (pouze inicializace v této fázi).")

    def start_game(self):
        """
        Metoda pro spuštění hry.
        V této fázi pouze zobrazí inicializovanou prázdnou plochu.
        Herní smyčka a logika tahů budou implementovány v dalších fázích.
        """
        print("Spouštění hry...")
        self.board.display() # Zobrazení prázdné hrací plochy.
        print("Hra byla inicializována a zobrazena prázdná plocha.")
        print("Pro plnou funkčnost je potřeba implementovat herní smyčku a logiku tahů.")


if __name__ == "__main__":
    # Hlavní bod spuštění programu.
    # Vytvoří instanci hry a spustí ji.
    game = Game()
    game.start_game()
