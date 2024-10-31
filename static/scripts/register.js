$(document).ready(function() {
    // Alterna a visibilidade da senha
    $('#togglePassword').click(function() {
        const passwordInput = $('#password');
        const passwordFieldType = passwordInput.attr('type');
        if (passwordFieldType === 'password') {
            passwordInput.attr('type', 'text');
            $(this).text('🔓'); // Ícone para mostrar a senha
        } else {
            passwordInput.attr('type', 'password');
            $(this).text('🔒'); // Ícone para esconder a senha
        }
    });

    // Envio do formulário via AJAX
    $('#registerForm').on('submit', function(e) {
        e.preventDefault();
        const formData = {
            username: $('#username').val(),
            password: $('#password').val(),
            secret_code: $('#secret_code').val(),
        };

        $.ajax({
            url: '/register',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                alert(response.message);
                window.location.href = '/login';  // Redireciona para a página de login
            },
            error: function(xhr) {
                alert(xhr.responseJSON.message);
            }
        });
    });
});
