document.addEventListener('DOMContentLoaded', () => {
    let vibrationBaseChartInstance = null;
    let vibrationBracoChartInstance = null;
    let currentChartInstance = null;
    let temperatureChartInstance = null;

    const applyFilterBtn = document.getElementById('applyFilter');
    applyFilterBtn.addEventListener('click', () => {
        const timeRange = document.getElementById('timeRange').value;
        fetchData(timeRange);
    });

    // Função para buscar os dados filtrados do backend
    function fetchData(timeRange) {
        fetch(`/api/dados?time_range=${timeRange}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro no servidor:", data.error);
                    return;
                }

                console.log("Dados recebidos:", data);

                const vibrationBaseData = {
                    labels: data.tempo,
                    datasets: [{
                        label: 'Vibração Base',
                        data: data.vibracao_base,
                        backgroundColor: 'rgba(75, 192, 192, 0.8)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        fill: true
                    }]
                };

                const vibrationBracoData = {
                    labels: data.tempo,
                    datasets: [{
                        label: 'Vibração Braço',
                        data: data.vibracao_braco,
                        backgroundColor: 'rgba(255, 159, 64, 0.8)',
                        borderColor: 'rgba(255, 159, 64, 1)',
                        borderWidth: 1,
                        fill: true
                    }]
                };

                const correnteData = {
                    labels: data.tempo,
                    datasets: [{
                        label: 'Corrente',
                        data: data.corrente,
                        backgroundColor: 'rgba(153, 102, 255, 0.8)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 2,
                        fill: true
                    }]
                };

                const temperatureData = {
                    labels: data.tempo,
                    datasets: [{
                        label: 'Temperatura',
                        data: data.temperatura,
                        backgroundColor: 'rgba(255, 99, 132, 0.8)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        fill: true
                    }]
                };

                loadCharts(vibrationBaseData, vibrationBracoData, correnteData, temperatureData);
            })
            .catch(error => console.error('Erro ao carregar dados:', error));
    }

    // Função para destruir o gráfico anterior, se existir
    function destroyChart(chartInstance) {
        if (chartInstance) {
            chartInstance.destroy();
        }
    }

    // Função para carregar os gráficos (tipo de gráfico: barras)
    function loadCharts(vibrationBaseData, vibrationBracoData, correnteData, temperatureData) {
        destroyChart(vibrationBaseChartInstance);
        destroyChart(vibrationBracoChartInstance);
        destroyChart(currentChartInstance);
        destroyChart(temperatureChartInstance);

        const zoomOptions = {
            pan: {
                enabled: true,
                mode: 'x',
                speed: 20,
                threshold: 10
            },
            zoom: {
                wheel: {
                    enabled: true
                },
                drag: {
                    enabled: true
                },
                mode: 'x',
                speed: 0.1
            }
        };

        // Gráfico de Barras - Vibração Base
        const ctxVibrationBase = document.getElementById('vibrationBaseChart').getContext('2d');
        vibrationBaseChartInstance = new Chart(ctxVibrationBase, {
            type: 'bar',
            data: vibrationBaseData,
            options: {
                responsive: true,
                plugins: {
                    zoom: zoomOptions
                },
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

        // Gráfico de Barras - Vibração Braço
        const ctxVibrationBraco = document.getElementById('vibrationBracoChart').getContext('2d');
        vibrationBracoChartInstance = new Chart(ctxVibrationBraco, {
            type: 'bar',
            data: vibrationBracoData,
            options: {
                responsive: true,
                plugins: {
                    zoom: zoomOptions
                },
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

        // Gráfico de Barras - Corrente
        const ctxCurrent = document.getElementById('currentChart').getContext('2d');
        currentChartInstance = new Chart(ctxCurrent, {
            type: 'bar',
            data: correnteData,
            options: {
                responsive: true,
                plugins: {
                    zoom: zoomOptions
                },
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

        // Gráfico de Barras - Temperatura
        const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');
        temperatureChartInstance = new Chart(ctxTemperature, {
            type: 'bar',
            data: temperatureData,
            options: {
                responsive: true,
                plugins: {
                    zoom: zoomOptions
                },
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

    // Carregar os gráficos iniciais com o intervalo 'day'
    fetchData('day');
});
