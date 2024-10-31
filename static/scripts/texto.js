// Função para buscar os dados via AJAX e armazenar nas variáveis globais
async function fetchData(filters) {
    console.log('fetchData chamado com os filtros:', filters);
    const response = await fetch('/dados_graficos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
    });

    if (!response.ok) {
        console.error('Erro ao buscar dados do servidor:', response.statusText);
        return null;
    }

    const data = await response.json();
    console.log('Dados recebidos do servidor:', data); // Verificação se os dados estão chegando

    return data;
}

// Função para aplicar filtros e atualizar a UI
async function applyFilters() {
    console.log('applyFilters chamado');
    const selectedTimeRange = document.getElementById('timeRange').value;
    const filters = {
        timeRange: selectedTimeRange,
        day: document.getElementById('day').value,
        month: document.getElementById('month').value,
        week: document.getElementById('week').value,
        year: document.getElementById('year').value,
        monthWeek: document.getElementById('monthWeek').value
    };
    console.log('Filtros aplicados:', filters);
    const data = await fetchData(filters);
    
    if (data && data.timestamp && data.timestamp.length > 0) {
        const vibracaoBraco = data.vibracao_braco;
        const vibracaoBase = data.vibracao_base;
        const corrente = data.corrente;
        const temperatura = data.temperatura;
        const timestamps = data.timestamp;
        console.log('Dados separados:', vibracaoBraco, vibracaoBase, corrente, temperatura);
        
        // Atualizar caixas de média
        updateMediaBoxes(vibracaoBraco, vibracaoBase, corrente, temperatura);
        
        // Detectar outliers e atualizar a UI
        detectAndDisplayOutliers(vibracaoBraco, vibracaoBase, corrente, temperatura, timestamps);
    } else {
        console.error('Dados recebidos são inválidos:', data);
        
        // Atualiza as caixinhas para indicar que não há dados
        document.getElementById('vibrationBracoMedia').innerText = 'N/A';
        document.getElementById('vibrationBaseMedia').innerText = 'N/A';
        document.getElementById('currentMedia').innerText = 'N/A';
        document.getElementById('temperatureMedia').innerText = 'N/A';
        
        // Limpa a lista de outliers se não houver dados
        updateOutliersUI({ vibracaoBraco: [], vibracaoBase: [], corrente: [], temperatura: [] });
    }
}

// Função para calcular médias e atualizar caixas de média
function updateMediaBoxes(vibracaoBraco, vibracaoBase, corrente, temperatura) {
    const mediaVibracaoBraco = vibracaoBraco.reduce((a, b) => a + b, 0) / vibracaoBraco.length || 0;
    const mediaVibracaoBase = vibracaoBase.reduce((a, b) => a + b, 0) / vibracaoBase.length || 0;
    const mediaCorrente = corrente.reduce((a, b) => a + b, 0) / corrente.length || 0;
    const mediaTemperatura = temperatura.reduce((a, b) => a + b, 0) / temperatura.length || 0;

    console.log('Médias calculadas:', {
        mediaVibracaoBraco,
        mediaVibracaoBase,
        mediaCorrente,
        mediaTemperatura
    });

    // Verifique se os elementos HTML existem antes de atualizar
    if (document.getElementById('vibrationBracoMedia')) {
        document.getElementById('vibrationBracoMedia').innerText = mediaVibracaoBraco.toFixed(2);
    } else {
        console.warn("Elemento 'vibrationBracoMedia' não encontrado");
    }

    if (document.getElementById('vibrationBaseMedia')) {
        document.getElementById('vibrationBaseMedia').innerText = mediaVibracaoBase.toFixed(2);
    } else {
        console.warn("Elemento 'vibrationBaseMedia' não encontrado");
    }

    if (document.getElementById('currentMedia')) {
        document.getElementById('currentMedia').innerText = mediaCorrente.toFixed(2);
    } else {
        console.warn("Elemento 'currentMedia' não encontrado");
    }

    if (document.getElementById('temperatureMedia')) {
        document.getElementById('temperatureMedia').innerText = mediaTemperatura.toFixed(2);
    } else {
        console.warn("Elemento 'temperatureMedia' não encontrado");
    }
}

// Adicionando event listeners para garantir que a função seja chamada quando necessário
document.getElementById('timeRange').addEventListener('change', applyFilters);
document.getElementById('day').addEventListener('change', applyFilters);
document.getElementById('month').addEventListener('change', applyFilters);
document.getElementById('week').addEventListener('change', applyFilters);
document.getElementById('year').addEventListener('change', applyFilters);
document.getElementById('monthWeek').addEventListener('change', applyFilters);

// Função para detectar e exibir outliers
function detectAndDisplayOutliers(vibracaoBraco, vibracaoBase, corrente, temperatura, timestamps) {
    const limits = {
        vibracaoBraco: { min: 1.0, max: 5.0 },
        vibracaoBase: { min: 1.0, max: 5.0 },
        corrente: { min: 2.0, max: 10.0 },
        temperatura: { min: 10, max: 50 },
    };
    let outliers = {
        vibracaoBraco: [],
        vibracaoBase: [],
        corrente: [],
        temperatura: [],
    };
    for (let i = 0; i < vibracaoBraco.length; i++) {
        const originalTimestamp = timestamps[i];
        if (vibracaoBraco[i] < limits.vibracaoBraco.min || vibracaoBraco[i] > limits.vibracaoBraco.max) {
            outliers.vibracaoBraco.push({ index: i, valor: vibracaoBraco[i], timestamp: originalTimestamp });
        }
        if (vibracaoBase[i] < limits.vibracaoBase.min || vibracaoBase[i] > limits.vibracaoBase.max) {
            outliers.vibracaoBase.push({ index: i, valor: vibracaoBase[i], timestamp: originalTimestamp });
        }
        if (corrente[i] < limits.corrente.min || corrente[i] > limits.corrente.max) {
            outliers.corrente.push({ index: i, valor: corrente[i], timestamp: originalTimestamp });
        }
        if (temperatura[i] < limits.temperatura.min || temperatura[i] > limits.temperatura.max) {
            outliers.temperatura.push({ index: i, valor: temperatura[i], timestamp: originalTimestamp });
        }
    }
    console.log('Outliers detectados:', outliers);
    updateOutliersUI(outliers);
}

// Função para atualizar a UI com outliers
function updateOutliersUI(outliers) {
    const outliersContainer = document.getElementById('outliersList');
    let instructionContainer = document.getElementById('instructionText');
    
    if (!outliersContainer) {
        console.error("Elemento para exibição de outliers não encontrado.");
        return;
    }

    // Limpa o conteúdo dos contêineres para exibir novos resultados
    outliersContainer.innerHTML = '';

    // Cria o contêiner de instruções apenas se ele não existir
    if (!instructionContainer) {
        instructionContainer = document.createElement('div');
        instructionContainer.id = 'instructionText';
        instructionContainer.style.marginLeft = '20px';
        document.getElementById('main-dashboard').appendChild(instructionContainer);
    }
    instructionContainer.innerHTML = '';

    // Verifica se há dados de outliers para serem exibidos
    let hasOutliers = false;

    for (const [metric, values] of Object.entries(outliers)) {
        if (values && values.length > 0) {
            hasOutliers = true;
            const section = document.createElement('div');
            section.innerHTML = `<h4>Outliers de ${metric}:</h4>`;
            const list = document.createElement('ul');
            
            values.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = `Entrada ${item.index + 1}: ${item.valor} - Encontrado em: ${item.timestamp}`;
                list.appendChild(listItem);
            });
            
            section.appendChild(list);
            outliersContainer.appendChild(section);

            // Adiciona instruções baseadas na métrica do outlier
            let instructionText = "";
            if (metric === "vibracaoBraco") {
                instructionText = "Instruções para Vibração do Braço: Realize a manutenção regularmente e verifique o balanceamento.";
            } else if (metric === "vibracaoBase") {
                instructionText = "Instruções para Vibração da Base: Verifique a fixação e alinhamento dos motores.";
            } else if (metric === "corrente") {
                instructionText = "Instruções para Corrente: Inspecione os cabos e conexões.";
            } else if (metric === "temperatura") {
                instructionText = "Instruções para Temperatura: Avalie o sistema de refrigeração.";
            }
            instructionContainer.innerHTML += `<p>${instructionText}</p>`;
        }
    }

    // Exibe mensagem caso não haja outliers
    if (!hasOutliers) {
        outliersContainer.innerHTML = '<p>Não foram encontrados outliers.</p>';
        instructionContainer.innerHTML = '';
    }
}

// Chama applyFilters ao carregar a página para exibir os dados iniciais
document.addEventListener('DOMContentLoaded', () => {
    applyFilters();
});
