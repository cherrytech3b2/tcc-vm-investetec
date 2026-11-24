import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader

_cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
_api_key = os.environ.get("CLOUDINARY_API_KEY")
_api_secret = os.environ.get("CLOUDINARY_API_SECRET")

if not (_cloud_name and _api_key and _api_secret):
    _url = os.environ.get("CLOUDINARY_URL")
    if _url:
        _parsed = urlparse(_url)
        _cloud_name = _cloud_name or _parsed.hostname
        _api_key = _api_key or _parsed.username
        _api_secret = _api_secret or _parsed.password

cloudinary.config(
    cloud_name=_cloud_name,
    api_key=_api_key,
    api_secret=_api_secret,
    secure=True,
)

FOTO_EXTS = {"jpg", "jpeg", "png", "webp"}
VIDEO_EXTS = {"mp4", "webm", "mov"}


def enviar_arquivo(arq, tipo):
    """Envia foto ou vídeo ao Cloudinary. Retorna (url, erro)."""
    if not arq or not arq.filename:
        return None, None

    if tipo == "foto":
        exts, mb, rtype = FOTO_EXTS, 5, "image"
    else:
        exts, mb, rtype = VIDEO_EXTS, 100, "video"

    ext = arq.filename.rsplit(".", 1)[-1].lower()
    if ext not in exts:
        return None, "Formato inválido. Use: " + ", ".join(sorted(exts)).upper() + "."

    arq.stream.seek(0, 2)
    tamanho = arq.stream.tell()
    arq.stream.seek(0)
    if tamanho > mb * 1048576:
        return None, f"Arquivo maior que {mb} MB."

    try:
        r = cloudinary.uploader.upload(
            arq.stream, resource_type=rtype, folder="investetec/projetos"
        )
        return r["secure_url"], None
    except Exception as e:
        print("Erro Cloudinary:", e)
        return None, "Não foi possível enviar o arquivo. Tente novamente."