let mainChart = null;
let allMunicipios = [];   // aquí guardamos TODOS los datos para filtrarlos

function buildMainChart(ctx) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    type: 'bar',
                    label: 'Temperatura (°C)',
                    data: [],
                    backgroundColor: 'rgba(242, 163, 65, 0.85)',
                    borderRadius: 12,
                    maxBarThickness: 28
                },
                {
                    type: 'bar',
                    label: 'Humedad (%)',
                    data: [],
                    backgroundColor: 'rgba(107, 143, 113, 0.85)',
                    borderRadius: 12,
                    maxBarThickness: 28
                },
                {
                    type: 'line',
                    label: 'Luz (lux)',
                    data: [],
                    borderColor: '#BF6B63',
                    borderWidth: 2.5,
                    pointRadius: 3.5,
                    pointBackgroundColor: '#BF6B63',
                    yAxisID: 'y1',
                    tension: 0.35
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#7A6156',
                        font: { size: 11 }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(200, 160, 120, 0.25)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#7A6156',
                        font: { size: 11 }
                    }
                },
                y1: {
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false },
                    ticks: {
                        color: '#BF6B63',
                        font: { size: 11 }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 16,
                        color: '#392A28',
                        font: { size: 11 }
                    }
                },
                tooltip: {
                    backgroundColor: '#2C2430',
                    titleColor: '#F2D0A4',
                    bodyColor: '#FFFFFF',
                    padding: 10,
                    cornerRadius: 12,
                    displayColors: false
                }
            }
        }
    });
}

// Actualiza el gráfico a partir de un arreglo de municipios (ya filtrado)
function updateChartFromData(data) {
    if (!mainChart) return;

    const labels = [];
    const temps = [];
    const hums  = [];
    const luces = [];

    data.forEach(item => {
        labels.push(item.municipio);
        temps.push(item.temperatura ?? null);
        hums.push(item.humedad ?? null);
        luces.push(item.luz ?? null);
    });

    mainChart.data.labels = labels;
    mainChart.data.datasets[0].data = temps;
    mainChart.data.datasets[1].data = hums;
    mainChart.data.datasets[2].data = luces;
    mainChart.update();
}


function applySearchFilter() {
    if (!mainChart) return;

    const input = document.querySelector('.search input');
    if (!input) {
        updateChartFromData(allMunicipios);
        return;
    }

    const term = input.value.trim().toLowerCase();
    let filtered = allMunicipios;

    if (term) {
        filtered = allMunicipios.filter(item =>
            item.municipio.toLowerCase().includes(term) ||
            item.slug.toLowerCase().includes(term)
        );
    }

    updateChartFromData(filtered);
}

function refreshMainChart() {
    fetch('/api/ultimas/')
        .then(response => response.json())
        .then(json => {
            allMunicipios = json.data || [];
            applySearchFilter(); // actualiza usando lo que haya en el cuadro de búsqueda
        })
        .catch(err => console.error('Error actualizando gráfico', err));
}

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('mainChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    mainChart = buildMainChart(ctx);
    refreshMainChart();
    setInterval(refreshMainChart, 3000);

    // Hacer que el cuadro de búsqueda filtre en vivo
    const input = document.querySelector('.search input');
    if (input) {
        input.addEventListener('input', () => {
            applySearchFilter();
        });
    }
});