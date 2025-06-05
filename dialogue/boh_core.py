"""
BOH! Core - Sistema completo de diálogo e animação
Versão consolidada baseada em _Boh.py original
"""

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


class BOHCore:
    """Sistema completo de diálogo com BOH! - Versão consolidada"""

    def __init__(self):
        self.current_step = 0
        self.user_name = ""
        self.paused = False
        self.completed = False
        self.expressions = self._init_expressions()
        self.dialogue_sequence = self._init_dialogue_sequence()
        self.list_models = self._init_list_models()
        self.aux_art = self._init_aux_art()
        self.messages = self._init_messages()

    def _init_expressions(self):
        """Inicializa as expressões do BOH"""
        return {
            "idle": [
                "[ ▀ ¸ ▀]", "[ ▀ ° ▀]", "[ ▀ ■ ▀]", "[ ▀ ─ ▀]", 
                "[ ▀ ~ ▀]", "[ ▀ ▄ ▀]", "[ ▀ ¬ ▀]", "[ ▀ · ▀]", "[ ▀ _ ▀]"
            ],
            "pokerface": ["[ ▀ ‗ ▀]", "[ ▀ ¯ ▀]", "[ ▀ ¡ ▀]"],
            "thinking": ["[ ─ ´ ─]", "[ ─ » ─]"],
            "open_mouth": ["[ ▀ ß ▀]", "[ ▀ █ ▀]"],
            "annoyed": ["[ ▀ ı ▀]", "[ ▀ ^ ▀]"],
            "looking_down": ["[ ▄ . ▄]", "[ ▄ _ ▄]", "[ ▄ ₒ ▄]", "[ ▄ ‗ ▄]"],
        }

    def _init_list_models(self):
        """Inicializa os modelos ASCII das listas"""
        return {
            "basic": "None × ‹[H]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[T]» × None",
            "swapped": "None × ‹[T]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            "colored": "None × ‹<span class='text-red'>[T]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹<span class='text-blue'>[H]</span>» × None",
            "two_heads": "None × ‹<span class='text-blue'>[H]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹<span class='text-blue'>[H]</span>» × None",
            "highlighted_tail": "None × ‹<span class='text-red'>[T]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            "arrows_inverted": "None × «<span class='text-red'>[T]</span>› ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            "node_highlighted": "None × «[T]› ‹<span class='text-red'>[]</span>» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            "node_inverted": "None × «[T]› «<span class='text-red'>[]</span>» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None",
            "progression_1": "None × «[T]› «[]› ‹<span class='text-red'>[]</span>» ... ‹[]» ‹[]» ‹[H]» × None",
            "progression_2": "None × «[T]› «[]› «[]› ... ‹<span class='text-red'>[]</span>» ‹[]» ‹[H]» × None",
            "final_inversion": "None × «[T]› «[]› «[]› ... «[]› «[]› «<span class='text-red'>[H]</span>» × None",
            "complete": "None × «[T]› «[]› «[]› ... «[]› «[]› «[H]› <span class='text-red'>× <span class='text-purple'>None</span></span>"
        }

    def _init_aux_art(self):
        """Inicializa a arte ASCII do personagem AUX"""
        return {
            "normal": """       __
   _  |@@|
  / \\ \\--/ __
  ) O|----|  |   __
 / / \\ }{ /\\ )_ / _\\
 )/  /\\__/\\ \\__O (__
|/  (--/\\--)    \\__/
/   _)(  )(_
   `---''---`""",

            "holding_tail": """       __
   _  |@@|
  / \\ \\--/ __
  ) O|----|  |   __
 / / \\ }{ /\\ )_ / _\\
 )/  /\\__/\\ \\__O (<span class='text-red'>[T]</span>
|/  (--/\\--)    \\__/
/   _)(  )(_
   `---''---`""",

            "waving": """        __
 _(\\    |@@|
(__/\\__ \\--/ __
   \\___|----|  |   __
       \\ }{ /\\ )_ / _\\
       /\\__/\\ \\__O (<span class='text-red'>[T]</span>
      (--/\\--)    \\__/
      _)(  )(_
     `---''---`""",

            "holding_arrow": """       __
   _  |@@|
  / \\ \\--/ __
  ) O|----|  |   __
 / / \\ }{ /\\ )_ / _\\
 )/  /\\__/\\ \\__O (‹_
|/  (--/\\--)    \\__/
/   _)(  )(_
   `---''---`""",

            "goodbye": """        __
(_|)   |@@|
 \\ \\__ \\--/ __ 
  \\o__|----|  |   __
      \\ }{ /\\ )_ / _\\
      /\\__/\\ \\__O (__
     (--/\\--)    \\__/
     _)(  )(_
    `---''---`"""
        }

    def _init_messages(self):
        """Inicializa mensagens do sistema"""
        return {
            "timeout": "Poxa, tá difícil assim de encontrar a tecla?",
            "invalid": "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
            "negative": "Não?",
            "retry": "Pera, deixa eu repetir",
            "positive": "Show de bola!",
            "english_positive": "Sim, inglês também tá valendo...",
            "recognition_retry": "Como assim pô? Me esforcei tanto desenhar ela...",
            "understanding_negative": "Tudo bem então, vamos fazer o seguinte...",
            "pause_message": "Tô aqui pertinho, quando quiser continuar é só chamar!"
        }

    def _init_dialogue_sequence(self):
        """Inicializa a sequência completa de diálogo"""
        return [
            # Sequência de abertura
            {
                "id": "greeting",
                "type": "text",
                "text": "Oi, tudo bem?",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "introduction",
                "type": "text", 
                "text": "Muito obrigado por executar o meu script",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "name_reveal",
                "type": "text",
                "text": "Eu me chamo <span class='text-green text-bold'>BOH!</span>",
                "expression": "idle",
                "delay": 750
            },
            {
                "id": "laugh",
                "type": "text",
                "text": "He He",
                "expression": "open_mouth",
                "delay": 750
            },
            {
                "id": "buildup",
                "type": "text",
                "text": "Sabe...",
                "expression": "thinking",
                "delay": 750
            },
            {
                "id": "name_play_sequence",
                "type": "name_play",
                "steps": [
                    "Tipo,",
                    "Tipo, <span class='text-bold'>ROH</span>",
                    "Tipo, <span class='text-bold'>ROH-</span><span class='text-bold text-green'>BOH</span>"
                ],
                "expression": "idle",
                "delay": 500
            },
            {
                "id": "laughter_sequence",
                "type": "laughter",
                "count": 10,
                "expression": "open_mouth",
                "delay": 50
            },
            {
                "id": "self_aware",
                "type": "text",
                "text": "Ai ai, sou meio comédia às vezes, sabe?",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "transition",
                "type": "text",
                "text": "Mas, enfim,",
                "expression": "idle",
                "delay": 500
            },
            {
                "id": "ask_name",
                "type": "input_name",
                "text": "E você, como se chama?",
                "expression": "idle",
                "delay": 500
            },

            # Sequência da conversa sobre lista
            {
                "id": "time_constraint",
                "type": "text",
                "text": "Olha olha olha, na verdade, eu não tenho muito tempo...",
                "expression": "pokerface",
                "delay": 1500
            },
            {
                "id": "apology",
                "type": "text",
                "text": "Me desculpa! Você parece ser uma pessoa muito legal, mas...",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "topic_intro",
                "type": "text",
                "text": "A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓",
                "expression": "looking_down",
                "delay": 200
            },
            {
                "id": "show_list",
                "type": "display",
                "text": "Reconhece?",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1500
            },
            {
                "id": "response_problem",
                "type": "text",
                "text": "Ih, verdade, cê não consegue me responder, né?",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "thinking_sequence",
                "type": "thinking_dots",
                "count": 3,
                "expression": "thinking",
                "delay": 500
            },
            {
                "id": "solution",
                "type": "text",
                "text": "Já sei!",
                "expression": "open_mouth",
                "delay": 500
            },
            {
                "id": "response_intro",
                "type": "text",
                "text": "Aqui, toma",
                "show_controls": True,
                "expression": "idle",
                "delay": 1500
            },

            # Instruções sobre controles
            {
                "id": "explain_controls_1",
                "type": "text",
                "text": "Agora sempre que eu te perguntar algo,",
                "show_controls": True,
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "explain_controls_2",
                "type": "text",
                "text": "Você pode responder digitando",
                "show_controls": True,
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "explain_controls_3",
                "type": "text",
                "text": "A letra destacada que achar mais cabível.",
                "show_controls": True,
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "first_question",
                "type": "response",
                "text": "Entendeu, né?",
                "show_controls": True,
                "expression": "idle"
            },

            # Continuação do tópico sobre listas
            {
                "id": "back_to_topic",
                "type": "text",
                "text": "Enfim, voltando ao assunto...",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "list_recognition",
                "type": "response",
                "text": "Reconhece isso aqui, né?",
                "ascii": "basic",
                "expression": "looking_down",
                "alt_responses": {
                    "negative": [
                        "Não?",
                        "Como assim pô? Me esforcei tanto desenhar ela...",
                        "É uma lista! A estrutura de dados!",
                        "Tá vendo?"
                    ]
                }
            },
            {
                "id": "list_explanation",
                "type": "text",
                "text": "Pois é, uma lista.",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },

            # Explicação sobre estrutura de dados
            {
                "id": "list_challenge_intro",
                "type": "text",
                "text": "Bom, como você já sabe... a lista é uma estrutura de dados",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "list_challenge_specific",
                "type": "text",
                "text": "Mas tô aqui pra discutir um desafio específico relacionado a ela...",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "challenge_reveal",
                "type": "text",
                "text": "O desafio é o seguinte:",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "inversion_question",
                "type": "text",
                "text": "Que tal inverter uma lista?",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "efficiency_question",
                "type": "text",
                "text": "Ou melhor, qual seria a maneira mais eficiente de fazer isso?",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "multiple_ways",
                "type": "text",
                "text": "Bom, a gente pode fazer isso de várias maneiras...",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "first_thought",
                "type": "text",
                "text": "Mas, acho que a primeira coisa que vem à cabeça é...",
                "ascii": "basic",
                "expression": "idle",
                "delay": 1000
            },

            # Demonstração da troca Head/Tail
            {
                "id": "swap_demo",
                "type": "text",
                "text": "Fazer isso, né?",
                "ascii": "colored",
                "expression": "idle",
                "delay": 1500
            },
            {
                "id": "swap_explanation_1",
                "type": "text",
                "text": "Trocando Head e Tail, o que era a \"frente\" da lista,",
                "ascii": "swapped",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "swap_explanation_2",
                "type": "text",
                "text": "Passa a ser o \"final\" dela, e vice-versa.",
                "ascii": "swapped",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "but_wait",
                "type": "text",
                "text": "Mas, pera aí! Como isso acontece exatamente?",
                "ascii": "swapped",
                "expression": "thinking",
                "delay": 1000
            },
            {
                "id": "assignment_example",
                "type": "text",
                "text": "Digamos que, a gente iguale <span class='text-red'>Tail</span> a <span class='text-blue'>Head</span>",
                "ascii": "swapped",
                "expression": "idle",
                "delay": 1000
            },

            # Problema dos dois Heads
            {
                "id": "two_heads_problem",
                "type": "text",
                "text": "Eita... agora temos duas Heads!",
                "ascii": "two_heads",
                "expression": "open_mouth",
                "delay": 1500
            },
            {
                "id": "assignment_explanation_1",
                "type": "text",
                "text": "Isso porque <span class='text-red'>Tail</span> = <span class='text-blue'>Head</span> não é uma troca de valores,",
                "ascii": "two_heads",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "assignment_explanation_2",
                "type": "text",
                "text": "Só estamos dizendo que <span class='text-red'>Tail</span> agora recebe",
                "ascii": "two_heads",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "assignment_explanation_3",
                "type": "text",
                "text": "O objeto contido dentro de <span class='text-blue'>Head</span>.",
                "ascii": "two_heads",
                "expression": "idle",
                "delay": 1000
            },

            # Analogia da estante
            {
                "id": "bookshelf_analogy_1",
                "type": "text",
                "text": "Mas assim como abrir espaço numa estante pra guardar um livro,",
                "ascii": "two_heads",
                "expression": "thinking",
                "delay": 1500
            },
            {
                "id": "bookshelf_analogy_2",
                "type": "text",
                "text": "Não significa que haverá espaço para guardar novamente",
                "ascii": "two_heads",
                "expression": "thinking",
                "delay": 1000
            },
            {
                "id": "bookshelf_analogy_3",
                "type": "text",
                "text": "O antigo livro que tiramos para guardar o livro novo...",
                "ascii": "two_heads",
                "expression": "thinking",
                "delay": 1000
            },
            {
                "id": "aux_need_1",
                "type": "text",
                "text": "O que significa que precisamos salvar",
                "ascii": "two_heads",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "aux_need_2",
                "type": "text",
                "text": "O antigo valor de Tail, antes de trocá-lo por Head.",
                "ascii": "two_heads",
                "expression": "idle",
                "delay": 1500
            },

            # Introdução do AUX
            {
                "id": "aux_introduction",
                "type": "text",
                "text": "Meu mano aqui se chama AUX,",
                "aux": "normal",
                "expression": "idle",
                "delay": 1250
            },
            {
                "id": "aux_greeting",
                "type": "text",
                "text": "Tudo bem contigo, patrão?",
                "aux": "normal",
                "expression": "idle",
                "delay": 750
            },
            {
                "id": "aux_offer",
                "type": "text",
                "text": "Ele se ofereceu pra guardar o valor de Tail",
                "aux": "holding_tail",
                "expression": "idle",
                "delay": 1000
            },
            {
                "id": "aux_purpose",
                "type": "text",
                "text": "Pra que a gente não perca na hora de trocar...",
                "aux": "waving",
                "expression": "idle",
                "delay": 1000
            }

            # ... continuação será implementada nos próximos passos
        ]

    def colorize_arrows(self, text):
        """Coloriza as setas no texto"""
        if not text:
            return text
        
        # Substituir setas simples (laranja)
        text = text.replace("‹", "<span class='text-orange'>‹</span>")
        text = text.replace("›", "<span class='text-orange'>›</span>")
        
        # Substituir setas duplas (azul)
        text = text.replace("»", "<span class='text-blue'>»</span>")
        text = text.replace("«", "<span class='text-blue'>«</span>")
        
        return text

    def get_expression(self, expr_type="idle"):
        """Retorna uma expressão do tipo especificado"""
        expressions = self.expressions.get(expr_type, self.expressions["idle"])
        return choice(expressions)

    def get_list_model(self, model_type="basic"):
        """Retorna um modelo de lista específico"""
        return self.list_models.get(model_type, self.list_models["basic"])

    def get_aux_art(self, state="normal"):
        """Retorna arte ASCII do AUX em estado específico"""
        return self.aux_art.get(state, self.aux_art["normal"])

    def get_current_dialogue_item(self):
        """Retorna o item atual da sequência de diálogo"""
        if self.current_step < len(self.dialogue_sequence):
            return self.dialogue_sequence[self.current_step]
        return None

    def advance_step(self):
        """Avança para o próximo passo do diálogo"""
        self.current_step += 1
        return self.get_current_dialogue_item()

    def set_user_name(self, name):
        """Define o nome do usuário"""
        self.user_name = name.strip()

    def get_message(self, message_type):
        """Retorna uma mensagem específica do sistema"""
        return self.messages.get(message_type, "")

    def to_json(self):
        """Serializa o estado atual para JSON"""
        return {
            "current_step": self.current_step,
            "user_name": self.user_name,
            "paused": self.paused,
            "completed": self.completed
        }

    def from_json(self, data):
        """Carrega estado a partir de dados JSON"""
        self.current_step = data.get("current_step", 0)
        self.user_name = data.get("user_name", "")
        self.paused = data.get("paused", False)
        self.completed = data.get("completed", False)

    def reset(self):
        """Reseta o estado do diálogo"""
        self.current_step = 0
        self.user_name = ""
        self.paused = False
        self.completed = False

    def get_all_data(self):
        """Retorna todos os dados necessários para o frontend"""
        return {
            "expressions": self.expressions,
            "dialogue_sequence": self.dialogue_sequence,
            "list_models": self.list_models,
            "aux_art": self.aux_art,
            "messages": self.messages,
            "current_state": self.to_json()
        }
