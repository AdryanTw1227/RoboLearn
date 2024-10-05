// Obter a lista de jogos
fetch('/jogos')
  .then(response => response.json())
  .then(data => {
    const gameGrid = document.querySelector('.game-grid');
    data.forEach(jogo => {
      const gameCard = document.createElement('div');
      gameCard.classList.add('game-card');
      const gameImage = document.createElement('img');
      gameImage.src = jogo.imagem;
      gameImage.alt = jogo.nome;
      gameImage.classList.add('game-image');
      const gameTitle = document.createElement('h3');
      gameTitle.textContent = jogo.nome;
      gameCard.appendChild(gameImage);
      gameCard.appendChild(gameTitle);
      gameGrid.appendChild(gameCard);
    });
  });

// Criar um novo jogo
document.querySelector('.game-grid').addEventListener('click', (e) => {
  if (e.target.classList.contains('game-image')) {
    const jogoId = e.target.alt;
    const jogoNome = e.target.src;
    const jogoDescricao = 'Descrição do jogo';
    const jogoImagem = jogoNome;
    const jogoCategoria = 'Categoria do jogo';

    fetch('/jogos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nome: jogoNome,
        descricao: jogoDescricao,
        imagem: jogoImagem,
        categoria: jogoCategoria
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
      });
  }
});

// Obter os scores de um jogo
document.querySelector('.game-grid').addEventListener('click', (e) => {
  if (e.target.classList.contains('game-image')) {
    const jogoId = e.target.alt;
    fetch(`/jogos/${jogoId}/scores`)
      .then(response => response.json())
      .then(data => {
        console.log(data);
      });
  }
});

// Criar um novo score para um jogo
document.querySelector('.game-grid').addEventListener('click', (e) => {
  if (e.target.classList.contains('game-image')) {
    const jogoId = e.target.alt;
    const score = 100;
    fetch(`/jogos/${jogoId}/scores`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        score: score
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
      });
  }
});
