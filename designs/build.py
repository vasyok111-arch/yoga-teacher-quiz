from pathlib import Path
import re


DESIGNS = Path(__file__).resolve().parent
SOURCE = DESIGNS.parent / "index.html"
THEMES = {
    "zen": ("Тихая практика", "#f5f1e8"),
    "apple": ("Студия", "#f5f5f7"),
    "edtech": ("Учебная платформа", "#f5f6ff"),
    "impact": ("Пульс", "#151610"),
}


def render_variant(source: str, slug: str, name: str, color: str) -> str:
    page = source.replace('<html lang="ru">', f'<html lang="ru" data-design="{slug}">', 1)
    page = page.replace('name="theme-color" content="#f8f5f3"', f'name="theme-color" content="{color}"', 1)
    page = page.replace("</title>", f" · {name}</title>", 1)
    page = page.replace("</head>", f'<link rel="stylesheet" href="../{slug}.css">\n</head>', 1)
    page = page.replace("assets/", "../../assets/")

    if slug == "edtech":
        outline = """    <ol class="lesson-outline" aria-label="План пробного урока">
      <li><span>Вопросы 1–2</span><strong>Цель и группа</strong></li>
      <li><span>Вопросы 3–4</span><strong>Основы йоги</strong></li>
      <li><span>Вопросы 5–6</span><strong>Решения на уроке</strong></li>
    </ol>
"""
        page = page.replace("    </figure>\n  </section>", "    </figure>\n" + outline + "  </section>", 1)
    elif slug == "impact":
        page = page.replace(
            'src="../../assets/scenes/first-class.webp" width="1080" height="810"',
            'src="poster.webp" width="1080" height="1080"',
            1,
        )
        page = page.replace(
            'А если йога станет <span>вашей профессией?</span>',
            'Готовы вести <span>уроки йоги?</span>',
            1,
        )
        page = page.replace(
            'Преподаватель встречает учеников перед началом занятия в студии йоги',
            'Преподаватель йоги объясняет задание группе',
            1,
        )
        ticket = re.search(r"^      <figcaption class=\"intro-offer\".*?</figcaption>\n", page, re.S | re.M)
        if not ticket:
            raise ValueError("The quiz intro offer could not be located")
        page = page[:ticket.start()] + page[ticket.end():]
        offer = ticket.group().replace("figcaption", "div")
        page = page.replace('      <button class="solid start-btn"', offer + '      <button class="solid start-btn"', 1)

    return page.replace(
        "<!doctype html>",
        "<!doctype html>\n<!-- Generated from the original quiz by designs/build.py. -->",
        1,
    )


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    for slug, (name, color) in THEMES.items():
        if not (DESIGNS / f"{slug}.css").is_file():
            raise FileNotFoundError(f"Missing stylesheet for {slug}")
        folder = DESIGNS / slug
        folder.mkdir(exist_ok=True)
        page = render_variant(source, slug, name, color)
        (folder / "index.html").write_text(page, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
