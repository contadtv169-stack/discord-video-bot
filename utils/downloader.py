import yt_dlp
import os
import re
import asyncio
from typing import Optional

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)[:100]

async def search_youtube(query: str, max_results: int = 5) -> list[dict]:
    def _search():
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "force_generic_extractor": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            if not result or "entries" not in result:
                return []
            return [
                {
                    "title": entry.get("title", "Sem título"),
                    "url": f"https://youtube.com/watch?v={entry['id']}",
                    "platform": "youtube",
                    "duration": entry.get("duration"),
                    "thumbnail": entry.get("thumbnail"),
                    "channel": entry.get("uploader", "Desconhecido"),
                }
                for entry in result["entries"]
            ]
    return await asyncio.to_thread(_search)

async def search_tiktok(query: str, max_results: int = 5) -> list[dict]:
    def _search():
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch{max_results}:{query} tiktok", download=False)
                if not result or "entries" not in result:
                    return []
                videos = []
                for entry in result["entries"]:
                    url = entry.get("url") or f"https://youtube.com/watch?v={entry['id']}"
                    videos.append({
                        "title": entry.get("title", "Sem título"),
                        "url": url,
                        "platform": "tiktok",
                        "duration": entry.get("duration"),
                        "thumbnail": entry.get("thumbnail"),
                        "channel": entry.get("uploader", "Desconhecido"),
                    })
                return videos[:max_results]
        except Exception:
            return []
    return await asyncio.to_thread(_search)

async def search_kwai(query: str, max_results: int = 5) -> list[dict]:
    def _search():
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch{max_results}:{query} kwai", download=False)
                if not result or "entries" not in result:
                    return []
                videos = []
                for entry in result["entries"]:
                    url = entry.get("url") or f"https://youtube.com/watch?v={entry['id']}"
                    videos.append({
                        "title": entry.get("title", "Sem título"),
                        "url": url,
                        "platform": "kwai",
                        "duration": entry.get("duration"),
                        "thumbnail": entry.get("thumbnail"),
                        "channel": entry.get("uploader", "Desconhecido"),
                    })
                return videos[:max_results]
        except Exception:
            return []
    return await asyncio.to_thread(_search)

async def search_all(query: str, max_results: int = 3) -> list[dict]:
    results = []
    yt, tt, kw = await asyncio.gather(
        search_youtube(query, max_results),
        search_tiktok(query, max_results),
        search_kwai(query, max_results),
    )
    results.extend(yt)
    results.extend(tt)
    results.extend(kw)
    return results

async def download_video(url: str, platform: str = "youtube") -> Optional[str]:
    def _dl():
        filename = sanitize_filename(f"{platform}_{url.split('/')[-1][:20]}")
        filepath = os.path.join(DOWNLOAD_DIR, f"{filename}.%(ext)s")
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": filepath,
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                ext = info.get("ext", "mp4")
                actual_path = os.path.join(DOWNLOAD_DIR, f"{filename}.{ext}")
                if os.path.exists(actual_path):
                    return actual_path
                for f in os.listdir(DOWNLOAD_DIR):
                    if f.startswith(filename):
                        return os.path.join(DOWNLOAD_DIR, f)
            return None
        except Exception:
            return None
    return await asyncio.to_thread(_dl)
