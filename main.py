import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "investetec-chave-desenvolvimento")

PROJETOS = [
    {
        "id": 1,
        "titulo": "Smart School",
        "descricao": "Plataforma inteligente criada para melhorar a organização e a experiência dos alunos no ambiente escolar.",
        "curso": "Informática para Internet",
        "categoria": "Informática para Internet",
        "nivel": "Em desenvolvimento",
        "tipo": "Integrado",
        "integrado": True,
        "cursos_integrados": ["Informática para Internet", "Administração"],
        "imagem": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
        "foto_1": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
        "foto_2": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80",
        "foto_3": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1200&q=80",
        "video": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "problema": "A dificuldade de organizar informações e atividades escolares em diferentes plataformas.",
        "solucao": "Uma plataforma centralizada para organizar informações, atividades e recursos utilizados pelos alunos.",
        "diferencial": "Integra tecnologia, organização escolar e uma interface simples para estudantes.",
        "publico_alvo": "Escolas, estudantes e instituições de ensino.",
        "potencial": "Pode ser adaptado para diferentes instituições de ensino e expandido com novos recursos.",
        "tecnologias": ["HTML", "CSS", "JavaScript", "Flask"],
        "contato_tipo": "E-mail",
        "contato": "smartschool@investetec.com"
    },
    {
        "id": 2,
        "titulo": "EcoTech",
        "descricao": "Solução tecnológica voltada para conscientização ambiental e acompanhamento do consumo de recursos.",
        "curso": "Mecatrônica",
        "categoria": "Mecatrônica",
        "nivel": "Protótipo",
        "tipo": "Integrado",
        "integrado": True,
        "cursos_integrados": ["Mecatrônica", "Informática para Internet"],
        "imagem": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80",
        "foto_1": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80",
        "foto_2": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=1200&q=80",
        "foto_3": "https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=1200&q=80",
        "video": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "problema": "O desperdício de recursos e a dificuldade de acompanhar hábitos de consumo.",
        "solucao": "Um sistema capaz de coletar dados e apresentar informações sobre consumo de recursos.",
        "diferencial": "Combina automação, sensores e visualização de dados.",
        "publico_alvo": "Escolas, empresas e instituições interessadas em sustentabilidade.",
        "potencial": "Pode ser utilizado para monitoramento ambiental e educação sustentável.",
        "tecnologias": ["Arduino", "Sensores", "C++", "IoT"],
        "contato_tipo": "Telefone",
        "contato": "(16) 99999-1111"
    },
    {
        "id": 3,
        "titulo": "Gestão Fácil",
        "descricao": "Sistema desenvolvido para auxiliar pequenos negócios na organização de tarefas, clientes e processos.",
        "curso": "Administração",
        "categoria": "Administração",
        "nivel": "Concluído",
        "tipo": "Individual",
        "integrado": False,
        "cursos_integrados": ["Administração"],
        "imagem": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80",
        "foto_1": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80",
        "foto_2": "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1200&q=80",
        "foto_3": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        "video": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "problema": "Pequenos negócios muitas vezes utilizam processos manuais para organizar suas atividades.",
        "solucao": "Uma solução simples para centralizar informações e facilitar a organização empresarial.",
        "diferencial": "Foco em pequenos negócios e facilidade de utilização.",
        "publico_alvo": "Microempreendedores e pequenos negócios.",
        "potencial": "Pode ser expandido para diferentes segmentos empresariais.",
        "tecnologias": ["Gestão", "Banco de dados", "Análise de processos"],
        "contato_tipo": "E-mail",
        "contato": "gestaofacil@investetec.com"
    }
]


def obter_favoritos():
    return session.get("favoritos", [])


@app.route("/")
def index():
    return render_template("pages/landingpage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["investidor"] = request.form.get("nome") or "Investidor"
        return redirect(url_for("feed"))

    return render_template("login/login.html")


@app.route("/feed")
def feed():
    investidor = session.get("investidor", "Investidor")
    favoritos = obter_favoritos()

    return render_template(
        "feed/feedinvestidor.html",
        investidor=investidor,
        projetos=PROJETOS,
        favoritos=favoritos
    )


@app.route("/register")
def register():
    return render_template("login/register.html")


@app.route("/sobre")
def sobre():
    return render_template("Sobre Nós/sobre.html")


@app.route("/favoritos")
def favoritos():
    favoritos_ids = obter_favoritos()
    projetos_favoritos = [
        projeto for projeto in PROJETOS
        if projeto["id"] in favoritos_ids
    ]

    return render_template(
        "feed/favoritos.html",
        projetos_favoritos=projetos_favoritos
    )


@app.route("/api/favorito/<int:projeto_id>", methods=["POST"])
def alternar_favorito(projeto_id):
    projeto = next(
        (projeto for projeto in PROJETOS if projeto["id"] == projeto_id),
        None
    )

    if projeto is None:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    favoritos = obter_favoritos()

    if projeto_id in favoritos:
        favoritos.remove(projeto_id)
        favoritado = False
    else:
        favoritos.append(projeto_id)
        favoritado = True

    session["favoritos"] = favoritos
    session.modified = True

    return jsonify({
        "favoritado": favoritado,
        "total": len(favoritos)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)