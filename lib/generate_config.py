from pathlib import Path
import json
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
AVAILABLE_FILE = BASE_DIR / "cache" / "filtered" / "available.json"
OUTPUT_CONFIG = BASE_DIR / "config" / "generated.yaml"

INTERNAL_KEYS = {"_source", "_check", "exit_ip", "country", "country_code", "available"}

def clean_proxy_config(proxy: dict) -> dict:
    cleaned = {k: v for k, v in proxy.items() if k not in INTERNAL_KEYS and not str(k).startswith("_")}
    p_type = str(cleaned.get("type", "")).lower()

    if p_type == "hysteria2":
        
        # Переносим 'auth' в 'auth-str' или 'password' (стандарт Mihomo)
        auth_val = cleaned.pop("auth", None)
        if auth_val and "password" not in cleaned:
            cleaned["password"] = str(auth_val)

        if "username" in cleaned and "password" in cleaned:
            cleaned["password"] = str(cleaned["username"]) + ":" + str(cleaned["password"])
            cleaned.pop("username", None)


        # Корректируем obfs
        obfs_val = cleaned.get("obfs")
        if obfs_val and not isinstance(obfs_val, dict):
            cleaned["obfs"] = "salamander"
            cleaned["obfs-password"] = str(obfs_val)

    elif p_type in ("tuic", "trojan", "vless"):
        pass

    return cleaned

def generate_mihomo_config():
    if not AVAILABLE_FILE.exists():
        print("AVAILABLE_FILE NOT FOUND")
        return

    with AVAILABLE_FILE.open("r", encoding="utf-8") as f:
        available_proxies = json.load(f)

    if not available_proxies:
        print("EMPTY PROXIES LIST")
        return

    clean_proxies = [clean_proxy_config(p) for p in available_proxies]
    proxy_names = [p["name"] for p in clean_proxies if "name" in p]

    config = {
        "mixed-port": 7890,
        "allow-lan": True,
        "mode": "rule",
        "log-level": "info",
        "ipv6": False,
        "external-controller": "127.0.0.1:9090",
        "proxies": clean_proxies,
        "proxy-groups": [
            {
                "name": "PROXY",
                "type": "select",
                "proxies": proxy_names
            }
        ],
        "rules": [
            "MATCH,PROXY"
        ]
    }

    OUTPUT_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CONFIG.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("CONFIG GENERATED OK")

if __name__ == "__main__":
    generate_mihomo_config()
