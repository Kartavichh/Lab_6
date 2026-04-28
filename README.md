# 🔐 Task Tracker API (Secure)

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

REST API для управления задачами с внедрёнными механизмами информационной безопасности.  
Разработано в рамках лабораторных работ №6-7 по дисциплине «Скриптовые языки программирования»  
(НГТУ им. Р.Е. Алексеева, кафедра ИБВСиС).

---

## 📋 О проекте

**Task Tracker API** — это серверная часть приложения для управления задачами, реализованная на фреймворке **FastAPI**. Проект демонстрирует практическое применение принципов **Secure by Design**:

### ✨ Функционал
- 🗂️ Полный цикл CRUD-операций с задачами
- 🔍 Строгая валидация данных через Pydantic v2
- 🧹 Санитизация пользовательского ввода (защита от XSS)
- 🔒 Маскирование PII-данных (email) в ответах API
- 🚦 Ограничение частоты запросов (Rate Limiting)
- 🛡️ Защитные HTTP-заголовки (CSP, HSTS, X-Frame-Options и др.)
- 🌐 Настройка CORS для контроля кросс-доменных запросов
- ⚙️ Вынос конфигурации в переменные окружения (.env)

### 🏗️ Архитектура
```
task_tracker_api/
├── main.py # Точка входа, middleware, конфигурация
├── config.py # Настройки через pydantic-settings
├── dependencies.py # Общие зависимости (limiter)
├── .env.example # Шаблон переменных окружения
├── routers/
│ └── tasks.py # Маршруты API (CRUD + security decorators)
├── schemas/
│ └── task.py # Pydantic-модели с валидаторами
├── services/
│ └── task_service.py # Бизнес-логика, маскирование данных
├── .gitignore # Исключения для Git
└── README.md # Этот файл
```
---

## 🚀 Быстрый старт

### Требования
- Python 3.12+
- pip (менеджер пакетов)
- Виртуальное окружение (рекомендуется)

### Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/your-username/task-tracker-api-secure.git
   cd task-tracker-api-secure
   
2. **Создайте и активируйте виртуальное окружение**:
     ```bash
     python -m venv venv
     
     # Windows:
     venv\Scripts\activate
     # Linux/macOS:
     source venv/bin/activate
     ```
3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Запустите сервер разработки**:
   ```bash
   cp .env.example .env
   # Отредактируйте .env при необходимости

   ```
## ⚙️ Конфигурация
**Переменные окружения (.env)**
```bash
Лимит запросов (формат: количество/период)
RATE_LIMIT=10/minute

Разрешённые источники для CORS (через запятую)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

Режим окружения (development/production)
ENVIRONMENT=development
```
