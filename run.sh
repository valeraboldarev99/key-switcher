#!/bin/bash

# Получаем переменные из текущей сессии пользователя
export WAYLAND_DISPLAY=wayland-0
export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus

# Полные пути к утилитам
WL_PASTE=/usr/bin/wl-paste
WL_COPY=/usr/bin/wl-copy
PYTHON3=/usr/bin/python3

# Выполняем команду с логированием в syslog для отладки
{
    TEXT=$($WL_PASTE 2>&1)
    RESULT=$(printf '%s' "$TEXT" | $PYTHON3 /home/valeriy/work/programs/key_switcher/switch_layout.py 2>&1)
    printf '%s' "$RESULT" | $WL_COPY
} 2>&1 | tee /tmp/keyswitcher.log

