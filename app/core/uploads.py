import io
import os
import traceback
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader


def _limpar(valor):
    if not valor:
        return None
    v = valor.strip().strip("'\"")
    return v or None


def _env_flex(*nomes):
    for nome in nomes:
        for candidato in (nome, nome.upper(), nome.lower()):
            val = _limpar(os.environ.get(candidato))
            if val:
                return val
    return None


def _resolver_credenciais():
    cloud_name = _env_flex("CLOUDINARY_CLOUD_NAME", "CLOUD_NAME")
    api_key = _env_flex("CLOUDINARY_API_KEY")
    api_secret = _env_flex("CLOUDINARY_API_SECRET")

    if not (cloud_name and api_key and api_secret):
        raw_url = _env_flex("CLOUDINARY_URL")
        if raw_url:
            # Trata caso comum no Render onde colam "CLOUDINARY_URL=cloudinary://..." no valor
            if raw_url.startswith("CLOUDINARY_URL="):
                raw_url = _limpar(raw_url.split("=", 1)[1])
            if raw_url and "://" in raw_url:
                parsed = urlparse(raw_url)
                cloud_name = cloud_name or _limpar(parsed.hostname)
                api_key = api_key or _limpar(parsed.username)
                api_secret = api_secret or _limpar(parsed.password)

    return cloud_name, api_key, api_secret


def configurar_cloudinary():
    cloud_name, api_key, api_secret = _resolver_credenciais()
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )
    return cloud_name, api_key, api_secret


_cn, _ak, _as = configurar_cloudinary()
print(
    f"-> [Cloudinary] cloud_name={_cn or 'AUSENTE'} | "
    f"api_key={'OK' if _ak else 'AUSENTE'} | "
    f"api_secret={'OK' if _as else 'AUSENTE'}",
    flush=True,
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

    cloud_name, api_key, api_secret = configurar_cloudinary()
    if not (cloud_name and api_key and api_secret):
        print(
            "-> [Cloudinary ERRO] Credenciais ausentes no ambiente "
            f"(cloud_name={'OK' if cloud_name else 'AUSENTE'}, "
            f"api_key={'OK' if api_key else 'AUSENTE'}, "
            f"api_secret={'OK' if api_secret else 'AUSENTE'})",
            flush=True,
        )
        return (
            None,
            "Cloudinary não configurado no servidor. Verifique as variáveis de ambiente.",
        )

    arq.stream.seek(0)
    conteudo = arq.read()
    tamanho = len(conteudo)
    if tamanho == 0:
        return None, "O arquivo enviado está vazio."
    if tamanho > mb * 1048576:
        return None, f"Arquivo maior que {mb} MB."

    buffer = io.BytesIO(conteudo)
    buffer.name = os.path.basename(arq.filename) or f"arquivo.{ext}"

    try:
        if rtype == "video" and tamanho > 20 * 1048576:
            r = cloudinary.uploader.upload_large(
                buffer,
                resource_type="video",
                folder=pasta,
                chunk_size=6 * 1024 * 1024,
            )
        else:
            r = cloudinary.uploader.upload(
                buffer,
                resource_type=rtype,
                folder=pasta,
            )
        return r["secure_url"], None
    except Exception as e:
        print(f"-> [Cloudinary ERRO] ({arq.filename}): {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
        msg = str(e)
        if any(k in msg for k in ("Must supply", "Invalid Signature", "Invalid cloud_name", "Unknown API key", "401")):
            return None, f"Erro de credenciais no Cloudinary: {msg}"
        return None, "Não foi possível enviar o arquivo. Tente novamente."
