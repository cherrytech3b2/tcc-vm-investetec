import os
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

def _get_credentials_from_env_vars():
    """Monta o dicionário de credenciais se as variáveis foram adicionadas individualmente (ex: via Render Environment Groups)."""
    private_key = os.environ.get("private_key") or os.environ.get("FIREBASE_PRIVATE_KEY")
    client_email = os.environ.get("client_email") or os.environ.get("FIREBASE_CLIENT_EMAIL")
    project_id = os.environ.get("project_id") or os.environ.get("FIREBASE_PROJECT_ID")

    if private_key and client_email and project_id:
        return {
            "type": os.environ.get("type", "service_account"),
            "project_id": project_id,
            "private_key_id": os.environ.get("private_key_id", ""),
            "private_key": private_key.replace("\\n", "\n"),
            "client_email": client_email,
            "client_id": os.environ.get("client_id", ""),
            "auth_uri": os.environ.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.environ.get("token_uri", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.environ.get(
                "auth_provider_x509_cert_url",
                "https://www.googleapis.com/oauth2/v1/certs",
            ),
            "client_x509_cert_url": os.environ.get("client_x509_cert_url", ""),
            "universe_domain": os.environ.get("universe_domain", "googleapis.com"),
        }
    return None

def init_firebase():
    """Inicializa o Firebase Admin SDK com credenciais de ambiente ou arquivo."""
    if firebase_admin._apps:
        return

    # 1. Tentar via variáveis individuais (ex: Render Environment Group)
    env_dict = _get_credentials_from_env_vars()
    if env_dict:
        cred = credentials.Certificate(env_dict)
        firebase_admin.initialize_app(cred)
        return

    # 2. Tentar via variável de ambiente FIREBASE_CREDENTIALS (JSON completo ou Base64)
    firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")
    if firebase_credentials:
        # Se for um caminho de arquivo existente
        if os.path.isfile(firebase_credentials):
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)
            return

        # Se for uma string JSON (direta ou codificada em base64)
        raw_content = firebase_credentials.strip()
        try:
            cert_dict = json.loads(raw_content)
        except json.JSONDecodeError:
            try:
                decoded = base64.b64decode(raw_content).decode("utf-8")
                cert_dict = json.loads(decoded)
            except Exception as e:
                raise ValueError(
                    f"A variável FIREBASE_CREDENTIALS não pôde ser convertida em JSON ou Base64: {e}"
                )

        # Corrige quebras de linha escapadas na chave privada
        if isinstance(cert_dict, dict) and "private_key" in cert_dict:
            cert_dict["private_key"] = cert_dict["private_key"].replace("\\n", "\n")

        cred = credentials.Certificate(cert_dict)
        firebase_admin.initialize_app(cred)
        return

    # 3. Tentar via arquivo físico (local ou Secret File no Render)
    account_path = _find_service_account_path()
    if account_path:
        cred = credentials.Certificate(account_path)
        firebase_admin.initialize_app(cred)
        return

    raise RuntimeError(
        "Erro ao inicializar Firebase: Configure o Environment Group no Render, a variável FIREBASE_CREDENTIALS "
        "ou adicione o arquivo serviceAccountKey.json."
    )

def get_db():
    try:
        firebase_admin.get_app()
    except ValueError:
        init_firebase()
    return firestore.client()

