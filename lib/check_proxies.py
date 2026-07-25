#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import argparse
import json
import socket
import time
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
IMPORTED_FILE = BASE_DIR / "cache" / "imported" / "proxies.json"
FILTERED_DIR = BASE_DIR / "cache" / "filtered"
AVAILABLE_FILE = FILTERED_DIR / "available.json"


def check_tcp(server, port, timeout):
    start = time.perf_counter()

    try:
        with socket.create_connection(
            (server, int(port)),
            timeout=timeout
        ):
            elapsed = round((time.perf_counter() - start) * 1000, 2)

            return {
                "available": True,
                "latency_ms": elapsed,
                "error": None,
            }

    except Exception as e:
        elapsed = round((time.perf_counter() - start) * 1000, 2)

        return {
            "available": False,
            "latency_ms": elapsed,
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(
        description="Проверка доступности прокси-серверов"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="Таймаут TCP-проверки в секундах"
    )

    args = parser.parse_args()

    if not IMPORTED_FILE.exists():
        print(
            f"Ошибка: отсутствует {IMPORTED_FILE}",
            file=sys.stderr
        )
        sys.exit(1)

    with IMPORTED_FILE.open("r", encoding="utf-8") as f:
        proxies = json.load(f)

    FILTERED_DIR.mkdir(parents=True, exist_ok=True)

    available = []

    print()
    print("Проверка подключений")
    print("----------------------------")

    for index, proxy in enumerate(proxies, start=1):

        name = proxy.get("name", f"Proxy {index}")
        server = proxy.get("server")
        port = proxy.get("port")
        proxy_type = proxy.get("type", "unknown")

        print(
            f"[{index}/{len(proxies)}] "
            f"{name} "
            f"({proxy_type} {server}:{port})",
            end=" ... ",
            flush=True
        )

        if not server or not port:
            print("INVALID")

            continue

        result = check_tcp(
            server,
            port,
            args.timeout
        )

        proxy_copy = dict(proxy)

        proxy_copy["check"] = {
            "available": result["available"],
            "latency_ms": result["latency_ms"],
            "checked_at": int(time.time()),
        }

        if result["available"]:
            available.append(proxy_copy)

            print(
                f"OK "
                f"{result['latency_ms']} ms"
            )

        else:
            print(
                f"FAIL "
                f"{result['error']}"
            )

    with AVAILABLE_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            available,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("----------------------------")
    print("Проверка завершена")
    print(f"Всего:       {len(proxies)}")
    print(f"Доступно:    {len(available)}")
    print(f"Недоступно:  {len(proxies) - len(available)}")
    print(f"Результат:   {AVAILABLE_FILE}")

    if available:
        print()
        print("Доступные подключения:")

        for proxy in sorted(
            available,
            key=lambda x: x["check"]["latency_ms"]
        ):
            print(
                f"  "
                f"{proxy['check']['latency_ms']:>8} ms  "
                f"{proxy.get('type', 'unknown'):10}  "
                f"{proxy.get('name', 'Unnamed')}"
            )


if __name__ == "__main__":
    main()
