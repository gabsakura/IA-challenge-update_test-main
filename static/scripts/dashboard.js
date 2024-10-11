function loadCharts(vibrationData, currentData, temperatureData) {
    // Gráfico de Linhas - Setor de Vibração
    const ctxVibration = document.getElementById('vibrationChart').getContext('2d');
    new Chart(ctxVibration, {
        type: 'line',
        data: {
            labels: vibrationData.labels,
            datasets: [{
                label: 'Vibração',
                data: vibrationData.values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: true
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de Meio Círculo (Gauge) - Setor de Temperatura
    const ctxGauge = document.getElementById('gaugeChart').getContext('2d');
    new Chart(ctxGauge, {
        type: 'doughnut',
        data: {
            labels: ['Temperatura'],
            datasets: [{
                data: [temperatureData.value, 100 - temperatureData.value], // Valor atual e o restante
                backgroundColor: ['rgba(255, 99, 132, 1)', 'rgba(0, 0, 0, 0)'],
                borderWidth: 0
            }]
        },
        options: {
            circumference: Math.PI,
            rotation: -Math.PI,
            cutout: '75%',
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            }
        }
    });

    // Adicionando o número no centro do Gauge
    Chart.pluginService.register({
        beforeDraw: function(chart) {
            if (chart.config.type === 'doughnut') {
                var width = chart.chart.width,
                    height = chart.chart.height,
                    ctx = chart.chart.ctx;
                ctx.restore();
                var fontSize = (height / 160).toFixed(2);
                ctx.font = fontSize + "em sans-serif";
                ctx.textBaseline = "middle";
                var text = temperatureData.value + "%", // Valor no centro
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = height / 2 + chart.chartArea.top / 2;
                ctx.fillStyle = '#ffffff';
                ctx.fillText(text, textX, textY);
                ctx.save();
            }
        }
    });

    // Gráfico de Linhas - Setor de Corrente
    const ctxCurrent = document.getElementById('temperatureChart').getContext('2d');
    new Chart(ctxCurrent, {
        type: 'line',
        data: {
            labels: currentData.labels,
            datasets: [{
                label: 'Corrente',
                data: currentData.values,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1,
                fill: true
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}
