from sys import exit as sys_exit
from subprocess import run
from importlib.util import find_spec
from re import match, sub


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
        ansi_match = match(ansi_pattern, text[i:])
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


def talk(input=" ", expression="idle", amount=1.0, static="", colorize_arrows=False):
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

        with term.cbreak():
            term_input = term.inkey(timeout=0.01)
            if term_input == " ":
                term_input = term.inkey(timeout=None)
            term_input = None

        displayed.append(remaining.pop(0))

        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        print("\033[1;1H\033[0J", end="")

        def arrow_color(arrow):
            return (
                term.orange + arrow + term.normal
                if arrow == "‹" or arrow == "›"
                else term.blue + arrow + term.normal
            )

        static_text = static

        if colorize_arrows:
            displayed = [
                arrow_color(char) if char in ["‹", "»", "«", "›"] else char
                for char in displayed
            ]

            static_text = "".join(
                arrow_color(char) if char in ["‹", "»", "«", "›"] else char
                for char in static
            )

        displayed_text = "".join(displayed) if input != " " else static_text

        print(
            f"{current_expr}  ──┤ {displayed_text} │  ",
            end="",
            flush=True,
        )
        print(f"{static_text if input != " " else ""}", end="", flush=True)

    sleep(amount)


def main():
    list_model = "\n\n\n\n                        None × ‹[H]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[T]» × None"
    swapped_edges = "\n\n\n\n                        None × ‹[T]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None"
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
            key_input = term.inkey(timeout=10)
            if not key_input.is_sequence and key_input.isalnum():
                sike.append(key_input)
                print(sike[-1], end="", flush=True)
            else:
                talk("Você sabe seu nome, né?", amount=0.5)
                print(
                    term.move_yx(term.height - 3, 0) + "Digite seu nome aqui: ",
                    end="",
                    flush=True,
                )

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
        talk("Reconhece isso aqui, né?", amount=0.1)
        talk(static="Reconhece isso aqui, né?", expression="looking down", amount=0.25)
        print(list_model, flush=True)
        print(ask_template, flush=True)
        while True:
            key = term.inkey(timeout=5)
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
        talk("Bom, a gente pode fazer isso de várias maneiras...", static=list_model)
        talk(
            "Mas, acho que a primeira coisa que vem à cabeça é...",
            static=list_model,
        )
        talk(
            "Fazer isso, né?",
            static=f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
            amount=1.5,
        )
        talk(
            'Trocando Head e Tail, o que era a "frente" da lista,',
            static=swapped_edges,
        )
        talk(
            'Passa a ser o "final" dela, e vice-versa.',
            static=swapped_edges,
        )
        talk("Mas, pera aí! Como isso acontece exatamente?", static=swapped_edges)
        talk(
            f"Digamos que, a gente iguale {term.red}Tail \033[0ma {term.blue}Head",
            static=swapped_edges,
        )
        talk(
            "Eita... agora temos duas Heads!",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
            amount=1.5,
        )
        talk(
            f"Isso porque {term.red}Tail \033[0m= {term.blue}Head \033[0mnão é uma troca de valores,",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
        )
        talk(
            f"Só estamos dizendo que {term.red}Tail \033[0magora recebe",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
        )
        talk(
            f"O objeto contido dentro de {term.blue}Head\033[0m.",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
        )
        talk(
            f"Mas assim como abrir espaço numa estante pra guardar um livro,",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
            amount=1.5,
        )
        talk(
            f"Não significa que haverá espaço para guardar novamente",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
        )
        talk(
            f"O antigo livro que tiramos para guardar o livro novo...",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
        )
        talk("O que significa que precisamos salvar", static=swapped_edges)
        talk(
            "O antigo valor de Tail, antes de trocá-lo por Head.",
            static=f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None",
            amount=1.5,
        )
        talk(
            "Meu mano aqui se chama AUX,",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            amount=1.25,
        )
        talk(
            "Tudo bem contigo, patrão?",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            amount=0.75,
        )
        talk(
            "Ele se ofereceu pra guardar o valor de Tail",
            static="""
        __
(_|)   |@@|
 \ \__ \--/ __ 
  \o__|----|  |   __
      \ }{ /\ )_ / _\\
      /\__/\ \__O (__
     (--/\--)    \__/
     _)(  )(_
    `---''---`
""",
        )
        talk(
            "Pra que a gente não perca na hora de trocar...",
            static="""
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\\
       /\__/\ \__O (\033[31m[T]\033[0m
      (--/\--)    \__/
      _)(  )(_
     `---''---`
""",
        )
        talk(
            "Revisitando então o estado da nossa lista",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (\033[31m[T]\033[0m      None × ‹\033[34m[H]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹\033[34m[H]\033[0m» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
        )
        talk(
            "Graças ao AUX, que guardou o valor de Tail",
            static="""
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\\
       /\__/\ \__O (\033[31m[T]\033[0m      None × ‹\033[34m[H]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹\033[34m[H]\033[0m» × None
      (--/\--)    \__/
      _)(  )(_
     `---''---`
""",
        )
        talk(
            "Podemos facilmente colocar Tail onde o Head original está",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × ‹\033[31m[T]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹\033[34m[H]\033[0m» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
        )
        talk(
            "Obrigado AUX, você é o cara! Até mais tarde!",
            static="""
        __
(_|)   |@@|
 \ \__ \--/ __ 
  \o__|----|  |   __
      \ }{ /\ )_ / _\\
      /\__/\ \__O (__
     (--/\--)    \__/
     _)(  )(_
    `---''---`
""",
        )
        talk("Só que, isso não é o suficiente, né?", static=swapped_edges)
        talk("Por causa desses caras aqui: ‹[]»", static=swapped_edges)
        talk(
            f"Mais especificamente, ‹ » , esses dois.",
            static=swapped_edges,
        )
        talk("No nosso caso, eles representam", static=swapped_edges)
        talk("Os ponteiros que identificam", static=swapped_edges)
        talk("Quais elementos precedem e sucedem", static=swapped_edges)
        talk("O objeto observado, seja lá qual você escolha.", static=swapped_edges)
        talk("Até aí tudo bem, né?", static=swapped_edges)
        while True:
            talk(
                "Estamos na mesma página, então?",
                expression="thinking",
                static=swapped_edges,
                amount=0.2,
            )
            talk(
                static="Estamos na mesma página, então?",
                expression="thinking",
                amount=0.5,
            )
            print(swapped_edges, ask_template, flush=True)
            key = term.inkey(timeout=10)
            if key.lower() in affirmative:
                break
            elif key.lower() in negative:
                talk(
                    "Bom, resumidamente, nesse conceito de lista,", static=swapped_edges
                )
                talk("Não usamos um conceito de índice,", static=swapped_edges)
                talk('Então a única forma de saber "aonde"', static=swapped_edges)
                talk(
                    "Cada objeto se encontra, é através desses ponteiros,",
                    static=swapped_edges,
                )
                talk("Pense que é como uma corrente.", static=swapped_edges)
                talk(
                    "Cada elo da corrente aponta para o próximo,",
                    static=swapped_edges,
                )
                talk(
                    "E cada um também sabe qual é o elo anterior.",
                    static=swapped_edges,
                )
                while True:
                    talk("Agora fez mais sentido?", static=ask_template)
                    incepted = term.inkey(timeout=5)
                    if incepted.lower() in affirmative:
                        break
                    elif incepted.lower() in negative:
                        talk(
                            "Tudo bem então, vamos fazer o seguinte...",
                            static=ask_template,
                        )
                        talk("Vôce tá precisando de um descanso,", static=ask_template)
                        talk("Eu tô precisando de um descanso.", static=ask_template)
                        talk("Vou dar uma pausa aqui, beleza?", static=ask_template)
                        talk(
                            "Quando quiser continuar, é só teclar", static=ask_template
                        )
                        print("\033[1;1H\033[0J", end="", flush=True)
                        print(
                            "──┤ Tô aqui pertinho, quando quiser continuar é só chamar! │"
                        )
                        term.inkey(timeout=None)
                    elif incepted.is_sequence:
                        continue
                    elif not incepted:
                        talk(
                            "Muita falta de educação, ignorar os outros desse jeito!",
                            expression="annoyed",
                            static=ask_template,
                        )
                    else:
                        talk(
                            "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                            "annoyed",
                            static=ask_template,
                        )
            elif key.is_sequence:
                continue
            elif not key:
                talk(
                    "Me deixa no vácuo assim não, poxa! ;-;",
                    expression="looking down",
                    amount=1.5,
                    static=ask_template,
                )
            else:
                talk(
                    "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                    "annoyed",
                    static=ask_template,
                )
        talk("Então, vamos lá!", expression="open mouth", static=swapped_edges)
        talk(
            "De modo geral, essas setinhas são tão importantes",
            static=swapped_edges,
        )
        talk(
            "Pra esse exercício, que a gente vai precisar",
            static=swapped_edges,
        )
        talk(
            "Deixar elas bem visíveis, pra não confundir.",
            static=swapped_edges,
        )
        talk("Que tal...", expression="thinking", static=swapped_edges, amount=1.5)
        talk(static="Assim...", expression="thinking", amount=0.5)
        talk(
            static="Assim... ‹›«»",
            expression="thinking",
            colorize_arrows=True,
        )
        talk(
            "Melhorou, né?",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "As setas simples, ou seja, ‹ & › , destacadas em laranja,",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Representam a variável do nosso objeto que",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Nos mostra qual é o elemento que o precede",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Já as setas duplas, ou seja, » & « , destacadas em azul,",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Representam a variável do nosso objeto que",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Nos mostra qual é o elemento que o sucede",
            static=swapped_edges,
            colorize_arrows=True,
            amount=1.5,
        )
        talk(
            "Seguindo essa lógica,",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Acho que deu pra perceber que a gente",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Também vai precisar inverter essas setinhas",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Pra inverter a lista, certo?",
            static=swapped_edges,
            colorize_arrows=True,
            amount=1.5,
        )
        talk(
            "Já que, simplesmente trocar Head e Tail",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Não trocou as setinhas, de cada elemento.",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Então é como se olhássemos para trás,",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Mas continuássemos andando para frente.",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Até aqui tudo bem? Posso continuar?",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(static="Até aqui tudo bem? Posso continuar?", amount=0.2)
        print(ask_template, flush=True)
        while True:
            key = term.inkey(timeout=10)
            if key.lower() in affirmative:
                break
            elif key.lower() in negative:
                talk(
                    "Tudo bem então, vamos fazer o seguinte...",
                    static=ask_template,
                    colorize_arrows=True,
                )
                talk("Vôce tá precisando de um descanso,", static=ask_template)
                talk("Eu tô precisando de um descanso.", static=ask_template)
                talk("Vou dar uma pausa aqui, beleza?", static=ask_template)
                talk("Quando quiser continuar, é só teclar", static=ask_template)
                print("\033[1;1H\033[0J", end="", flush=True)
                print("──┤ Tô aqui pertinho, quando quiser continuar é só chamar! │")
                term.inkey(timeout=None)
            elif key.is_sequence:
                continue
            elif not key:
                talk(
                    "Muita falta de educação, ignorar os outros desse jeito!",
                    expression="annoyed",
                    static=ask_template,
                    colorize_arrows=True,
                )
            else:
                talk(
                    "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                    "annoyed",
                    static=ask_template,
                    colorize_arrows=True,
                )
        talk(
            "Então, vamos lá!",
            expression="open mouth",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Se formos então focar particularmente",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Na posição que a Tail ocupa agora,",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(
            "Ora, se as setas são direções,",
            static=f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            colorize_arrows=True,
        )
        talk(
            "Podemos simplemente invertê-las, certo?",
            static=f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            expression="thinking",
            colorize_arrows=True,
        )
        talk(
            "Assim como fizemos antes entre Tail e Head.",
            static=f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            colorize_arrows=True,
        )
        talk(
            "Ou seja...",
            static=f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            colorize_arrows=True,
        )
        talk(
            f"{term.bold}AUX!",
            static=f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            colorize_arrows=True,
        )
        talk(
            "Chega aí, meu querido!",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × ‹\033[31m[T]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Segura aqui pá nóis, fazendo favô.",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (‹_        None × \033[31m[T]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Agora que Aux tem o valor de anterior,",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (‹_        None × \033[31m[T]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "A gente coloca o valor de próximo no lugar de anterior,",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (‹_        None × «\033[31m[T]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "E o valor do Aux, no lugar de próximo. Mas...",
            amount=1.5,
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Se a gente inverteu anterior e próximo,",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Como mudar os valores subsequentes?",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "O que é frente e o que é trás?",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Bom, tudo depende se estamos começando de Head ou Tail.",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
            amount=1.5,
        )
        talk(
            "Como estamos começando de Tail, estamos no final.",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Para alterar todos os demais valores,",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Só precisamos ir até cada elemento que nos antecede,",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «\033[31m[T]\033[0m› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Que da nossa perspectiva atual, seria esse aqui:",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «[T]› ‹\033[31m[]\033[0m» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "E ao invertermos as setinhas desse elemento também,",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (‹_        None × «[T]› «\033[31m[]\033[0m» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Vemos que se simplesmente continuarmos indo em direção",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «[T]› «\033[31m[]\033[0m› ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "À atual direção do elemento anterior,",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «[T]› «\033[31m[]\033[0m› ‹[]» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Em algum momento...",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «[T]› «[]› ‹\033[31m[]\033[0m» ... ‹[]» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Nós estaremos de cara com a outra ponta da lista,",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «[T]› «[]› «[]› ... ‹\033[31m[]\033[0m» ‹[]» ‹[H]» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "E ao perceber que não há mais elementos",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (‹_        None × «[T]› «[]› «[]› ... «[]› «[]› «\033[31m[H]\033[0m» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Tcharam! Invertemos a lista com sucesso! :D",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × «[T]› «[]› «[]› ... «[]› «[]› «[H]› \033[31m× \033[38;5;93mNone\033[0m
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "E era isso que eu e AUX tínhamos pra te mostrar hoje!",
            expression="looking down",
            static="""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            colorize_arrows=True,
        )
        talk(
            "Espero que tenhamos conseguido te ajudar!",
            static="""
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\\
       /\__/\ \__O (\033[31m[T]\033[0m
      (--/\--)    \__/
      _)(  )(_
     `---''---`
""",
        )
        talk(
            "A gente se vê na próxima, beleza?",
            expression="open mouth",
            static="""
        __
(_|)   |@@|
 \ \__ \--/ __ 
  \o__|----|  |   __
      \ }{ /\ )_ / _\\
      /\__/\ \__O (__
     (--/\--)    \__/
     _)(  )(_
    `---''---`
""",
        )
        print(
            "\033[1;1H\033[0J",
            end="",
            flush=True,
        )
        print(
            """
(„• ֊ •„)੭      ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣿⣿⣶⣦⡀⠀⠀⠀⠀⠀⢀⣤⣶⣾⡿⠿⣷⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⠛⠉⠉⠉⠙⢿⣿⡆⠀⠀⠀⣴⣿⠟⠉⠀⠀⠀⠀⠈⠹⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⢸⣿⡏⠀⠀⠀⠀⠀⠀⠸⣿⡇⠀⠀⣾⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⡀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⢻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣷⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠸⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠻⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣷⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣈⣻⣿⣆⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⢀⣴⣿⠿⠛⠙⠻⢿⣧⡀⠀⠀⣠⡶⠟⠋⠉⠛⠷⣶⣄⠀⠀⠀⠹⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⣾⡿⠁⠀⠀⠀⠀⠀⠙⢿⣤⡾⠋⠀⠀⠀⠀⠀⠀⠀⠙⢷⠀⠀⠀⢿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⣀⡴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠸⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠸⣿⡇⠀⠀⠀⠀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⢻⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⢻⣿⡀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡞⠁⣀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠹⣿⣆⡀⠀⠈⠛⠶⢤⣤⣤⠤⠤⠖⠋⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⠶⣤⣤⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⠷⢤⣀⣀⠀⠲⣄⣀⠀⠀⠀⠀⠀⢀⣀⣤⠾⠋⢰⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣷⡀⠀⠈⠉⠀⠀⠈⠉⠉⠉⠉⠉⠉⠁⠀⠀⣰⣿⠏⠀⣠⣶⣶⡄⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⢠⣶⣷⣤⡀⠀⠀⠀⠙⠿⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣶⣿⠟⣁⣴⣿⣿⣿⡁⣠⣤⡀⠀⠀⠀
                ⠀⠀⢀⣴⣿⡿⢻⣿⡟⢠⣤⣤⢀⣄⠀⠉⠛⠛⠿⠿⠿⠿⠿⠿⣿⣛⠛⢹⣶⣄⢹⣿⡏⠙⢿⣿⣿⣟⠉⢠⣶⣦
                ⢀⣴⣿⡿⢿⣿⣿⠟⠁⢹⣿⣇⣼⣿⢿⣿⣿⣶⣶⡆⠀⠀⢸⣿⣿⢿⣷⡌⠛⢿⣿⣿⣷⡀⠀⠙⢿⣿⣿⣿⡿⠋
                ⢿⣿⣿⣤⣼⣿⡿⠀⠀⣸⣿⣿⠟⠁⢸⣿⣏⣈⡉⠁⣀⣀⡈⣿⣿⣴⣿⣿⣀⠀⠈⠻⣿⣷⡄⠀⠀⠙⠛⠉⠀⠀
                ⠀⠈⠙⠛⠛⠋⠁⠀⣠⣿⣿⠃⠀⠀⣿⣿⠿⠿⠇⠸⠿⠿⠋⢻⣿⣏⠙⣿⣿⡇⠀⠀⠹⣿⡿⠆⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⠇⠀⠀⢰⣿⣿⣦⣤⣷⡄⠀⠀⠀⢸⣿⣿⣶⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠛⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
        )

        if term.inkey(timeout=None):
            return


if __name__ == "__main__":
    main()

"""Setinhas: «»‹›"""
