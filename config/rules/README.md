# Domain Routing

The generator reads two text files from this directory.

## vpn_domains.txt

Domains that should always use the VPN (PROXY group).

Example:

youtube.com
googlevideo.com
chat.openai.com
claude.ai

## direct_domains.txt

Domains that should always bypass the VPN (DIRECT).

Example:

yandex.ru
gosuslugi.ru
ozon.ru
wildberries.ru

## Rules

- One domain per line.
- Empty lines are ignored.
- Lines beginning with # are comments.
- Do not write DOMAIN-SUFFIX manually.
- The generator automatically creates DOMAIN-SUFFIX rules.
