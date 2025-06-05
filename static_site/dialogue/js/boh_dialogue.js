/**
 * BOH! Dialogue System - Sistema completo de diálogo e animação
 * Versão consolidada baseada no _Boh.py original
 */

class BOHDialogue {
  constructor() {
    // Estado do sistema
    this.currentStep = 0;
    this.isTyping = false;
    this.isPaused = false;
    this.isWaitingForResponse = false;
    this.isWaitingForName = false;
    this.soundEnabled = true;
    this.userName = '';
    this.keyboardEventsSetup = false;

    // Dados carregados do backend
    this.dialogueData = null;
    this.expressions = {};
    this.listModels = {};
    this.auxArt = {};
    this.messages = {};

    // Controles de animação
    this.currentTimeout = null;
    this.currentAudio = null;
    this.audioFiles = [];

    // Elementos DOM - inicializar após DOM carregar
    this.elements = {};    // Configurações
    this.config = {
      typingSpeed: 30, // Mais rápido (era 80)
      expressionChangeSpeed: 50, // Mais rápido (era 100)
      audioVolume: 0.7,
      sfxPath: '/static/dialogue/sfx/'
    };

    console.log('BOHDialogue inicializado');
  }

  /**
   * Inicializa elementos DOM
   */
  initElements() {
    this.elements = {
      expression: document.getElementById('boh-expression'),
      dialogueText: document.getElementById('dialogue-text'),
      staticDisplay: document.getElementById('static-display'),
      asciiDisplay: document.getElementById('ascii-display'),
      auxDisplay: document.getElementById('aux-display'),
      responseArea: document.getElementById('response-area'),
      nameInput: document.getElementById('name-input'),
      soundIndicator: document.getElementById('sound-indicator'),
      loadingScreen: document.getElementById('loading-screen')
    };
  }

  /**
   * Inicializa o sistema de diálogo
   */
  async initDialogue() {
    try {
      this.initElements();
      this.setupKeyboardControls();
      await this.loadDialogueData();
      await this.preloadAudio();
      this.startDialogue();
    } catch (error) {
      console.error('Erro ao inicializar o diálogo:', error);
      this.showError('Erro ao carregar o diálogo do BOH!');
    }
  }

  /**
   * Carrega todos os dados do diálogo do backend
   */
  async loadDialogueData() {
    try {
      const response = await fetch('/api/dialogue/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'get_all_data' })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      this.dialogueSequence = data.dialogue_sequence || [];
      this.expressions = data.expressions || {};
      this.listModels = data.list_models || {};
      this.auxArt = data.aux_art || {};
      this.messages = data.messages || {};

      console.log('Dados do diálogo carregados:', data);
    } catch (error) {
      console.error('Erro ao carregar dados do diálogo:', error);
      throw error;
    }
  }
  /**
   * Pré-carrega arquivos de áudio
   */
  async preloadAudio() {
    const audioPromises = [];

    for (let i = 1; i <= 8; i++) {
      const audio = new Audio(`${this.config.sfxPath}p03voice_calm%23${i}.wav`);
      audio.preload = 'auto';
      audio.volume = this.config.audioVolume;
      this.audioFiles.push(audio);

      audioPromises.push(new Promise((resolve) => {
        audio.addEventListener('canplaythrough', resolve);
        audio.addEventListener('error', resolve);
      }));
    }

    await Promise.all(audioPromises);
    console.log('Áudios pré-carregados');
  }

  /**
   * Inicia a sequência de diálogo
   */
  async startDialogue() {
    this.currentStep = 0;
    await this.processCurrentStep();
  }

  /**
   * Processa o passo atual do diálogo
   */
  async processCurrentStep() {
    try {
      const response = await fetch('/api/dialogue/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'get_dialogue_item',
          step: this.currentStep
        })
      });

      const data = await response.json();
      const item = data.item;

      if (item) {
        await this.executeDialogueItem(item);
      } else {
        this.completeDialogue();
      }
    } catch (error) {
      console.error('Erro ao processar step:', error);
    }
  }

  /**
   * Executa um item específico do diálogo
   */
  async executeDialogueItem(item) {
    console.log('Executando item:', item);

    // Atualiza expressão se especificada
    if (item.expression) {
      this.updateExpression(item.expression);
    }

    // Aguarda delay se especificado
    if (item.delay) {
      await this.wait(item.delay);
    }    // Processa baseado no tipo
    switch (item.type) {
      case 'text':
        await this.processTextItem(item);
        break;
      case 'name_input':
        await this.processNameInputItem(item);
        return; // Não avança automaticamente
      case 'name_play':
        await this.processNamePlayItem(item);
        break;
      case 'laughter':
        await this.processLaughterItem(item);
        break;
      case 'response':
        await this.processResponseItem(item);
        return; // Não avança automaticamente
      case 'display':
        await this.processDisplayItem(item);
        break;
      case 'static_update':
        await this.processStaticUpdateItem(item);
        break;
      default:
        console.warn('Tipo de item desconhecido:', item.type);
    }

    // Avança para o próximo step automaticamente (exceto inputs)
    if (!this.isWaitingForResponse && !this.isWaitingForName) {
      this.advanceStep();
    }
  }

  /**
   * Processa item de texto
   */
  async processTextItem(item) {
    if (item.text) {
      await this.typeText(item.text, this.config.typingSpeed);
    }
  }

  /**
   * Processa item de input de nome
   */
  async processNameInputItem(item) {
    if (item.text) {
      await this.typeText(item.text, this.config.typingSpeed);
    }
    this.showNameInput(true);
    this.isWaitingForName = true;
  }

  /**
   * Processa item de resposta
   */
  async processResponseItem(item) {
    if (item.text) {
      await this.typeText(item.text, this.config.typingSpeed);
    }
    this.showResponseControls(true);
    this.isWaitingForResponse = true;
  }

  /**
   * Processa item de display
   */
  async processDisplayItem(item) {
    if (item.ascii_type) {
      this.showASCII(item.ascii_type);
    }
    if (item.aux_state) {
      this.showAux(item.aux_state);
    }
    if (item.text) {
      await this.typeText(item.text, this.config.typingSpeed);
    }
  }
  /**
   * Processa atualização de texto estático
   */
  async processStaticUpdateItem(item) {
    if (item.static_text) {
      this.updateStaticDisplay(item.static_text);
    }
    if (item.text) {
      await this.typeText(item.text, this.config.typingSpeed);
    }
  }

  /**
   * Processa item de name_play (digitação do nome)
   */
  async processNamePlayItem(item) {
    if (item.text) {
      await this.typeText(item.text, this.config.typingSpeed);
    }
    // Simula digitação aleatória do nome
    if (item.random_chars && item.count) {
      const chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'];
      for (let i = 0; i < item.count; i++) {
        const randomChar = chars[Math.floor(Math.random() * chars.length)];
        await this.typeText(randomChar, 200);
        await this.wait(100);
      }
    }
  }

  /**
   * Processa item de laughter (risada)
   */
  async processLaughterItem(item) {
    const laughText = item.text || "He";
    const count = item.count || 5;
    const delay = item.delay || 100;

    for (let i = 0; i < count; i++) {
      await this.typeText(laughText, 50);
      await this.wait(delay);
      if (i < count - 1) {
        // Adiciona espaço entre risadas
        if (this.elements.dialogueText) {
          this.elements.dialogueText.innerHTML += " ";
        }
      }
    }
  }

  /**
   * Digita texto com efeito de máquina de escrever
   */
  async typeText(text, speed = 100) {
    return new Promise((resolve) => {
      if (this.isPaused) {
        this.currentTimeout = setTimeout(() => this.typeText(text, speed).then(resolve), 100);
        return;
      }

      this.isTyping = true;
      const textElement = this.elements.dialogueText;
      if (!textElement) {
        console.error('Elemento dialogue-text não encontrado!');
        resolve();
        return;
      }

      // Coloriza setas se necessário
      this.colorizeText(text).then((colorizedText) => {
        textElement.innerHTML = '';
        let i = 0;

        const typeNextChar = () => {
          if (this.isPaused) {
            this.currentTimeout = setTimeout(typeNextChar, 100);
            return;
          }

          if (i < colorizedText.length) {
            textElement.innerHTML += colorizedText[i];
            i++;

            // Toca som ocasionalmente
            if (Math.random() > 0.7) {
              this.playTypingSound();
            }

            this.currentTimeout = setTimeout(typeNextChar, speed);
          } else {
            this.isTyping = false;
            resolve();
          }
        };

        typeNextChar();
      });
    });
  }

  /**
   * Coloriza texto com setas
   */
  async colorizeText(text) {
    try {
      const response = await fetch('/api/dialogue/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'colorize_arrows',
          text: text
        })
      });

      const data = await response.json();
      return data.colorized_text || text;
    } catch (error) {
      console.error('Erro ao colorizar texto:', error);
      return text;
    }
  }

  /**
   * Toca som de digitação
   */
  playTypingSound() {
    if (!this.soundEnabled || this.audioFiles.length === 0) return;

    const randomAudio = this.audioFiles[Math.floor(Math.random() * this.audioFiles.length)];
    if (randomAudio) {
      randomAudio.currentTime = 0;
      randomAudio.play().catch(() => {
        // Ignora erros de áudio
      });
    }
  }

  /**
   * Atualiza a expressão do BOH
   */
  updateExpression(expressionType) {
    if (this.elements.expression) {
      const expressions = this.expressions[expressionType] || this.expressions.idle || ['[ ▀ ¸ ▀]'];
      const randomExpression = expressions[Math.floor(Math.random() * expressions.length)];
      this.elements.expression.textContent = randomExpression;
    }
  }

  /**
   * Mostra ASCII art
   */
  showASCII(type) {
    if (this.elements.asciiDisplay && this.listModels[type]) {
      const model = this.listModels[type];
      this.elements.asciiDisplay.innerHTML = `<pre>${model}</pre>`;
      this.elements.asciiDisplay.style.display = 'block';
    }
  }

  /**
   * Mostra arte do AUX
   */
  showAux(state) {
    if (this.elements.auxDisplay && this.auxArt[state]) {
      const art = this.auxArt[state];
      this.elements.auxDisplay.innerHTML = `<pre>${art}</pre>`;
      this.elements.auxDisplay.style.display = 'block';
    }
  }

  /**
   * Atualiza display de texto estático
   */
  updateStaticDisplay(text) {
    if (this.elements.staticDisplay) {
      this.elements.staticDisplay.innerHTML = `<pre>${text}</pre>`;
      this.elements.staticDisplay.style.display = 'block';
    }
  }

  /**
   * Limpa display de texto estático
   */
  clearStaticDisplay() {
    if (this.elements.staticDisplay) {
      this.elements.staticDisplay.innerHTML = '';
      this.elements.staticDisplay.style.display = 'none';
    }
  }

  /**
   * Mostra/esconde controles de resposta
   */
  showResponseControls(show) {
    if (this.elements.responseArea) {
      this.elements.responseArea.style.display = show ? 'block' : 'none';
    }
  }

  /**
   * Mostra/esconde input de nome
   */
  showNameInput(show) {
    if (this.elements.nameInput) {
      this.elements.nameInput.style.display = show ? 'block' : 'none';
      if (show) {
        // Criar input se não existir
        if (!document.getElementById('name-input-field')) {
          this.elements.nameInput.innerHTML = `
            <div class="input-field">
              <input type="text" id="name-input-field" placeholder="Digite seu nome..." maxlength="20">
              <button onclick="window.bohDialogue.submitName()">Enviar</button>
              <button onclick="window.bohDialogue.cancelNameInput()">Cancelar</button>
            </div>
          `;
        }
        const inputField = document.getElementById('name-input-field');
        if (inputField) {
          inputField.focus();
        }
      }
    }
  }

  /**
   * Mostra mensagem de erro
   */
  showError(message) {
    if (this.elements.dialogueText) {
      this.elements.dialogueText.innerHTML = `<span class="error">${message}</span>`;
    }
  }

  /**
   * Avança para o próximo passo
   */
  advanceStep() {
    this.currentStep++;
    setTimeout(() => this.processCurrentStep(), 100);
  }

  /**
   * Manipula pressionamento de teclas
   */
  handleKeyPress(event) {
    const key = event.key.toLowerCase();

    if (this.isWaitingForResponse) {
      if (key === 's' || key === 'y') {
        this.sendResponse('positive');
      } else if (key === 'n') {
        this.sendResponse('negative');
      }
    }

    if (this.isWaitingForName && key === 'enter') {
      this.submitName();
    }

    // Tecla de espaço para pausar/retomar
    if (key === ' ' && !this.isWaitingForName) {
      event.preventDefault();
      this.togglePause();
    }
  }

  /**
   * Envia resposta
   */
  sendResponse(response) {
    if (!this.isWaitingForResponse) return;

    this.isWaitingForResponse = false;
    this.showResponseControls(false);

    console.log('Resposta enviada:', response);

    // Avança para próximo step baseado na resposta
    this.advanceStep();
  }

  /**
   * Submete nome do usuário
   */
  async submitName() {
    if (!this.isWaitingForName) return;

    const inputField = document.getElementById('name-input-field');
    if (!inputField) return;

    const name = inputField.value.trim();

    if (name.length < 2) {
      await this.typeText("Nome muito curto!", this.config.typingSpeed);
      await this.wait(1000);
      inputField.value = '';
      inputField.focus();
      return;
    }

    this.userName = name;
    this.isWaitingForName = false;
    this.showNameInput(false);

    console.log('Nome submetido:', this.userName);

    // Salva nome no backend
    try {
      await fetch('/api/dialogue/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'set_user_name',
          name: this.userName
        })
      });
    } catch (error) {
      console.error('Erro ao salvar nome:', error);
    }

    this.advanceStep();
  }

  /**
   * Cancela input de nome
   */
  cancelNameInput() {
    if (!this.isWaitingForName) return;

    this.userName = 'Humano';
    this.isWaitingForName = false;
    this.showNameInput(false);

    console.log('Input de nome cancelado');
    this.advanceStep();
  }

  /**
   * Alterna som ligado/desligado
   */
  toggleSound() {
    this.soundEnabled = !this.soundEnabled;

    if (this.elements.soundIndicator) {
      this.elements.soundIndicator.textContent = this.soundEnabled ? '🔊' : '🔇';
    }

    if (!this.soundEnabled && this.currentAudio) {
      this.currentAudio.pause();
    }

    console.log('Som:', this.soundEnabled ? 'ligado' : 'desligado');
  }

  /**
   * Alterna pausa
   */
  togglePause() {
    this.isPaused = !this.isPaused;

    if (this.isPaused) {
      if (this.currentTimeout) {
        clearTimeout(this.currentTimeout);
      }
      if (this.currentAudio) {
        this.currentAudio.pause();
      }
    } else {
      // Retoma a partir do estado atual
      this.processCurrentStep();
    }

    console.log('Pausa:', this.isPaused ? 'ativada' : 'desativada');
  }

  /**
   * Configura controles de teclado
   */
  setupKeyboardControls() {
    if (this.keyboardEventsSetup) return;

    document.addEventListener('keydown', (event) => {
      this.handleKeyPress(event);
    });

    this.keyboardEventsSetup = true;
    console.log('Controles de teclado configurados');
  }

  /**
   * Reseta o diálogo
   */
  reset() {
    this.currentStep = 0;
    this.userName = '';
    this.isPaused = false;
    this.isTyping = false;
    this.isWaitingForResponse = false;
    this.isWaitingForName = false;

    if (this.currentTimeout) {
      clearTimeout(this.currentTimeout);
      this.currentTimeout = null;
    }

    if (this.currentAudio) {
      this.currentAudio.pause();
    }

    this.clearStaticDisplay();
    this.showResponseControls(false);
    this.showNameInput(false);

    if (this.elements.dialogueText) {
      this.elements.dialogueText.innerHTML = '';
    }

    if (this.elements.asciiDisplay) {
      this.elements.asciiDisplay.style.display = 'none';
    }

    if (this.elements.auxDisplay) {
      this.elements.auxDisplay.style.display = 'none';
    }

    console.log('BOHDialogue resetado');
  }

  /**
   * Completa o diálogo
   */
  completeDialogue() {
    console.log('Diálogo completado!');

    if (this.elements.dialogueText) {
      this.elements.dialogueText.innerHTML = `
        <div class="final-art">
          <pre>
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
          </pre>
          <div class="completion-message">
            <h3>Obrigado por conversar comigo!</h3>
            <p>Pressione Ctrl+R para reiniciar</p>
          </div>
        </div>
      `;
    }
  }

  /**
   * Utilitário para aguardar
   */
  wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Funções globais para compatibilidade
window.sendResponse = function (response) {
  if (window.bohDialogue) {
    window.bohDialogue.sendResponse(response);
  }
};

window.submitName = function () {
  if (window.bohDialogue) {
    window.bohDialogue.submitName();
  }
};

// Instância global
window.bohDialogue = null;

// Inicialização automática
document.addEventListener('DOMContentLoaded', function () {
  window.bohDialogue = new BOHDialogue();
  console.log('BOHDialogue instanciado globalmente');
});

// Exporta para uso global
window.BOHDialogue = BOHDialogue;
