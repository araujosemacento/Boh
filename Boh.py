from sys import exit as sys_exit
from subprocess import run
from importlib.util import find_spec


def check_dependencies():
    required_modules = ["blessed", "keyboard"]
    missing_modules = []

    for module in required_modules:
        if find_spec(module) is None:
            missing_modules.append(module)

    if missing_modules:
        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()

            message = f"Os seguintes módulos não estão instalados:\n{', '.join(missing_modules)}\n\nDeseja instalá-los automaticamente?"

            result = messagebox.askyesno("Dependências Faltando", message)

            if result:
                cmd = f"pip install {' '.join(missing_modules)}"
                print(f"Executando: {cmd}")
                run(cmd, shell=True)
                print("Reinicie o script após a instalação.")
            else:
                print("Instalação cancelada.")

            root.destroy()
            sys_exit()

        except ImportError:
            print(f"Módulos faltando: {', '.join(missing_modules)}")
            print(f"Execute: pip install {' '.join(missing_modules)}")
            sys_exit()


check_dependencies()

from time import sleep
from blessed import Terminal
from keyboard import read_key
from re import sub, match

term = Terminal()


def main():
    list_model = "\n\n\n\n                        None × ↽[H]⇀ ↽[]⇀ ↽[]⇀ ... ↽[]⇀ ↽[]⇀ ↽[T]⇀ × None"
    ask_template = f"\n\n\n\n                    [{term.green}S{term.normal}im]     [{term.red}N{term.normal}ão]"
    response = False
    affirmative = ["S", "s", "y", "Y"]
    negative = ["N", "n"]

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
            press = str(read_key(suppress=True)).strip()
            if press.isalnum() and len(press) == 1:
                sike.append(press)
                print(sike[-1], end="", flush=True)
                sleep(0.1)

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

        while not response:
            talk("Agora sempre que eu te perguntar algo,", static=ask_template)
            talk("Você pode responder digitando", static=ask_template)
            talk("A letra destacada que achar mais cabível.", static=ask_template)
            talk("Entendeu, né?", static=ask_template)

            key = str(read_key(suppress=True)).strip()
            if key in affirmative:
                response = True
                if key in affirmative[2:]:
                    talk(
                        "Sim, inglês também tá valendo...",
                        "pokerface",
                        static=ask_template,
                    )
                else:
                    talk("Show de bola!", "open mouth", static=ask_template)
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

        print(
            term.move_yx(term.height - 1, 0)
            + "Pressione qualquer tecla para continuar...",
            end="",
        )
        if read_key(suppress=True):
            return


def talk(input=" ", expression="idle", amount=1.0, static=""):
    ansi_pattern = r"\033\[[0-9;]*m|\033\[[0-9]*[A-Za-z]"

    clean_text = sub(ansi_pattern, "", input)

    effect_positions = {}
    clean_pos = 0
    active_effects = []
    i = 0

    while i < len(input):
        ansi_match = match(ansi_pattern, input[i:])
        if ansi_match:
            ansi_code = ansi_match.group()
            if ansi_code == term.normal:
                active_effects.clear()
            else:
                active_effects.append(ansi_code)
            i += len(ansi_code)
        else:
            if active_effects:
                effect_positions[clean_pos] = "".join(active_effects)
            clean_pos += 1
            i += 1

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

    print(term.home + "\033[1;1H\033[0J", end="")

    while remaining:
        sleep(0.03)
        displayed.append(remaining.pop(0))

        output_text = ""
        for i, char in enumerate(displayed):
            if i in effect_positions:
                output_text += f"{effect_positions[i]}{char}{term.normal}"
            else:
                output_text += char

        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        print(term.home + "\033[1;1H\033[0J", end="")
        print(
            f"{current_expr}  ──┤ {output_text if input != " " else static} │  ", end=""
        )
        print(f"{static if input != " " else ""}", end="", flush=True)

    sleep(amount)


if __name__ == "__main__":
    main()
