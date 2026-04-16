#!/usr/bin/env python3
import sys
import re

EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,./"
RU = "йцукенгшщзхъфывапролджэячсмитьбю."
EN_SHIFT = "QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
RU_SHIFT = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"

def build_map(src: str, dst: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for src_ch, dst_ch in zip(src, dst):
        mapping[src_ch] = dst_ch
    return mapping


EN_TO_RU = build_map(EN + EN_SHIFT, RU + RU_SHIFT)
RU_TO_EN = build_map(RU + RU_SHIFT, EN + EN_SHIFT)

EN_ALPHA = {ch for ch in (EN + EN_SHIFT) if ch.isalpha()}
RU_ALPHA = {ch for ch in (RU + RU_SHIFT) if ch.isalpha()}


def translate_token(token: str) -> str:
    en_count = sum(1 for ch in token if ch in EN_ALPHA)
    ru_count = sum(1 for ch in token if ch in RU_ALPHA)

    if en_count > ru_count:
        return "".join(EN_TO_RU.get(ch, ch) for ch in token)
    if ru_count > en_count:
        return "".join(RU_TO_EN.get(ch, ch) for ch in token)
    return token


def convert_text(text: str) -> str:
    return re.sub(r"\S+", lambda m: translate_token(m.group(0)), text)


def main():
    text = sys.stdin.read()
    if not text.strip():
        return
    sys.stdout.write(convert_text(text))

if __name__ == "__main__":
    main()

    