from tkinter import *  # type: ignore # Esse comentário evita um aviso de linting no VSCODE, só isso.
from colorama import init, Fore, Back, Style


class Boh:

    def __init__(self) -> None:
        # Inicializa a janela principal
        self.root = Tk()
        self.setup_window()

        # Controle de estado, pra manipular interações
        self.current_text = ""
        self.waiting_for_key = False

    def setup_window(
        self,
    ) -> None:  # Definição de atributos da janela durante a inicialização.
        self.root.title("Boh v0.2")
        self.root.geometry(
            "0x0"
        )  # Quero que a janela seja imperceptível antes de alterar seu tamanho.
        self.root.resizable(True, True)  # Permite redimensionamento da janela.
        self.root.configure(bg="black")  # Define a cor de fundo da janela.

        self.root.update_idletasks()  # Atualiza a janela para aplicar as configurações.
        size = self.root.winfo_screenheight() // 2
        x = (self.root.winfo_screenwidth() // 2) - (size // 2)
        y = size // 2

    def run(self) -> None:
        # Inicia o loop principal da interface gráfica
        self.root.mainloop()


class colors:
    # Remove estilizações aplicadas anteriormente
    reset = Style.RESET_ALL

    # Estilizações de tipo
    bold = Style.BRIGHT
    faint = Style.DIM
    # O Colorama não suporta os seguintes estilos - Deixando aqui pra caso de necessidade futura
    italic = "\033[03m"
    underline = "\033[04m"
    reverse = "\033[07m"
    invisible = "\033[08m"
    strikethrough = "\033[09m"

    class fg:  # Estilizações referentes às cores do texto
        black = Fore.BLACK
        red = Fore.RED
        green = Fore.GREEN
        yellow = Fore.YELLOW
        blue = Fore.BLUE
        magenta = Fore.MAGENTA
        cyan = Fore.CYAN
        white = Fore.WHITE
        default = Fore.RESET
        # Cores mais claras
        brightblack = Fore.LIGHTBLACK_EX
        brightred = Fore.LIGHTRED_EX
        brightgreen = Fore.LIGHTGREEN_EX
        brightyellow = Fore.LIGHTYELLOW_EX
        brightblue = Fore.LIGHTBLUE_EX
        brightmagenta = Fore.LIGHTMAGENTA_EX
        brightcyan = Fore.LIGHTCYAN_EX
        brightwhite = Fore.LIGHTWHITE_EX

    class bg:  # Ficou óbvio que essas são as cores de fundo a esse ponto
        black = Back.BLACK
        red = Back.RED
        green = Back.GREEN
        yellow = Back.YELLOW
        blue = Back.BLUE
        magenta = Back.MAGENTA
        cyan = Back.CYAN
        white = Back.WHITE
        default = Back.RESET
        # Cores de fundo mais claras
        brightblack = Back.LIGHTBLACK_EX
        brightred = Back.LIGHTRED_EX
        brightgreen = Back.LIGHTGREEN_EX
        brightyellow = Back.LIGHTYELLOW_EX
        brightblue = Back.LIGHTBLUE_EX
        brightmagenta = Back.LIGHTMAGENTA_EX
        brightcyan = Back.LIGHTCYAN_EX
        brightwhite = Back.LIGHTWHITE_EX


def main():
    boh = Boh()  # Cria uma instância da classe Boh
    boh.run()  # Inicia o loop principal da interface gráfica


if __name__ == "__main__":
    init(
        autoreset=False
    )  # Inicializa o colorama para usar cores no terminal, sem reset automático
    main()  # Chama a função principal para iniciar o programa
