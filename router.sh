#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

IMPORTER="$BASE_DIR/lib/import_sources.py"
CHECKER="$BASE_DIR/lib/check_proxies_mihomo.py"
GENERATOR="$BASE_DIR/lib/generate_config.py"

show_help() {
    echo
    echo "Clash Meta Router"
    echo
    echo "Использование:"
    echo
    echo "  ./router.sh import"
    echo "      Импортировать все YAML-файлы из sources/"
    echo
    echo "  ./router.sh import FILE.yaml"
    echo "      Импортировать конкретный YAML-файл"
    echo
    echo "  ./router.sh generate"
    echo "      Сгенерировать итоговый Clash Meta конфиг"
    echo
    echo "  ./router.sh build"
    echo "      Импортировать источники и создать конфиг"
    echo
    echo "  ./router.sh status"
    echo "      Показать состояние проекта"
    echo
}


cmd_import() {
    if [[ $# -gt 0 ]]; then
        python3 "$IMPORTER" --input "$1"
    else
        python3 "$IMPORTER"
    fi
}


cmd_check() {
    python3 "$CHECKER"
}


cmd_generate() {
    python3 "$GENERATOR"
}


cmd_build() {
    echo "========================================"
    echo " Clash Meta Router BUILD"
    echo "========================================"

    echo
    echo "[1/3] Импорт источников"
    cmd_import

    echo
    echo "[2/3] Проверка прокси через Mihomo"
    cmd_check

    echo
    echo "[3/3] Генерация конфигурации"
    cmd_generate

    echo
    echo "BUILD завершён"
}


cmd_status() {
    echo
    echo "Проект: $BASE_DIR"
    echo

    echo "Источники:"
    find "$BASE_DIR/sources" \
        -maxdepth 1 \
        -type f \
        \( -name "*.yaml" -o -name "*.yml" \) \
        -printf "  - %f\n" 2>/dev/null || true

    echo

    echo "Cache:"
    find "$BASE_DIR/cache" \
        -type f \
        -printf "  - %p\n" 2>/dev/null || true

    echo
}


case "${1:-help}" in

    import)
        shift
        cmd_import "$@"
        ;;

    check)
        cmd_check
        ;;

    generate)
        cmd_generate
        ;;

    build)
        cmd_build
        ;;

    status)
        cmd_status
        ;;

    help|--help|-h)
        show_help
        ;;

    *)
        echo "Неизвестная команда: $1"
        show_help
        exit 1
        ;;

esac
