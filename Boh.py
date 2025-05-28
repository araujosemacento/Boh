from sys import exit as sys_exit
from subprocess import run
from importlib.util import find_spec
import re


def check_dependencies() -> None:
    module = "blessed"

    if find_spec(module) is None:
        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()

            message = f"Oi, tudo bem?\nEntão, o Boh meio que precisa\ndesse módulo pra te entender\ne ficar bonitinho\n conversando com você:\n\n{module}\n\nQuer que eu instale ele por você?"

            result = messagebox.askyesno("Dependências Faltando", message)

            if result:
                cmd = f"pip install {' '.join(module)}"
                print(f"\033[31mShow de Bola!\033[0m Executando: {cmd}\n")
                run(cmd, shell=True)
                print("\n\033[34mReinicie o script após a instalação, beleza?\033[0m")
            else:
                print(
                    "\n\033[31mInstalação cancelada :(\033[0m\nSe quiser instalar depois, por conta própria,\nexecute:\n\n\033[34mpip install {module}\033[0m\n"
                )

            root.destroy()
            sys_exit()

        except ImportError:
            print(f"Módulos faltando: {', '.join(module)}")
            print(f"Execute: pip install {' '.join(module)}")
            sys_exit()


check_dependencies()

from time import sleep
from blessed import Terminal

term = Terminal()


def parse_formatted_text(text):
    # Padrão para encontrar códigos ANSI (somente cores e formatação tipográfica)
    ansi_pattern = r"\033\[[0-9;]*m"

    result = []
    current_format = ""
    i = 0

    while i < len(text):
        # Verifica se encontrou um código ANSI
        ansi_match = re.match(ansi_pattern, text[i:])
        if ansi_match:
            ansi_code = ansi_match.group()
            if ansi_code == "\033[0m":
                current_format = ""
            else:
                current_format += ansi_code
            i += len(ansi_code)
        else:
            # Adiciona o caractere com sua formatação atual
            char = text[i]
            if char != " " or current_format:  # Preserva espaços formatados
                formatted_char = (
                    current_format + char + ("\033[0m" if current_format else "")
                )
                result.append(formatted_char)
            else:
                result.append(char)
            i += 1

    return result


def talk(input=" ", expression="idle", amount=1.0, static=""):
    if input == " ":
        remaining = list(input)
        displayed = []
    else:
        parsed_chars = parse_formatted_text(input)
        remaining = parsed_chars.copy()
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

    print("\033[1;1H\033[0J", end="")

    while remaining:
        sleep(0.03)
        displayed.append(remaining.pop(0))

        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        print("\033[1;1H\033[0J", end="")

        displayed_text = "".join(displayed) if input != " " else static

        print(
            f"{current_expr}  ──┤ {displayed_text} │  ",
            end="",
            flush=True,
        )
        print(f"{static if input != " " else ""}", end="", flush=True)

    sleep(amount)


def main():
    list_model = "\n\n\n\n                        None × ↽[H]⇀ ↽[]⇀ ↽[]⇀ ... ↽[]⇀ ↽[]⇀ ↽[T]⇀ × None"
    ask_template = f"\n\n\n\n                    [{term.green}S{term.normal}im]     [{term.red}N{term.normal}ão]"
    affirmative = ["s", "y"]
    negative = ["n"]

    with term.fullscreen(), term.cbreak():
        talk("Oi, tudo bem?")
        talk("Muito obrigado por executar o meu script")
        talk(f"Eu me chamo {term.green}{term.bold}BOH!")
        talk("He He", amount=0.75)
        talk("Sabe...", amount=0.75)
        talk("Tipo,")
        talk(static=f"Tipo, {term.bold}ROH{term.normal}")
        talk(
            static=f"Tipo, {term.bold}ROH-{term.normal}{term.bold}{term.green}BOH{term.normal}"
        )

        for i in range(10):
            talk(static=f"{"HahA" * i}", expression="open mouth", amount=0.05)

        sleep(1)
        talk("Ai ai, sou meio comédia às vezes, sabe?")
        talk("Mas, enfim,")
        talk("E você, como se chama?", amount=0.5)

        print(
            term.move_yx(term.height - 3, 0) + "Digite seu nome aqui: ",
            end="",
            flush=True,
        )
        sike = []
        while len(sike) < 4:
            key_input = term.inkey(timeout=None)
            if not key_input.is_sequence and key_input.isalnum():
                sike.append(key_input)
                print(sike[-1], end="", flush=True)

        talk(
            "Olha olha olha, na verdade, eu não tenho muito tempo...", "pokerface", 1.5
        )
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
            talk(static=f"Hmmm{"." * (i + 1)}", expression="thinking")

        talk("Já sei!", expression="open mouth")
        talk("Aqui, toma", static=ask_template, amount=1.5)

        while True:
            talk("Agora sempre que eu te perguntar algo,", static=ask_template)
            talk("Você pode responder digitando", static=ask_template)
            talk("A letra destacada que achar mais cabível.", static=ask_template)
            talk("Entendeu, né?", static=ask_template)

            key = term.inkey(timeout=5)
            if key.lower() in affirmative:
                if key.lower() == "y":
                    talk(
                        "Sim, inglês também tá valendo...",
                        "pokerface",
                        static=ask_template,
                    )
                    break
                talk("Show de bola!", "open mouth", static=ask_template)
                break
            elif key.lower() in negative:
                talk("Não?", "pokerface", static=ask_template)
                talk("Pera, deixa eu repetir", static=ask_template)
            elif key.is_sequence:
                continue
            elif not key:
                talk(
                    "Poxa, tá difícil assim de encontrar a tecla?",
                    expression="thinking",
                    amount=1.5,
                )
            else:
                talk(
                    "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                    "annoyed",
                    static=ask_template,
                )

        talk("Enfim, voltando ao assunto...", expression="idle")
        talk("Reconhece isso aqui, né?")
        talk(static="Reconhece isso aqui, né?", expression="looking down")
        print(list_model, flush=True)
        print(ask_template, flush=True)
        while True:
            key = term.inkey(timeout=None)
            if key.lower() in affirmative:
                talk(
                    "Pois é, uma lista.",
                    static=list_model,
                )
                break
            elif key.lower() in negative:
                talk("Não?", "open mouth", static=list_model)
                talk(
                    "Como assim pô? Me esforcei tanto desenhar ela...",
                    expression="pokerface",
                    static=list_model,
                )
                talk("É uma lista! A estrutura de dados!", static=list_model)
                talk("Tá vendo?", static=f"{list_model}{ask_template}")
            elif key.is_sequence:
                continue
            elif not key:
                talk(
                    "Poxa, tá difícil assim de encontrar a tecla?",
                    expression="thinking",
                    amount=1.5,
                    static=f"{list_model}{ask_template}",
                )
            else:
                talk(
                    "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                    "annoyed",
                    static=f"{list_model}{ask_template}",
                )
        talk(
            "Bom, como você já sabe... a lista é uma estrutura de dados",
            static=list_model,
        )
        talk(
            "Mas tô aqui pra discutir um desafio específico relacionado a ela...",
            static=list_model,
        )
        talk("O desafio é o seguinte:", expression="thinking", static=list_model)
        talk("Que tal inverter uma lista?", expression="open mouth", static=list_model)
        talk(
            "Ou melhor, qual seria a maneira mais eficiente de fazer isso?",
            static=list_model,
        )

        if term.inkey(timeout=None):
            return


if __name__ == "__main__":
    main()
