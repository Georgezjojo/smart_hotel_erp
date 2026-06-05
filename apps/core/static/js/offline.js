window.addEventListener('offline', () => {
    const alert = document.getElementById('offlineAlert');
    if (alert) alert.classList.remove('hidden');
});
window.addEventListener('online', () => {
    const alert = document.getElementById('offlineAlert');
    if (alert) alert.classList.add('hidden');
});