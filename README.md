# Clash Meta Router

Автоматический генератор конфигурации **Mihomo / Clash Meta**
для OpenWRT роутеров с OpenClash.

Проект собирает VPN-подписки, проверяет прокси через Mihomo,
удаляет нерабочие соединения и создаёт готовый YAML-файл
для загрузки в OpenClash.

---

# Назначение проекта

Проект предназначен для автоматического создания рабочей
VPN-конфигурации на домашнем роутере.

Основные функции:

- импорт подписок;
- фильтрация прокси;
- проверка через Mihomo;
- удаление нерабочих серверов;
- генерация YAML;
- использование в OpenClash.

---

# Архитектура

Источники подписок

↓

Импорт прокси

↓

Фильтрация протоколов

↓

Проверка Mihomo

↓

Генерация YAML

↓

OpenClash на OpenWRT

---
# Рабочие протоколы

В текущей версии проекта используются:

- VLESS
- Trojan
- Hysteria2

Эти протоколы импортируются,
проверяются и добавляются в итоговый YAML.

NaiveProxy полностью исключён.

---

# Группы маршрутизации

После генерации создаются:

🚀 PROXY

├── ⭐ OWN

├── 🌐 FOREIGN

├── 🇷🇺 RUSSIA

└── DIRECT


---

# ⭐ OWN

Группа собственных VPN-серверов пользователя.

Используется для личных VPS.

---

# 🌐 FOREIGN

Группа зарубежных подписок.

Структура:

🌐 FOREIGN

├── 🌐 FOREIGN-AUTO

└── отдельные серверы

FOREIGN-AUTO выбирает рабочие зарубежные серверы.

---
# 🇷🇺 RUSSIA

Группа российских направлений.

Используется для:

- российских сайтов;
- банков;
- маркетплейсов;
- государственных сервисов.

Примеры:

yandex.ru
ozon.ru
wildberries.ru
vk.com
gosuslugi.ru


---

# Логика маршрутизации

Российские сайты:

RU сайты

↓

🇷🇺 RUSSIA


Остальной интернет:

Интернет

↓

🚀 PROXY


Пользователь выбирает:

🚀 PROXY

├── ⭐ OWN

├── 🌐 FOREIGN

└── DIRECT

---

---

# Генерация YAML-конфигурации

После проверки прокси выполняется создание итогового файла.

Команда:

```bash
python3 lib/generate_config.py

Готовый файл:

config/generated.yaml

загружается в OpenClash.

Загрузка в OpenClash

Файл:

config/generated.yaml

используется как готовая конфигурация для OpenClash
на роутере OpenWRT.

После загрузки доступны группы:

🚀 PROXY

├── ⭐ OWN

├── 🌐 FOREIGN

├── 🌐 FOREIGN-AUTO

├── 🇷🇺 RUSSIA

└── DIRECT
Проверка проекта

Проверка Python-файлов:

python3 -m py_compile lib/*.py

Проверка Git:

git status
Текущее состояние проекта

Работает:

✅ импорт подписок
✅ фильтрация прокси
✅ проверка через Mihomo
✅ генерация YAML
✅ OpenClash конфигурация
✅ группы OWN / FOREIGN / RUSSIA / DIRECT
✅ FOREIGN-AUTO
✅ удаление NaiveProxy

Полный цикл обновления
cd ~/clash-meta-router

python3 lib/import_sources.py

python3 lib/check_proxies_mihomo.py

python3 lib/generate_config.py

Результат:

config/generated.yaml

готов для загрузки в OpenClash.

Clash Meta Router

Генератор управляемых VPN-конфигураций
для OpenWRT + OpenClash.

