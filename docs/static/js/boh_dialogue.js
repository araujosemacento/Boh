/**
 * BOH! Dialogue System - Sistema completo de diálogo e animação
 * Versão consolidada baseada no _Boh.py original
 */

/**
 * Classe para selecionar itens aleatórios sem repetição
 * Mimetiza o comportamento do ShuffledSelector do Python
 */
class ShuffledSelector {
  constructor(items) {
    this.items = [...items]; // Cria uma cópia da lista de itens
    this.availableIndices = [...Array(items.length).keys()]; // Índices disponíveis
  }

  select() {
    // Se não houver índices disponíveis, recarrega todos
    if (this.availableIndices.length === 0) {
      this.availableIndices = [...Array(this.items.length).keys()];
    }

    // Escolhe um índice aleatório dos disponíveis
    const randomIndex = Math.floor(Math.random() * this.availableIndices.length);
    const selectedIndex = this.availableIndices[randomIndex];

    // Remove o índice escolhido da lista de disponíveis
    this.availableIndices.splice(randomIndex, 1);

    // Retorna o item correspondente ao índice
    return this.items[selectedIndex];
  }
}

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

    // Configuração da API baseada no ambiente
    this.apiBaseUrl = this.getApiUrl();

    // Dados carregados do backend
    this.dialogueData = null;
    this.expressions = {};
    this.listModels = {};
    this.auxArt = {};
    this.messages = {};    // Controles de animação
    this.currentTimeout = null;

    // Sistema de áudio melhorado - mimetizando o comportamento do Python
    this.audioFiles = [];
    this.audioChannel = null; // Canal único de áudio (similar ao pygame)
    this.lastSoundTime = null; // Controle de tempo entre sons
    this.soundCooldown = 300; // 0.3 segundos como no Python
    this.availableAudioIndices = []; // Para seleção sem repetição (ShuffledSelector)

    // Elementos DOM - inicializar após DOM carregar
    this.elements = {};// Configurações
    this.config = {
      typingSpeed: 30, // Mais rápido (era 80)
      expressionChangeSpeed: 50, // Mais rápido (era 100)
      audioVolume: 0.7,
      sfxPath: '/static/dialogue/sfx/'
    }; console.log('BOHDialogue inicializado');

    // Executar testes de conectividade
    this.runConnectivityTests();
  }  /**
   * Executa testes de conectividade com o endpoint
   */
  async runConnectivityTests() {
    console.log('🔍 Iniciando testes de conectividade...');
    console.log(`📍 API Base URL: ${this.apiBaseUrl}`);

    // Atualizar indicador visual
    this.updateConnectionStatus('testing', 'Testando conectividade...');

    const results = {};

    // Teste 1: Verificar se o endpoint está respondendo
    console.log('🏥 Executando teste de saúde do endpoint...');
    results.health = await this.testEndpointHealth();

    // Teste 2: Verificar dados de diálogo
    console.log('💬 Executando teste de dados de diálogo...');
    results.data = await this.testDialogueData();

    // Teste 3: Verificar API de colorização
    console.log('🎨 Executando teste de colorização...');
    results.colorize = await this.testColorizeAPI();

    // Teste 4: Verificar recursos de áudio (opcional)
    console.log('🔊 Executando teste de recursos de áudio...');
    results.audio = await this.testAudioResources();

    // Relatório final
    console.log('📊 RELATÓRIO DE CONECTIVIDADE:');
    console.log(`   ✓ Saúde do Endpoint: ${results.health ? '✅ OK' : '❌ FALHOU'}`);
    console.log(`   ✓ Dados de Diálogo: ${results.data ? '✅ OK' : '❌ FALHOU'}`);
    console.log(`   ✓ API Colorização: ${results.colorize ? '✅ OK' : '❌ FALHOU'}`);
    console.log(`   ✓ Recursos de Áudio: ${results.audio ? '✅ OK' : '⚠️  OPCIONAL'}`);

    const criticalTests = results.health && results.data && results.colorize;
    const allTestsPassed = criticalTests && results.audio;

    // Atualizar status final
    this.updateConnectionStatus(
      criticalTests ? (allTestsPassed ? 'connected' : 'warning') : 'error',
      criticalTests ? (allTestsPassed ? 'Totalmente Conectado' : 'Conectado (sem áudio)') : 'Falha na Conectividade'
    );

    console.log(criticalTests ? '✅ Testes críticos aprovados - Sistema funcional' : '❌ Falha nos testes críticos - Sistema pode não funcionar');

    // Armazenar resultados para consulta posterior
    this.lastConnectivityTest = {
      timestamp: new Date().toISOString(),
      results: results,
      critical_passed: criticalTests,
      all_passed: allTestsPassed
    };

    // Esconder indicador após 15 segundos se tudo estiver OK
    if (criticalTests) {
      setTimeout(() => {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) statusElement.style.display = 'none';
      }, 15000);
    }

    return results;
  }
  /**
   * Testa se o endpoint principal está respondendo
   */
  async testEndpointHealth() {
    try {
      console.log('🏥 Testando saúde do endpoint...');

      const response = await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 5000 // 5 segundos
      });

      if (response.ok) {
        console.log('✅ Endpoint respondendo:', response.status, response.statusText);
        const data = await response.json();
        console.log('📊 Dados recebidos:', Object.keys(data));
        return true;
      } else {
        console.warn('⚠️  Endpoint com problema:', response.status, response.statusText);
        return false;
      }
    } catch (error) {
      console.error('❌ Erro ao conectar com endpoint:', error.message);
      console.error('📍 URL testada:', `${this.apiBaseUrl}/api/dialogue/`);

      // Informações adicionais para debug
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        console.error('🌐 Possível problema de CORS ou endpoint inacessível');
      }
      return false;
    }
  }

  /**
   * Testa carregamento de dados de diálogo
   */
  async testDialogueData() {
    try {
      console.log('💬 Testando carregamento de dados de diálogo...');

      const response = await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'get_dialogue_data'
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Dados de diálogo carregados com sucesso');
        console.log('📋 Estrutura dos dados:', {
          dialogue_steps: data.dialogue_data ? data.dialogue_data.length : 0,
          expressions: data.expressions ? Object.keys(data.expressions).length : 0,
          list_models: data.list_models ? Object.keys(data.list_models).length : 0,
          aux_art: data.aux_art ? Object.keys(data.aux_art).length : 0,
          messages: data.messages ? Object.keys(data.messages).length : 0
        });
        return true;
      } else {
        console.warn('⚠️  Problema ao carregar dados de diálogo:', response.status);
        return false;
      }
    } catch (error) {
      console.error('❌ Erro ao testar dados de diálogo:', error.message);
      return false;
    }
  }

  /**
   * Testa API de colorização de texto
   */
  async testColorizeAPI() {
    try {
      console.log('🎨 Testando API de colorização...');

      const testText = "→ Teste de colorização ←";
      const response = await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'colorize_arrows',
          text: testText
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ API de colorização funcionando');
        console.log('🎨 Texto original:', testText);
        console.log('🎨 Texto colorizado:', data.colorized_text);
        return true;
      } else {
        console.warn('⚠️  Problema na API de colorização:', response.status);
        return false;
      }
    } catch (error) {
      console.error('❌ Erro ao testar colorização:', error.message);
      return false;
    }
  }

  /**
   * Atualiza o indicador visual de status de conectividade
   */
  updateConnectionStatus(status, message) {
    const indicator = document.getElementById('connection-indicator');
    const apiUrl = document.getElementById('api-url-display');

    if (indicator) {
      indicator.textContent = message;
      indicator.style.color = status === 'connected' ? '#7ee787' :
        status === 'testing' ? '#f2cc60' : '#ff7b72';
    }

    if (apiUrl) {
      apiUrl.textContent = this.apiBaseUrl.replace('https://', '').replace('http://', '');
    }
  }

  /**
   * Testa conectividade com informações detalhadas para debug
   */
  async debugConnectivity() {
    console.log('🔧 Modo Debug - Informações detalhadas de conectividade:');
    console.log('🌍 Ambiente detectado:', {
      hostname: window.location.hostname,
      protocol: window.location.protocol,
      port: window.location.port,
      pathname: window.location.pathname
    });

    console.log('⚙️  Configuração da API:', {
      apiBaseUrl: this.apiBaseUrl,
      isGitHubPages: window.location.hostname.includes('github.io'),
      isLocalhost: ['localhost', '127.0.0.1'].includes(window.location.hostname),
      vercelApiUrl: window.VERCEL_API_URL
    });

    // Teste de conectividade básica
    try {
      const response = await fetch(this.apiBaseUrl, { method: 'HEAD' });
      console.log('🔗 Conectividade básica:', response.status === 200 ? 'OK' : 'PROBLEMA');
    } catch (error) {
      console.error('🔗 Conectividade básica: FALHOU -', error.message);
    }
  }
  /**
   * Determina a URL da API baseada no ambiente
   */
  getApiUrl() {
    const hostname = window.location.hostname;

    // Se estiver no GitHub Pages, usar API do Vercel
    if (hostname.includes('github.io')) {
      return window.VERCEL_API_URL || 'https://boh-dialogue-api.vercel.app';
    }

    // Se estiver em desenvolvimento local
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }

    // Se estiver no Vercel (fallback)
    return window.location.origin;
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
      const response = await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
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
  }  /**
   * Pré-carrega arquivos de áudio com sistema melhorado
   * Mimetiza o comportamento do _Boh.py
   */
  async preloadAudio() {
    // Limpa áudios anteriores se existirem
    if (this.audioFiles.length > 0) {
      this.audioFiles.forEach(audio => {
        try {
          audio.src = '';
          audio.load();
        } catch (error) {
          // Silencioso - erro esperado em alguns casos
        }
      });
      this.audioFiles.length = 0;
    }

    const audioPromises = [];

    for (let i = 1; i <= 8; i++) {
      const audio = new Audio(`${this.config.sfxPath}p03voice_calm%23${i}.wav`);
      audio.preload = 'auto';
      audio.volume = this.config.audioVolume;

      this.audioFiles.push(audio);

      audioPromises.push(new Promise((resolve) => {
        const handleReady = () => {
          audio.removeEventListener('canplaythrough', handleReady);
          audio.removeEventListener('error', handleError);
          resolve();
        };

        const handleError = () => {
          audio.removeEventListener('canplaythrough', handleReady);
          audio.removeEventListener('error', handleError);
          resolve(); // Resolve mesmo com erro para não travar
        };

        audio.addEventListener('canplaythrough', handleReady);
        audio.addEventListener('error', handleError);
      }));
    }

    await Promise.all(audioPromises);

    // Inicializa o ShuffledSelector com os áudios carregados
    this.soundSelector = new ShuffledSelector(this.audioFiles); console.log('Áudios pré-carregados com ShuffledSelector');
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
      const response = await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
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
    // CORREÇÃO: Evita execução sobrepostas se já estiver processando
    if (this.isTyping) {
      console.log('Ignorando execução sobrepostas - já está digitando');
      return;
    }

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

    // CORREÇÃO: Acumula o texto da risada em uma string para evitar múltiplas animações
    let fullLaughText = '';
    for (let i = 0; i < count; i++) {
      fullLaughText += laughText;
      if (i < count - 1) {
        fullLaughText += " ";
      }
    }

    // Digita tudo de uma vez
    await this.typeText(fullLaughText, 50);
  }/**
   * Digita texto com efeito de máquina de escrever
   * Mimetiza o comportamento do talk() do _Boh.py
   */
  async typeText(text, speed = 100) {
    return new Promise((resolve) => {
      // CORREÇÃO 1: Cancela qualquer animação em andamento
      if (this.isTyping) {
        if (this.currentTimeout) {
          clearTimeout(this.currentTimeout);
          this.currentTimeout = null;
        }
      }

      if (this.isPaused) {
        this.currentTimeout = setTimeout(() => this.typeText(text, speed).then(resolve), 100);
        return;
      }

      // CORREÇÃO 2: Define estado de digitação ANTES de qualquer operação assíncrona
      this.isTyping = true;

      const textElement = this.elements.dialogueText;
      if (!textElement) {
        console.error('Elemento dialogue-text não encontrado!');
        this.isTyping = false; // Reset estado em caso de erro
        resolve();
        return;
      }

      // CORREÇÃO 3: Limpa o conteúdo anterior imediatamente
      textElement.innerHTML = '';

      // Coloriza setas se necessário
      this.colorizeText(text).then((colorizedText) => {
        // CORREÇÃO 4: Verifica se ainda deve continuar (pode ter sido cancelado)
        if (!this.isTyping) {
          resolve();
          return;
        }

        let i = 0;
        // Converte o texto colorizado em array de caracteres (como no Python)
        const chars = Array.from(colorizedText);

        const typeNextChar = () => {
          // CORREÇÃO 5: Sempre verifica se foi pausado ou cancelado
          if (this.isPaused) {
            this.currentTimeout = setTimeout(typeNextChar, 100);
            return;
          }

          // CORREÇÃO 6: Verifica se ainda está no estado de digitação
          if (!this.isTyping) {
            resolve();
            return;
          }

          if (i < chars.length) {
            const currentChar = chars[i];
            textElement.innerHTML += currentChar;

            // Verifica se o caractere atual é alfanumérico para reproduzir o som
            // Remove códigos ANSI para verificar (como no Python)
            const cleanChar = currentChar.replace(/[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '');

            // Reproduz o som apenas se for um caractere alfanumérico (como no Python)
            if (cleanChar && /[a-zA-Z0-9]/.test(cleanChar)) {
              this.playTypingSound(false, cleanChar);
            }

            i++;
            this.currentTimeout = setTimeout(typeNextChar, speed);
          } else {
            // CORREÇÃO 7: Reset estado ao finalizar
            this.isTyping = false;
            this.currentTimeout = null;
            resolve();
          }
        };

        typeNextChar();
      }).catch((error) => {
        // CORREÇÃO 8: Reset estado em caso de erro
        console.error('Erro ao colorizar texto:', error);
        this.isTyping = false;
        this.currentTimeout = null;
        resolve();
      });
    });
  }

  /**
   * Coloriza texto com setas
   */
  async colorizeText(text) {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
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
  }  /**
   * Toca som de digitação mimetizando o comportamento do _Boh.py
   * Implementa:
   * - Controle de tempo entre reproduções (cooldown)
   * - Canal único de áudio (para apenas um som por vez)
   * - Seleção sem repetição usando ShuffledSelector
   * - Verificação de caracteres alfanuméricos
   */
  playTypingSound(staticMode = true, character = " ") {
    if (!this.soundEnabled || !this.soundSelector) return;

    const currentTime = Date.now();
    let shouldPlay = false;

    // Implementa a lógica de controle de tempo do Python
    if (this.lastSoundTime) {
      if (staticMode && character === " ") {
        shouldPlay = true;
      } else {
        shouldPlay = (currentTime - this.lastSoundTime) > this.soundCooldown;
      }
    } else {
      this.lastSoundTime = currentTime;
      shouldPlay = true;
    }

    // Verifica se é um caractere alfanumérico (como no Python)
    const cleanChar = character.replace(/[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '');
    const isAlphaNumeric = /[a-zA-Z0-9]/.test(cleanChar);

    // Só toca som se deve tocar e se é alfanumérico (ou modo estático)
    if (shouldPlay && (isAlphaNumeric || (staticMode && character === " "))) {
      this.lastSoundTime = currentTime;

      // Para qualquer som em reprodução (canal único como pygame)
      if (this.audioChannel && !this.audioChannel.paused) {
        this.audioChannel.pause();
        this.audioChannel.currentTime = 0;
      }

      // Seleciona som sem repetição usando ShuffledSelector
      const selectedAudio = this.soundSelector.select();

      // Cria nova instância para reprodução (como no Python)
      this.audioChannel = new Audio(selectedAudio.src);
      this.audioChannel.volume = this.config.audioVolume;
      this.audioChannel.currentTime = 0;      // Reproduz o som
      this.audioChannel.play().catch(error => {
        console.warn('Erro ao reproduzir som:', error);
      });
    }
  }

  /**
   * Para o canal de áudio atual (similar ao sound_channel.stop() do Python)
   */
  stopAudioChannel() {
    if (this.audioChannel && !this.audioChannel.paused) {
      this.audioChannel.pause();
      this.audioChannel.currentTime = 0;
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
    // CORREÇÃO: Evita avanços múltiplos se já estiver digitando
    if (this.isTyping) {
      return;
    }

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
      await fetch(`${this.apiBaseUrl}/api/dialogue/`, {
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
  }  /**
   * Alterna som ligado/desligado
   */
  toggleSound() {
    this.soundEnabled = !this.soundEnabled;

    if (this.elements.soundIndicator) {
      this.elements.soundIndicator.textContent = this.soundEnabled ? '🔊' : '🔇';
    }

    if (!this.soundEnabled) {
      // Para o canal de áudio quando som é desligado
      this.stopAudioChannel();
    }

    console.log('Som:', this.soundEnabled ? 'ligado' : 'desligado');
  }  /**
   * Alterna pausa
   */
  togglePause() {
    this.isPaused = !this.isPaused;

    if (this.isPaused) {
      // Ao pausar: para qualquer digitação e áudio em andamento
      this.isTyping = false;
      if (this.currentTimeout) {
        clearTimeout(this.currentTimeout);
        this.currentTimeout = null;
      }
      this.stopAudioChannel();
      console.log('⏸️ Pausado - pressione espaço para continuar do início');
    } else {
      // Ao despausar: SEMPRE reinicia a fala atual do início para reavaliação
      console.log('▶️ Retomando do início para reavaliação...');
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
  }  /**
   * Reseta o diálogo
   */
  reset() {
    // CORREÇÃO: Para qualquer digitação em andamento
    this.isTyping = false;

    this.currentStep = 0;
    this.userName = '';
    this.isPaused = false;
    this.isWaitingForResponse = false;
    this.isWaitingForName = false;

    // CORREÇÃO: Limpa todos os timeouts
    if (this.currentTimeout) {
      clearTimeout(this.currentTimeout);
      this.currentTimeout = null;
    }

    // Para o canal de áudio e reseta o sistema de som
    this.stopAudioChannel();
    this.lastSoundTime = null;

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
  }  /**
   * Método de teste para verificar controle de áudio
   */
  testAudioControl() {
    console.log('=== TESTE DE CONTROLE DE ÁUDIO ===');

    // Simula múltiplos sons rapidamente
    for (let i = 0; i < 5; i++) {
      setTimeout(() => {
        this.playTypingSound();
      }, i * 100);
    }

    // Verifica estado após 2 segundos
    setTimeout(() => {
      const audioStatus = this.audioChannel && !this.audioChannel.paused ? 'reproduzindo' : 'parado';
      console.log(`Estado do canal de áudio após teste: ${audioStatus}`);
      console.log('=== FIM DO TESTE ===');
    }, 2000);
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

// Funções globais para testes de conectividade (uso no console)
window.testConnection = function () {
  if (window.bohDialogue) {
    console.log('🔄 Executando teste de conectividade manual...');
    window.bohDialogue.runConnectivityTests();
  } else {
    console.error('❌ BOHDialogue não está inicializado');
  }
};

window.debugAPI = function () {
  if (window.bohDialogue) {
    console.log('🔧 Executando debug detalhado da API...');
    window.bohDialogue.debugConnectivity();
  } else {
    console.error('❌ BOHDialogue não está inicializado');
  }
};

window.testEndpoint = function (customUrl = null) {
  if (!window.bohDialogue) {
    console.error('❌ BOHDialogue não está inicializado');
    return;
  }

  const testUrl = customUrl || window.bohDialogue.apiBaseUrl;
  console.log(`🎯 Testando endpoint customizado: ${testUrl}`);

  fetch(`${testUrl}/api/dialogue/`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => {
      console.log(`✅ Resposta recebida: ${response.status} ${response.statusText}`);
      return response.json();
    })
    .then(data => {
      console.log('📊 Dados:', data);
    })
    .catch(error => {
      console.error('❌ Erro:', error.message);
    });
};

// Instância global
window.bohDialogue = null;

// Inicialização automática com tratamento de erros
document.addEventListener('DOMContentLoaded', function () {
  try {
    console.log('🚀 Inicializando BOH! Dialogue System...');
    window.bohDialogue = new BOHDialogue();
    console.log('✅ BOHDialogue instanciado com sucesso');
    console.log('💡 Use no console: testConnection(), debugAPI(), testEndpoint()');
  } catch (error) {
    console.error('❌ Erro na inicialização do BOHDialogue:', error);
    console.error('🔧 Stack trace:', error.stack);
  }
});

// Exporta para uso global
window.BOHDialogue = BOHDialogue;
