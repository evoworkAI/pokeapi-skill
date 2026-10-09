#!/usr/bin/env python3
"""查 PokéAPI，并可选下载官方精灵图。不用 Key。

    python3 poke.py pikachu
    python3 poke.py 25 --out pikachu.png
    python3 poke.py charizard --sprite default --out charizard.png
"""
import argparse
import json
import os
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

API = "https://pokeapi.co/api/v2"
SPRITES = {
    "gen3": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/{id}.png",
    "default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png",
}


def ssl_context() -> ssl.SSLContext:
    for cand in (os.environ.get("SSL_CERT_FILE"), "/etc/ssl/cert.pem"):
        if cand and pathlib.Path(cand).exists():
            return ssl.create_default_context(cafile=cand)
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "pokeapi-skill", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"没找到：{url}\n名字用英文小写，比如 pikachu、mr-mime；或直接用图鉴编号。")
        sys.exit(f"HTTP {e.code}\n{e.read().decode('utf-8', 'replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"网络错误: {e.reason}")


def chinese_name(species: dict) -> str:
    for item in species.get("names") or []:
        if ((item.get("language") or {}).get("name") or "").lower() == "zh-hans":
            return item.get("name") or ""
    return ""


def main() -> None:
    ap = argparse.ArgumentParser(description="查 PokéAPI 并下载官方精灵图")
    ap.add_argument("name", help="英文名或图鉴编号，如 pikachu、25、mr-mime")
    ap.add_argument("--sprite", default="gen3", choices=sorted(SPRITES))
    ap.add_argument("--out", help="把精灵图存到这个路径")
    args = ap.parse_args()

    key = args.name.strip().lower().replace(" ", "-").replace(".", "")
    pokemon = get_json(f"{API}/pokemon/{key}")
    species = get_json(pokemon["species"]["url"])
    number = pokemon["id"]
    sprite = SPRITES[args.sprite].format(id=number)
    info = {
        "id": number,
        "name": pokemon["name"],
        "name_zh": chinese_name(species),
        "types": [slot["type"]["name"] for slot in pokemon.get("types") or []],
        "sprite": sprite,
        "sprite_set": args.sprite,
    }
    print(json.dumps(info, ensure_ascii=False))

    if not args.out:
        return
    req = urllib.request.Request(sprite, headers={"User-Agent": "pokeapi-skill"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as resp:
            blob = resp.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"精灵图下载失败 HTTP {e.code}: {sprite}")
    except urllib.error.URLError as e:
        sys.exit(f"精灵图下载失败: {e.reason}")
    path = pathlib.Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)
    print(path.resolve())


if __name__ == "__main__":
    main()
