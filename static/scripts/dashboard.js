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
    const ctxVibrationBraco = document.getElementById('vibrationBracoChart').getContext('2d');
    const vibrationBracoChart = new Chart(ctxVibrationBraco, {
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
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const ctxVibrationBase = document.getElementById('vibrationBaseChart').getContext('2d');
    const vibrationBaseChart = new Chart(ctxVibrationBase, {
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
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const ctxCurrent = document.getElementById('currentChart').getContext('2d');
    const currentChart = new Chart(ctxCurrent, {
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
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');
    const temperatureChart = new Chart(ctxTemperature, {
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
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    return { vibrationBracoChart, vibrationBaseChart, currentChart, temperatureChart };
}

// Função para aplicar os filtros
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
        monthWeek: selectedTimeRange === 'week' ? monthWeek : null
    };

    const data = await fetchData(filters);
    updateCharts(data, selectedTimeRange);  // Passa o intervalo de tempo
}

// Função para atualizar os gráficos com base no intervalo de tempo selecionado
function updateCharts(data, timeRange) {
    if (data && data.timestamp) {
        let labelFormat;
        switch (timeRange) {
            case 'day':
                labelFormat = ts => new Date(ts).toLocaleTimeString();  // Exibe horas
                break;
            case 'week':
                labelFormat = ts => new Date(ts).toLocaleDateString();  // Exibe dias
                break;
            case 'month':
                labelFormat = ts => `Semana ${getWeekOfMonth(new Date(ts))}`;  // Exibe semanas do mês
                break;
            case 'year':
                labelFormat = ts => new Date(ts).toLocaleString('default', { month: 'short' });  // Exibe meses
                break;
            default:
                labelFormat = ts => new Date(ts).toLocaleString();  // Exibe data completa como fallback
        }

        vibrationBracoChart.data.labels = data.timestamp.map(labelFormat);
        vibrationBracoChart.data.datasets[0].data = data.vibracao_braco || [];
        vibrationBracoChart.update();

        vibrationBaseChart.data.labels = data.timestamp.map(labelFormat);
        vibrationBaseChart.data.datasets[0].data = data.vibracao_base || [];
        vibrationBaseChart.update();

        currentChart.data.labels = data.timestamp.map(labelFormat);
        currentChart.data.datasets[0].data = data.corrente || [];
        currentChart.update();

        temperatureChart.data.labels = data.timestamp.map(labelFormat);
        temperatureChart.data.datasets[0].data = data.temperatura || [];
        temperatureChart.update();
    } else {
        console.error("Os dados fornecidos não são válidos:", data);
    }
}

// Função auxiliar para obter a semana do mês
function getWeekOfMonth(date) {
    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    return Math.ceil((date.getDate() + firstDay) / 7);
}

const { vibrationBracoChart, vibrationBaseChart, currentChart, temperatureChart } = initCharts();
document.getElementById('applyFilter').addEventListener('click', applyFilters);
