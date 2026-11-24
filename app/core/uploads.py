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


def gerar_thumbnail_imagem(url, largura=600, altura=360):
    """Gera URL de thumbnail otimizada via transformação do Cloudinary."""
    if not url or not isinstance(url, str):
        return None
    marcador = "/image/upload/"
    if marcador in url:
        transform = f"c_fill,g_auto,w_{largura},h_{altura},q_auto,f_auto/"
        base, resto = url.split(marcador, 1)
        if not resto.startswith("c_fill,"):
            return f"{base}{marcador}{transform}{resto}"
    return url


def gerar_thumbnail_video(url, largura=640, altura=360):
    """Gera URL de thumbnail (.jpg) de um vídeo hospedado no Cloudinary."""
    if not url or not isinstance(url, str):
        return None
    marcador = "/video/upload/"
    if marcador not in url:
        return None
    transform = f"so_auto,c_fill,w_{largura},h_{altura},q_auto,f_auto/"
    base, resto = url.split(marcador, 1)
    if "." in resto.rsplit("/", 1)[-1]:
        resto = resto.rsplit(".", 1)[0] + ".jpg"
    else:
        resto = resto + ".jpg"
    return f"{base}{marcador}{transform}{resto}"


def sincronizar_midias_projeto(p):
    """Garante que o documento do projeto tenha URLs do Cloudinary e thumbnails consistentes."""
    if not isinstance(p, dict):
        return p

    fotos = []
    for campo in ("foto_1", "foto_2", "foto_3"):
        url = p.get(campo)
        if url and url not in fotos:
            fotos.append(url)
    for url in (p.get("fotos") or []):
        if url and url not in fotos:
            fotos.append(url)

    for idx, url in enumerate(fotos[:3], start=1):
        p.setdefault(f"foto_{idx}", url)

    capa = p.get("foto_1") or (fotos[0] if fotos else p.get("imagem"))
    thumbnails = [gerar_thumbnail_imagem(u) for u in fotos]
    capa_thumb = thumbnails[0] if thumbnails else gerar_thumbnail_imagem(capa)
    video_url = p.get("video") or None
    video_thumb = p.get("video_thumbnail") or gerar_thumbnail_video(video_url)

    p["fotos"] = fotos
    p["imagem"] = capa
    p["thumbnail"] = capa_thumb
    p["thumbnails"] = thumbnails
    p["video_thumbnail"] = video_thumb
    p["midias"] = {
        "capa": capa,
        "thumbnail": capa_thumb,
        "fotos": [
            {"url": u, "thumbnail": t}
            for u, t in zip(fotos, thumbnails)
        ],
        "video": (
            {"url": video_url, "thumbnail": video_thumb}
            if video_url
            else None
        ),
    }
    return p


def enviar_arquivo(arq, tipo, pasta="investetec/projetos"):
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
            arq.stream, resource_type=rtype, folder=pasta
        )
        return r["secure_url"], None
    except Exception as e:
        print("Erro Cloudinary:", e, flush=True)
        return None, "Não foi possível enviar o arquivo. Tente novamente."