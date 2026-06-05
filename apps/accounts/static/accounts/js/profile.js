document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const fileNameSpan = document.querySelector('.file-name');

    if (fileInput && fileNameSpan) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'No file chosen';
            fileNameSpan.textContent = fileName;
        });
    }
});