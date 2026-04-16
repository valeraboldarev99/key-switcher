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
QDBUS=/usr/bin/qdbus
KXKBRC=/home/valeriy/.config/kxkbrc

switch_layout_if_needed() {
    local target_layout current_index layout_list target_index idx item

    target_layout="$1"
    [ -n "$target_layout" ] || return 0
    [ -x "$QDBUS" ] || return 0
    [ -f "$KXKBRC" ] || return 0

    current_index="$($QDBUS org.kde.keyboard /Layouts org.kde.KeyboardLayouts.getLayout 2>/dev/null)" || return 0
    layout_list="$(grep '^LayoutList=' "$KXKBRC" | cut -d= -f2)"

    idx=0
    target_index=""
    OLD_IFS="$IFS"
    IFS=,
    for item in $layout_list; do
        if [ "$item" = "$target_layout" ]; then
            target_index="$idx"
            break
        fi
        idx=$((idx + 1))
    done
    IFS="$OLD_IFS"

    [ -n "$target_index" ] || return 0
    [ "$current_index" = "$target_index" ] && return 0

    $QDBUS org.kde.keyboard /Layouts org.kde.KeyboardLayouts.setLayout "$target_index" >/dev/null 2>&1 || true
}

should_switch_layout=true
for arg in "$@"; do
    if [ "$arg" = "--invert-case" ]; then
        should_switch_layout=false
        break
    fi
done

# Выполняем команду с логированием в syslog для отладки
{
    TEXT=$($WL_PASTE 2>&1)
    RESULT=$(printf '%s' "$TEXT" | $PYTHON3 /home/valeriy/work/programs/key_switcher/switch_layout.py "$@" 2>&1)
    printf '%s' "$RESULT" | $WL_COPY

    if [ "$should_switch_layout" = true ]; then
        TARGET_LAYOUT=$(printf '%s' "$TEXT" | $PYTHON3 /home/valeriy/work/programs/key_switcher/switch_layout.py --print-target-layout)
        switch_layout_if_needed "$TARGET_LAYOUT"
    fi
} 2>&1 | tee /tmp/keyswitcher.log

