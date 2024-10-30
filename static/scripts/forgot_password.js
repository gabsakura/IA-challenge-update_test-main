async function enviarSolicitacao(event) {
    event.preventDefault(); // Impede o envio padrão do formulário
  
    const username = document.getElementById('username').value;
  
    try {
      const response = await fetch('/esqueci_senha', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
          username: username
        })
      });
  
      if (response.redirected) {
        // Se o servidor redirecionou, atualiza a localização
        window.location.href = response.url;
      } else {
        const errorMessage = await response.text();
        alert('Erro: ' + errorMessage);
      }
    } catch (error) {
      console.error('Erro ao enviar solicitação:', error);
      alert('Ocorreu um erro. Tente novamente mais tarde.');
    }
  }
  