// Função para gerar a senha
function generatePassword() {
    const length = document.getElementById('slider').value;
    const numbers = document.getElementById('numbers').checked;
    const symbols = document.getElementById('symbols').checked;
    const uppercase = document.getElementById('uppercase').checked;
    const lowercase = document.getElementById('lowercase').checked;

    let characters = "";
    if (numbers) characters += "0123456789";
    if (symbols) characters += "!@#$%^&*()_+[]{}|;:,.<>?";
    if (uppercase) characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    if (lowercase) characters += "abcdefghijklmnopqrstuvwxyz";

    if (characters.length === 0) {
        document.getElementById('generated-password').value = '';
        return;
    }

    let password = '';
    for (let i = 0; i < length; i++) {
        password += characters.charAt(Math.floor(Math.random() * characters.length));
    }

    document.getElementById('generated-password').value = password;
}

// Função para atualizar o valor mostrado do slider
function updateLengthLabel(value) {
    document.getElementById('slider-value').textContent = value;
}

// Gera a senha automaticamente quando a página é carregada pela primeira vez
document.addEventListener('DOMContentLoaded', (event) => {
    generatePassword();
});
