# Mercenary's Path — як запустити гру

Гра працює без інтернету й без сервера: герой і налаштування зберігаються на твоєму комп'ютері.

## Windows

1. Розпакуй `MercenarysPath-windows.zip` у будь-яку теку (не запускай прямо з архіву).
2. Запусти `MercenarysPath.exe`. Якщо Windows покаже «Windows захистив ваш ПК» —
   «Докладніше» → «Однаково запустити» (гра не підписана, це нормально).

## Linux

```
mkdir MercenarysPath && tar -xzf MercenarysPath-linux.tar.gz -C MercenarysPath
cd MercenarysPath
./MercenarysPath.x86_64
```

Якщо файл не запускається — `chmod +x MercenarysPath.x86_64`. Потрібна відеокарта з OpenGL 3.3
(будь-яка звичайна з драйверами від дистрибутива).

## Де лежить збереження

Гра зберігається щоразу, коли герой приходить до табору. Файли — у теці гри:

- Windows: `%APPDATA%\Godot\app_userdata\Mercenary's Path\` (вставити в адресний рядок Провідника);
- Linux: `~/.local/share/godot/app_userdata/Mercenary's Path/`.

`hero.json` — герой, `settings.cfg` — налаштування. Щоб перенести гру на інший комп'ютер,
скопіюй ці файли в ту саму теку там. Нова версія гри їх не стирає.
