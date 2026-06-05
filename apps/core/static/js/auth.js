// ============================================
// Auth helpers: password toggle, strength meter
// ============================================

function togglePassword(fieldId = 'passwordField') {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = field.type === 'password' ? 'text' : 'password';
    }
}

function checkPasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    return score; // 0–4
}

function updateStrengthMeter(inputId, meterId) {
    const input = document.getElementById(inputId);
    const meter = document.getElementById(meterId);
    if (!input || !meter) return;

    input.addEventListener('input', () => {
        const strength = checkPasswordStrength(input.value);
        const colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e'];
        const labels = ['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'];
        meter.style.width = `${(strength + 1) * 20}%`;
        meter.style.backgroundColor = colors[strength];
        meter.textContent = labels[strength];
        meter.style.color = strength >= 4 ? '#fff' : '#000';
    });
}

// Initialize strength meter on pages with password field
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('password1')) {
        updateStrengthMeter('password1', 'strengthMeter');
    } else if (document.getElementById('passwordField')) {
        updateStrengthMeter('passwordField', 'strengthMeter');
    }
});