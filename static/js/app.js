(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const dados = JSON.parse($('#dados')?.textContent || '[]');
  const porId = Object.fromEntries(dados.map(p => [p.id, p]));
  const modo = window.APP?.modo, favs = new Set(window.APP?.favs || []);
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function toast(msg) {
    const t = $('#toast'); t.textContent = msg; t.classList.add('toast--visivel');
    clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('toast--visivel'), 2400);
  }

  /* ---------- filtros ---------- */
  const busca = $('#busca'), fc = $('#f-curso'), fn = $('#f-nivel'), ft = $('#f-tipo');
  function filtrar() {
    const q = (busca?.value || '').toLowerCase().trim(); let n = 0;
    const cards = $$('.card[data-id]');
    cards.forEach(c => {
      const ok = (!q || c.dataset.texto.includes(q)) && (!fc?.value || c.dataset.categoria === fc.value) &&
                 (!fn?.value || c.dataset.nivel === fn.value) && (!ft?.value || c.dataset.tipo === ft.value);
      c.hidden = !ok; if (ok) n++;
    });
    $('#n').textContent = n;
    $('#msg-vazio').hidden = n > 0 || !cards.length;
  }
  [busca, fc, fn, ft].forEach(e => e && e.addEventListener('input', filtrar));
  $('#limpar')?.addEventListener('click', () => { [busca, fc, fn, ft].forEach(e => e && (e.value = '')); filtrar(); });

  /* ---------- modal ---------- */
  const sec = (k, t, ic, corpo) => corpo ? `<section class="detail-section"><div class="detail-section__heading"><span><i class="bi ${ic}"></i></span><div><small>${k}</small><h3>${t}</h3></div></div>${corpo}</section>` : '';
  const lista = (cls, itens) => itens?.length ? `<div class="${cls}">${itens.map(i => `<span>${esc(i)}</span>`).join('')}</div>` : '';

  function modalHtml(p) {
    const fotos = [p.foto_1, p.foto_2, p.foto_3].filter(Boolean), f = favs.has(p.id);
    const favBtn = modo === 'investidor' ? `<button class="modal__favorite" type="button" data-fav="${p.id}"><i class="bi ${f ? 'bi-heart-fill' : 'bi-heart'}"></i> <span>${f ? 'Favoritado' : 'Favoritar'}</span></button>` : '';
    const galeria = fotos.length ? `<div class="galeria"><img class="galeria__principal" src="${esc(fotos[0])}" alt="Foto 1 de ${esc(p.titulo)}"><div class="galeria__secundarias">${fotos.slice(1).map((u, i) => `<img src="${esc(u)}" alt="Foto ${i + 2} de ${esc(p.titulo)}">`).join('')}</div></div>` : '';
    const video = p.video ? `<div class="video-box"><div class="video-box__heading"><i class="bi bi-play-circle-fill"></i><div><strong>Vídeo de apresentação</strong><span>Veja o projeto em ação</span></div></div><video controls preload="metadata" src="${esc(p.video)}"></video></div>` : '';
    const pitchItens = [['problema', 'Problema', 'bi-exclamation-triangle-fill'], ['solucao', 'Solução', 'bi-lightbulb-fill'], ['diferencial', 'Diferencial', 'bi-stars'], ['publico_alvo', 'Público-alvo', 'bi-people-fill'], ['potencial', 'Potencial', 'bi-graph-up-arrow']]
      .filter(([k]) => p[k]).map(([k, t, ic]) => `<div class="pitch__item ${k === 'potencial' ? 'pitch__item--full' : ''}"><i class="bi ${ic}"></i><strong>${t}</strong><p>${esc(p[k])}</p></div>`).join('');
    const pitch = pitchItens ? `<section class="pitch"><div class="pitch__heading"><span><i class="bi bi-rocket-takeoff-fill"></i></span><div><small>PITCH DO PROJETO</small><h3>Pitch de negócios</h3></div></div><div class="pitch__grid">${pitchItens}</div></section>` : '';
    const caixa = (t, v) => v ? `<div class="info-box"><span>${t}</span><strong>${esc(v)}</strong></div>` : '';
    const info = `<div class="info-grid">${caixa('Estágio', p.nivel)}${caixa('Tipo', p.tipo)}${caixa('Responsável', p.responsavel)}${caixa('Turma', p.turma)}` +
      (p.cursos_integrados?.length ? `<div class="info-box info-box--wide"><span>Cursos envolvidos</span>${lista('course-list', p.cursos_integrados)}</div>` : '') +
      (p.integrantes_lista?.length ? `<div class="info-box info-box--wide"><span>Integrantes</span>${lista('course-list', p.integrantes_lista)}</div>` : '') +
      (p.tecnologias?.length ? `<div class="info-box info-box--wide"><span>Tecnologias</span>${lista('technology-list', p.tecnologias)}</div>` : '') + '</div>';
    const tel = (p.contato_telefone || '').replace(/\D/g, '');
    const contato = (p.contato_email || p.contato_telefone) ? `<div class="contact-box"><div class="contact-box__icon"><i class="bi bi-chat-heart-fill"></i></div><div class="contact-box__content"><span>CONTATO</span><h3>Entre em contato com os responsáveis</h3><div class="contact-box__actions">${p.contato_email ? `<a class="contact-link" href="mailto:${esc(p.contato_email)}"><i class="bi bi-envelope-fill"></i> ${esc(p.contato_email)}</a>` : ''}${tel ? `<a class="contact-link" href="tel:${tel}"><i class="bi bi-telephone-fill"></i> ${esc(p.contato_telefone)}</a>` : ''}</div></div></div>` : '';
    return `<div class="modal__hero">${p.imagem ? `<img src="${esc(p.imagem)}" alt="Foto principal de ${esc(p.titulo)}">` : ''}<div class="modal__hero-overlay"></div>
      <div class="modal__hero-info"><span>${esc(p.categoria)}</span><h2>${esc(p.titulo)}</h2><p>${esc(p.descricao)}</p></div>${favBtn}</div>
      <div class="modal__body">${sec('SOBRE', 'Sobre o projeto', 'bi-info-circle-fill', p.descricao_completa ? `<p>${esc(p.descricao_completa)}</p>` : '')}
      ${sec('MÍDIAS', 'Fotos e vídeo', 'bi-images', galeria + video)}${pitch}${sec('DETALHES', 'Equipe e tecnologias', 'bi-people-fill', info)}${contato}</div>`;
  }

  function abrir(id) {
    const p = porId[id]; if (!p) return;
    $('#modal-corpo').innerHTML = modalHtml(p);
    $('#modal').classList.add('modal--aberto'); document.body.classList.add('modal-aberto');
    $('.modal__content').scrollTop = 0;
  }
  function fechar() {
    $('#modal').classList.remove('modal--aberto'); document.body.classList.remove('modal-aberto');
    $('#modal video')?.pause();
  }

  /* ---------- favoritos (só investidor) ---------- */
  async function alternar(id) {
    try {
      const r = await fetch('/api/favorito/' + id, { method: 'POST' });
      if (!r.ok) throw new Error();
      const d = await r.json();
      d.favoritado ? favs.add(id) : favs.delete(id);
      $$(`[data-fav="${id}"]`).forEach(b => {
        b.classList.toggle('favorite-button--active', d.favoritado);
        b.querySelector('i').className = 'bi ' + (d.favoritado ? 'bi-heart-fill' : 'bi-heart');
        const s = b.querySelector('span'); if (s) s.textContent = d.favoritado ? 'Favoritado' : 'Favoritar';
      });
      toast(d.favoritado ? 'Adicionado aos favoritos' : 'Removido dos favoritos');
      if (document.body.dataset.pagina === 'favoritos' && !d.favoritado) {
        fechar(); $(`.card[data-id="${id}"]`)?.remove(); filtrar();
        if (!$$('.card[data-id]').length) { $('#vazio-geral').hidden = false; $('#msg-vazio').hidden = true; }
      }
    } catch { toast('Não foi possível favoritar. Tente novamente.'); }
  }

  document.addEventListener('click', e => {
    const a = e.target.closest('[data-abrir]'); if (a) return abrir(+a.dataset.abrir);
    if (e.target.closest('[data-fechar]')) return fechar();
    const f = e.target.closest('[data-fav]'); if (f) alternar(+f.dataset.fav);
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') fechar(); });
})();