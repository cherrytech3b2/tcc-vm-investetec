from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
import uuid
import re
from app.repositories.firebase_repository import ProjectRepository
from app.services.project_service import ProjectService

project_bp = Blueprint('project_bp', __name__)
project_repo = ProjectRepository()
project_service = ProjectService()

CURSOS = ["Informática para Internet", "Mecatrônica", "Administração"]
NIVEIS = ["Em desenvolvimento", "Protótipo", "Concluído"]

def check_aluno():
    if session.get("perfil") != "aluno":
        abort(403)

@project_bp.route("/aluno/inicio")
def aluno_inicio():
    check_aluno()
    meus = project_repo.get_by_owner(session["email"])
    return render_template("aluno/aluno_inicio.html", projetos=meus)

@project_bp.route("/aluno/novo", methods=["GET", "POST"])
@project_bp.route("/aluno/editar/<string:pid>", methods=["GET", "POST"])
def aluno_form(pid=None):
    check_aluno()
    novo = pid is None
    
    if novo:
        p = {"owner_email": session["email"], "owner": session["email"], "status": "Rascunho", "tipo": "Individual"}
    else:
        p = project_repo.get_by_id(pid)
        if not p or p.get("owner_email", p.get("owner")) != session["email"]:
            abort(404)
            
    erros = {}
    
    if request.method == "POST":
        f = request.form
        enviar = f.get("acao") == "enviar"
        
        for c in ("titulo", "descricao", "descricao_completa", "categoria", "tipo", "nivel", "responsavel",
                  "turma", "integrantes", "problema", "solucao", "diferencial", "publico_alvo", "potencial",
                  "contato_email", "contato_telefone"):
            p[c] = f.get(c, "").strip()
            
        p["curso"] = p.get("categoria", "")
        p["integrado"] = p.get("tipo") == "Integrado"
        p["cursos_integrados"] = f.getlist("cursos_integrados") if p["integrado"] else [p["categoria"]]
        p["tecnologias"] = [t.strip() for t in f.get("tecnologias", "").split(",") if t.strip()]
        p["autoriza"] = bool(f.get("autoriza"))
        
        # O Controller agora delega a regra de negócio para o Service
        p, erros = project_service.create_or_update_project(p, is_new=novo, is_submit=enviar)
        
        if erros:
            flash("Verifique os campos destacados.", "erro")
            return render_template("aluno/aluno_form.html", p=p, erros=erros, cursos=CURSOS, niveis=NIVEIS)
            
        flash("Projeto salvo com sucesso.", "ok")
        return redirect(url_for("project_bp.aluno_inicio"))
        
    return render_template("aluno/aluno_form.html", p=p, erros=erros, cursos=CURSOS, niveis=NIVEIS)

@project_bp.route("/aluno/apagar/<string:pid>", methods=["POST"])
def aluno_apagar(pid):
    check_aluno()
    sucesso = project_service.delete_project(pid, session["email"])
    if sucesso:
        flash("Projeto apagado.", "ok")
    else:
        abort(404)
    return redirect(url_for("project_bp.aluno_inicio"))