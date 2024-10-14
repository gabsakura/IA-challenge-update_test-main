// Função para buscar os dados via AJAX
async function fetchData(filters) {
    const response = await fetch('/dados_graficos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    });
    const data = await response.json();
    return data;
}

// Variáveis globais para os gráficos
let vibrationBracoChart, vibrationBaseChart, currentChart, temperatureChart;

// Função para inicializar os gráficos vazios
function initCharts() {
    const ctxVibrationBraco = document.getElementById('vibrationBracoChart').getContext('2d');
    const ctxVibrationBase = document.getElementById('vibrationBaseChart').getContext('2d');
    const ctxCurrent = document.getElementById('currentChart').getContext('2d');
    const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');

    vibrationBracoChart = new Chart(ctxVibrationBraco, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Vibração do Braço',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 2,
            }
        }
    });

    vibrationBaseChart = new Chart(ctxVibrationBase, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Vibração da Base',
                data: [],
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 2,
            }
        }
    });

    currentChart = new Chart(ctxCurrent, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Corrente',
                data: [],
                borderColor: 'rgba(255, 159, 64, 1)',
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 2,
            }
        }
    });

    temperatureChart = new Chart(ctxTemperature, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperatura',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 20,
            }
        }
    });
}

// Função genérica para atualizar os gráficos
function updateChart(chart, labels, data) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data || [];
    chart.update();
}

// Função para formatar timestamps
function formatTimestamps(timestamps, type) {
    if (type === 'daily') {
        return timestamps.map(ts => new Date(`1970-01-01T${ts}:00Z`).toLocaleTimeString());
    } else if (type === 'weekly' || type === 'monthly') {
        return timestamps.map(ts => new Date(ts).toLocaleDateString('pt-BR'));
    }
    return timestamps;
}

// Funções específicas para atualizar gráficos
function updateChartsDaily(data) {
    if (data && data.timestamp) {
        const formattedTimestamps = formatTimestamps(data.timestamp, 'daily');
        updateChart(vibrationBracoChart, formattedTimestamps, data.vibracao_braco);
        updateChart(vibrationBaseChart, formattedTimestamps, data.vibracao_base);
        updateChart(currentChart, formattedTimestamps, data.corrente);
        updateChart(temperatureChart, formattedTimestamps, data.temperatura);
    } else {
        console.error("Os dados fornecidos não são válidos:", data);
    }
}

function updateChartsWeekly(data) {
    if (data && data.timestamp) {
        const formattedTimestamps = formatTimestamps(data.timestamp, 'weekly');
        updateChart(vibrationBracoChart, formattedTimestamps, data.vibracao_braco);
        updateChart(vibrationBaseChart, formattedTimestamps, data.vibracao_base);
        updateChart(currentChart, formattedTimestamps, data.corrente);
        updateChart(temperatureChart, formattedTimestamps, data.temperatura);
    } else {
        console.error("Os dados fornecidos não são válidos:", data);
    }
}

function updateChartsMonthly(data) {
    if (data && data.timestamp) {
        const semanas = [];
        const totalDias = data.timestamp.length;
        const diasPorSemana = Math.ceil(totalDias / 4);  // Dividindo o mês em 4 semanas

        for (let i = 0; i < 4; i++) {
            const inicio = i * diasPorSemana;
            const fim = inicio + diasPorSemana;

            // Agrupar os dados semanais
            const semanaVibracaoBraco = data.vibracao_braco.slice(inicio, fim);
            const semanaVibracaoBase = data.vibracao_base.slice(inicio, fim);
            const semanaCorrente = data.corrente.slice(inicio, fim);
            const semanaTemperatura = data.temperatura.slice(inicio, fim);

            // Verificar se há dados suficientes para a semana
            if (semanaVibracaoBraco.length > 0) {
                // Calcula as médias semanais
                const mediaVibracaoBraco = semanaVibracaoBraco.reduce((a, b) => a + b, 0) / semanaVibracaoBraco.length;
                const mediaVibracaoBase = semanaVibracaoBase.reduce((a, b) => a + b, 0) / semanaVibracaoBase.length;
                const mediaCorrente = semanaCorrente.reduce((a, b) => a + b, 0) / semanaCorrente.length;
                const mediaTemperatura = semanaTemperatura.reduce((a, b) => a + b, 0) / semanaTemperatura.length;

                semanas.push({
                    timestamp: `Semana ${i + 1}`,  // Exibe "Semana 1", "Semana 2", etc.
                    vibracao_braco: mediaVibracaoBraco,
                    vibracao_base: mediaVibracaoBase,
                    corrente: mediaCorrente,
                    temperatura: mediaTemperatura
                });
            } else {
                console.warn(`Dados insuficientes para a semana ${i + 1}`);
            }
        }

        // Atualiza os gráficos com os dados das semanas
        const formattedTimestamps = semanas.map(semana => semana.timestamp);
        const vibracaoBracoData = semanas.map(semana => semana.vibracao_braco);
        const vibracaoBaseData = semanas.map(semana => semana.vibracao_base);
        const correnteData = semanas.map(semana => semana.corrente);
        const temperaturaData = semanas.map(semana => semana.temperatura);

        updateChart(vibrationBracoChart, formattedTimestamps, vibracaoBracoData);
        updateChart(vibrationBaseChart, formattedTimestamps, vibracaoBaseData);
        updateChart(currentChart, formattedTimestamps, correnteData);
        updateChart(temperatureChart, formattedTimestamps, temperaturaData);
    } else {
        console.error("Os dados fornecidos não são válidos:", data);
    }
}




// Adicionar o evento de clique ao botão "Aplicar Filtro"
document.getElementById('applyFilter').addEventListener('click', applyFilters);
async function applyFilters() {
    const selectedTimeRange = document.getElementById('timeRange').value;
    const filters = {
        timeRange: selectedTimeRange,
        day: document.getElementById('day').value,
        month: document.getElementById('month').value,
        week: document.getElementById('week').value,
        year: document.getElementById('year').value,
        monthWeek: document.getElementById('monthWeek').value
    };

    const data = await fetchData(filters);
    if (selectedTimeRange === 'day') {
        updateChartsDaily(data);
    } else if (selectedTimeRange === 'week') {
        updateChartsWeekly(data);
    } else if (selectedTimeRange === 'month') {
        updateChartsMonthly(data);
    }
}



//FAZER PDF ESSA PARTE::::::::

// Função assíncrona para gerar um relatório em PDF com os dados de sensores
async function generatePDFReport(filters, data) {
    // Carregar a biblioteca jsPDF
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF(); // Instância do jsPDF

    // Adicionar título do relatório
    doc.setFontSize(16);
    doc.text(`Relatório de Dados de Sensores (${filters.timeRange})`, 10, 20);

    // Informações sobre o filtro usado
    doc.setFontSize(12);
    doc.text(`Período: ${filters.timeRange}`, 10, 30);
    if (filters.day) doc.text(`Dia: ${filters.day}`, 10, 40);
    if (filters.month) doc.text(`Mês: ${filters.month}`, 10, 50);
    if (filters.year) doc.text(`Ano: ${filters.year}`, 10, 60);

    // Criar tabela de dados
    let startY = 70;  // Posição inicial da tabela

    // Cabeçalho da tabela
    doc.setFontSize(10);
    const headers = ["Data", "Vibração (Braço)", "Vibração (Base)", "Corrente", "Temperatura"];
    headers.forEach((header, index) => {
        doc.text(header, 10 + index * 40, startY); // Distribui os cabeçalhos uniformemente
    });
    startY += 10; // Incrementar posição para a primeira linha de dados

    // Adicionar linhas de dados
    data.timestamp.forEach((timestamp, index) => {
        doc.text(new Date(timestamp).toLocaleDateString('pt-BR'), 10, startY);
        doc.text(data.vibracao_braco[index].toFixed(2), 50, startY);
        doc.text(data.vibracao_base[index].toFixed(2), 100, startY);
        doc.text(data.corrente[index].toFixed(2), 150, startY);
        doc.text(data.temperatura[index].toFixed(2), 190, startY);
        startY += 10; // Incrementar posição para a próxima linha
    });

    // Adicionar rodapé
    doc.setFontSize(10);
    doc.text('Relatório gerado automaticamente por [Nome do Sistema]', 10, startY + 20);

    // Salvar ou baixar o PDF
    doc.save(`relatorio_sensores_${filters.timeRange}.pdf`);
}

// Função assíncrona para aplicar filtros e gerar o relatório
async function applyFilters() {
    // Coletar os filtros selecionados pelo usuário
    const selectedTimeRange = document.getElementById('timeRange').value;
    const filters = {
        timeRange: selectedTimeRange,
        day: document.getElementById('day').value,
        month: document.getElementById('month').value,
        week: document.getElementById('week').value,
        year: document.getElementById('year').value,
        monthWeek: document.getElementById('monthWeek').value
    };

    // Fetch os dados com base nos filtros aplicados
    const data = await fetchData(filters);

    // Atualizar os gráficos com base no intervalo de tempo selecionado
    switch (selectedTimeRange) {
        case 'day':
            updateChartsDaily(data);
            break;
        case 'week':
            updateChartsWeekly(data);
            break;
        case 'month':
            updateChartsMonthly(data);
            break;
        default:
            console.warn('Intervalo de tempo não reconhecido');
    }

    // Gerar o PDF com os dados filtrados
    generatePDFReport(filters, data);
}


// Inicializar os gráficos ao carregar a página
initCharts();
