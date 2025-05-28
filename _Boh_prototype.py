import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import queue
import re
from typing import Dict, List, Optional, Callable


class VirtualTerminal:
    """
    Terminal virtual que simula a funcionalidade do programa BOH original
    com capacidades de depuração e interface gráfica aprimorada.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_widgets()
        self.setup_colors()

        # Controle de estado
        self.current_text = ""
        self.waiting_for_key = False
        self.key_queue = queue.Queue()
        self.debug_queue = queue.Queue()
        self.animation_active = False

        # Configurar bindings de teclado
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.focus_set()

        # Thread para processar eventos de depuração
        self.debug_thread = threading.Thread(target=self.debug_processor, daemon=True)
        self.debug_thread.start()

    def setup_window(self):
        """Configura a janela principal da aplicação."""
        self.root.title("BOH - Terminal Virtual")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0c0c0c")
        self.root.resizable(True, True)

        # Centralizar janela na tela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_widgets(self):
        """Configura os widgets da interface."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#0c0c0c")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Terminal principal (centralizado verticalmente)
        self.terminal_frame = tk.Frame(main_frame, bg="#0c0c0c")
        self.terminal_frame.pack(fill=tk.BOTH, expand=True)

        # Área de texto do terminal
        self.terminal = scrolledtext.ScrolledText(
            self.terminal_frame,
            bg="#0c0c0c",
            fg="#ffffff",
            font=("Consolas", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            cursor="arrow",
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)

        # Frame de depuração (inicialmente oculto)
        self.debug_frame = tk.Frame(main_frame, bg="#1a1a1a", height=200)
        self.debug_visible = False

        # Área de depuração
        debug_label = tk.Label(
            self.debug_frame,
            text="🐛 Console de Depuração",
            bg="#1a1a1a",
            fg="#00ff00",
            font=("Consolas", 10, "bold"),
        )
        debug_label.pack(anchor=tk.W, padx=5, pady=2)

        self.debug_text = scrolledtext.ScrolledText(
            self.debug_frame,
            bg="#1a1a1a",
            fg="#00ff00",
            font=("Consolas", 9),
            wrap=tk.WORD,
            height=10,
        )
        self.debug_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Botão para alternar depuração
        toggle_frame = tk.Frame(main_frame, bg="#0c0c0c")
        toggle_frame.pack(fill=tk.X, pady=(5, 0))

        self.debug_toggle = tk.Button(
            toggle_frame,
            text="🐛 Mostrar Depuração",
            command=self.toggle_debug,
            bg="#333333",
            fg="#ffffff",
            font=("Consolas", 9),
            relief=tk.FLAT,
        )
        self.debug_toggle.pack(side=tk.RIGHT)

        # Status bar
        self.status_var = tk.StringVar(value="Pronto para iniciar...")
        status_bar = tk.Label(
            main_frame,
            textvariable=self.status_var,
            bg="#333333",
            fg="#ffffff",
            font=("Consolas", 9),
            anchor=tk.W,
            relief=tk.SUNKEN,
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def setup_colors(self):
        """Define tags de cores para o terminal."""
        # Tags para colorização do texto
        color_tags = {
            "green": "#00ff00",
            "red": "#ff0000",
            "yellow": "#ffff00",
            "blue": "#0080ff",
            "magenta": "#ff00ff",
            "cyan": "#00ffff",
            "white": "#ffffff",
            "bold": None,
            "dim": "#888888",
        }

        for tag, color in color_tags.items():
            if color:
                self.terminal.tag_configure(tag, foreground=color)
            elif tag == "bold":
                self.terminal.tag_configure(tag, font=("Consolas", 12, "bold"))

    def debug_log(self, message: str, level: str = "INFO"):
        """Adiciona mensagem ao console de depuração."""
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {level}: {message}\n"
        self.debug_queue.put(formatted_msg)

    def debug_processor(self):
        """Processa mensagens de depuração em thread separada."""
        while True:
            try:
                message = self.debug_queue.get(timeout=0.1)
                self.root.after(0, self._update_debug_text, message)
            except queue.Empty:
                continue

    def _update_debug_text(self, message: str):
        """Atualiza o texto de depuração (thread-safe)."""
        self.debug_text.insert(tk.END, message)
        self.debug_text.see(tk.END)

    def toggle_debug(self):
        """Alterna a visibilidade do painel de depuração."""
        if self.debug_visible:
            self.debug_frame.pack_forget()
            self.debug_toggle.config(text="🐛 Mostrar Depuração")
            self.debug_visible = False
        else:
            self.debug_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
            self.debug_toggle.config(text="🐛 Ocultar Depuração")
            self.debug_visible = True

    def clear_terminal(self):
        """Limpa o terminal virtual."""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete(1.0, tk.END)
        self.terminal.config(state=tk.DISABLED)
        self.debug_log("Terminal limpo")

    def write_to_terminal(self, text: str, tags: List[str] = []):
        """Escreve texto no terminal com formatação opcional."""
        self.terminal.config(state=tk.NORMAL)
        start_pos = self.terminal.index(tk.END)
        self.terminal.insert(tk.END, text)

        if len(tags) > 0:
            end_pos = self.terminal.index(tk.END)
            for tag in tags:
                self.terminal.tag_add(tag, start_pos, end_pos)

        self.terminal.config(state=tk.DISABLED)
        self.terminal.see(tk.END)

    def center_text_vertically(self, text: str):
        """Centraliza o texto verticalmente no terminal."""
        self.clear_terminal()
        # Calcula linhas vazias necessárias para centralizar
        terminal_height = self.terminal.winfo_height()
        line_height = self.terminal.tk.call(
            "font", "metrics", self.terminal["font"], "-linespace"
        )
        visible_lines = max(1, terminal_height // line_height)
        text_lines = text.count("\n") + 1
        empty_lines = max(0, (visible_lines - text_lines) // 2)

        centered_text = "\n" * empty_lines + text
        self.write_to_terminal(centered_text)

    def on_key_press(self, event):
        """Manipula eventos de teclado."""
        if self.waiting_for_key:
            key = event.char if event.char.isprintable() else event.keysym
            self.key_queue.put(key)
            self.debug_log(f"Tecla pressionada: {key}")
            return "break"  # Impede propagação do evento

    def wait_for_key(self) -> str:
        """Aguarda uma tecla ser pressionada."""
        self.waiting_for_key = True
        self.status_var.set("Aguardando entrada do usuário...")

        while True:
            try:
                key = self.key_queue.get(timeout=0.1)
                self.waiting_for_key = False
                self.status_var.set("Processando...")
                return key
            except queue.Empty:
                self.root.update()
                continue

    def talk(
        self,
        input_text: str = " ",
        expression: str = "idle",
        amount: float = 1.0,
        static: str = "",
    ):
        """
        Simula a função talk original com animação de texto.

        Args:
            input_text: Texto a ser exibido com animação
            expression: Expressão facial do personagem
            amount: Tempo de pausa após completar a animação
            static: Texto estático a ser exibido junto
        """
        self.debug_log(f"Talk chamado: '{input_text}', expression='{expression}'")

        # Dicionário de expressões faciais
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

        # Processar cores ANSI (simplificado)
        clean_text = self._strip_ansi(input_text)
        color_info = self._extract_colors(input_text)

        # Animar texto letra por letra
        self.animation_active = True
        displayed_chars = []

        expr_list = expressions.get(expression, expressions["idle"])

        for i, char in enumerate(clean_text):
            if not self.animation_active:
                break

            displayed_chars.append(char)
            current_text = "".join(displayed_chars)

            # Escolher expressão baseada no progresso
            expr_idx = i // max(1, len(expr_list) // 2) % len(expr_list)
            current_expr = expr_list[expr_idx]

            # Construir linha completa
            display_text = current_text if input_text != " " else ""
            full_line = f"{current_expr}  ──┤ {display_text} │"

            if static:
                full_line += f"\n{static}"

            # Centralizar e exibir
            self.center_text_vertically(full_line)

            # Aplicar cores se necessário
            if color_info and i < len(color_info):
                # Implementar colorização baseada em color_info
                pass

            time.sleep(0.03)  # Delay da animação

        self.animation_active = False
        time.sleep(amount)  # Pausa final

    def _strip_ansi(self, text: str) -> str:
        """Remove códigos ANSI do texto."""
        ansi_pattern = r"\033\[[0-9;]*m"
        return re.sub(ansi_pattern, "", text)

    def _extract_colors(self, text: str) -> Dict:
        """Extrai informações de cor do texto com códigos ANSI."""
        # Implementação simplificada - pode ser expandida
        colors = {}
        if "\033[32m" in text:  # Verde
            colors["green"] = True
        if "\033[31m" in text:  # Vermelho
            colors["red"] = True
        return colors

    def run_boh_dialogue(self):
        """Executa o diálogo do BOH adaptado para a interface gráfica."""
        self.debug_log("Iniciando diálogo do BOH")

        # Modelo da lista
        list_model = "\n\n\n\n                        None × ↽[H]⇀ ↽[]⇀ ↽[]⇀ ... ↽[]⇀ ↽[]⇀ ↽[T]⇀ × None"
        ask_template = "\n\n\n\n                    [Sim]     [Não]"

        response = False
        affirmative = ["S", "s", "y", "Y"]
        negative = ["N", "n"]

        # Sequência de diálogo
        self.talk("Oi, tudo bem?")
        self.talk("Muito obrigado por executar o meu script")
        self.talk("Eu me chamo BOH!")
        self.talk("He He", amount=0.75)
        self.talk("Sabe...", amount=0.75)
        self.talk("Tipo,")
        self.talk("Tipo, ROH", static="")
        self.talk("Tipo, ROH-BOH", static="")

        # Animação de risada
        for i in range(10):
            self.talk("HahA" * i, expression="open mouth", amount=0.05)

        time.sleep(1)
        self.talk("Ai ai, sou meio comédia às vezes, sabe?")
        self.talk("Mas, enfim,")
        self.talk("E você, como se chama?", amount=0.5)

        # Simular entrada de nome
        self.write_to_terminal("\n\nDigite seu nome (4 caracteres): ")
        self.debug_log("Aguardando entrada do nome do usuário")

        name_chars = []
        while len(name_chars) < 4:
            key = self.wait_for_key()
            if key.isalnum() and len(key) == 1:
                name_chars.append(key)
                self.write_to_terminal(key)
                time.sleep(0.1)

        self.debug_log(f"Nome inserido: {''.join(name_chars)}")

        self.talk(
            "Olha olha olha, na verdade, eu não tenho muito tempo...", "pokerface", 1.5
        )
        self.talk("Me desculpa! Você parece ser uma pessoa muito legal, mas...")
        self.talk(
            "A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓", amount=0.2
        )
        self.talk(
            "A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓",
            expression="looking down",
            amount=0.2,
        )

        self.center_text_vertically(list_model)
        time.sleep(2)

        self.talk("Reconhece?", static=list_model, amount=1.5)
        self.talk("Ih, verdade, cê não consegue me responder, né?", static=list_model)
        self.talk("Hmmm", expression="thinking")

        for i in range(3):
            self.talk("Hmmm" + "." * (i + 1), expression="thinking")

        self.talk("Já sei!", expression="open mouth")
        self.talk("Aqui, toma", static=ask_template, amount=1.5)

        # Loop de confirmação
        while not response:
            self.talk("Agora sempre que eu te perguntar algo,", static=ask_template)
            self.talk("Você pode responder digitando", static=ask_template)
            self.talk("A letra destacada que achar mais cabível.", static=ask_template)
            self.talk("Entendeu, né?", static=ask_template)

            key = self.wait_for_key()
            self.debug_log(f"Resposta recebida: {key}")

            if key in affirmative:
                response = True
                if key in affirmative[2:]:
                    self.talk(
                        "Sim, inglês também tá valendo...",
                        "pokerface",
                        static=ask_template,
                    )
                else:
                    self.talk("Show de bola!", "open mouth", static=ask_template)
            elif key in negative:
                response = False
                self.talk("Não?", "pokerface", static=ask_template)
                self.talk("Pera, deixa eu repetir", static=ask_template)
            elif not key.isalnum() or len(key) != 1:
                continue
            else:
                response = False
                self.talk(
                    "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                    "annoyed",
                    static=ask_template,
                )

        self.write_to_terminal("\n\nPressione qualquer tecla para finalizar...")
        self.wait_for_key()
        self.debug_log("Diálogo finalizado")
        self.status_var.set("Diálogo concluído!")

    def start(self):
        """Inicia a aplicação."""
        # Iniciar diálogo em thread separada para não bloquear a GUI
        dialogue_thread = threading.Thread(target=self.run_boh_dialogue, daemon=True)
        dialogue_thread.start()

        # Iniciar loop principal da GUI
        self.root.mainloop()


def main():
    """Função principal da aplicação."""
    app = VirtualTerminal()
    app.start()


if __name__ == "__main__":
    main()
# Execute o script principal
