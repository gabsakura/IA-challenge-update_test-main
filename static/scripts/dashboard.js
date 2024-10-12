document.addEventListener('DOMContentLoaded', () => {
    let vibrationChartInstance = null;
    let currentChartInstance = null;
    let temperatureChartInstance = null;

    const applyFilterBtn = document.getElementById('applyFilter');
    applyFilterBtn.addEventListener('click', () => {
        const timeRange = document.getElementById('timeRange').value;
        fetchData(timeRange);
    });

    function fetchData(timeRange) {
        fetch(`/api/dados?time_range=${timeRange}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro no servidor:", data.error);
                    return;
                }
                console.log("Dados recebidos:", data);
                const vibrationData = {
                    labels: data.tempo,
                    values: data.vibracao
                };
                const correnteData = {
                    labels: data.tempo,
                    values: data.corrente
                };
                const temperatureData = {
                    labels: data.tempo,
                    values: data.temperatura
                };
                loadCharts(vibrationData, correnteData, temperatureData);
            })
            .catch(error => console.error('Erro ao carregar dados:', error));
    }

    function destroyChart(chartInstance) {
        if (chartInstance) {
            chartInstance.destroy();
        }
    }

    function loadCharts(vibrationData, correnteData, temperatureData) {
        destroyChart(vibrationChartInstance);
        destroyChart(currentChartInstance);
        destroyChart(temperatureChartInstance);

        const ctxVibration = document.getElementById('vibrationChart').getContext('2d');
        vibrationChartInstance = new Chart(ctxVibration, {
            type: 'line',
            data: {
                labels: vibrationData.labels,
                datasets: [{
                    label: 'Vibração Base',
                    data: vibrationData.values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'dd/MM/yyyy HH:mm',
                            displayFormats: { day: 'dd/MM' }
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        const ctxCurrent = document.getElementById('currentChart').getContext('2d');
        currentChartInstance = new Chart(ctxCurrent, {
            type: 'line',
            data: {
                labels: correnteData.labels,
                datasets: [{
                    label: 'Corrente',
                    data: correnteData.values,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'dd/MM/yyyy HH:mm',
                            displayFormats: { day: 'dd/MM' }
                        }
                    },
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });

        const ctxTemperature = document.getElementById('gaugeChart').getContext('2d');
        temperatureChartInstance = new Chart(ctxTemperature, {
            type: 'line',
            data: {
                labels: temperatureData.labels,
                datasets: [{
                    label: 'Temperatura',
                    data: temperatureData.values,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'dd/MM/yyyy HH:mm',
                            displayFormats: { day: 'dd/MM' }
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    fetchData('day');
});
