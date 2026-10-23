import os
import sys
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def _find_service_account_path():
    """Busca o arquivo de credenciais do Firebase nos locais padrão."""
    candidates = [
        os.environ.get("FIREBASE_CREDENTIALS_PATH"),
        os.path.join(BASE_DIR, "serviceAccountKey.json"),
        "serviceAccountKey.json",
        "/etc/secrets/serviceAccountKey.json",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None

def _env(name: str):
    """Busca uma variável de ambiente de forma flexível (case-insensitive e com prefixo)."""
    for candidate in [name, name.upper(), name.lower(), f"FIREBASE_{name.upper()}"]:
        val = os.environ.get(candidate)
        if val is not None and val != "":
            return val
    return None

def _get_credentials_from_env_vars():
    """Monta o dicionário de credenciais a partir de variáveis individuais (ex: Render Environment Groups)."""
    private_key = _env("private_key")
    client_email = _env("client_email")
    project_id = _env("project_id")

    if not (private_key and client_email and project_id):
        return None

    # Sanitização da chave privada (remove aspas e ajusta quebras de linha)
    cleaned_key = private_key.strip().strip("'\"")
    cleaned_key = cleaned_key.replace("\\r\\n", "\n").replace("\\n", "\n")
    if not cleaned_key.endswith("\n"):
        cleaned_key += "\n"

    cert_dict = {
        "type": (_env("type") or "service_account").strip().strip("'\""),
        "project_id": project_id.strip().strip("'\""),
        "private_key_id": (_env("private_key_id") or "").strip().strip("'\""),
        "private_key": cleaned_key,
        "client_email": client_email.strip().strip("'\""),
        "client_id": (_env("client_id") or "").strip().strip("'\""),
        "auth_uri": (_env("auth_uri") or "https://accounts.google.com/o/oauth2/auth").strip().strip("'\""),
        "token_uri": (_env("token_uri") or "https://oauth2.googleapis.com/token").strip().strip("'\""),
        "auth_provider_x509_cert_url": (_env("auth_provider_x509_cert_url") or "https://www.googleapis.com/oauth2/v1/certs").strip().strip("'\""),
        "client_x509_cert_url": (_env("client_x509_cert_url") or "").strip().strip("'\""),
        "universe_domain": (_env("universe_domain") or "googleapis.com").strip().strip("'\""),
    }
    return cert_dict

def init_firebase():
    """Inicializa o Firebase Admin SDK com credenciais de ambiente ou arquivo."""
    if firebase_admin._apps:
        return

    print("-> [Firebase] Inicializando Firebase Admin SDK...", flush=True)

    # 1. Tentar via variáveis individuais (Render Environment Group)
    try:
        env_dict = _get_credentials_from_env_vars()
        if env_dict:
            print(f"-> [Firebase] Variáveis de ambiente detectadas para o projeto '{env_dict.get('project_id')}'. Conectando...", flush=True)
            cred = credentials.Certificate(env_dict)
            firebase_admin.initialize_app(cred)
            print("-> [Firebase] Conexão com Firebase estabelecida com sucesso via Environment Variables!", flush=True)
            return
        else:
            print("-> [Firebase] Variáveis individuais não encontradas no ambiente (project_id, private_key ou client_email ausentes).", flush=True)
    except Exception as e:
        print(f"-> [Firebase ERRO] Falha ao carregar variáveis individuais: {e}", flush=True)
        import traceback
        traceback.print_exc()

    # 2. Tentar via variável de ambiente FIREBASE_CREDENTIALS (JSON completo ou Base64)
    firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")
    if firebase_credentials:
        try:
            print("-> [Firebase] Tentando carregar via FIREBASE_CREDENTIALS...", flush=True)
            if os.path.isfile(firebase_credentials):
                cred = credentials.Certificate(firebase_credentials)
                firebase_admin.initialize_app(cred)
                print("-> [Firebase] Conectado via arquivo em FIREBASE_CREDENTIALS!", flush=True)
                return

            raw_content = firebase_credentials.strip()
            try:
                cert_dict = json.loads(raw_content)
            except json.JSONDecodeError:
                decoded = base64.b64decode(raw_content).decode("utf-8")
                cert_dict = json.loads(decoded)

            if isinstance(cert_dict, dict) and "private_key" in cert_dict:
                cert_dict["private_key"] = cert_dict["private_key"].replace("\\r\\n", "\n").replace("\\n", "\n")

            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
            print("-> [Firebase] Conectado via JSON de FIREBASE_CREDENTIALS!", flush=True)
            return
        except Exception as e:
            print(f"-> [Firebase ERRO] Falha ao processar FIREBASE_CREDENTIALS: {e}", flush=True)
            import traceback
            traceback.print_exc()

    # 3. Tentar via arquivo físico (local ou Secret File no Render)
    account_path = _find_service_account_path()
    if account_path:
        try:
            print(f"-> [Firebase] Arquivo de credenciais encontrado em: {account_path}", flush=True)
            cred = credentials.Certificate(account_path)
            firebase_admin.initialize_app(cred)
            print("-> [Firebase] Conectado com sucesso via arquivo serviceAccountKey.json!", flush=True)
            return
        except Exception as e:
            print(f"-> [Firebase ERRO] Falha ao carregar credenciais do arquivo {account_path}: {e}", flush=True)
            import traceback
            traceback.print_exc()

    msg_erro = (
        "Erro ao inicializar Firebase: Nenhuma credencial foi encontrada no ambiente.\n"
        "Verifique se o Environment Group no Render está VINCULADO (Linked) ao serviço."
    )
    print(f"-> [Firebase FATAL] {msg_erro}", flush=True)
    raise RuntimeError(msg_erro)

def get_db():
    try:
        firebase_admin.get_app()
    except ValueError:
        init_firebase()
    return firestore.client()


