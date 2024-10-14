// Dados para cada parte: imagem e texto
const partData = {
    1: {
        img: ['static/images/braco/Camera-thermica.jpg'],
        text: 'Esse é o componente AMG8833 uma camera termica no qual é responsavel em captar os dados referentes a temperatura.'
    },
    2: {
        img: ['static/images/braco/Stepdown-grande.jpg', 'static/images/braco/Sensor_corrente.jpg'],
        text: 'Este é o componente XY6020L junto ao ACS712, responsáveis por setar e monitorar a voltagem e corrente do braço robótico.'
    },
    3: {
        img: ['static/images/braco/Servo-grande.webp'],
        text: 'Este é um servo MG945 no qual está dentro do eixo, servindo como movimentação crucial do braço robótico.'
    },
    4: {
        img: ['static/images/braco/MPU6050.jpg'],
        text: 'Usamos o sensor MPU6050 para o cálculo de vibração no projeto, utilizando a mudança entre os eixos.'
    },
    5: {
        img: ['static/images/braco/Mega.webp', 'static/images/braco/CNC_shield.jpg', 'static/images/braco/Driver_A4988.jpg','static/images/braco/Fonte.jpg','static/images/braco/stepdown_pequeno.webp' ],
        text: 'Essa é a caixa que guarda todos os componentes do projeto, como Arduino Mega, CNC Shield V3, Driver A4988(roxo), Fonte chaveada S-250, Stepdown: LM2596.'
    },
    6: {
        img: ['static/images/braco/Motor_passo.jpg'],
        text: 'Utilizamos o motor Nema 17 para movimentar a base e os eixos do projeto.'
    },
    7: {
        img: ['static/images/braco/minimotor.webp'],
        text: 'Esta é a garra utilizada para pegar e colocar objetos, manipulada por um mini motor DC N20.'
    },
};
let currentIndex = 0; // Índice da imagem atual
let currentPart = null; // Parte atual sendo visualizada

function showPart(part) {
    const modal = document.getElementById('modal');
    const zoomedImg = document.getElementById('zoomed-img');
    const zoomedText = document.getElementById('zoomed-text');
    const imgContainer = document.querySelector('.img-container img');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    // Armazena a parte atual
    currentPart = part;
    currentIndex = 0; // Reinicia o índice da imagem

    // Adiciona o blur na imagem principal
    imgContainer.classList.add('blur');

    // Define o texto e a primeira imagem a ser exibida
    zoomedImg.src = partData[part].img[currentIndex];
    zoomedText.textContent = partData[part].text;

    // Verifica se há mais de uma imagem e exibe as setas se necessário
    if (partData[part].img.length > 1) {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
    } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
    }

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

// Função para navegar entre as imagens
function changeImage(n) {
    const zoomedImg = document.getElementById('zoomed-img');
    const images = partData[currentPart].img; // Obtém as imagens da parte atual

    // Atualiza o índice da imagem, garantindo que fique dentro dos limites
    currentIndex = (currentIndex + n + images.length) % images.length;

    // Atualiza a imagem no modal
    zoomedImg.src = images[currentIndex];
}
