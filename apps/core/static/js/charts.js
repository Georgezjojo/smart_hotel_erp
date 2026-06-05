// Example: create a Chart.js chart on elements with .chart-canvas
document.addEventListener('DOMContentLoaded', () => {
    const canvases = document.querySelectorAll('.chart-canvas');
    canvases.forEach(canvas => {
        const url = canvas.dataset.url;
        if (url) {
            fetch(url)
                .then(res => res.json())
                .then(data => {
                    new Chart(canvas, {
                        type: 'line',
                        data: data,
                        options: { responsive: true }
                    });
                });
        }
    });
});