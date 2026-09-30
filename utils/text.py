import html
import re


def sanitize_text(text: str) -> str:

    replacements = {

        "\u2018": "'",
        "\u2019": "'",

        "\u201c": '"',
        "\u201d": '"',

        "\u2013": "-",
        "\u2014": "-",

        "\u2026": "...",

        "\u00a0": " ",

        "\u2022": "-",
    }


    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )


    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )


    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )


    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text
    )


    return text.strip()


def html_preview(text: str) -> str:

    safe = html.escape(
        sanitize_text(text)
    )

    blocks = []


    for block in safe.split("\n\n"):

        lines = block.split("\n")

        if not lines:
            continue


        first = lines[0].strip()


        if (
            first.isupper()
            and len(first) <= 100
            and not first.startswith("-")
        ):

            blocks.append(
                f"<h3>{first}</h3>"
            )

        else:

            body = "<br>".join(
                line
                for line in lines
                if line.strip()
            )

            blocks.append(
                f"<p>{body}</p>"
            )


    return "\n".join(blocks)