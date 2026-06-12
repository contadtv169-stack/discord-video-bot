import asyncio
import re
from typing import Optional

import yt_dlp

SHOPEE_DOMAINS = {
    "br": "shopee.com.br",
    "global": "shopee.com",
}

async def search_shopee_products(query: str, max_results: int = 5, region: str = "br") -> list[dict]:
    def _search():
        results = []
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        search_terms = [
            f"{query} shopee",
            f"{query} shopee anúncio",
            f"{query} shopee review",
        ]
        seen_urls = set()
        for term in search_terms:
            if len(results) >= max_results:
                break
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(f"ytsearch{max_results}:{term}", download=False)
                    if result and "entries" in result:
                        for entry in result["entries"]:
                            url = f"https://youtube.com/watch?v={entry['id']}"
                            if url not in seen_urls:
                                seen_urls.add(url)
                                results.append({
                                    "title": entry.get("title", "Sem título"),
                                    "url": url,
                                    "platform": "youtube",
                                    "type": "video",
                                    "thumbnail": entry.get("thumbnail"),
                                    "channel": entry.get("uploader", "Desconhecido"),
                                })
                                if len(results) >= max_results:
                                    break
            except Exception:
                continue
        return results[:max_results]
    return await asyncio.to_thread(_search)

async def get_product_info(product_url: str) -> Optional[dict]:
    def _scrape():
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(product_url, download=False)
                if info:
                    title = info.get("title", "")
                    price_match = re.search(r'R?\$?[\d.,]+', title)
                    return {
                        "title": title,
                        "url": product_url,
                        "price": price_match.group(0) if price_match else "Ver no site",
                        "thumbnail": info.get("thumbnail"),
                        "description": info.get("description", "")[:200],
                    }
        except Exception:
            pass

        try:
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            resp = requests.get(product_url, headers=headers, timeout=15)
            if resp.status_code == 200:
                title_match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE)
                price_match = re.search(r'R?\$?([\d.,]+)', resp.text)
                return {
                    "title": title_match.group(1).strip() if title_match else "Produto Shopee",
                    "url": product_url,
                    "price": f"R$ {price_match.group(1)}" if price_match else "Ver no site",
                }
        except Exception:
            pass
        return None
    return await asyncio.to_thread(_scrape)

async def search_shopee_videos(query: str, max_results: int = 5) -> list[dict]:
    products = await search_shopee_products(query, max_results)
    for p in products:
        p["type"] = "video"
    return products
