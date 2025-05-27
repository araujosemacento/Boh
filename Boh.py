from time import sleep
from sys import stdout
from keyboard import read_key  # pip install keyboard
from re import sub, match
from colorama import init, Fore, Back, Style
import os

# Initialize colorama for cross-platform ANSI support
init(autoreset=False)  # Don't auto-reset so we can handle it manually


def main():
    list_model = "\n\n\n\n                        None × ↽[H]⇀ ↽[]⇀ ↽[]⇀ ... ↽[]⇀ ↽[]⇀ ↽[T]⇀ × None"
    ask_template = f"\n\n\n\n                    [{colors.fg.green}S{colors.reset}im]     [{colors.fg.red}N{colors.reset}ão]"
    response = False
    affirmative = ["S", "s", "y", "Y"]
    negative = ["N", "n"]

    # Enable ANSI support on Windows if needed
    if os.name == "nt":
        os.system("")  # Enable ANSI escape sequences on Windows 10+

    talk("Oi, tudo bem?")
    talk("Muito obrigado por executar o meu script")
    talk(f"Eu me chamo {colors.fg.green}{colors.bold}BOH{colors.reset}!")
    talk("He He", amount=0.75)
    talk("Sabe...", amount=0.75)
    talk("Tipo,")
    talk(static=f"Tipo, {colors.bold}ROH{colors.reset}")
    talk(
        static=f"Tipo, {colors.bold}ROH-{colors.reset}{colors.bold}{colors.fg.green}BOH{colors.reset}"
    )
    for i in range(10):
        talk(static=f"{"HahA" * i}", expression="open mouth", amount=0.05)
    sleep(1)
    talk("Ai ai, sou meio comédia às vezes, sabe?")
    talk("Mas, enfim,")
    talk("E você, como se chama?", amount=0.5)
    print("\n\nDigite seu nome aqui: ", end="")
    sike = []
    while len(sike) < 4:
        press = str(
            read_key(
                suppress=True
            )  # Pega a tecla pressionada, mas não exibe no terminal
        ).strip()  # Pega a tecla pressionada e remove espaços extras
        if press.isalnum() and len(press) == 1:
            sike.append(press)
            print(sike[-1], end="", flush=True)
            sleep(0.1)  # Delay pra não ficar muito rápido
    talk("Olha olha olha, na verdade, eu não tenho muito tempo...", "pokerface", 1.5)
    talk("Me desculpa! Você parece ser uma pessoa muito legal, mas...")
    talk("A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓", amount=0.2)
    talk(
        expression="looking down",
        static="A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓",
        amount=0.2,
    )
    print(list_model, flush=True)
    sleep(2)
    talk("Reconhece?", static=list_model, amount=1.5)
    talk("Ih, verdade, cê não consegue me responder, né?", static=list_model)
    talk("Hmmm", expression="thinking")
    for i in range(3):
        talk(
            static=f"Hmmm{"." * (i + 1)}",
            expression="thinking",
        )
    talk("Já sei!", expression="open mouth")
    talk("Aqui, toma", static=ask_template, amount=1.5)
    while not response:
        talk("Agora sempre que eu te perguntar algo,", static=ask_template)
        talk(
            "Você pode responder digitando",
            static=ask_template,
        )
        talk("A letra destacada que achar mais cabível.", static=ask_template)
        talk("Entendeu, né?", static=ask_template)
        key = str(read_key(suppress=True)).strip()
        if key in affirmative:
            response = True
            (
                talk(
                    "Sim, inglês também tá valendo...", "pokerface", static=ask_template
                )
                if key in affirmative[2:]
                else talk("Show de bola!", "open mouth", static=ask_template)
            )
        elif key in negative:
            response = False
            talk("Não?", "pokerface", static=ask_template)
            talk("Pera, deixa eu repetir", static=ask_template)
        elif not key.isalnum() or len(key) != 1:
            continue
        else:
            response = False
            talk(
                "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                "annoyed",
                static=ask_template,
            )

    print("\n\nPressione qualquer tecla para continuar...", end="")
    if read_key(suppress=True):
        exit()


def talk(input=" ", expression="idle", amount=1.0, static=""):
    ansi_pattern = r"\033\[[0-9;]*m"

    # Extrair texto limpo (sem códigos ANSI)
    clean_text = sub(ansi_pattern, "", input)

    # Dicionário preenchido com todas as posições de efeitos no texto original
    effect_positions = {}

    # Processar o texto original pra mapear efeitos às posições
    clean_pos = 0
    active_effects = []
    i = 0

    while i < len(input):
        # Verificar se esbarramos em um código ANSI
        ansi_match = match(ansi_pattern, input[i:])
        if ansi_match:
            ansi_code = ansi_match.group()
            if ansi_code == colors.reset:
                active_effects.clear()
            else:
                active_effects.append(ansi_code)
            i += len(ansi_code)
        else:
            # Caractere normal - mapear TODOS os efeitos ativos
            if active_effects:
                effect_positions[clean_pos] = "".join(active_effects)
            clean_pos += 1
            i += 1

    # Converter o texto de uma string literal pra lista de caracteres para animação
    remaining = list(clean_text)
    displayed = []

    expressions = {
        "idle": [
            "[ ▀ ¸ ▀]",
            "[ ▀ ° ▀]",
            "[ ▀ ■ ▀]",
            "[ ▀ ─ ▀]",
            "[ ▀ ~ ▀]",
            "[ ▀ ▄ ▀]",
            "[ ▀ ¬ ▀]",
            "[ ▀ · ▀]",
            "[ ▀ _ ▀]",
        ],
        "pokerface": ["[ ▀ ‗ ▀]", "[ ▀ ¯ ▀]", "[ ▀ ¡ ▀]"],
        "thinking": ["[ ─ ´ ─]", "[ ─ » ─]"],
        "open mouth": ["[ ▀ ß ▀]", "[ ▀ █ ▀]"],
        "annoyed": ["[ ▀ ı ▀]", "[ ▀ ^ ▀]"],
        "looking down": ["[ ▄ . ▄]", "[ ▄ _ ▄]", "[ ▄ ₒ ▄]", "[ ▄ ‗ ▄]"],
    }

    # Keep using ANSI for screen clearing - it's fast and works with colorama
    stdout.write("\033[1;1H\033[0J")

    # Animar o texto letra a letra
    while remaining:
        sleep(0.03)

        # Adicionar próximo caractere pra mostrar
        displayed.append(remaining.pop(0))

        # Construir string com efeitos aplicados
        output_text = ""
        for i, char in enumerate(displayed):
            if i in effect_positions:
                output_text += f"{effect_positions[i]}{char}{colors.reset}"
            else:
                output_text += char

        # Obter expressão atual
        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        # Keep using ANSI for cursor positioning and clearing
        stdout.write("\033[1;1H\033[0J")

        stdout.write(
            f"{current_expr}  ──┤ {output_text if input != " " else static} │  "
        )
        stdout.write(f"{static if input != " " else ""}")
        stdout.flush()

    sleep(amount)


# Refactored colors class to use colorama constants
class colors:
    # Reset using colorama
    reset = Style.RESET_ALL

    # Text styles using colorama
    bold = Style.BRIGHT
    faint = Style.DIM
    # Note: colorama doesn't have italic, underline, etc. - keeping ANSI for these
    italic = "\033[03m"
    underline = "\033[04m"
    reverse = "\033[07m"
    invisible = "\033[08m"
    strikethrough = "\033[09m"

    class fg:  # Foreground colors using colorama
        black = Fore.BLACK
        red = Fore.RED
        green = Fore.GREEN
        yellow = Fore.YELLOW
        blue = Fore.BLUE
        magenta = Fore.MAGENTA
        cyan = Fore.CYAN
        white = Fore.WHITE
        default = Fore.RESET
        # Bright colors
        brightblack = Fore.LIGHTBLACK_EX
        brightred = Fore.LIGHTRED_EX
        brightgreen = Fore.LIGHTGREEN_EX
        brightyellow = Fore.LIGHTYELLOW_EX
        brightblue = Fore.LIGHTBLUE_EX
        brightmagenta = Fore.LIGHTMAGENTA_EX
        brightcyan = Fore.LIGHTCYAN_EX
        brightwhite = Fore.LIGHTWHITE_EX

    class bg:  # Background colors using colorama
        black = Back.BLACK
        red = Back.RED
        green = Back.GREEN
        yellow = Back.YELLOW
        blue = Back.BLUE
        magenta = Back.MAGENTA
        cyan = Back.CYAN
        white = Back.WHITE
        default = Back.RESET
        # Bright backgrounds
        brightblack = Back.LIGHTBLACK_EX
        brightred = Back.LIGHTRED_EX
        brightgreen = Back.LIGHTGREEN_EX
        brightyellow = Back.LIGHTYELLOW_EX
        brightblue = Back.LIGHTBLUE_EX
        brightmagenta = Back.LIGHTMAGENTA_EX
        brightcyan = Back.LIGHTCYAN_EX
        brightwhite = Back.LIGHTWHITE_EX


if __name__ == "__main__":
    main()
