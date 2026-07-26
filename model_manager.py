import re

# 支援的戰鬥陀螺型號前綴
SERIES = [
    "BX",
    "UX",
    "CX",
]


def extract_model(name):

    text = name.upper()

    for series in SERIES:

        # BX-39、UX-05、CX-01
        match = re.search(rf"\b{series}-?(\d{{2,3}})\b", text)

        if match:
            number = match.group(1).zfill(2)
            return f"{series}-{number}"

    return None