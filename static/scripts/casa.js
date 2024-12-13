// scripts/home.js

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

// Aplicar o observer a todos os elementos com a classe 'hidden'
const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));



function toggleText(memberId) {
    const contributions = document.querySelectorAll('.contribuicoes');
    contributions.forEach(contribution => {
        if (contribution.id === memberId) {
            contribution.style.display = 'block';
        } else {
            contribution.style.display = 'none';
        }
    });
}