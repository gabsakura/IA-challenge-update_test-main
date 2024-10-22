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

// Função assíncrona para aplicar filtros e separar os dados em variáveis
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
        // Separar os dados em quatro variáveis
        const vibracaoBraco = data.vibracao_braco;
        const vibracaoBase = data.vibracao_base;
        const corrente = data.corrente;
        const temperatura = data.temperatura;

        console.log('Dados separados:');
        console.log('vibracao_braco:', vibracaoBraco);
        console.log('vibracao_base:', vibracaoBase);
        console.log('corrente:', corrente);
        console.log('temperatura:', temperatura);

        // Atualizar as caixas de média com as médias calculadas
        updateMediaBoxes(vibracaoBraco, vibracaoBase, corrente, temperatura);
    } else {
        console.error('Dados recebidos são inválidos:', data);
        // Atualiza as caixinhas para indicar que não há dados
        document.getElementById('vibrationBracoMedia').innerText = 'N/A';
        document.getElementById('vibrationBaseMedia').innerText = 'N/A';
        document.getElementById('currentMedia').innerText = 'N/A';
        document.getElementById('temperatureMedia').innerText = 'N/A';
    }
}

// Função para calcular médias e atualizar caixas de média
function updateMediaBoxes(vibracaoBraco, vibracaoBase, corrente, temperatura) {
    const mediaVibracaoBraco = vibracaoBraco.reduce((a, b) => a + b, 0) / vibracaoBraco.length;
    const mediaVibracaoBase = vibracaoBase.reduce((a, b) => a + b, 0) / vibracaoBase.length;
    const mediaCorrente = corrente.reduce((a, b) => a + b, 0) / corrente.length;
    const mediaTemperatura = temperatura.reduce((a, b) => a + b, 0) / temperatura.length;

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

// Inicializar os gráficos ao carregar a página (ou outros elementos se necessário)
window.onload = applyFilters;
