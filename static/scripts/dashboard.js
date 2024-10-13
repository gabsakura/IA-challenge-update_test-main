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

// Função para inicializar os gráficos vazios
function initCharts() {
    // Gráfico de Vibração do Braço
    const ctxVibrationBraco = document.getElementById('vibrationBracoChart').getContext('2d');
    const vibrationBracoChart = new Chart(ctxVibrationBraco, {
        type: 'line', // Mudança para gráfico de barras
        data: {
            labels: [], // Inicializa vazio
            datasets: [{
                label: 'Vibração do Braço',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)', // Alteração para melhor visualização
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { 
                    beginAtZero: true 
                },
                y: { 
                    beginAtZero: true 
                }
            }
        }
    });

    // Gráfico de Vibração da Base
    const ctxVibrationBase = document.getElementById('vibrationBaseChart').getContext('2d');
    const vibrationBaseChart = new Chart(ctxVibrationBase, {
        type: 'line', // Mudança para gráfico de barras
        data: {
            labels: [], // Inicializa vazio
            datasets: [{
                label: 'Vibração da Base',
                data: [],
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.5)', // Alteração para melhor visualização
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { 
                    beginAtZero: true 
                },
                y: { 
                    beginAtZero: true 
                }
            }
        }
    });

    // Gráfico de Corrente
    const ctxCurrent = document.getElementById('currentChart').getContext('2d');
    const currentChart = new Chart(ctxCurrent, {
        type: 'line', // Mudança para gráfico de barras
        data: {
            labels: [], // Inicializa vazio
            datasets: [{
                label: 'Corrente',
                data: [],
                borderColor: 'rgba(255, 159, 64, 1)',
                backgroundColor: 'rgba(255, 159, 64, 0.5)', // Alteração para melhor visualização
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { 
                    beginAtZero: true 
                },
                y: { 
                    beginAtZero: true 
                }
            }
        }
    });

    // Gráfico de Temperatura
    const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');
    const temperatureChart = new Chart(ctxTemperature, {
        type: 'line', // Mudança para gráfico de barras
        data: {
            labels: [], // Inicializa vazio
            datasets: [{
                label: 'Temperatura',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)', // Alteração para melhor visualização
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: { 
                    beginAtZero: true 
                },
                y: { 
                    beginAtZero: true 
                }
            }
        }
    });

    // Retornar as referências dos gráficos para atualizar depois
    return {
        vibrationBracoChart,
        vibrationBaseChart,
        currentChart,
        temperatureChart
    };
}

async function applyFilters() {
    const selectedTimeRange = document.getElementById('timeRange').value;
    const day = document.getElementById('day').value;
    const month = document.getElementById('month').value;
    const week = document.getElementById('week').value;
    const year = document.getElementById('year').value;
    const monthWeek = document.getElementById('monthWeek').value;

    const filters = {
        timeRange: selectedTimeRange,
        day: selectedTimeRange === 'day' ? day : null,
        month: selectedTimeRange === 'month' ? month : null,
        week: selectedTimeRange === 'week' ? week : null,
        year: selectedTimeRange === 'year' ? year : null,
        monthWeek: selectedTimeRange === 'week' ? monthWeek : null // Adiciona monthWeek quando o filtro é "semana"
    };

    // Enviar os filtros para a rota do Flask e obter novos dados
    const data = await fetchData(filters);

    // Atualizar os gráficos com os novos dados
    updateCharts(data);
}


// Função para atualizar os gráficos com os novos dados
function updateCharts(data) {
    // Verifica se os dados estão disponíveis
    if (data && data.timestamp) {
        // Atualizar gráfico de Vibração do Braço
        vibrationBracoChart.data.labels = data.timestamp.map(ts => new Date(ts).toLocaleTimeString()); // Formatação das labels
        vibrationBracoChart.data.datasets[0].data = data.vibracao_braco || [];
        vibrationBracoChart.update();

        // Atualizar gráfico de Vibração da Base
        vibrationBaseChart.data.labels = data.timestamp.map(ts => new Date(ts).toLocaleTimeString()); // Formatação das labels
        vibrationBaseChart.data.datasets[0].data = data.vibracao_base || [];
        vibrationBaseChart.update();

        // Atualizar gráfico de Corrente
        currentChart.data.labels = data.timestamp.map(ts => new Date(ts).toLocaleTimeString()); // Formatação das labels
        currentChart.data.datasets[0].data = data.corrente || [];
        currentChart.update();

        // Atualizar gráfico de Temperatura
        temperatureChart.data.labels = data.timestamp.map(ts => new Date(ts).toLocaleTimeString()); // Formatação das labels
        temperatureChart.data.datasets[0].data = data.temperatura || [];
        temperatureChart.update();
    } else {
        console.error("Os dados fornecidos não são válidos:", data);
    }
}

// Inicializar os gráficos ao carregar a página
const { vibrationBracoChart, vibrationBaseChart, currentChart, temperatureChart } = initCharts();

// Adicionar o evento de clique ao botão "Aplicar Filtro"
document.getElementById('applyFilter').addEventListener('click', applyFilters);
