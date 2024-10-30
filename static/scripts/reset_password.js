document.getElementById('resetPasswordForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const messageElement = document.getElementById('message');

    if (password !== confirmPassword) {
        messageElement.textContent = 'As senhas não coincidem.';
        messageElement.style.display = 'block';
        return;
    }

    // Simula uma solicitação de redefinição de senha bem-sucedida
    messageElement.textContent = 'Senha redefinida com sucesso!';
    messageElement.style.display = 'block';
});
