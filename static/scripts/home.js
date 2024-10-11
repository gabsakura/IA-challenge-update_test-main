// scripts/home.js

function toggleText(memberId) {
    const contributions = document.querySelectorAll('.contribuicoes');
    contributions.forEach(contribution => {
        if (contribution.id === memberId) {
            contribution.style.display = contribution.style.display === 'block' ? 'none' : 'block';
        } else {
            contribution.style.display = 'none'; // Oculta outros
        }
    });
}
