
// Classe para selecionar itens aleatórios sem repetição (equivalente ao ShuffledSelector)
class ShuffledSelector {
    constructor(items) {
        this.items = [...items];
        this.availableIndices = [...Array(items.length).keys()];
    }

    select() {
        if (this.availableIndices.length === 0) {
            this.availableIndices = [...Array(this.items.length).keys()];
        }

        const randomIndex = Math.floor(Math.random() * this.availableIndices.length);
        const selectedIndex = this.availableIndices[randomIndex];

        this.availableIndices.splice(randomIndex, 1);
        return this.items[selectedIndex];
    }
}

// Configuração de áudio
let audioContext = null;
let soundSelector = null;
let isMuted = false;
let lastSoundTime = null;

// Elementos DOM
const elements = {
    expression: document.getElementById('expression'),
    dialogueText: document.getElementById('dialogue-text'),
    staticText: document.getElementById('static-text'),
    listModel: document.getElementById('list-model'),
    inputArea: document.getElementById('input-area'),
    nameInput: document.getElementById('name-input'),
    userInput: document.getElementById('user-input'),
    nameField: document.getElementById('name-field'),
    nameSubmit: document.getElementById('name-submit'),
    inputOptions: document.getElementById('input-options'),
    muteBtn: document.getElementById('mute-btn'),
    soundIndicator: document.getElementById('sound-indicator')
};

// Expressões do BOH (equivalente ao dicionário expressions do Python)
const expressions = {
    idle: [
        "[ ▀ ¸ ▀]",
        "[ ▀ ° ▀]",
        "[ ▀ ■ ▀]",
        "[ ▀ ─ ▀]",
        "[ ▀ ~ ▀]",
        "[ ▀ ▄ ▀]",
        "[ ▀ ¬ ▀]",
        "[ ▀ · ▀]",
        "[ ▀ _ ▀]"
    ],
    pokerface: ["[ ▀ ‗ ▀]", "[ ▀ ¯ ▀]", "[ ▀ ¡ ▀]"],
    thinking: ["[ ─ ´ ─]", "[ ─ » ─]"],
    "open mouth": ["[ ▀ ß ▀]", "[ ▀ █ ▀]"],
    annoyed: ["[ ▀ ı ▀]", "[ ▀ ^ ▀]"],
    "looking down": ["[ ▄ . ▄]", "[ ▄ _ ▄]", "[ ▄ ₒ ▄]", "[ ▄ ‗ ▄]"]
};

// Estado do sistema
let currentDialogue = [];
let dialogueIndex = 0;
let isTyping = false;
let isPaused = false;
let currentExpression = 'idle';
let currentExpressionIndex = 0;
let userName = '';

// Variáveis para controle de estado de conversa
let conversationState = 'intro';
let awaitingResponse = false;
let validResponses = [];

// Inicialização do áudio
async function initAudio() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Lista de arquivos de som disponíveis
        const soundFiles = [
            'static/sfx/p03voice_calm#1.wav',
            'static/sfx/p03voice_calm#2.wav',
            'static/sfx/p03voice_calm#3.wav',
            'static/sfx/p03voice_calm#4.wav',
            'static/sfx/p03voice_calm#5.wav',
            'static/sfx/p03voice_calm#6.wav',
            'static/sfx/p03voice_calm#7.wav',
            'static/sfx/p03voice_calm#8.wav'
        ];

        const sounds = [];

        for (const file of soundFiles) {
            try {
                const response = await fetch(file);
                if (response.ok) {
                    const arrayBuffer = await response.arrayBuffer();
                    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                    sounds.push(audioBuffer);
                }
            } catch (error) {
                console.warn(`Erro ao carregar ${file}:`, error);
            }
        }

        if (sounds.length > 0) {
            soundSelector = new ShuffledSelector(sounds);
            console.log(`${sounds.length} sons carregados com sucesso`);
        } else {
            console.warn('Nenhum arquivo de som foi carregado');
        }

    } catch (error) {
        console.warn('Erro ao inicializar áudio:', error);
    }
}

// Reproduzir som de digitação
function playTypingSound() {
    if (!audioContext || !soundSelector || isMuted) return;

    const now = Date.now();
    if (lastSoundTime && now - lastSoundTime < 300) return;

    lastSoundTime = now;

    try {
        const audioBuffer = soundSelector.select();
        const source = audioContext.createBufferSource();
        const gainNode = audioContext.createGain();

        source.buffer = audioBuffer;
        gainNode.gain.value = 0.7;

        source.connect(gainNode);
        gainNode.connect(audioContext.destination);

        source.start();

        // Indicador visual
        elements.soundIndicator.classList.add('active');
        setTimeout(() => {
            elements.soundIndicator.classList.remove('active');
        }, 100);

    } catch (error) {
        console.warn('Erro ao reproduzir som:', error);
    }
}

// Colorir setas (equivalente a arrow_colorize)
function colorizeArrows(text, colorizeArrows = false) {
    if (!colorizeArrows) return text;

    return text
        .replace(/[‹›]/g, '<span class="arrow-orange">$&</span>')
        .replace(/[»«]/g, '<span class="arrow-blue">$&</span>');
}

// Parsear texto formatado (equivalente a parse_formatted_text)
function parseFormattedText(text) {
    // Substitui códigos ANSI por classes CSS
    return text
        .replace(/\033\[31m/g, '<span class="text-red">')
        .replace(/\033\[32m/g, '<span class="text-green">')
        .replace(/\033\[34m/g, '<span class="text-blue">')
        .replace(/\033\[33m/g, '<span class="text-yellow">')
        .replace(/\033\[35m/g, '<span class="text-purple">')
        .replace(/\033\[36m/g, '<span class="text-cyan">')
        .replace(/\033\[1m/g, '<span class="text-bold">')
        .replace(/\033\[0m/g, '</span>')
        .replace(/\033\[[0-9;]*m/g, ''); // Remove outros códigos ANSI
}

// Função principal talk (equivalente à função talk do Python)
async function talk(inputText = " ", expression = "idle", amount = 1.0, staticText = "", colorizeArrows = false) {
    return new Promise((resolve) => {
        if (isPaused) {
            setTimeout(() => resolve(talk(inputText, expression, amount, staticText, colorizeArrows)), 100);
            return;
        }

        isTyping = true;
        currentExpression = expression;
        currentExpressionIndex = 0;

        // Limpar conteúdo anterior
        elements.dialogueText.innerHTML = '';
        elements.staticText.innerHTML = parseFormattedText(colorizeArrows(staticText, colorizeArrows));

        let textToType = inputText === " " ? staticText : inputText;
        textToType = parseFormattedText(textToType);

        let displayedText = '';
        let charIndex = 0;

        const typeChar = () => {
            if (isPaused) {
                setTimeout(typeChar, 100);
                return;
            }

            if (charIndex < textToType.length) {
                const char = textToType[charIndex];
                displayedText += char;
                elements.dialogueText.innerHTML = colorizeArrows(displayedText, colorizeArrows);

                // Reproduzir som para caracteres alfanuméricos
                if (/[a-zA-Z0-9]/.test(char)) {
                    playTypingSound();
                }

                // Atualizar expressão
                updateExpression();

                charIndex++;
                setTimeout(typeChar, 30);
            } else {
                isTyping = false;
                setTimeout(resolve, amount * 1000);
            }
        };

        typeChar();
    });
}

// Atualizar expressão do BOH
function updateExpression() {
    const exprList = expressions[currentExpression] || expressions.idle;
    const expr = exprList[currentExpressionIndex % exprList.length];
    elements.expression.textContent = expr;
    currentExpressionIndex++;
}

// Aguardar resposta do usuário (equivalente a wait_for_response)
function waitForResponse(affirmative = ['s', 'y'], negative = ['n'], staticText = "", askTemplate = "", timeout = 5000, messages = null) {
    return new Promise((resolve) => {
        if (!messages) {
            messages = {
                timeout: "Poxa, tá difícil assim de encontrar a tecla?",
                invalid: "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                negative: "Não?",
                retry: "Pera, deixa eu repetir",
                positive: "Show de bola!"
            };
        }

        awaitingResponse = true;
        validResponses = [...affirmative, ...negative];

        // Mostrar opções de input
        elements.inputArea.style.display = 'block';
        elements.inputOptions.innerHTML = `Pressione [${affirmative.join('/')}] para Sim ou [${negative.join('/')}] para Não`;
        elements.userInput.focus();

        const timeoutId = setTimeout(() => {
            if (awaitingResponse) {
                awaitingResponse = false;
                elements.inputArea.style.display = 'none';
                talk(messages.timeout, "thinking", 1.5, staticText + askTemplate).then(() => resolve(false));
            }
        }, timeout);

        const handleKeyPress = (event) => {
            if (!awaitingResponse) return;

            const key = event.key.toLowerCase();

            if (affirmative.includes(key)) {
                clearTimeout(timeoutId);
                awaitingResponse = false;
                elements.inputArea.style.display = 'none';
                document.removeEventListener('keydown', handleKeyPress);

                const message = key === 'y' ? "Sim, inglês também tá valendo..." : messages.positive;
                const expr = key === 'y' ? "pokerface" : "open mouth";
                talk(message, expr, 1.0, askTemplate).then(() => resolve(true));

            } else if (negative.includes(key)) {
                clearTimeout(timeoutId);
                awaitingResponse = false;
                elements.inputArea.style.display = 'none';
                document.removeEventListener('keydown', handleKeyPress);

                talk(messages.negative, "pokerface", 1.0, askTemplate).then(() => {
                    return talk(messages.retry, "idle", 1.0, staticText);
                }).then(() => resolve(false));

            } else if (!/[a-zA-Z]/.test(key) || event.ctrlKey || event.altKey) {
                // Ignorar teclas especiais
                return;
            } else {
                talk(messages.invalid, "annoyed", 1.0, staticText + askTemplate);
                elements.userInput.value = '';
            }
        };

        document.addEventListener('keydown', handleKeyPress);

        // Handle input field
        elements.userInput.addEventListener('input', (event) => {
            const value = event.target.value.toLowerCase();
            if (validResponses.includes(value)) {
                handleKeyPress({ key: value });
            }
            event.target.value = '';
        });
    });
}

// Controle de pausa com ESPAÇO (comportamento idêntico ao BOH.py original)
function handleSpaceKey() {
    if (isTyping) {
        isPaused = !isPaused;
        console.log(isPaused ? 'Diálogo pausado' : 'Diálogo retomado');
    }
}

// Configurar controles de teclado
function setupKeyboardControls() {
    document.addEventListener('keydown', (event) => {
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                handleSpaceKey();
                break;
            case 'KeyM':
                toggleMute();
                break;
            case 'Escape':
                if (isTyping) {
                    isPaused = false;
                    isTyping = false;
                }
                break;
        }
    });
}

// Toggle mute
function toggleMute() {
    isMuted = !isMuted;
    elements.muteBtn.textContent = isMuted ? '🔇' : '🔊';
    console.log(isMuted ? 'Áudio desabilitado' : 'Áudio habilitado');
}

// Função principal que executa a conversa (equivalente ao main() do Python)
async function main() {
    const listModel = "\n\n\n\n                        None × ‹[H]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[T]» × None";
    const swappedEdges = "\n\n\n\n                        None × ‹[T]» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹[H]» × None";
    const askTemplate = '\n\n\n\n                    [<span class="text-green">S</span>im]     [<span class="text-red">N</span>ão]';
    const affirmative = ['s', 'y'];
    const negative = ['n'];

    try {
        // Sequência inicial de diálogos
        await talk("Oi, tudo bem?");
        await talk("Muito obrigado por visitar minha página!");
        await talk('Eu me chamo <span class="text-green text-bold">BOH!</span>');
        await talk("He He", "idle", 0.75);
        await talk("Sabe...", "idle", 0.75);
        await talk("Tipo,");
        await talk("", "idle", 1.0, "Tipo, <span class='text-bold'>ROH</span>");
        await talk("", "idle", 1.0, "Tipo, <span class='text-bold'>ROH-</span><span class='text-bold text-green'>BOH</span>");

        // Sequência de "HahA"
        for (let i = 1; i <= 10; i++) {
            await talk("", "open mouth", 0.05, "HahA".repeat(i));
        }

        await sleep(1000);
        await talk("Ai ai, sou meio comédia às vezes, sabe?");
        await talk("Mas, enfim,");
        await talk("E você, como se chama?", "idle", 0.5);

        // Input do nome
        userName = await getName();

        await talk("Olha olha olha, na verdade, eu não tenho muito tempo...", "pokerface", 1.5);
        await talk("Me desculpa! Você parece ser uma pessoa muito legal, mas...");
        await talk("A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓", "idle", 0.2);
        await talk("", "looking down", 0.2, "A pessoa que me mandou aqui, queria falar sobre ↓ isso ↓");

        // Mostrar lista
        elements.listModel.style.display = 'block';
        elements.listModel.innerHTML = listModel;
        await sleep(2000);

        await talk("Reconhece?", "idle", 1.5, listModel);
        await talk("Ih, verdade, cê não consegue me responder, né?", "idle", 1.0, listModel);
        await talk("Hmmm", "thinking");

        for (let i = 1; i <= 3; i++) {
            await talk("", "thinking", 1.0, "Hmmm" + ".".repeat(i));
        }

        await talk("Já sei!", "open mouth");
        await talk("Aqui, toma", "idle", 1.5, askTemplate);

        // Primeira instrução sobre respostas
        await talk("Agora sempre que eu te perguntar algo,", "idle", 1.0, askTemplate);
        await talk("Você pode responder digitando", "idle", 1.0, askTemplate);
        await talk("A letra destacada que achar mais cabível.", "idle", 1.0, askTemplate);
        await talk("Entendeu, né?", "idle", 1.0, askTemplate);

        await waitForResponse(affirmative, negative, "", askTemplate);

        await talk("Enfim, voltando ao assunto...", "idle");
        await talk("Reconhece isso aqui, né?", "idle", 0.1);
        await talk("", "looking down", 0.25, "Reconhece isso aqui, né?");

        elements.listModel.innerHTML = listModel + askTemplate;

        // Verificar reconhecimento da lista
        let recognizes = false;
        while (!recognizes) {
            recognizes = await waitForResponse(
                affirmative,
                negative,
                listModel,
                askTemplate,
                5000,
                {
                    timeout: "Poxa, tá difícil assim de encontrar a tecla?",
                    invalid: "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                    negative: "Não?",
                    retry: "Como assim pô? Me esforcei tanto desenhar ela...",
                    positive: "Pois é, uma lista."
                }
            );

            if (!recognizes) {
                await talk("É uma lista! A estrutura de dados!", "pokerface", 1.0, listModel);
                await talk("Tá vendo?", "idle", 1.0, listModel + askTemplate);
            }
        }

        // Continuar com as explicações sobre listas...
        const talkSequence = [
            "Bom, como você já sabe... a lista é uma estrutura de dados",
            "Mas tô aqui pra discutir um desafio específico relacionado a ela...",
            "O desafio é o seguinte:",
            "Que tal inverter uma lista?",
            "Ou melhor, qual seria a maneira mais eficiente de fazer isso?",
            "Bom, a gente pode fazer isso de várias maneiras...",
            "Mas, acho que a primeira coisa que vem à cabeça é..."
        ];

        for (const text of talkSequence) {
            await talk(text, "idle", 1.0, listModel);
        }

        // Lista com Head e Tail coloridos
        const coloredList = '\n\n\n\n                        None × ‹<span class="text-red">[T]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹<span class="text-blue">[H]</span>» × None';
        elements.listModel.innerHTML = coloredList;

        await talk("Fazer isso, né?", "idle", 1.5, coloredList);

        // Continuar com as explicações sobre inversão...
        await explainListInversion(swappedEdges, askTemplate, affirmative, negative);

    } catch (error) {
        console.error('Erro durante a conversa:', error);
        await talk("Ops! Algo deu errado. Mas foi legal te conhecer!", "annoyed");
    }
}

// Explicações sobre inversão de lista
async function explainListInversion(swappedEdges, askTemplate, affirmative, negative) {
    const swapExplanations = [
        'Trocando Head e Tail, o que era a "frente" da lista,',
        'Passa a ser o "final" dela, e vice-versa.',
        "Mas, pera aí! Como isso acontece exatamente?",
        'Digamos que, a gente iguale <span class="text-red">Tail</span> a <span class="text-blue">Head</span>'
    ];

    for (const explanation of swapExplanations) {
        await talk(explanation, "idle", 1.0, swappedEdges);
    }

    // Lista com duas Heads
    const listWithTwoHeads = '\n\n\n\n                        None × ‹<span class="text-blue">[H]</span>» ‹[]» ‹[]» ... ‹[]» ‹[]» ‹<span class="text-blue">[H]</span>» × None';
    elements.listModel.innerHTML = listWithTwoHeads;

    await talk("Eita... agora temos duas Heads!", "open mouth", 1.5, listWithTwoHeads);

    // Explicação sobre atribuição de variáveis
    const assignmentExplanations = [
        'Isso porque <span class="text-red">Tail</span> = <span class="text-blue">Head</span> não é uma troca de valores,',
        'Só estamos dizendo que <span class="text-red">Tail</span> agora recebe',
        'O objeto contido dentro de <span class="text-blue">Head</span>.',
        "Mas assim como abrir espaço numa estante pra guardar um livro,",
        "Não significa que haverá espaço para guardar novamente",
        "O antigo livro que tiramos para guardar o livro novo...",
        "O que significa que precisamos salvar",
        "O antigo valor de Tail, antes de trocá-lo por Head."
    ];

    for (let i = 0; i < assignmentExplanations.length; i++) {
        const amount = (i === 3 || i === 7) ? 1.5 : 1.0;
        await talk(assignmentExplanations[i], "idle", amount, listWithTwoHeads);
    }

    // Introduzir o AUX
    await introduceAux(askTemplate, affirmative, negative, swappedEdges);
}

// Introduzir o personagem AUX
async function introduceAux(askTemplate, affirmative, negative, swappedEdges) {
    const auxAscii = `
       __
   _  |@@|
  / \\ \\--/ __
  ) O|----|  |   __
 / / \\ }{ /\\ )_ / _\\\\
 )/  /\\__/\\ \\__O (__
|/  (--/\\--)    \\__/
/   _)(  )(_
   \`---''---\`
`;

    // Adicionar ASCII art do AUX ao static text
    elements.staticText.innerHTML = `<pre class="ascii-art">${auxAscii}</pre>`;

    const auxSequence = [
        "Meu mano aqui se chama AUX,",
        "Tudo bem contigo, patrão?",
        "Ele se ofereceu pra guardar o valor de Tail",
        "Pra que a gente não perca na hora de trocar..."
    ];

    for (let i = 0; i < auxSequence.length; i++) {
        const amount = i === 0 ? 1.25 : i === 1 ? 0.75 : 1.0;
        await talk(auxSequence[i], "idle", amount, auxAscii);

        if (i === 2) {
            // AUX segurando o valor de Tail
            const auxWithTail = auxAscii.replace('(__', '(<span class="text-red">[T]</span>');
            elements.staticText.innerHTML = `<pre class="ascii-art">${auxWithTail}</pre>`;
        }
    }

    // Continuar com o resto da explicação...
    await continueExplanation(askTemplate, affirmative, negative, swappedEdges);
}

// Continuar explicação
async function continueExplanation(askTemplate, affirmative, negative, swappedEdges) {
    await talk("Obrigado AUX, você é o cara! Até mais tarde!", "open mouth");
    elements.staticText.innerHTML = '';

    // Explicar sobre ponteiros
    const pointerExplanations = [
        "Só que, isso não é o suficiente, né?",
        "Por causa desses caras aqui: ‹[]»",
        "Mais especificamente, ‹ » , esses dois.",
        "No nosso caso, eles representam",
        "Os ponteiros que identificam",
        "Quais elementos precedem e sucedem",
        "O objeto observado, seja lá qual você escolha.",
        "Até aí tudo bem, né?"
    ];

    for (const explanation of pointerExplanations) {
        await talk(explanation, "idle", 1.0, swappedEdges, true);
    }

    // Verificar entendimento
    await talk("Estamos na mesma página, então?", "thinking", 0.2, swappedEdges, true);
    await talk("", "thinking", 0.5, "Estamos na mesma página, então?");
    elements.listModel.innerHTML = swappedEdges + askTemplate;

    const understands = await waitForResponse(affirmative, negative, swappedEdges, askTemplate);

    if (!understands) {
        await additionalExplanations(swappedEdges, askTemplate, affirmative, negative);
    }

    await finalExplanations(swappedEdges, askTemplate, affirmative, negative);
}

// Explicações adicionais se o usuário não entender
async function additionalExplanations(swappedEdges, askTemplate, affirmative, negative) {
    const additionalExplanations = [
        "Bom, resumidamente, nesse conceito de lista,",
        "Não usamos um conceito de índice,",
        'Então a única forma de saber "aonde"',
        "Cada objeto se encontra, é através desses ponteiros,",
        "Pense que é como uma corrente.",
        "Cada elo da corrente aponta para o próximo,",
        "E cada um também sabe qual é o elo anterior."
    ];

    for (const explanation of additionalExplanations) {
        await talk(explanation, "idle", 1.0, swappedEdges, true);
    }

    // Verificar novamente
    let confirmation = false;
    while (!confirmation) {
        confirmation = await waitForResponse(
            affirmative,
            negative,
            "",
            askTemplate,
            5000,
            {
                timeout: "Muita falta de educação, ignorar os outros desse jeito!",
                invalid: "Oh! Digitou uma letra que eu não pedi! Presta atenção aí, pô!",
                negative: "Tudo bem então, vamos fazer o seguinte...",
                positive: "Show de bola!"
            }
        );

        if (!confirmation) {
            await talk("Vôce tá precisando de um descanso,", "idle", 1.0, askTemplate);
            await talk("Eu tô precisando de um descanso.", "idle", 1.0, askTemplate);
            await talk("Vou dar uma pausa aqui, beleza?", "idle", 1.0, askTemplate);
            await talk("Quando quiser continuar, é só teclar", "idle", 1.0, askTemplate);

            elements.dialogueText.innerHTML = "Tô aqui pertinho, quando quiser continuar é só chamar!";
            await waitForAnyKey();
            confirmation = true;
        }
    }
}

// Explicações finais
async function finalExplanations(swappedEdges, askTemplate, affirmative, negative) {
    await talk("Então, vamos lá!", "open mouth", 1.0, swappedEdges, true);

    // Explicações sobre setas coloridas
    const arrowExplanations = [
        "De modo geral, essas setinhas são tão importantes",
        "Pra esse exercício, que a gente vai precisar",
        "Deixar elas bem visíveis, pra não confundir."
    ];

    for (const explanation of arrowExplanations) {
        await talk(explanation, "idle", 1.0, swappedEdges, true);
    }

    await talk("Que tal...", "thinking", 1.5, swappedEdges, true);
    await talk("", "thinking", 0.5, "Assim...", true);
    await talk("", "thinking", 1.0, "Assim... ‹›«»", true);

    // Explicar setas coloridas
    const coloredArrowExplanations = [
        "Melhorou, né?",
        "As setas simples, ou seja, ‹ & › , destacadas em laranja,",
        "Representam a variável do nosso objeto que",
        "Nos mostra qual é o elemento que o precede",
        "Já as setas duplas, ou seja, » & « , destacadas em azul,",
        "Representam a variável do nosso objeto que",
        "Nos mostra qual é o elemento que o sucede"
    ];

    for (let i = 0; i < coloredArrowExplanations.length; i++) {
        const amount = i === 6 ? 1.5 : 1.0;
        await talk(coloredArrowExplanations[i], "idle", amount, swappedEdges, true);
    }

    // Finalizar explicação
    await talk("E era isso que eu tinha pra te mostrar hoje!", "open mouth");
    await talk("Espero que tenha conseguido te ajudar!", "idle");
    await talk("A gente se vê na próxima, beleza?", "looking down");

    // Arte final
    showFinalArt();
}

// Mostrar arte ASCII final
function showFinalArt() {
    const finalArt = `
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
`;

    elements.dialogueText.innerHTML = '';
    elements.staticText.innerHTML = `<pre class="ascii-art">${finalArt}</pre>`;
    elements.listModel.style.display = 'none';
}

// Aguardar qualquer tecla
function waitForAnyKey() {
    return new Promise((resolve) => {
        const handler = (event) => {
            document.removeEventListener('keydown', handler);
            resolve();
        };
        document.addEventListener('keydown', handler);
    });
}

// Obter nome do usuário
function getName() {
    return new Promise((resolve) => {
        elements.nameInput.style.display = 'block';
        elements.nameField.focus();

        let nameChars = [];

        const handleKeyPress = (event) => {
            if (event.key === 'Enter' && nameChars.length >= 4) {
                elements.nameInput.style.display = 'none';
                document.removeEventListener('keydown', handleKeyPress);
                resolve(nameChars.join(''));
            } else if (/[a-zA-Z0-9]/.test(event.key) && nameChars.length < 20) {
                nameChars.push(event.key);
                elements.nameField.value = nameChars.join('');
            } else if (event.key === 'Backspace') {
                nameChars.pop();
                elements.nameField.value = nameChars.join('');
            } else if (nameChars.length < 4) {
                talk("Você sabe seu nome, né?", "annoyed", 0.5);
            }
        };

        const handleSubmit = () => {
            if (nameChars.length >= 4) {
                elements.nameInput.style.display = 'none';
                document.removeEventListener('keydown', handleKeyPress);
                resolve(nameChars.join(''));
            }
        };

        document.addEventListener('keydown', handleKeyPress);
        elements.nameSubmit.addEventListener('click', handleSubmit);
    });
}

// Função utilitária para sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Configurar controles
elements.muteBtn.addEventListener('click', toggleMute);

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Inicializando BOH!...');

    // Inicializar áudio
    await initAudio();

    // Configurar controles
    setupKeyboardControls();

    // Aguardar interação do usuário para iniciar áudio
    const startButton = document.createElement('button');
    startButton.textContent = 'Clique para começar!';
    startButton.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); padding: 20px; font-size: 18px; background: #238636; color: white; border: none; border-radius: 8px; cursor: pointer; z-index: 1000;';

    startButton.addEventListener('click', async () => {
        startButton.remove();

        // Resumir contexto de áudio se necessário
        if (audioContext && audioContext.state === 'suspended') {
            await audioContext.resume();
        }

        // Iniciar conversa
        await main();
    });

    document.body.appendChild(startButton);

    console.log('BOH! pronto para começar!');
});