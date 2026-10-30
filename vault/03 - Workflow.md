# Workflow — Повний цикл розробки

## Схема

```
PM → spec
  ↓
BA → user stories + acceptance criteria  
  ↓
Tech Lead → таски з критеріями (TaskCreate)
  ↓
Developer → реалізація (scenes → scripts)
  ↓
Reviewer → APPROVED або CHANGES REQUESTED
  ↓
QA → PASS або FAIL
  ↓
✅ таск закритий
```

## Правила закриття таску
- Таск **не може** бути закритий без APPROVED від Reviewer
- Таск **не може** бути закритий без PASS від QA
- При CHANGES REQUESTED або FAIL — таск повертається в `pending`
- Developer виправляє → Reviewer → QA → цикл повторюється

## Формати документів

### Spec (PM)
`docs/{feature}_SPEC.md`
- Що це в Java (з посиланнями на рядки)
- Поточний стан в Godot
- Розбіжності (нумерований список)

### Stories (BA)  
`docs/{feature}_STORIES.md`
- User stories (Як гравець я хочу... щоб...)
- Acceptance criteria (конкретні перевіряємі умови)

## Хуки (автоматичні)
PostToolUse на Edit|Write → agent-reviewer перевіряє .gd і .tscn файли
Налаштований в `.claude/settings.json`

## Статуси тасків
- `pending` — чекає або повернутий після FAIL/CHANGES REQUESTED
- `in_progress` — Developer працює
- `completed` — пройшов Reviewer + QA
