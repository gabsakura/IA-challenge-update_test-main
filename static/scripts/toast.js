// toast.js

$(document).ready(function () {
    // Função para exibir toast
    function showToast(message) {
        const toastContainer = $('#toastContainer');
        toastContainer.find('.toast-body').text(message);
        const toastElement = new bootstrap.Toast(toastContainer);
        toastElement.show();
    }

    // Exemplo: Exibir toast de boas-vindas após o login
    showToast('Bem-vindo ao Dashboard!');
});
