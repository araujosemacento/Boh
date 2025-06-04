from sys import exit as sys_exit
from subprocess import run
from importlib.util import find_spec
from re import match, sub
from time import sleep, time as current_time
from random import choice
from os import path, makedirs, listdir


def check_dependencies() -> None:
    modules = ["blessed", "pygame"]

    for module in modules:
        if find_spec(module) is None:
            try:
                import tkinter as tk
                from tkinter import messagebox

                root = tk.Tk()
                root.withdraw()

                message = f"Oi, tudo bem?\nEntão, o Boh meio que precisa\ndesse módulo pra te entender\ne ficar bonitinho\n conversando com você:\n\n{module}\n\nQuer que eu instale ele por você?"

                result = messagebox.askyesno("Dependências Faltando", message)

                if result:
                    cmd = f"pip install {module}"
                    print(f"\033[31mShow de Bola!\033[0m Executando: {cmd}\n")
                    run(cmd, shell=True)
                    print(
                        "\n\033[34mReinicie o script após a instalação, beleza?\033[0m"
                    )
                else:
                    print(
                        f"\n\033[31mInstalação cancelada :(\033[0m\nSe quiser instalar depois, por conta própria,\nexecute:\n\n\033[34mpip install {module}\033[0m\n"
                    )

                root.destroy()
                sys_exit()

            except ImportError:
                print(f"Módulos faltando: {module}")
                print(f"Execute: pip install {module}")
                sys_exit()


check_dependencies()

from blessed import Terminal  # type: ignore
from pygame import mixer, error as pygame_error  # type: ignore

term = Terminal()


# Classe para selecionar itens aleatórios sem repetição
class ShuffledSelector:
    def __init__(self, items):
        self.items = list(items)  # Cria uma cópia da lista de itens
        self.available_indices = list(range(len(items)))  # Índices disponíveis

    def select(self):
        # Se não houver índices disponíveis, recarrega todos
        if not self.available_indices:
            self.available_indices = list(range(len(self.items)))

        # Escolhe um índice aleatório dos disponíveis
        idx = choice(self.available_indices)

        # Remove o índice escolhido da lista de disponíveis
        self.available_indices.remove(idx)

        # Retorna o item correspondente ao índice
        return self.items[idx]


# Inicializar o mixer do pygame
mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

# Diretório onde os efeitos sonoros estão armazenados
sfx_dir = path.join(path.dirname(path.abspath(__file__)), "sfx")
makedirs(sfx_dir, exist_ok=True)

# Verificar se existem arquivos de som, ou criar uma lista padrão
sfx_files = (
    [f for f in listdir(sfx_dir) if f.endswith((".wav", ".ogg", ".mp3"))]
    if path.exists(sfx_dir)
    else []
)

# Se não existirem arquivos de som, usamos apenas o canal sem reproduzir nada
if not sfx_files:
    print(
        f"Aviso: Nenhum arquivo de som encontrado em {sfx_dir}. Os efeitos sonoros não serão reproduzidos."
    )
    print("Para adicionar sons, coloque arquivos .wav, .ogg ou .mp3 na pasta 'sfx'.")

# Carregar os efeitos sonoros
sound_effects = []
for sfx_file in sfx_files:
    try:
        sound = mixer.Sound(path.join(sfx_dir, sfx_file))
        sound.set_volume(0.7)  # Ajuste o volume conforme necessário (0.0 a 1.0)
        sound_effects.append(sound)
    except pygame_error:
        print(f"Erro ao carregar o arquivo de som: {sfx_file}")

# Criar o seletor de sons sem repetição
sound_selector = ShuffledSelector(sound_effects)

# Canal para reprodução de som
sound_channel = mixer.Channel(0)


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


time = None  # Variável para controlar o tempo do último som reproduzido


def play_typing_sound(static=True, input=" "):
    """Reproduz um som aleatório de digitação, interrompendo qualquer som em curso."""
    global time
    play = False
    if time:
        play = True if static and input == " " else current_time() - time > 0.3
    else:
        time = current_time()
        play = True
    if play and sound_effects:
        time = current_time()
        sound_channel.stop()  # Interrompe qualquer som em reprodução
        sound = sound_selector.select()
        sound_channel.play(sound)


def arrow_colorize(text, colorize_arrows=False):
    """Coloriza as setas no texto se colorize_arrows=True."""
    if not colorize_arrows:
        return text

    def colorize(char):
        if char in ["‹", "›"]:
            return term.orange + char + term.normal
        elif char in ["»", "«"]:
            return term.blue + char + term.normal
        return char

    if isinstance(text, list):
        return [colorize(char) for char in text]
    else:
        return "".join(colorize(char) for char in text)


def talk(input=" ", expression="idle", amount=1.0, static="", colorize_arrows=False):
    """Exibe texto animado com expressões e efeitos sonoros a cada caractere alfanumérico."""
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

        # Verificamos se o caractere atual é alfanumérico para reproduzir o som
        current_char = displayed[-1]
        # Remove códigos ANSI para verificar se é alfanumérico
        clean_char = sub(r"\033\[[0-9;]*m", "", current_char)

        # Reproduz o som apenas se for um caractere alfanumérico
        if clean_char and any(c.isalnum() for c in clean_char):
            play_typing_sound(static=True if static else False, input=clean_char)
        elif static and input == " ":
            play_typing_sound()

        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        print("\033[1;1H\033[0J", end="\n   ")

        displayed_text = ""
        if input != " ":
            displayed_text = "".join(arrow_colorize(displayed, colorize_arrows))
        else:
            displayed_text = arrow_colorize(static, colorize_arrows)

        static_text = arrow_colorize(static, colorize_arrows) if input != " " else ""

        print(
            f"{current_expr}  ──┤ {displayed_text} │  ",
            end="",
            flush=True,
        )
        print(f"{static_text}", end="", flush=True)

    sleep(amount)


def wait_for_response(
    affirmative=["s", "y"],
    negative=["n"],
    static="",
    ask_template="",
    timeout=5,
    messages=None,
):
    """Espera pela resposta do usuário e processa de acordo."""
    if messages is None:
        messages = {
            "timeout": "Poxa, tá difícil assim de encontrar a tecla?",
            "invalid": "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
            "negative": "Não?",
            "retry": "Pera, deixa eu repetir",
            "positive": "Show de bola!",
        }

    while True:
        key = term.inkey(timeout=timeout)

        if key.lower() in affirmative:
            if key.lower() == "y":
                talk(
                    "Sim, inglês também tá valendo...",
                    "pokerface",
                    static=ask_template,
                )
            else:
                talk(messages["positive"], "open mouth", static=ask_template)
            return True

        elif key.lower() in negative:
            talk(messages["negative"], "pokerface", static=ask_template)
            talk(messages["retry"], static=ask_template)

        elif key.is_sequence:
            continue

        elif not key:
            talk(
                messages["timeout"],
                expression="thinking",
                amount=1.5,
                static=static + ask_template,
            )

        else:
            talk(
                messages["invalid"],
                "annoyed",
                static=static + ask_template,
            )


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

        # Primeira instrução sobre como responder
        talk("Agora sempre que eu te perguntar algo,", static=ask_template)
        talk("Você pode responder digitando", static=ask_template)
        talk("A letra destacada que achar mais cabível.", static=ask_template)
        talk("Entendeu, né?", static=ask_template)

        wait_for_response(
            affirmative=affirmative, negative=negative, ask_template=ask_template
        )

        talk("Enfim, voltando ao assunto...", expression="idle")
        talk("Reconhece isso aqui, né?", amount=0.1)
        talk(static="Reconhece isso aqui, né?", expression="looking down", amount=0.25)
        print(list_model, flush=True)
        print(ask_template, flush=True)

        # Verificando se o usuário reconhece a lista
        recognition_messages = {
            "timeout": "Poxa, tá difícil assim de encontrar a tecla?",
            "invalid": "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
            "negative": "Não?",
            "retry": "Como assim pô? Me esforcei tanto desenhar ela...",
        }

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
                    recognition_messages["retry"],
                    expression="pokerface",
                    static=list_model,
                )
                talk("É uma lista! A estrutura de dados!", static=list_model)
                talk("Tá vendo?", static=f"{list_model}{ask_template}")
            elif key.is_sequence:
                continue
            elif not key:
                talk(
                    recognition_messages["timeout"],
                    expression="thinking",
                    amount=1.5,
                    static=f"{list_model}{ask_template}",
                )
            else:
                talk(
                    recognition_messages["invalid"],
                    "annoyed",
                    static=f"{list_model}{ask_template}",
                )

        # Explicações sobre a lista
        talk_sequence = [
            "Bom, como você já sabe... a lista é uma estrutura de dados",
            "Mas tô aqui pra discutir um desafio específico relacionado a ela...",
            "O desafio é o seguinte:",
            "Que tal inverter uma lista?",
            "Ou melhor, qual seria a maneira mais eficiente de fazer isso?",
            "Bom, a gente pode fazer isso de várias maneiras...",
            "Mas, acho que a primeira coisa que vem à cabeça é...",
        ]

        for text in talk_sequence[:-1]:
            talk(text, static=list_model)

        talk(talk_sequence[-1], static=list_model)

        # Lista com Head e Tail invertidos
        colored_list = f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None"
        talk(
            "Fazer isso, né?",
            static=colored_list,
            amount=1.5,
        )

        # Explicações sobre inversão de lista
        swap_explanations = [
            'Trocando Head e Tail, o que era a "frente" da lista,',
            'Passa a ser o "final" dela, e vice-versa.',
            "Mas, pera aí! Como isso acontece exatamente?",
            f"Digamos que, a gente iguale {term.red}Tail \033[0ma {term.blue}Head",
        ]

        for explanation in swap_explanations:
            talk(explanation, static=swapped_edges)

        # Visualizações da lista após operações
        list_with_two_heads = f"\n\n\n\n                        None × ‹{term.blue}[H]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹{term.blue}[H]{term.normal}» × None"

        talk(
            "Eita... agora temos duas Heads!",
            static=list_with_two_heads,
            amount=1.5,
        )

        # Explicação sobre a atribuição de variáveis
        assignment_explanations = [
            f"Isso porque {term.red}Tail \033[0m= {term.blue}Head \033[0mnão é uma troca de valores,",
            f"Só estamos dizendo que {term.red}Tail \033[0magora recebe",
            f"O objeto contido dentro de {term.blue}Head\033[0m.",
            f"Mas assim como abrir espaço numa estante pra guardar um livro,",
            f"Não significa que haverá espaço para guardar novamente",
            f"O antigo livro que tiramos para guardar o livro novo...",
            "O que significa que precisamos salvar",
            "O antigo valor de Tail, antes de trocá-lo por Head.",
        ]

        # Mostrando as explicações
        for i, explanation in enumerate(assignment_explanations):
            static_display = list_with_two_heads
            amount = 1.5 if i == 3 or i == 7 else 1.0
            talk(explanation, static=static_display, amount=amount)

        # Introduzindo o auxiliar
        aux_ascii = """
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
"""

        # Sequência do AUX
        aux_sequence = [
            "Meu mano aqui se chama AUX,",
            "Tudo bem contigo, patrão?",
            "Ele se ofereceu pra guardar o valor de Tail",
            "Pra que a gente não perca na hora de trocar...",
        ]

        for i, text in enumerate(aux_sequence):
            if i == 2:
                aux_ascii = """
        __
(_|)   |@@|
 \ \__ \--/ __ 
  \o__|----|  |   __
      \ }{ /\ )_ / _\\
      /\__/\ \__O (\033[31m[T]\033[0m
      (--/\--)    \__/
      _)(  )(_
     `---''---`
"""
            elif i == 3:
                aux_ascii = """
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\\
       /\__/\ \__O (\033[31m[T]\033[0m
      (--/\--)    \__/
      _)(  )(_
     `---''---`
"""
            amount = 1.25 if i == 0 else 0.75 if i == 1 else 1.0
            talk(text, static=aux_ascii, amount=amount)

        # Revisão do estado da lista com AUX
        aux_with_list = """
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (\033[31m[T]\033[0m      None × ‹\033[34m[H]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹\033[34m[H]\033[0m» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
"""

        review_sequence = [
            "Revisitando então o estado da nossa lista",
            "Graças ao AUX, que guardou o valor de Tail",
            "Podemos facilmente colocar Tail onde o Head original está",
        ]

        for i, text in enumerate(review_sequence):
            if i == 2:
                aux_with_list = """
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\\
 )/  /\__/\ \__O (__        None × ‹\033[31m[T]\033[0m» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹\033[34m[H]\033[0m» × None
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
"""
            talk(text, static=aux_with_list)

        # Despedindo-se do AUX
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

        # Explicando sobre os ponteiros da lista
        pointer_explanations = [
            "Só que, isso não é o suficiente, né?",
            "Por causa desses caras aqui: ‹[]»",
            "Mais especificamente, ‹ » , esses dois.",
            "No nosso caso, eles representam",
            "Os ponteiros que identificam",
            "Quais elementos precedem e sucedem",
            "O objeto observado, seja lá qual você escolha.",
            "Até aí tudo bem, né?",
        ]

        for explanation in pointer_explanations:
            talk(explanation, static=swapped_edges)

        # Verificando entendimento
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

        # Resposta do usuário sobre entendimento
        understanding_check = False
        while not understanding_check:
            key = term.inkey(timeout=10)
            if key.lower() in affirmative:
                understanding_check = True
            elif key.lower() in negative:
                # Explicações adicionais sobre a lista
                additional_explanations = [
                    "Bom, resumidamente, nesse conceito de lista,",
                    "Não usamos um conceito de índice,",
                    'Então a única forma de saber "aonde"',
                    "Cada objeto se encontra, é através desses ponteiros,",
                    "Pense que é como uma corrente.",
                    "Cada elo da corrente aponta para o próximo,",
                    "E cada um também sabe qual é o elo anterior.",
                ]

                for explanation in additional_explanations:
                    talk(explanation, static=swapped_edges)

                # Verificando novamente o entendimento
                confirmation = False
                while not confirmation:
                    talk("Agora fez mais sentido?", static=ask_template)
                    incepted = term.inkey(timeout=5)
                    if incepted.lower() in affirmative:
                        understanding_check = True
                        confirmation = True
                    elif incepted.lower() in negative:
                        # Oferecendo uma pausa
                        pause_sequence = [
                            "Tudo bem então, vamos fazer o seguinte...",
                            "Vôce tá precisando de um descanso,",
                            "Eu tô precisando de um descanso.",
                            "Vou dar uma pausa aqui, beleza?",
                            "Quando quiser continuar, é só teclar",
                        ]

                        for text in pause_sequence:
                            talk(text, static=ask_template)

                        print("\033[1;1H\033[0J", end="", flush=True)
                        print(
                            "──┤ Tô aqui pertinho, quando quiser continuar é só chamar! │"
                        )
                        term.inkey(timeout=None)
                        confirmation = True
                        understanding_check = True
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

        # Continuando com a explicação
        talk("Então, vamos lá!", expression="open mouth", static=swapped_edges)

        # Explicações sobre as setinhas
        arrow_explanations = [
            "De modo geral, essas setinhas são tão importantes",
            "Pra esse exercício, que a gente vai precisar",
            "Deixar elas bem visíveis, pra não confundir.",
        ]

        for explanation in arrow_explanations:
            talk(explanation, static=swapped_edges)

        # Mostrando setas coloridas
        talk("Que tal...", expression="thinking", static=swapped_edges, amount=1.5)
        talk(static="Assim...", expression="thinking", amount=0.5)
        talk(
            static="Assim... ‹›«»",
            expression="thinking",
            colorize_arrows=True,
        )

        # Explicando as setas coloridas
        colored_arrow_explanations = [
            "Melhorou, né?",
            "As setas simples, ou seja, ‹ & › , destacadas em laranja,",
            "Representam a variável do nosso objeto que",
            "Nos mostra qual é o elemento que o precede",
            "Já as setas duplas, ou seja, » & « , destacadas em azul,",
            "Representam a variável do nosso objeto que",
            "Nos mostra qual é o elemento que o sucede",
        ]

        for i, explanation in enumerate(colored_arrow_explanations):
            amount = 1.5 if i == 6 else 1.0
            talk(explanation, static=swapped_edges, colorize_arrows=True, amount=amount)

        # Explicando a necessidade de inverter as setas
        inversion_explanations = [
            "Seguindo essa lógica,",
            "Acho que deu pra perceber que a gente",
            "Também vai precisar inverter essas setinhas",
            "Pra inverter a lista, certo?",
            "Já que, simplesmente trocar Head e Tail",
            "Não trocou as setinhas, de cada elemento.",
            "Então é como se olhássemos para trás,",
            "Mas continuássemos andando para frente.",
        ]

        for i, explanation in enumerate(inversion_explanations):
            amount = 1.5 if i == 3 else 1.0
            talk(explanation, static=swapped_edges, colorize_arrows=True, amount=amount)

        # Verificando se pode continuar
        talk(
            "Até aqui tudo bem? Posso continuar?",
            static=swapped_edges,
            colorize_arrows=True,
        )
        talk(static="Até aqui tudo bem? Posso continuar?", amount=0.2)
        print(ask_template, flush=True)

        # Verificando resposta do usuário
        while True:
            key = term.inkey(timeout=10)
            if key.lower() in affirmative:
                break
            elif key.lower() in negative:
                pause_sequence = [
                    "Tudo bem então, vamos fazer o seguinte...",
                    "Vôce tá precisando de um descanso,",
                    "Eu tô precisando de um descanso.",
                    "Vou dar uma pausa aqui, beleza?",
                    "Quando quiser continuar, é só teclar",
                ]

                for text in pause_sequence:
                    talk(text, static=ask_template, colorize_arrows=True)

                print("\033[1;1H\033[0J", end="", flush=True)
                print("──┤ Tô aqui pertinho, quando quiser continuar é só chamar! │")
                term.inkey(timeout=None)
                break
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

        # Continuando com a explicação
        talk(
            "Então, vamos lá!",
            expression="open mouth",
            static=swapped_edges,
            colorize_arrows=True,
        )

        # Explicações sobre as direções das setas
        direction_explanations = [
            "Se formos então focar particularmente",
            "Na posição que a Tail ocupa agora,",
        ]

        for explanation in direction_explanations:
            talk(explanation, static=swapped_edges, colorize_arrows=True)

        # Lista com Tail destacada
        list_with_highlighted_tail = f"\n\n\n\n                        None × ‹{term.red}[T]{term.normal}» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None"

        # Explicações sobre como inverter as setas
        arrow_inversion_explanations = [
            "Ora, se as setas são direções,",
            "Podemos simplemente invertê-las, certo?",
            "Assim como fizemos antes entre Tail e Head.",
            "Ou seja...",
            f"{term.bold}AUX!",
            "Chega aí, meu querido!",
        ]

        for i, explanation in enumerate(arrow_inversion_explanations):
            expression = "thinking" if i == 1 else "idle"
            talk(
                explanation,
                static=list_with_highlighted_tail,
                colorize_arrows=True,
                expression=expression,
            )

        # Sequência com AUX manipulando as setas
        aux_sequences = [
            (
                "Segura aqui pá nóis, fazendo favô.",
                """
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
            ),
            (
                "Agora que Aux tem o valor de anterior,",
                """
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
            ),
            (
                "A gente coloca o valor de próximo no lugar de anterior,",
                """
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
            ),
            (
                "E o valor do Aux, no lugar de próximo. Mas...",
                """
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
            ),
        ]

        for i, (text, ascii_art) in enumerate(aux_sequences):
            amount = 1.5 if i == 3 else 1.0
            talk(text, static=ascii_art, colorize_arrows=True, amount=amount)

        # Explicação sobre inversão de direções
        direction_questions = [
            (
                "Se a gente inverteu anterior e próximo,",
                """
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
            ),
            (
                "Como mudar os valores subsequentes?",
                """
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
            ),
            (
                "O que é frente e o que é trás?",
                """
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
            ),
            (
                "Bom, tudo depende se estamos começando de Head ou Tail.",
                """
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
            ),
        ]

        for i, (text, ascii_art) in enumerate(direction_questions):
            amount = 1.5 if i == 3 else 1.0
            talk(text, static=ascii_art, colorize_arrows=True, amount=amount)

        # Explicações sobre percorrer a lista invertida
        traversal_explanations = [
            (
                "Como estamos começando de Tail, estamos no final.",
                """
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
            ),
            (
                "Para alterar todos os demais valores,",
                """
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
            ),
            (
                "Só precisamos ir até cada elemento que nos antecede,",
                """
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
            ),
        ]

        for text, ascii_art in traversal_explanations:
            talk(text, static=ascii_art, colorize_arrows=True)

        # Animação de percorrer e inverter cada elemento
        node_traversal = [
            (
                "Que da nossa perspectiva atual, seria esse aqui:",
                """
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
            ),
            (
                "E ao invertermos as setinhas desse elemento também,",
                """
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
            ),
            (
                "Vemos que se simplesmente continuarmos indo em direção",
                """
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
            ),
            (
                "À atual direção do elemento anterior,",
                """
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
            ),
            (
                "Em algum momento...",
                """
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
            ),
            (
                "Nós estaremos de cara com a outra ponta da lista,",
                """
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
            ),
            (
                "E ao perceber que não há mais elementos",
                """
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
            ),
            (
                "Tcharam! Invertemos a lista com sucesso! :D",
                """
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
            ),
        ]

        for text, ascii_art in node_traversal:
            talk(
                text, expression="looking down", static=ascii_art, colorize_arrows=True
            )

        # Conclusão
        conclusion = [
            (
                "E era isso que eu e AUX tínhamos pra te mostrar hoje!",
                """
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
            ),
            (
                "Espero que tenhamos conseguido te ajudar!",
                """
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
            ),
            (
                "A gente se vê na próxima, beleza?",
                """
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
            ),
        ]

        for i, (text, ascii_art) in enumerate(conclusion):
            expression = (
                "looking down" if i == 0 else "open mouth" if i == 2 else "idle"
            )
            talk(
                text, expression=expression, static=ascii_art, colorize_arrows=(i == 0)
            )

        # Arte final
        print(
            "\033[1;1H\033[0J",
            end="",
            flush=True,
        )
        print(
            """
(„• ֊ •„)੭      ⠀⠀⠀⢀⡴⠟⠛⢷⡄⠀⣠⠞⠋⠉⠳⡄⠀⠀⠀⠀
                ⠀⠀⠀⣸⠁⠀⠀⠈⣧⢰⠇⠀⠀⠀⢠⡇⠀⠀⠀⠀
                ⠀⠀⠀⠸⣆⠀⠀⠀⠘⣿⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠹⣦⠀⠀⠀⠘⡄⠀⠀⠀⡇⠀⠀⠀⠀⠀
                ⠀⠀⠀⡴⠚⠙⠳⣀⡴⠂⠁⠒⢄⠀⢿⡀⠀⠀⠀⠀
                ⠀⠀⢸⡇⠀⢀⠔⠉⠀⠀⠀⡀⠀⠂⠘⣇⠀⠀⠀⠀
                ⠀⠀⠀⢳⡀⠘⢄⣀⣀⠠⠶⠄⠀⠀⠀⡿⠀⠀⠀⠀
                ⠀⠀⠀⠀⠻⣕⠂⠁⠀⠀⠀⠀⠀⠀⣰⡇⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠹⣅⠒⠀⠒⠂⠐⠒⢉⡼⢁⣤⠀⠀⠀
                ⠀⢀⣼⣻⣆⣤⢈⣙⣒⠶⠶⣶⣞⢿⣸⡟⠳⣾⣂⣤
                ⠸⢿⣽⠏⢠⡿⠋⣿⣭⢁⣈⣿⣽⣆⠙⢷⣄⠙⠋⠁
                ⠀⠀⠀⠀⠛⠃⠰⠿⣤⠄⠀⠸⠷⠟⠀⠀⠁⠀⠀⠀
"""
        )

        if term.inkey(timeout=None):
            return


if __name__ == "__main__":
    main()

"""Setinhas: «»‹›"""
