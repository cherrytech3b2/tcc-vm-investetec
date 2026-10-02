import os, json, re, uuid
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   session, jsonify, flash, abort)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "investetec-chave-desenvolvimento")
app.config["MAX_CONTENT_LENGTH"] = 110 * 1024 * 1024

BASE = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(BASE, "projetos_alunos.json")
ARQ_PERFIS = os.path.join(BASE, "perfis.json")
CURSOS = ["Informática para Internet", "Mecatrônica", "Administração"]
NIVEIS = ["Em desenvolvimento", "Protótipo", "Concluído"]
PROJETOS = []  # sem projetos fictícios: tudo vem do cadastro dos alunos


from app.repositories.firebase_repository import UserRepository, ProjectRepository

user_repo = UserRepository()
project_repo = ProjectRepository()

def gravar():
    pass # Managed by Firebase automatically upon save



def chave():
    return f"{session.get('perfil')}:{session.get('email')}"


def disponiveis():
    return project_repo.get_all_available()


def publico(p):
    """Versão do projeto que pode ir para a tela (sem dados internos)."""
    d = {k: v for k, v in p.items() if k not in ("owner", "autoriza", "status")}
    d["integrantes_lista"] = [l.strip() for l in (p.get("integrantes") or "").splitlines() if l.strip()]
    d["meu"] = p.get("owner") == session.get("email")
    return d


def so_perfil(*perfis):
    def deco(f):
        @wraps(f)
        def w(*a, **k):
            if session.get("perfil") not in perfis:
                return redirect(url_for("login"))
            return f(*a, **k)
        return w
    return deco


@app.context_processor
def injetar():
    eu_data = {}
    if session.get("email") and session.get("perfil"):
        eu_data = user_repo.get_by_email(session["email"], session["perfil"]) or {}
    return {"eu": eu_data}


def obter_favoritos():
    return session.get("favoritos", [])


@app.route("/")
def index():
    return render_template("pages/landingpage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        perfil = request.form.get("perfil")
        if perfil not in ("aluno", "investidor"):
            return redirect(url_for("login"))
        email = request.form.get("email", "").strip().lower()
        salvo = user_repo.get_by_email(email, perfil) or {}
        nome = salvo.get("nome") or email.split("@")[0].replace(".", " ").title() or "Usuário"
        session.update(perfil=perfil, email=email, nome=nome, investidor=nome)
        return redirect(url_for("aluno_inicio" if perfil == "aluno" else "feed"))
    return render_template("login/login.html")


@app.route("/logout")
def logout():
    for k in ("perfil", "email", "nome", "investidor"):
        session.pop(k, None)
    return redirect(url_for("login"))


@app.route("/register")
def register():
    return render_template("login/register.html")


@app.route("/sobre")
def sobre():
    return render_template("Sobre Nós/sobre.html")


@app.route("/feed")
@so_perfil("investidor")
def feed():
    return render_template("feed.html", modo="investidor", projetos=[publico(p) for p in disponiveis()],
                           favoritos=obter_favoritos(), cursos=CURSOS, niveis=NIVEIS)


@app.route("/aluno/feed")
@so_perfil("aluno")
def aluno_feed():
    return render_template("feed.html", modo="aluno", projetos=[publico(p) for p in disponiveis()],
                           favoritos=[], cursos=CURSOS, niveis=NIVEIS)


@app.route("/favoritos")
@so_perfil("investidor")
def favoritos():
    ids = obter_favoritos()
    return render_template("favoritos.html", modo="investidor", favoritos=ids, cursos=CURSOS, niveis=NIVEIS,
                           projetos=[publico(p) for p in disponiveis() if p["id"] in ids])


@app.route("/api/favorito/<string:projeto_id>", methods=["POST"])
@so_perfil("investidor")
def alternar_favorito(projeto_id):
    if not any(p["id"] == projeto_id for p in disponiveis()):
        return jsonify({"erro": "Projeto não encontrado"}), 404
    fav = obter_favoritos()
    if projeto_id in fav:
        fav.remove(projeto_id); ativo = False
    else:
        fav.append(projeto_id); ativo = True
    session["favoritos"] = fav
    session.modified = True
    return jsonify({"favoritado": ativo, "total": len(fav)})


@app.route("/perfil", methods=["GET", "POST"])
@so_perfil("aluno", "investidor")
def perfil():
    email = session.get("email")
    perfil_str = session.get("perfil")
    d = user_repo.get_by_email(email, perfil_str) or {}
    erros = {}
    aluno = perfil_str == "aluno"
    if request.method == "POST":
        f = request.form
        for c in ("nome", "telefone", "bio") + (("curso", "turma") if aluno else ("empresa", "cargo", "interesses")):
            d[c] = f.get(c, "").strip()
        if not d["nome"]:
            erros["nome"] = "Informe seu nome."
        if len(d["bio"]) > 300:
            erros["bio"] = "A bio deve ter até 300 caracteres."
        tel = re.sub(r"\D", "", d["telefone"])
        if tel and len(tel) not in (10, 11):
            erros["telefone"] = "Telefone inválido. Use DDD + número."
        if d.get("curso") and d["curso"] not in CURSOS:
            erros["curso"] = "Selecione um curso da lista."
        if f.get("remover_foto"):
            d.pop("foto", None)
        url, err = guardar(request.files.get("foto"), {"jpg", "jpeg", "png", "webp"}, 5)
        if err: erros["foto"] = err
        elif url: d["foto"] = url
        if erros:
            flash("Não foi possível salvar. Verifique os campos destacados.", "erro")
            return render_template("perfil.html", d=d, erros=erros, cursos=CURSOS)
        d["email"] = email
        d["perfil"] = perfil_str
        user_repo.save(d)
        session["nome"] = session["investidor"] = d["nome"]
        flash("Perfil atualizado.", "ok")
        return redirect(url_for("perfil"))
    return render_template("perfil.html", d=d, erros=erros, cursos=CURSOS)


def meu_projeto(pid):
    p = project_repo.get_by_id(str(pid))
    if not p or p.get("owner_email", p.get("owner")) != session["email"]:
        abort(404)  # não é seu = não existe
    return p


def guardar(arq, exts, mb):
    if not arq or not arq.filename:
        return None, None
    ext = arq.filename.rsplit(".", 1)[-1].lower()
    if ext not in exts:
        return None, "Formato inválido. Use: " + ", ".join(sorted(exts)).upper() + "."
    arq.stream.seek(0, 2); n = arq.stream.tell(); arq.stream.seek(0)
    if n > mb * 1048576:
        return None, f"Arquivo maior que {mb} MB."
    pasta = os.path.join(app.static_folder, "uploads")
    os.makedirs(pasta, exist_ok=True)
    nome = f"{uuid.uuid4().hex}.{ext}"
    arq.save(os.path.join(pasta, nome))
    return url_for("static", filename=f"uploads/{nome}"), None


def validar(p, enviar):
    e = {}
    if not p.get("titulo"):
        e["titulo"] = "Informe o nome do projeto."
    if p.get("contato_email") and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", p["contato_email"]):
        e["contato_email"] = "E-mail inválido."
    tel = re.sub(r"\D", "", p.get("contato_telefone", ""))
    if tel and len(tel) not in (10, 11):
        e["contato_telefone"] = "Telefone inválido. Use DDD + número."
    if not enviar:
        return e
    for c, m in {"descricao": "Informe a descrição resumida.", "descricao_completa": "Informe a descrição completa.",
                 "responsavel": "Informe o responsável.", "problema": "Informe o problema.",
                 "solucao": "Informe a solução.", "diferencial": "Informe o diferencial.",
                 "publico_alvo": "Informe o público-alvo.", "potencial": "Informe o potencial."}.items():
        if not p.get(c):
            e[c] = m
    if p.get("categoria") not in CURSOS:
        e["categoria"] = "Selecione o curso principal."
    if p.get("nivel") not in NIVEIS:
        e["nivel"] = "Selecione o estágio do projeto."
    if not p.get("tecnologias"):
        e["tecnologias"] = "Informe ao menos uma tecnologia."
    if p.get("tipo") == "Integrado" and not p.get("cursos_integrados"):
        e["cursos_integrados"] = "Selecione os cursos envolvidos."
    for i in (1, 2, 3):
        if not p.get(f"foto_{i}") and f"foto{i}" not in e:
            e[f"foto{i}"] = f"Envie a foto {i}."
    if not p.get("video") and "video" not in e:
        e["video"] = "Envie o vídeo."
    if not p.get("contato_email") and not tel:
        e["contato"] = "Informe ao menos um contato (e-mail ou telefone)."
    if not p.get("autoriza"):
        e["autoriza"] = "Confirme a autorização para divulgar o contato."
    return e


@app.route("/aluno")
@so_perfil("aluno")
def aluno_inicio():
    meus = project_repo.get_by_owner(session["email"])
    return render_template("aluno/aluno_inicio.html", projetos=meus)


@app.route("/aluno/novo", methods=["GET", "POST"])
@app.route("/aluno/editar/<string:pid>", methods=["GET", "POST"])
@so_perfil("aluno")
def aluno_form(pid=None):
    novo = pid is None
    p = {"owner_email": session["email"], "owner": session["email"], "status": "Rascunho", "tipo": "Individual"} if novo else meu_projeto(pid)
    erros = {}
    if request.method == "POST":
        f, enviar = request.form, request.form.get("acao") == "enviar"
        for c in ("titulo", "descricao", "descricao_completa", "categoria", "tipo", "nivel", "responsavel",
                  "turma", "integrantes", "problema", "solucao", "diferencial", "publico_alvo", "potencial",
                  "contato_email", "contato_telefone"):
            p[c] = f.get(c, "").strip()
        p["curso"] = p["categoria"]
        p["integrado"] = p["tipo"] == "Integrado"
        p["cursos_integrados"] = f.getlist("cursos_integrados") if p["integrado"] else [p["categoria"]]
        p["tecnologias"] = [t.strip() for t in f.get("tecnologias", "").split(",") if t.strip()]
        p["autoriza"] = bool(f.get("autoriza"))
        for i in (1, 2, 3):
            url, err = guardar(request.files.get(f"foto{i}"), {"jpg", "jpeg", "png", "webp"}, 5)
            if err: erros[f"foto{i}"] = err
            elif url: p[f"foto_{i}"] = url
        url, err = guardar(request.files.get("video"), {"mp4", "webm", "mov"}, 100)
        if err: erros["video"] = err
        elif url: p["video"] = url
        p["imagem"] = p.get("foto_1", "")
        p["contato_tipo"] = "E-mail" if p["contato_email"] else "Telefone"
        p["contato"] = p["contato_email"] or p["contato_telefone"]
        erros.update(validar(p, enviar))
        if erros:
            flash("Seu projeto ainda possui informações obrigatórias pendentes." if enviar
                  else "Não foi possível salvar. Verifique os campos destacados.", "erro")
            return render_template("aluno/aluno_form.html", p=p, erros=erros, cursos=CURSOS, niveis=NIVEIS)
        p["status"] = "Disponível" if enviar else "Rascunho"
        if novo:
            p["id"] = uuid.uuid4().hex
        project_repo.save(p)
        flash("Projeto enviado com sucesso." if enviar else "Projeto salvo como rascunho.", "ok")
        return redirect(url_for("aluno_inicio"))
    return render_template("aluno/aluno_form.html", p=p, erros=erros, cursos=CURSOS, niveis=NIVEIS)


@app.route("/aluno/apagar/<string:pid>", methods=["POST"])
@so_perfil("aluno")
def aluno_apagar(pid):
    project_repo.delete(str(pid))
    flash("Projeto apagado.", "ok")
    return redirect(url_for("aluno_inicio"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)