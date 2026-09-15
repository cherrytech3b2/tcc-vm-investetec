document.addEventListener("DOMContentLoaded", () => {
  configurarNavegacaoLateral();
  configurarBotoesInteresse();
  configurarBuscaEFiltros();
  configurarBotaoFiltros();
});

function configurarNavegacaoLateral() {
  const itens = document.querySelectorAll(".nav-item");
  itens.forEach((item) => {
    item.addEventListener("click", (evento) => {
      evento.preventDefault();
      itens.forEach((i) => i.classList.remove("nav-item--active"));
      item.classList.add("nav-item--active");
    });
  });
}

function configurarBotoesInteresse() {
  const botoes = document.querySelectorAll(".btn--interesse");

  botoes.forEach((botao) => {
    botao.addEventListener("click", async () => {
      if (botao.disabled) return;

      const projetoId = botao.dataset.projetoId;
      const textoOriginal = botao.textContent;

      botao.disabled = true;
      botao.classList.add("is-loading");
      botao.textContent = "Enviando...";

      try {
        const resposta = await fetch(`/api/interesse/${projetoId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (!resposta.ok) {
          throw new Error("Falha ao registrar interesse");
        }

        const dados = await resposta.json();

        botao.classList.remove("is-loading");
        botao.classList.add("btn--interesse-ativo");
        botao.textContent = "Interesse registrado ✓";

        mostrarToast(
          `Interesse registrado! Você é o ${dados.total_interesses}º investidor a demonstrar interesse.`
        );
      } catch (erro) {
        botao.disabled = false;
        botao.classList.remove("is-loading");
        botao.textContent = textoOriginal;
        mostrarToast("Não foi possível registrar seu interesse. Tente novamente.");
        console.error(erro);
      }
    });
  });
}

function configurarBuscaEFiltros() {
  const campoBusca = document.getElementById("campo-busca");
  const filtroCategoria = document.getElementById("filtro-categoria");
  const filtroNivel = document.getElementById("filtro-nivel");
  const filtroTipo = document.getElementById("filtro-tipo");
  const botaoLimpar = document.getElementById("btn-limpar-filtros");
  const cards = Array.from(document.querySelectorAll(".card"));
  const mensagemVazio = document.getElementById("msg-vazio");

  function aplicarFiltros() {
    const termoBusca = campoBusca.value.trim().toLowerCase();
    const categoria = filtroCategoria.value;
    const nivel = filtroNivel.value;
    const tipo = filtroTipo.value;

    let algumVisivel = false;

    cards.forEach((card) => {
      const combinaTexto = card.dataset.titulo.includes(termoBusca);
      const combinaCategoria = !categoria || card.dataset.categoria === categoria;
      const combinaNivel = !nivel || card.dataset.nivel === nivel;
      const combinaTipo = !tipo || card.dataset.tipo === tipo;

      const visivel = combinaTexto && combinaCategoria && combinaNivel && combinaTipo;
      card.style.display = visivel ? "" : "none";
      if (visivel) algumVisivel = true;
    });

    mensagemVazio.hidden = algumVisivel;
  }

  campoBusca.addEventListener("input", aplicarFiltros);
  filtroCategoria.addEventListener("change", aplicarFiltros);
  filtroNivel.addEventListener("change", aplicarFiltros);
  filtroTipo.addEventListener("change", aplicarFiltros);

  botaoLimpar.addEventListener("click", () => {
    campoBusca.value = "";
    filtroCategoria.value = "";
    filtroNivel.value = "";
    filtroTipo.value = "";
    aplicarFiltros();
  });
}

function configurarBotaoFiltros() {
  const botao = document.getElementById("btn-filtros");
  const painel = document.getElementById("filtros-extra");

  botao.addEventListener("click", () => {
    const expandido = botao.getAttribute("aria-expanded") === "true";
    botao.setAttribute("aria-expanded", String(!expandido));
    painel.hidden = expandido;
  });
}

let toastTimeoutId = null;

function mostrarToast(mensagem) {
  const toast = document.getElementById("toast");
  toast.textContent = mensagem;
  toast.classList.add("toast--visivel");

  if (toastTimeoutId) clearTimeout(toastTimeoutId);
  toastTimeoutId = setTimeout(() => {
    toast.classList.remove("toast--visivel");
  }, 3200);
}
