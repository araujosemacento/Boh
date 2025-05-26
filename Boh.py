import os, time, sys, re, keyboard


def main():
    talk("Oi, tudo bem?")
    talk("Muito obrigado por executar o meu script")
    # talk(f"Eu me chamo {colors.bold}{colors.}{}{}")
    print("\n\nPressione qualquer tecla para continuar...", end="")
    if keyboard.read_key():
        exit()


def talk(input="", expression="idle", ending="pause", amount=1.25, static=""):
    ansi_pattern = r"\033\[[0-9;]*m"

    # Extrair texto limpo (sem códigos ANSI [o código que deixa os caracteres coloridos, consulte a classe colors no fim do código pra consultar os literais e a correlação à cor em inglês])
    clean_text = re.sub(ansi_pattern, "", input)

    # Dicionário preenchido com todas as posições de códigos de cor no texto original
    color_positions = {}  # posição no texto limpo -> código de cor

    # Processar o texto original para mapear cores às posições
    clean_pos = 0
    current_color = None
    i = 0

    while i < len(input):
        # Verificar se esbarramos em um código ANSI (colorido), eu não sabia que dava pra puxar "fatias" de listas, refatorei tudo pra usar, salvou vários ms de atraso na execução, mas ainda tive que refatorar essa porra 🤡
        ansi_match = re.match(ansi_pattern, input[i:])
        if ansi_match:
            ansi_code = ansi_match.group()
            if ansi_code == colors.reset:
                current_color = None
            else:
                current_color = ansi_code
            i += len(ansi_code)
        else:
            # Caractere normal - mapear a cor atual (quando tiver)
            if current_color:
                color_positions[clean_pos] = current_color
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

    os.system("cls" if os.name == "nt" else "clear")

    # Animar o texto letra a letra, dando o efeito de uma máquina de escrever
    while remaining:
        time.sleep(0.03)

        # Adicionar próximo caractere pra mostrar
        displayed.append(remaining.pop(0))

        # Construir string com cores aplicadas individualmente por letra
        output_text = ""
        for i, char in enumerate(displayed):
            if i in color_positions:
                # Aplicar cor apenas a este caractere específico
                output_text += f"{color_positions[i]}{char}{colors.reset}"
            else:
                # Caractere normal sem cor
                output_text += char

        # Obter expressão atual baseada no comprimento exibido
        expr_list = expressions.get(expression, expressions["idle"])
        current_expr = expr_list[
            len(displayed) // (len(expr_list) // 2) % len(expr_list)
        ]

        # Move cursor para posição (1,1) e limpa da posição atual até o fim da tela
        sys.stdout.write("\033[1;1H\033[0J")

        # Isso aqui é um print, só que mais rápido, como se usasse o "echo" do terminal (sqn)
        sys.stdout.write(f"{current_expr}   ┤ {output_text} │")
        sys.stdout.flush()  # É o equivalente de print("string", flush=True). Caso você não sabe o que isso faz, sorte a sua. Mas basicamente, sem isso a tela fica preta até o loop acabar e só depois que o loop acaba o texto aparece

        sys.stdout.write(f"{static}")

    # Tratar comportamento de finalização. Vai virar um match ao invés de um if, se eu precisar de mais flexibilidade
    if ending == "pause":
        time.sleep(amount)


# Bem-vindo(a), veio por causa do aviso lá de cima? Sinta-se em casa, recomendo o repositório: https://github.com/fidian/ansi pra entender o que tá rolando por aqui, caso as propriedades da classe não sejam suficientes.
class colors:
    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"


# zZzZzZzZzZzZzZzZzZzZzZzZ
if __name__ == "__main__":
    main()
