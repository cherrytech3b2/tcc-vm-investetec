document.addEventListener("DOMContentLoaded", () => {
  const projetos = window.PROJETOS || [];
  let favoritos = new Set(window.FAVORITOS || []);

  const campoBusca = document.getElementById("campo-busca");
  const campoBuscaTopo = document.getElementById("campo-busca-topo");
  const filtroCurso = document.getElementById("filtro-curso");
  const filtroStatus = document.getElementById("filtro-status");
  const botaoLimpar = document.getElementById("btn-limpar-filtros");
  const cards = Array.from(document.querySelectorAll(".card"));
  const mensagemVazia = document.getElementById("msg-vazio");
  const contadorProjetos = document.getElementById("contador-projetos");

  const modal = document.getElementById("modal-projeto");
  const modalOverlay = document.getElementById("modal-overlay");
  const fecharModal = document.getElementById("fechar-modal");
  const modalFavorito = document.getElementById("modal-favorito");

  let projetoAtual = null;

  function normalizar(texto) {
      return String(texto || "")
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .toLowerCase();
  }

  function aplicarFiltros(valorBusca = campoBusca.value) {
      const termo = normalizar(valorBusca.trim());
      const curso = filtroCurso.value;
      const status = filtroStatus.value;

      let quantidadeVisivel = 0;

      cards.forEach((card) => {
          const titulo = normalizar(card.dataset.titulo);
          const descricao = normalizar(card.dataset.descricao);
          const cursoProjeto = card.dataset.curso;
          const statusProjeto = card.dataset.status;

          const correspondeBusca =
              !termo ||
              titulo.includes(termo) ||
              descricao.includes(termo) ||
              normalizar(cursoProjeto).includes(termo);

          const correspondeCurso =
              !curso || cursoProjeto === curso;

          const correspondeStatus =
              !status || statusProjeto === status;

          const visivel =
              correspondeBusca &&
              correspondeCurso &&
              correspondeStatus;

          card.style.display = visivel ? "" : "none";

          if (visivel) {
              quantidadeVisivel++;
          }
      });

      contadorProjetos.textContent =
          `${quantidadeVisivel} ${quantidadeVisivel === 1 ? "projeto" : "projetos"}`;

      mensagemVazia.hidden = quantidadeVisivel !== 0;
  }

  campoBusca.addEventListener("input", () => {
      campoBuscaTopo.value = campoBusca.value;
      aplicarFiltros();
  });

  campoBuscaTopo.addEventListener("input", () => {
      campoBusca.value = campoBuscaTopo.value;
      aplicarFiltros(campoBuscaTopo.value);
  });

  filtroCurso.addEventListener("change", aplicarFiltros);
  filtroStatus.addEventListener("change", aplicarFiltros);

  botaoLimpar.addEventListener("click", () => {
      campoBusca.value = "";
      campoBuscaTopo.value = "";
      filtroCurso.value = "";
      filtroStatus.value = "";
      aplicarFiltros();
  });

  document.querySelectorAll(".card__open").forEach((botao) => {
      botao.addEventListener("click", (evento) => {
          evento.stopPropagation();

          const id = Number(botao.dataset.projeto);
          abrirProjeto(id);
      });
  });

  document.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("click", (evento) => {
          if (evento.target.closest(".favorite-button")) {
              return;
          }

          abrirProjeto(Number(card.dataset.id));
      });
  });

  document.querySelectorAll(".favorite-button").forEach((botao) => {
      botao.addEventListener("click", async (evento) => {
          evento.stopPropagation();

          const id = Number(botao.dataset.favoritoId);
          await alternarFavorito(id);
      });
  });

  async function alternarFavorito(id) {
      try {
          const resposta = await fetch(`/api/favorito/${id}`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              }
          });

          if (!resposta.ok) {
              throw new Error("Não foi possível atualizar o favorito.");
          }

          const dados = await resposta.json();

          if (dados.favoritado) {
              favoritos.add(id);
              mostrarToast("Projeto adicionado aos favoritos.");
          } else {
              favoritos.delete(id);
              mostrarToast("Projeto removido dos favoritos.");
          }

          atualizarBotoesFavorito(id);
      } catch (erro) {
          console.error(erro);
          mostrarToast("Não foi possível atualizar os favoritos.");
      }
  }

  function atualizarBotoesFavorito(id) {
      const favoritado = favoritos.has(id);

      document.querySelectorAll(
          `.favorite-button[data-favorito-id="${id}"]`
      ).forEach((botao) => {
          botao.classList.toggle("favorite-button--active", favoritado);

          const icone = botao.querySelector("i");

          if (icone) {
              icone.className = favoritado
                  ? "bi bi-star-fill"
                  : "bi bi-star";
          }
      });

      if (projetoAtual && projetoAtual.id === id) {
          modalFavorito.innerHTML = favoritado
              ? '<i class="bi bi-star-fill"></i><span>Favoritado</span>'
              : '<i class="bi bi-star"></i><span>Favoritar</span>';

          modalFavorito.classList.toggle(
              "favorite-button--active",
              favoritado
          );
      }
  }

  function abrirProjeto(id) {
      projetoAtual = projetos.find((projeto) => projeto.id === id);

      if (!projetoAtual) {
          return;
      }

      document.getElementById("modal-imagem").src =
          projetoAtual.imagem;

      document.getElementById("modal-imagem").alt =
          `Imagem do projeto ${projetoAtual.titulo}`;

      document.getElementById("modal-curso").textContent =
          projetoAtual.curso;

      document.getElementById("modal-titulo").textContent =
          projetoAtual.titulo;

      document.getElementById("modal-descricao").textContent =
          projetoAtual.descricao;

      document.getElementById("modal-descricao-completa").textContent =
          projetoAtual.descricao;

      document.getElementById("modal-foto-1").src =
          projetoAtual.foto_1;

      document.getElementById("modal-foto-2").src =
          projetoAtual.foto_2;

      document.getElementById("modal-foto-3").src =
          projetoAtual.foto_3;

      const video = document.getElementById("modal-video");
      video.src = projetoAtual.video;
      video.load();

      document.getElementById("modal-problema").textContent =
          projetoAtual.problema;

      document.getElementById("modal-solucao").textContent =
          projetoAtual.solucao;

      document.getElementById("modal-diferencial").textContent =
          projetoAtual.diferencial;

      document.getElementById("modal-publico").textContent =
          projetoAtual.publico_alvo;

      document.getElementById("modal-potencial").textContent =
          projetoAtual.potencial;

      document.getElementById("modal-curso-info").textContent =
          projetoAtual.curso;

      document.getElementById("modal-status").textContent =
          projetoAtual.nivel;

      document.getElementById("modal-tipo").textContent =
          projetoAtual.integrado
              ? "Integrado com outros alunos"
              : "Projeto individual";

      const cursosContainer =
          document.getElementById("modal-cursos-integrados");

      cursosContainer.innerHTML = "";

      projetoAtual.cursos_integrados.forEach((curso) => {
          const elemento = document.createElement("span");
          elemento.textContent = curso;
          cursosContainer.appendChild(elemento);
      });

      const tecnologiasContainer =
          document.getElementById("modal-tecnologias");

      tecnologiasContainer.innerHTML = "";

      projetoAtual.tecnologias.forEach((tecnologia) => {
          const elemento = document.createElement("span");
          elemento.textContent = tecnologia;
          tecnologiasContainer.appendChild(elemento);
      });

      montarContato(projetoAtual);

      atualizarBotoesFavorito(id);

      modal.classList.add("modal--aberto");
      modal.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-aberto");
  }

  function montarContato(projeto) {
      const container = document.getElementById("modal-contato");

      container.innerHTML = "";

      const link = document.createElement("a");
      link.className = "contact-link";

      if (projeto.contato_tipo === "E-mail") {
          link.href = `mailto:${projeto.contato}`;
          link.innerHTML = `<i class="bi bi-envelope-fill"></i>${projeto.contato}`;
      } else if (projeto.contato_tipo === "Telefone") {
          const telefone = projeto.contato.replace(/\D/g, "");
          link.href = `tel:${telefone}`;
          link.innerHTML = `<i class="bi bi-telephone-fill"></i>${projeto.contato}`;
      } else {
          link.href = projeto.contato;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.innerHTML = `<i class="bi bi-link-45deg"></i>Acessar contato`;
      }

      container.appendChild(link);
  }

  modalFavorito.addEventListener("click", async () => {
      if (!projetoAtual) {
          return;
      }

      await alternarFavorito(projetoAtual.id);
  });

  function fecharJanelaModal() {
      const video = document.getElementById("modal-video");

      video.pause();
      video.removeAttribute("src");
      video.load();

      modal.classList.remove("modal--aberto");
      modal.setAttribute("aria-hidden", "true");
      document.body.classList.remove("modal-aberto");
      projetoAtual = null;
  }

  fecharModal.addEventListener("click", fecharJanelaModal);
  modalOverlay.addEventListener("click", fecharJanelaModal);

  document.addEventListener("keydown", (evento) => {
      if (evento.key === "Escape" && modal.classList.contains("modal--aberto")) {
          fecharJanelaModal();
      }
  });

  let toastTimeout;

  function mostrarToast(mensagem) {
      const toast = document.getElementById("toast");

      toast.textContent = mensagem;
      toast.classList.add("toast--visivel");

      clearTimeout(toastTimeout);

      toastTimeout = setTimeout(() => {
          toast.classList.remove("toast--visivel");
      }, 2800);
  }

  aplicarFiltros();
});