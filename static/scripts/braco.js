// Dados para cada parte: imagem e texto
const partData = {
    1: {
        img: 'images/part1.jpeg', // Substitua pelo caminho correto da imagem
        text: 'Parte 1: Esta é a base do braço robótico, onde todos os componentes se conectam.'
    },
    2: {
        img: 'images/part2.jpeg',
        text: 'Parte 2: Esta seção contém os atuadores responsáveis pelo movimento.'
    },
    3: {
        img: 'images/part3.jpeg',
        text: 'Parte 3: Aqui vemos os motores que permitem a rotação precisa do braço.'
    },
    4: {
        img: 'images/part4.jpeg',
        text: 'Parte 4: Estrutura intermediária, oferecendo suporte para o braço.'
    },
    5: {
        img: 'images/part5.jpeg',
        text: 'Parte 5: Sistema de controle de torque e força.'
    },
    6: {
        img: 'images/part6.jpeg',
        text: 'Parte 6: Conexões para os sensores de feedback.'
    },
    7: {
        img: 'images/part7.jpeg',
        text: 'Parte 7: A base da garra que é usada para manipulação de objetos.'
    },
    8: {
        img: 'images/part8.jpeg',
        text: 'Parte 8: Conectores hidráulicos que geram força de preensão.'
    },
    9: {
        img: 'images/part9.jpeg',
        text: 'Parte 9: A garra em si, utilizada para interagir com o ambiente.'
    }
};

// Função para abrir o modal e exibir a parte ampliada
function showPart(part) {
    const modal = document.getElementById('modal');
    const zoomedImg = document.getElementById('zoomed-img');
    const zoomedText = document.getElementById('zoomed-text');
    const imgContainer = document.querySelector('.img-container img');

    // Adiciona o blur na imagem principal
    imgContainer.classList.add('blur');

    // Define o caminho da imagem e o texto baseado na parte selecionada
    zoomedImg.src = partData[part].img;
    zoomedText.textContent = partData[part].text;

    // Exibe o modal
    modal.style.display = 'flex';
}

// Função para fechar o modal e remover o blur
function closeModal() {
    const modal = document.getElementById('modal');
    const imgContainer = document.querySelector('.img-container img');

    // Remove o blur da imagem principal
    imgContainer.classList.remove('blur');

    // Esconde o modal
    modal.style.display = 'none';
}
