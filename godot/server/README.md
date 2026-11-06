# Сервер гри (Godot-версія)

Окрема програма на нашому VPS, одна на всіх гравців (`docs/GODOT_PLAN.md`, розділ 3).
Python 3.10+, `websockets`, SQLite.

```
pip install -r godot/server/requirements.txt
cd godot/server
python -m game_server --port 28300 --db heroes.sqlite     # ws://0.0.0.0:28300
python -m pytest -q                                       # тести
```

За TLS-проксі (Caddy, nginx) гра ходить на `wss://`, сервер запускати з `--behind-proxy`
(адреса гравця — останній запис X-Forwarded-For).

## Протокол v1

Одне JSON-повідомлення = один текстовий кадр WebSocket. Запит: `type`, `id` (число клієнта,
повертається у відповіді), `v` (версія протоколу). Відповідь: `type` + `_ok` або
`{"type": "error", "code": ...}`; клієнт іншої версії отримує `error` `update`.

| Запит | Поля | Відповідь |
|---|---|---|
| `hello` | | `hello_ok {server, v}` |
| `guest_login` | `device` (16–64 знаки, випадковий ключ пристрою) | `guest_login_ok {account, token}` |
| `login` | `account`, `token` | `login_ok {account}` |
| `hero_get` | | `hero_get_ok {hero, rev}` (`hero` null, якщо немає) |
| `hero_put` | `hero`, `rev` (що гра востаннє отримала) | `hero_put_ok {rev}`, або `error stale` |

Гість — акаунт пристрою: гра один раз робить випадковий ключ і зберігає його й токен у
`user://account.cfg`. Сервер тримає лише хеші ключа й токена. Ліміти (`security.py`): з'єднань
з однієї адреси, нових акаунтів з адреси на годину, повідомлень за секунду.

Поки що сервер лише зберігає героя, якого надіслала гра (Live → Зберегти / Завантажити).
Рахувати золото, дроп і кузню на сервері — наступні кроки (G5, G7 у плані).
