from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
import re
import uuid
import os
from app.repositories.firebase_repository import UserRepository

user_bp = Blueprint('user_bp', __name__)
user_repo = UserRepository()

# Constantes (podem ser movidas para um arquivo config depois)
CURSOS = ["Informática para Internet", "Mecatrônica", "Administração"]

@user_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    if not session.get("perfil"):
        return redirect(url_for("login"))
        
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
        if d.get("bio") and len(d["bio"]) > 300:
            erros["bio"] = "A bio deve ter até 300 caracteres."
            
        tel = re.sub(r"\D", "", d.get("telefone", ""))
        if tel and len(tel) not in (10, 11):
            erros["telefone"] = "Telefone inválido. Use DDD + número."
            
        if d.get("curso") and d["curso"] not in CURSOS:
            erros["curso"] = "Selecione um curso da lista."
            
        if erros:
            flash("Não foi possível salvar. Verifique os campos destacados.", "erro")
            return render_template("perfil.html", d=d, erros=erros, cursos=CURSOS)
            
        d["email"] = email
        d["perfil"] = perfil_str
        user_repo.save(d)
        
        session["nome"] = session["investidor"] = d["nome"]
        flash("Perfil atualizado com sucesso.", "ok")
        return redirect(url_for("user_bp.perfil"))
        
    return render_template("perfil.html", d=d, erros=erros, cursos=CURSOS)
