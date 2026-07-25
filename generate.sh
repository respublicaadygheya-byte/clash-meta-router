#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVERS_DIR="$BASE_DIR/servers"
ROUTING_FILE="$BASE_DIR/config/routing.yaml"
OUTPUT_FILE="$BASE_DIR/config/generated.yaml"

echo "Генерация конфигурации Clash Meta..."

echo "Серверы:"
find "$SERVERS_DIR" -type f -name "*.yaml" -printf "  - %f\n"

echo
echo "Файлы серверов найдены."
echo "Следующим этапом будет полноценная генерация:"
echo "$OUTPUT_FILE"
