from random import choice
import json


class ShuffledSelector:
    """Classe para selecionar itens aleatórios sem repetição"""

    def __init__(self, items):
        self.items = list(items)
        self.available_indices = list(range(len(items)))

    def select(self):
        if not self.available_indices:
            self.available_indices = list(range(len(self.items)))

        idx = choice(self.available_indices)
        self.available_indices.remove(idx)
        return self.items[idx]


class BOHDialogueManager:
    """Gerencia o estado e fluxo do diálogo com BOH!"""

    def __init__(self):
        self.expressions = {
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

        self.dialogue_sequence = self._create_dialogue_sequence()

    def _create_dialogue_sequence(self):
        """Cria a sequência completa de diálogos"""
        return [
            {"text": "Oi, tudo bem?", "expression": "idle", "delay": 1000},
            {
                "text": "Muito obrigado por executar o meu script",
                "expression": "idle",
                "delay": 1000,
            },
            {
                "text": "Eu me chamo <span class='text-green text-bold'>BOH!</span>",
                "expression": "idle",
                "delay": 750,
            },
            {"text": "He He", "expression": "open mouth", "delay": 750},
            {"text": "Sabe...", "expression": "idle", "delay": 750},
            {
                "text": "Tipo,",
                "expression": "idle",
                "static": "Tipo, <span class='text-bold'>ROH</span>",
                "delay": 500,
            },
            {
                "text": "",
                "expression": "idle",
                "static": "Tipo, <span class='text-bold'>ROH-</span><span class='text-bold text-green'>BOH</span>",
                "delay": 500,
            },
        ]

    def get_list_models(self):
        """Retorna os modelos ASCII da lista"""
        return {
            "basic": "None × ‹[H]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[T]» × None",
            "swapped": "None × ‹[T]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            "colored": "None × ‹<span class='text-red'>[T]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹<span class='text-blue'>[H]</span>» × None",
            "two_heads": "None × ‹<span class='text-blue'>[H]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹<span class='text-blue'>[H]</span>» × None",
        }

    def get_aux_ascii(self, state="normal"):
        """Retorna ASCII art do personagem AUX em diferentes estados"""
        aux_states = {
            "normal": r"""
       __
   _  |@@|
  / \ \--/ __
  ) O|----|  |   __
 / / \ }{ /\ )_ / _\
 )/  /\__/\ \__O (__
|/  (--/\--)    \__/
/   _)(  )(_
   `---''---`
""",
            "holding": r"""
        __
(_|)   |@@|
 \ \__ \--/ __ 
  \o__|----|  |   __
      \ }{ /\ )_ / _\
      /\__/\ \__O (<span class='text-red'>[T]</span>
      (--/\--)    \__/
      _)(  )(_
     `---''---`
""",
            "waving": r"""
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\
       /\__/\ \__O (<span class='text-red'>[T]</span>
      (--/\--)    \__/
      _)(  )(_
     `---''---`
""",
        }
        return aux_states.get(state, aux_states["normal"])

    def colorize_arrows(self, text):
        """Coloriza as setas no texto"""
        text = text.replace("‹", "<span class='arrow-orange'>‹</span>")
        text = text.replace("›", "<span class='arrow-orange'>›</span>")
        text = text.replace("»", "<span class='arrow-blue'>»</span>")
        text = text.replace("«", "<span class='arrow-blue'>«</span>")
        return text

    def get_messages(self):
        """Retorna mensagens padrão para diferentes situações"""
        return {
            "timeout": "Poxa, tá difícil assim de encontrar a tecla?",
            "invalid": "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
            "negative": "Não?",
            "retry": "Pera, deixa eu repetir",
            "positive": "Show de bola!",
            "english_positive": "Sim, inglês também tá valendo...",
        }
