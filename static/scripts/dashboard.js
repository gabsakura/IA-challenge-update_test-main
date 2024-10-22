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
// Variáveis globais para os gráficos
let vibrationBracoChart, vibrationBaseChart, currentChart, temperatureChart;

// Função para inicializar os gráficos
function initCharts() {
    const ctxVibrationBraco = document.getElementById('vibrationBracoChart').getContext('2d');
    const ctxVibrationBase = document.getElementById('vibrationBaseChart').getContext('2d');
    const ctxCurrent = document.getElementById('currentChart').getContext('2d');
    const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');

    // Definindo os thresholds
    const temperatureThreshold = 40;
    const vibrationThreshold = 5;
    const currentThreshold = 5.5;

    // Função para adicionar a linha de threshold
    // Função para adicionar uma área de threshold vermelha
function addThresholdArea(chart, threshold) {
    chart.options.plugins.annotation = {
        annotations: {
            thresholdBox: {
                type: 'box',
                yMin: threshold, // O threshold no eixo Y
                yMax: chart.scales['y'].max, // Preenche até o topo do gráfico
                backgroundColor: 'rgba(255, 0, 0, 0.2)', // Cor vermelha transparente
                borderColor: 'rgba(255, 0, 0, 0)', // Sem borda
                borderWidth: 0,
                xMin: chart.scales['x'].min, // Preenche toda a área no eixo X
                xMax: chart.scales['x'].max,
                label: {
                    content: `Threshold: ${threshold}`,
                    enabled: true,
                    position: 'start',
                    backgroundColor: 'rgba(255, 0, 0, 0.5)'
                }
            }
        }
    };
}


    // Configuração do gráfico de vibração do braço
    vibrationBracoChart = new Chart(ctxVibrationBraco, {
        type: 'line',
        data: {
            labels: [], // Horas e dias
            datasets: [{
                label: 'Vibração do Braço',
                data: [], // Dados de vibração
                backgroundColor: 'rgba(103, 58, 183, 0.2)',
                borderColor: 'rgba(103, 58, 183, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 1
            },
            plugins: {
                annotation: {} // Certifique-se de que o plugin de anotações está habilitado
            }
        }
    });
    addThresholdArea(vibrationBracoChart, vibrationThreshold);

    // Configuração do gráfico de vibração da base
    vibrationBaseChart = new Chart(ctxVibrationBase, {
        type: 'line',
        data: {
            labels: [], // Horas e dias
            datasets: [{
                label: 'Vibração da Base',
                data: [], // Dados de vibração
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 1
            },
            plugins: {
                annotation: {}
            }
        }
    });
    addThresholdArea(vibrationBaseChart, vibrationThreshold);

    // Configuração do gráfico de corrente
    currentChart = new Chart(ctxCurrent, {
        type: 'line',
        data: {
            labels: [], // Horas e dias
            datasets: [{
                label: 'Corrente',
                data: [], // Dados de corrente
                backgroundColor: 'rgba(58, 134, 255, 0.2)',
                borderColor: 'rgba(58, 134, 255, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 2
            },
            plugins: {
                annotation: {}
            }
        }
    });
    addThresholdArea(currentChart, currentThreshold);

    // Configuração do gráfico de temperatura
    temperatureChart = new Chart(ctxTemperature, {
        type: 'line',
        data: {
            labels: [], // Horas e dias
            datasets: [{
                label: 'Temperatura',
                data: [], // Dados de temperatura
                backgroundColor: 'rgba(186, 104, 200, 0.2)',
                borderColor: 'rgba(186, 104, 200, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: { beginAtZero: true },
                y: 25
            },
            plugins: {
                annotation: {}
            }
        }
    });
    addThresholdArea(temperatureChart, temperatureThreshold);
}

// Função genérica para atualizar os gráficos
function updateChart(chart, labels, data, threshold) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data || [];

    // Atualiza o gráfico com os novos dados e atualiza a área de threshold
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

// Função assíncrona para aplicar filtros e atualizar as caixas de média

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



async function generatePDFReport(filters, data, imagePath) {
    // Carregar a biblioteca jsPDF
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF(); // Instância do jsPDF

    const reportData = {
        filters: filters,
        data: data
    };

    const response = await fetch('/pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reportData)
    });

    const pdfContent = await response.text(); // Supondo que a resposta seja um texto
    const lines = pdfContent.split('\n'); // Divide o texto em linhas
    let yPosition = 50; // Posição Y inicial após a imagem
    const lineHeight = 10; // Altura da linha
    const spacing = 10; // Espaçamento entre as seções
    const pageWidth = doc.internal.pageSize.getWidth(); // Largura da página
    const pageHeight = doc.internal.pageSize.getHeight(); // Altura da página

    // Lista de linhas que devem estar em negrito
    const boldList = [
        'Relatório Técnico',
        '1. Identificação da Máquina',
        '2. Resumo Executivo',
        '3. Descrição Técnica da Máquina',
        'Especificações Técnicas: ',
        '3.1. Estrutura Mecânica',
        '3.2. Motores de Passo',
        '3.3. Sensores',
        'Sensor de Corrente (ACS712):',
        'Sensor de Vibração (MPU6050):',
        'Sensor de Temperatura (AMG8833):',
        '3.4. Microcontroladores',
        '3.5. Fonte de Alimentação',
        '3.6. Software',
        '4. Histórico de Operação',
        '5. Procedimentos de Inspeção ou Manutenção',
        '6. Diagnóstico e Condição da Máquina',
        '7. Recomendações',
        '8. Conclusão'
    ];

    // Função para converter a imagem em Base64 e obter as dimensões
    async function getImageAndDimensions(imagePath) {
        const response = await fetch(imagePath);
        const blob = await response.blob();
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                const img = new Image();
                img.src = reader.result;
                img.onload = () => {
                    resolve({
                        base64: reader.result,
                        width: img.width,
                        height: img.height
                    });
                };
                img.onerror = reject;
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    // Carregar a imagem e obter as dimensões originais
    const { base64: imgData, width: imgOriginalWidth, height: imgOriginalHeight } = await getImageAndDimensions("static/images/logo_pdf.png");

    // Definir o tamanho máximo permitido (ajustável) mantendo a proporção
    const maxWidth = pageWidth - 20; // Margens de 10px em cada lado
    const maxHeight = 50; // Altura máxima desejada

    // Calcular o fator de escala para manter as proporções
    let scale = Math.min(maxWidth / imgOriginalWidth, maxHeight / imgOriginalHeight);
    const imgWidth = imgOriginalWidth * scale;
    const imgHeight = imgOriginalHeight * scale;

    // Calcular a posição X para centralizar a imagem
    const xPosition = (pageWidth - imgWidth) / 2;

    // Adiciona a imagem ao topo da página mantendo as proporções
    doc.addImage(imgData, 'PNG', xPosition, 10, imgWidth, imgHeight); // Adiciona a imagem (x, y, width, height)

    // Função para adicionar linhas ao PDF
    function addLines(lines) {
        lines.forEach((line) => {
            const trimmedLine = line.trim(); // Remove espaços em branco

            // Verifica se a linha atual está na lista de negrito
            if (boldList.includes(trimmedLine)) {
                yPosition += spacing; // Adiciona uma linha em branco antes da frase em negrito

                doc.setFont("helvetica", "bold"); // Define a fonte como negrito
            } else {
                doc.setFont("helvetica", "normal"); // Define a fonte como normal
            }

            // Quebra o texto para caber na largura da página
            const splitLines = doc.splitTextToSize(line, pageWidth - 20); // Margens de 10px de cada lado

            splitLines.forEach((splitLine) => {
                // Adiciona a linha ao PDF
                doc.text(splitLine, 10, yPosition);
                yPosition += lineHeight; // Incrementa a posição Y

                // Verifica se a posição Y excede a altura da página
                if (yPosition > doc.internal.pageSize.getHeight() - 20) { // Margem inferior
                    doc.addPage(); // Adiciona uma nova página
                    yPosition = 10; // Reinicia a posição Y
                }
            });
        });
    }

    // Adiciona as linhas ao PDF
    addLines(lines);

    doc.save('relatorio.pdf'); // Salva o PDF
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
}

// Inicializar os gráficos ao carregar a página
initCharts();
