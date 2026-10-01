import os, re, uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, current_app
from werkzeug.utils import secure_filename
from extensions import db  # <- ajuste
from models_aluno import Projeto, Foto, Integrante  # <- ajuste

aluno_bp = Blueprint("aluno", __name__, url_prefix="/aluno")

CURSOS = ["Informática para Internet", "Mecatrônica", "Administração"]
EXT_IMG, EXT_VID = {"jpg", "jpeg", "png", "webp"}, {"mp4", "webm", "mov"}
MAX_IMG, MAX_VID = 5 * 1024 * 1024, 100 * 1024 * 1024
# Em app.py: app.config["MAX_CONTENT_LENGTH"] = 110 * 1024 * 1024


def aluno_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        # Ajuste às suas chaves de sessão
        if not session.get("usuario_id") or session.get("perfil") != "aluno":
            return redirect(url_for("login"))
        return f(*a, **kw)
    return wrapper


def meu_projeto(pid):
    # Permissão no backend: só retorna se o projeto for do usuário logado
    return Projeto.query.filter_by(id=pid, usuario_id=session["usuario_id"]).first_or_404()


def ext_ok(arq, permitidas):
    return arq and "." in arq.filename and arq.filename.rsplit(".", 1)[1].lower() in permitidas


def tamanho(arq):
    arq.stream.seek(0, os.SEEK_END); n = arq.stream.tell(); arq.stream.seek(0)
    return n


def salvar_arquivo(arq, pid):
    pasta = os.path.join(current_app.static_folder, "uploads", str(pid))
    os.makedirs(pasta, exist_ok=True)
    nome = f"{uuid.uuid4().hex}_{secure_filename(arq.filename)}"
    arq.save(os.path.join(pasta, nome))
    return f"uploads/{pid}/{nome}"


def validar(p, form, files, enviar):
    """Retorna dict campo -> mensagem. Rascunho exige só o nome."""
    e, f = {}, form
    if not f.get("titulo", "").strip():
        e["titulo"] = "Informe o nome do projeto."
    # arquivos novos (valida formato/tamanho sempre)
    for i in (1, 2, 3):
        a = files.get(f"foto{i}")
        if a and a.filename:
            if not ext_ok(a, EXT_IMG): e[f"foto{i}"] = "Use JPG, PNG ou WEBP."
            elif tamanho(a) > MAX_IMG: e[f"foto{i}"] = "A imagem deve ter até 5 MB."
    v = files.get("video")
    if v and v.filename:
        if not ext_ok(v, EXT_VID): e["video"] = "Use MP4, WEBM ou MOV."
        elif tamanho(v) > MAX_VID: e["video"] = "O vídeo deve ter até 100 MB."
    email, tel = f.get("contato_email", "").strip(), re.sub(r"\D", "", f.get("contato_telefone", ""))
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email): e["contato_email"] = "E-mail inválido."
    if tel and len(tel) not in (10, 11): e["contato_telefone"] = "Telefone inválido. Use DDD + número."
    if not enviar:
        return e
    obrig = {"descricao": "Informe a descrição resumida.", "descricao_completa": "Informe a descrição completa.",
             "problema": "Informe o problema.", "solucao": "Informe a solução.", "diferencial": "Informe o diferencial.",
             "publico_alvo": "Informe o público-alvo.", "potencial": "Informe o potencial.",
             "responsavel": "Informe o nome do responsável."}
    for c, msg in obrig.items():
        if not f.get(c, "").strip(): e[c] = msg
    if f.get("categoria") not in CURSOS: e["categoria"] = "Selecione o curso principal."
    if f.get("tipo") not in ("Individual", "Integrado"): e["tipo"] = "Selecione o tipo."
    if f.get("tipo") == "Integrado":
        if not f.getlist("cursos_envolvidos"): e["cursos_envolvidos"] = "Selecione os cursos envolvidos."
        if not any(n.strip() for n in f.getlist("int_nome")): e["integrantes"] = "Adicione ao menos um integrante."
    for i in (1, 2, 3):
        tem = (files.get(f"foto{i}") and files[f"foto{i}"].filename) or p.foto(i)
        if not tem and f"foto{i}" not in e: e[f"foto{i}"] = f"Envie a foto {i}."
    if not ((v and v.filename) or p.video) and "video" not in e: e["video"] = "Envie o vídeo."
    if not email and not tel: e["contato"] = "Informe ao menos um contato (e-mail ou telefone)."
    if not f.get("contato_autorizado"): e["contato_autorizado"] = "Confirme a autorização para divulgar o contato."
    return e


@aluno_bp.route("/")
@aluno_required
def inicio():
    projetos = Projeto.query.filter_by(usuario_id=session["usuario_id"]).order_by(Projeto.atualizado_em.desc()).all()
    return render_template("aluno_inicio.html", projetos=projetos, nome=session.get("nome", "Aluno"))


@aluno_bp.route("/projeto/novo", methods=["GET", "POST"])
@aluno_bp.route("/projeto/<int:pid>/editar", methods=["GET", "POST"])
@aluno_required
def formulario(pid=None):
    p = meu_projeto(pid) if pid else Projeto(usuario_id=session["usuario_id"])
    if pid and p.status in ("Arquivado",):
        abort(403)
    erros = {}
    if request.method == "POST":
        enviar = request.form.get("acao") == "enviar"
        erros = validar(p, request.form, request.files, enviar)
        f = request.form
        if not erros or (not enviar and set(erros) <= set(erros) and "titulo" not in erros):
            # em rascunho, só bloqueia se faltar o nome; formatos inválidos já bloqueiam via erros
            pass
        if erros:
            flash("Não foi possível salvar. Verifique os campos destacados." if not enviar else
                  "Seu projeto ainda possui informações obrigatórias pendentes.", "erro")
            _preencher(p, f)  # mantém o que foi digitado
            return render_template("aluno_form.html", p=p, erros=erros, cursos=CURSOS)
        _preencher(p, f)
        db.session.add(p); db.session.flush()
        for i in (1, 2, 3):
            a = request.files.get(f"foto{i}")
            if a and a.filename:
                velha = p.foto(i)
                if velha: velha.arquivo = salvar_arquivo(a, p.id)
                else: db.session.add(Foto(projeto_id=p.id, posicao=i, arquivo=salvar_arquivo(a, p.id)))
        v = request.files.get("video")
        if v and v.filename: p.video = salvar_arquivo(v, p.id)
        p.integrantes.clear()
        if p.tipo == "Integrado":
            for n, c, fn in zip(f.getlist("int_nome"), f.getlist("int_curso"), f.getlist("int_funcao")):
                if n.strip(): p.integrantes.append(Integrante(nome=n.strip(), curso=c, funcao=fn.strip()))
        if enviar:
            p.status = "Disponível"  # sem aprovação administrativa; vai direto ao feed
        elif p.status != "Disponível":
            p.status = "Rascunho"
        db.session.commit()
        flash("Projeto enviado com sucesso." if enviar else "Projeto salvo como rascunho.", "ok")
        return redirect(url_for("aluno.inicio"))
    return render_template("aluno_form.html", p=p, erros=erros, cursos=CURSOS)


def _preencher(p, f):
    for c in ("titulo", "descricao", "descricao_completa", "categoria", "problema", "solucao", "diferencial",
              "publico_alvo", "potencial", "responsavel", "turma", "contato_email", "contato_telefone"):
        setattr(p, c, f.get(c, "").strip())
    p.tipo = f.get("tipo", "Individual")
    p.cursos_envolvidos = ",".join(f.getlist("cursos_envolvidos"))
    p.contato_autorizado = bool(f.get("contato_autorizado"))
    p.imagem_principal = int(f.get("imagem_principal", 1) or 1)


@aluno_bp.route("/projeto/<int:pid>/apagar", methods=["POST"])
@aluno_required
def apagar(pid):
    db.session.delete(meu_projeto(pid)); db.session.commit()
    flash("Projeto apagado.", "ok")
    return redirect(url_for("aluno.inicio"))

# --- No app.py ---
#   from aluno import aluno_bp; app.register_blueprint(aluno_bp)
# --- No feed do investidor, troque a lista fixa por: ---
#   projetos = Projeto.query.filter_by(status="Disponível").all()
# e no card use: p.titulo, p.categoria, p.tipo, p.descricao, p.capa
#   <img src="{{ url_for('static', filename=p.capa) }}">
