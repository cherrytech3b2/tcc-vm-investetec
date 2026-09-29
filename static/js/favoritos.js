document.addEventListener("DOMContentLoaded", () => {
    carregarFavoritos();
});

function carregarFavoritos() {
    const grid = document.getElementById("favoritos-grid");
    const vazio = document.getElementById("favoritos-vazio");
    const contador = document.getElementById("contador-favoritos");

    if (!grid) return;

    const favoritos =
        JSON.parse(localStorage.getItem("investetec_favoritos")) || [];

    if (contador) {
        contador.textContent = favoritos.length;
    }

    if (favoritos.length === 0) {
        grid.innerHTML = "";
        if (vazio) {
            vazio.hidden = false;
        }
        return;
    }

    if (vazio) {
        vazio.hidden = true;
    }

    grid.innerHTML = favoritos.map((projeto) => `
        <article class="favorite-card" data-projeto-id="${projeto.id}">
            <div
                class="favorite-card__image"
                style="background-image: url('${projeto.imagem}')"
            >
                <span class="favorite-card__icon">
                    ${projeto.icone || "📁"}
                </span>

                <button
                    class="favorite-card__remove"
                    type="button"
                    data-remover-favorito="${projeto.id}"
                    aria-label="Remover dos favoritos"
                >
                    <i class="bi bi-star-fill"></i>
                </button>
            </div>

            <div class="favorite-card__body">
                <span class="favorite-card__category">
                    <i class="bi bi-bookmark-fill"></i>
                    ${projeto.categoria}
                </span>

                <h3>${projeto.nome}</h3>

                <p>${projeto.descricao}</p>

                <div class="favorite-card__footer">
                    <span>${projeto.nivel}</span>

                    <button
                        type="button"
                        class="favorite-card__button"
                        data-ver-projeto="${projeto.id}"
                    >
                        Ver projeto
                        <i class="bi bi-arrow-right"></i>
                    </button>
                </div>
            </div>
        </article>
    `).join("");

    configurarRemocao();
    configurarVisualizacao();
}

function configurarRemocao() {
    const botoes = document.querySelectorAll("[data-remover-favorito]");

    botoes.forEach((botao) => {
        botao.addEventListener("click", (evento) => {
            evento.stopPropagation();

            const id = String(botao.dataset.removerFavorito);

            let favoritos =
                JSON.parse(localStorage.getItem("investetec_favoritos")) || [];

            favoritos = favoritos.filter(
                (favorito) => String(favorito.id) !== id
            );

            localStorage.setItem(
                "investetec_favoritos",
                JSON.stringify(favoritos)
            );

            carregarFavoritos();
        });
    });
}

function configurarVisualizacao() {
    const botoes = document.querySelectorAll("[data-ver-projeto]");

    botoes.forEach((botao) => {
        botao.addEventListener("click", () => {
            const id = botao.dataset.verProjeto;

            const favoritos =
                JSON.parse(localStorage.getItem("investetec_favoritos")) || [];

            const projeto = favoritos.find(
                (favorito) => String(favorito.id) === String(id)
            );

            if (!projeto) return;

            alert(
                `${projeto.nome}\n\n${projeto.descricao}`
            );
        });
    });
}