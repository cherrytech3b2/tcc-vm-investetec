import os, json, re, uuid
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   session, jsonify, flash, abort)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "investetec-chave-desenvolvimento")
app.config["MAX_CONTENT_LENGTH"] = 110 * 1024 * 1024

from app.controllers.user_controller import user_bp
from app.controllers.project_controller import project_bp

app.register_blueprint(user_bp)
app.register_blueprint(project_bp)

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
        if perfil not in ("aluno", "empresa"):
            return redirect(url_for("login"))
        email = request.form.get("email", "").strip().lower()
        salvo = user_repo.get_by_email(email, perfil) or {}
        nome = salvo.get("nome") or email.split("@")[0].replace(".", " ").title() or "Usuário"
        session.update(perfil=perfil, email=email, nome=nome, empresa=nome)
        return redirect(url_for("aluno_inicio" if perfil == "aluno" else "feed"))
    return render_template("login/login.html")


@app.route("/logout")
def logout():
    for k in ("perfil", "email", "nome", "empresa"):
        session.pop(k, None)
    return redirect(url_for("login"))


@app.route("/register")
def register():
    return render_template("login/register.html")


@app.route("/sobre")
def sobre():
    return render_template("Sobre Nós/sobre.html")


@app.route("/feed")
@so_perfil("empresa")
def feed():
    return render_template("feed.html", modo="empresa", projetos=[publico(p) for p in disponiveis()],
                           favoritos=obter_favoritos(), cursos=CURSOS, niveis=NIVEIS)


@app.route("/aluno/feed")
@so_perfil("aluno")
def aluno_feed():
    return render_template("feed.html", modo="aluno", projetos=[publico(p) for p in disponiveis()],
                           favoritos=[], cursos=CURSOS, niveis=NIVEIS)


@app.route("/favoritos")
@so_perfil("empresa")
def favoritos():
    ids = obter_favoritos()
    return render_template("favoritos.html", modo="empresa", favoritos=ids, cursos=CURSOS, niveis=NIVEIS,
                           projetos=[publico(p) for p in disponiveis() if p["id"] in ids])


@app.route("/api/favorito/<string:projeto_id>", methods=["POST"])
@so_perfil("empresa")
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


# As rotas de perfil foram movidas para user_controller.py


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


# As rotas de aluno (inicio, novo, editar, apagar) foram movidas para project_controller.py


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)