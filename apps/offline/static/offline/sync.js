const db = new Dexie('HotelERPOffline');
db.version(1).stores({
    pendingReservations: '++id, payload'
});

// Save offline booking
function saveOffline(data) {
    db.pendingReservations.add({ payload: JSON.stringify(data) });
    if ('serviceWorker' in navigator && 'SyncManager' in window) {
        navigator.serviceWorker.ready.then(reg => reg.sync.register('sync-reservations'));
    }
}

// Sync when online
window.addEventListener('online', () => {
    db.pendingReservations.toArray().then(rows => {
        rows.forEach(row => {
            fetch('/reservations/api/', {
                method: 'POST',
                body: row.payload,
                headers: {'Content-Type': 'application/json'}
            }).then(res => {
                if (res.ok) db.pendingReservations.delete(row.id);
            });
        });
    });
});