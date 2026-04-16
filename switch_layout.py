#!/usr/bin/env python3
import argparse
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


def invert_case(text: str) -> str:
    return text.swapcase()


def detect_target_layout(text: str) -> str:
    en_count = sum(1 for ch in text if ch in EN_ALPHA)
    ru_count = sum(1 for ch in text if ch in RU_ALPHA)

    if en_count > ru_count:
        return "ru"
    if ru_count > en_count:
        return "us"
    return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert keyboard layout or invert case")
    parser.add_argument(
        "--invert-case",
        action="store_true",
        help="Invert character case instead of converting keyboard layout",
    )
    parser.add_argument(
        "--print-target-layout",
        action="store_true",
        help="Print target layout code for the given text: us, ru, or empty",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    text = sys.stdin.read()
    if not text.strip():
        return
    if args.print_target_layout:
        sys.stdout.write(detect_target_layout(text))
        return
    if args.invert_case:
        sys.stdout.write(invert_case(text))
        return
    sys.stdout.write(convert_text(text))

if __name__ == "__main__":
    main()

    