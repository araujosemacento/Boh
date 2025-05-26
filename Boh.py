from time import sleep
from os import system, name
from sys import stdout
from keyboard import read_key, read_hotkey  # pip install keyboard
from re import sub, match


def main():
    talk("Oi, tudo bem?")
    talk("Muito obrigado por executar o meu script")
    talk(f"Eu me chamo {colors.fg.green}{colors.bold}BOH{colors.reset}!")
    talk("He He", amount=0.5)
    talk("Sabe...", amount=0.5)
    talk("Tipo,")
    talk(static=f"Tipo, {colors.bold}ROH")
    talk(static=f"Tipo, {colors.bold}ROH-{colors.fg.green}BOH{colors.reset}")
    for i in range(10):
        talk(static=f"{"HahA" * i}", "open mouth", 0.05)
    sleep(1)
    talk("Ai ai, sou meio comédia às vezes, sabe? Mas enfim,")
    talk("E você, como se chama?", amount=0.5)
    print("\n\nDigite seu nome aqui: ", end="")
    sike = []
    while len(sike) < 3:
        sike.append(read_key())
        print(sike[-1], end="", flush=True)
    talk("Olha, na verdade, eu não tenho muito tempo...", "pokerface", 1.5)
    talk("Me desculpa! Você parece ser uma pessoa muito legal, mas...")
    talk("A pessoa que me mandou aqui, queria te falar sobre ↓ aquilo ↓")

    print("\n\nPressione qualquer tecla para continuar...", end="")
    if read_hotkey():
        exit()


def talk(input=" ", expression="idle", amount=1.0, static=""):
    ansi_pattern = r"\033\[[0-9;]*m"

    # Extrair texto limpo (sem códigos ANSI [o código que deixa os caracteres coloridos, consulte a classe colors no fim do código pra consultar os literais e a correlação à cor em inglês])
    clean_text = sub(ansi_pattern, "", input)

    # Dicionário preenchido com todas as posições de efeitos no texto original - agora suporta múltiplos efeitos empilhados na mesma posição
    effect_positions = (
        {}
    )  # posição no texto limpo -> string com todos os efeitos acumulados (negrito + cor + sublinhado, sei lá)

    # Processar o texto original pra mapear efeitos às posições - refatorado pra suportar múltiplos efeitos simultâneos
    clean_pos = 0
    active_effects = (
        []
    )  # Stack (pilha) de efeitos ativos - substitui o current_color que só guardava um efeito por vez, agora é uma lista que guarda vários -_- zZzZ
    i = 0

    while i < len(input):
        # Verificar se esbarramos em um código ANSI (colorido/efeito), eu não sabia que dava pra puxar "fatias" de listas, refatorei tudo pra usar, salvou vários ms de atraso na execução, mas ainda tive que refatorar essa porra 🤡
        ansi_match = match(ansi_pattern, input[i:])
        if ansi_match:
            ansi_code = ansi_match.group()
            if ansi_code == colors.reset:
                active_effects.clear()  # Reset limpa TODOS os efeitos ativos de uma vez - nem um pouco prático fazer assim, mas pra fins de execução me pareceu apresentar processamento mais rápido.
            else:
                active_effects.append(
                    ansi_code
                )  # Adiciona novo efeito à pilha - agora acumula ao invés de substituir (levar 15 minutos pra perceber que era isso que tava acontecendo foi ridículo)
            i += len(ansi_code)
        else:
            # Caractere normal - mapear TODOS os efeitos ativos (quando tiver)
            if active_effects:
                effect_positions[clean_pos] = "".join(
                    active_effects
                )  # Junta todos os códigos ANSI numa string só
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

    system("cls" if name == "nt" else "clear")

    # Animar o texto letra a letra, dando o efeito de uma máquina de escrever
    while remaining:
        sleep(0.03)

        # Adicionar próximo caractere pra mostrar
        displayed.append(remaining.pop(0))

        # Construir string com efeitos aplicados individualmente por letra
        output_text = ""
        for i, char in enumerate(displayed):
            if i in effect_positions:
                # Aplicar TODOS os efeitos a este caractere específico - pode ser negrito + cor + sublinhado + qualquer coisa
                output_text += f"{effect_positions[i]}{char}{colors.reset}"
            else:
                # Caractere normal sem efeitos
                output_text += char

        # Obter expressão atual baseada no comprimento exibido
        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        # Move cursor para posição (1,1) e limpa da posição atual até o fim da tela
        stdout.write("\033[1;1H\033[0J")

        # Isso aqui é um print, só que mais rápido, como se usasse o "echo" do terminal (sqn)
        stdout.write(
            f"{current_expr}  ──┤ {output_text if input != " " else static} │  "
        )
        stdout.write(f"{static if input != " " else ""}")
        stdout.flush()  # É o equivalente de print("string", flush=True). Caso você não saiba o que isso faz, sorte a sua. Mas basicamente, sem isso a tela fica preta até o loop acabar e só depois que o loop acaba o texto aparece

    sleep(
        amount
    )  # Quantidade de tempo que o quadro da fala atual fica na tela antes de passar pra próxima fala


# Bem-vindo(a), veio por causa do aviso lá de cima? Sinta-se em casa, recomendo o repositório: https://github.com/fidian/ansi pra entender o que tá rolando por aqui, caso as propriedades da classe não sejam suficientes.
# UPDATE: Agora você pode combinar múltiplos efeitos! Ex: colors.bold + colors.fg.red + colors.underline = texto negrito, vermelho E sublinhado ao mesmo tempo
class colors:
    reset = "\033[0m"  # Limpa TODOS os efeitos de uma vez - muito útil
    bold = "\033[01m"  # Negrito - combina bem com qualquer cor
    faint = "\033[02m"  # Texto meio apagado
    italic = "\033[03m"  # Itálico - nem todos os terminais suportam
    underline = "\033[04m"  # Sublinhado - fica massa com cores
    reverse = "\033[07m"  # Inverte cor de fundo e texto
    invisible = "\033[08m"  # Texto invisível (mas selecionável)
    strikethrough = "\033[09m"  # Texto riscado - pra quando você muda de ideia

    class fg:  # Cores de texto (foreground)
        black = "\33[30m"
        red = "\33[31m"
        green = "\33[32m"
        yellow = "\33[33m"
        blue = "\33[34m"
        magenta = "\33[35m"
        cyan = "\33[36m"
        white = "\33[37m"
        default = "\33[39m"
        brightblack = "\33[90m"
        brightred = "\33[91m"
        brightgreen = "\33[92m"
        brightyellow = "\33[93m"
        brightblue = "\33[94m"
        brightmagenta = "\33[95m"
        brightcyan = "\33[96m"
        brightwhite = "\33[97m"

    class bg:  # Cores de fundo (background) - combina com fg pra fazer destaque
        black = "\33[40m"
        red = "\33[41m"
        green = "\33[42m"
        yellow = "\33[43m"
        blue = "\33[44m"
        magenta = "\33[45m"
        cyan = "\33[46m"
        white = "\33[47m"
        default = "\33[49m"
        brightblack = "\33[100m"
        brightred = "\33[101m"
        brightgreen = "\33[102m"
        brightyellow = "\33[103m"
        brightblue = "\33[104m"
        brightmagenta = "\33[105m"
        brightcyan = "\33[106m"
        brightwhite = "\33[107m"


# zZzZzZzZzZzZzZzZzZzZzZzZ
if __name__ == "__main__":
    main()
