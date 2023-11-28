# This is a bunch of quickly written code meant to explicit some fields
# in JWTs, SD-JWTs, and JSON structure. This is in no way safe code to use to parse these structures.

from __future__ import annotations

import base64
import json
from typing import Any

available_colors = range(31, 37)


def explain_disclosure(disclosure: str) -> str:
    nonce, claim_name, claim_value = [e for e in json.loads(disclosure)]

    explained_disclosure = f"""[
    \x1b[31m{nonce}\x1b[0m, <--- 🧂
    \x1b[32m{claim_name}\x1b[0m, <--- claim name"
    \x1b[33m{claim_value}\x1b[0m <--- claim value"
]"""

    return explained_disclosure


def _color(color_code: int, text: str) -> str:
    return f"\x1b[{color_code}m{text}\x1b[0m"


def explain_jwt(serialized_sd_jwt: str, presentation_jwt: bool = False) -> str:
    header, body, *signature_disclosures_keybinding = serialized_sd_jwt.split('.')
    signature_disclosures_keybinding = '.'.join(signature_disclosures_keybinding)
    includes_keybinding = presentation_jwt and signature_disclosures_keybinding[-1] != "~"

    signature_disclosures_keybinding = signature_disclosures_keybinding.split('~')

    # dismantle the last section to split the signature, disclosures and the keybinding JWT (if present)
    keybinding_jwt = signature_disclosures_keybinding.pop() if includes_keybinding else None
    signature = signature_disclosures_keybinding.pop(0)
    disclosures = signature_disclosures_keybinding

    color_indices = [31 + i % len(available_colors) for i in range(0, len([header, body, signature]) + len(disclosures) + (1 if keybinding_jwt else 0) + 1)]

    header = _color(color_indices.pop(0), header)
    body = _color(color_indices.pop(0), body)
    signature = _color(color_indices.pop(0), signature)

    disclosures = [_color(color_indices.pop(0), d) for d in disclosures]

    keybinding_jwt = _color(color_indices.pop(0), keybinding_jwt)

    explained_jwt = ".".join([header, body, signature])

    explained_keybinding = ""
    if presentation_jwt:
        explained_disclosures = "~".join(disclosures)
        explained_keybinding = "~" + keybinding_jwt if includes_keybinding else explained_keybinding

    return f"{explained_jwt}" if not presentation_jwt else f"{explained_jwt}~{explained_disclosures}{explained_keybinding}"


def explain_hashing(disclosure: str, encoded_disclosure: str, digest: str, screen_width: int = 200):
    arrow = '--->'
    arrow_padding_width = len(arrow) + 2
    elements = [disclosure, "URL-safe base 64", encoded_disclosure, "SHA-256", digest]

    lines = []
    top_line = ""
    content_line = ""
    for index, element in enumerate(elements):
        if len(top_line) + len(element) + 4 + arrow_padding_width > screen_width:
            lines.append((top_line, content_line))
            top_line = ""
            content_line = ""

        is_operand = index % 2 == 0
        if is_operand:
            content_line += f'| {element} |'
            no_width_characters = 9 if "\x1b" in element else 0
            top_line += '-' * (len(element) + 4 - no_width_characters)
        else:
            content_line += f" {element} "
            top_line += ' ' * (len(element) + 2)

        if index != len(elements)-1:
            top_line += ' ' * arrow_padding_width
            content_line += f" {arrow} "
    lines.append((top_line, content_line))

    for top_line, content_line in lines:
        print(f"""
{top_line}
{content_line}
{top_line}""")


def b64decode(encoded: str) -> str:
    return base64.urlsafe_b64decode(encoded + '==').decode('ascii')


def highlight(original: str, character: str, color_number: int = 31) -> str:
    return original.replace(character, f"\x1b[{color_number}m{character}\x1b[0m")


def pretty(json_str: str | Any) -> str:
    if type(json_str) is not str:
        json_str = json.dumps(json_str)
    return json.dumps(json.loads(json_str), indent=2)
