#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import argparse
import json
import sys
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCES_DIR = BASE_DIR / "sources"
CACHE_DIR = BASE_DIR / "cache"
IMPORTED_DIR = CACHE_DIR / "imported"
OUTPUT_FILE = IMPORTED_DIR / "proxies.json"
SUB_PROXIES_FILE = IMPORTED_DIR / "subscription_proxies.json"


SUPPORTED_TYPES = {
    "vless",
    "vmess",
    "trojan",
    "hysteria2",
    "tuic",
    "ss",
    "ssr",
    "socks5",
    "http",
    "https",
    "naive",
    "anytls",
}


def load_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            return None

        return data

    except Exception as e:
        print(f"ОШИБКА YAML: {path}")
        print(f"  {e}", file=sys.stderr)
        return None


def extract_proxies(data):
    if not isinstance(data, dict):
        return []

    proxies = data.get("proxies", [])

    if not isinstance(proxies, list):
        return []

    return proxies


def normalize_proxy(proxy, source):
    if not isinstance(proxy, dict):
        return None

    proxy_type = str(proxy.get("type", "")).lower().strip()

    if proxy_type not in SUPPORTED_TYPES:
        return None

    if not proxy.get("name"):
        proxy["name"] = f"{proxy_type}-{proxy.get('server', 'unknown')}"

    proxy["_source"] = source

    return proxy


def proxy_key(proxy):
    return (
        proxy.get("type"),
        proxy.get("server"),
        proxy.get("port"),
        proxy.get("uuid"),
        proxy.get("password"),
        proxy.get("username"),
    )


def find_source_files():
    if not SOURCES_DIR.exists():
        return []

    return sorted(
        path
        for path in SOURCES_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".yaml", ".yml"}
        and path.name != "remote.yaml"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Импорт всех источников Clash Meta"
    )

    parser.add_argument(
        "--input",
        help="Импортировать только указанный YAML-файл"
    )

    args = parser.parse_args()

    if args.input:
        source_files = [Path(args.input)]
    else:
        source_files = find_source_files()

    if not source_files and not SUB_PROXIES_FILE.exists():
        print("Источники не найдены.")
        sys.exit(1)

    all_proxies = []
    source_stats = Counter()
    type_stats = Counter()
    duplicates = 0

    if SUB_PROXIES_FILE.exists():
        with SUB_PROXIES_FILE.open("r", encoding="utf-8") as f:
            subscription_proxies = json.load(f)

        for proxy in subscription_proxies:
            key = proxy_key(proxy)

            if any(proxy_key(existing) == key for existing in all_proxies):
                duplicates += 1
                continue

            all_proxies.append(proxy)
            source_stats[proxy.get("_source", "subscription")] += 1
            type_stats[proxy.get("type")] += 1

    for path in source_files:
        print(f"Импорт: {path}")

        data = load_yaml(path)

        if data is None:
            continue

        proxies = extract_proxies(data)

        for proxy in proxies:
            normalized = normalize_proxy(
                proxy,
                path.name
            )

            if normalized is None:
                continue

            key = proxy_key(normalized)

            if any(proxy_key(existing) == key for existing in all_proxies):
                duplicates += 1
                continue

            all_proxies.append(normalized)

            source_stats[path.name] += 1
            type_stats[normalized["type"]] += 1

    IMPORTED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            all_proxies,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("Импорт завершён")
    print("----------------------------")
    print(f"Источников:      {len(source_files)}")
    print(f"Подключений:     {len(all_proxies)}")
    print(f"Дубликатов:      {duplicates}")
    print(f"Результат:       {OUTPUT_FILE}")

    print()
    print("Типы подключений:")

    for proxy_type, count in sorted(type_stats.items()):
        print(f"  {proxy_type}: {count}")

    print()
    print("Источники:")

    for source, count in sorted(source_stats.items()):
        print(f"  {source}: {count}")


if __name__ == "__main__":
    main()
