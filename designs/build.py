from pathlib import Path
import re


DESIGNS = Path(__file__).resolve().parent
SOURCE = DESIGNS.parent / "index.html"
THEMES = {
    "zen": ("Тихая практика", "#f5f2e9"),
    "apple": ("Студия", "#f5f5f7"),
    "edtech": ("Учебная платформа", "#f4f7fc"),
    "impact": ("Пульс", "#151610"),
    "editorial": ("Журнал", "#f4eee2"),
    "arcade": ("Аркада", "#0c1528"),
    "pop": ("Поп", "#fff5fa"),
    "atlas": ("Атлас движения", "#11336f"),
    "swiss": ("Швейцарская сетка", "#ffffff"),
    "sunroom": ("Солнечное ретро", "#fff6e7"),
    "foil": ("Голограмма", "#e9e9f7"),
    "ink": ("Тушь и бумага", "#f7f3e9"),
    "ticket": ("Билет на старт", "#2b101f"),
    "live": ("Прямой эфир", "#f6f5f0"),
    "drop": ("Дроп", "#f8f4ff"),
    "premiere": ("Премьера", "#160f0b"),
}

MARKETING = {
    "ticket": ("Ваш билет в новую профессию", "Из практики — <span>в преподавание йоги.</span>", "Получить свой разбор"),
    "live": ("Вы в главной роли на занятии", "Не просто на коврике. <span>Во главе группы.</span>", "Включиться в урок"),
    "drop": ("Новый поворот в вашей практике", "Йога — ваша тема? <span>Дайте ей новый масштаб.</span>", "Проверить себя за 2 минуты"),
    "premiere": ("Ваша новая роль · Академия Йоги", "Ваша практика. <span>Ваша новая роль.</span>", "Начать свою историю"),
}


def render_marketing(page: str, slug: str) -> str:
    """Add campaign interactions only to the four marketing experiments."""
    kicker, heading, cta = MARKETING[slug]
    def replace_once(old: str, new: str) -> None:
        nonlocal page
        if page.count(old) != 1:
            raise ValueError(f"Expected one marketing insertion point: {old[:64]}")
        page = page.replace(old, new, 1)

    timer = '''<div class="offer-timer" data-campaign>
        <span class="timer-label">До конца акции</span>
        <time class="timer-value" data-countdown>До 13 ноября</time>
        <small>До 13 ноября включительно · МСК</small>
      </div>'''
    replace_once(f'<link rel="stylesheet" href="../{slug}.css">',
                 f'<link rel="stylesheet" href="../marketing.css">\n<link rel="stylesheet" href="../{slug}.css">')
    replace_once('<script>\n/* QUIZ_SOURCE_START */', '<script src="../marketing.js"></script>\n<script>\n/* QUIZ_SOURCE_START */')
    replace_once('<p class="kicker">Профпроба Академии Йоги</p>', f'<p class="kicker">{kicker}</p>')
    replace_once('А если йога станет <span>вашей профессией?</span>', heading)
    replace_once('Пройти пробный урок <svg', cta + ' <svg')
    replace_once('<div class="intro-copy">', '''<div class="campaign-ribbon" data-campaign><strong>Чёрная пятница</strong><span>40 000 ₽ на обучение + курс в подарок</span><span class="ribbon-grants">Осталось грантов: <b class="grant-remaining">12 / 50</b></span></div>
    <div class="intro-copy">''')
    replace_once('      <button class="solid start-btn"', '      ' + timer + '\n      <button class="solid start-btn"')
    replace_once('  <div class="layout" id="layout" hidden>', '''  <aside class="quiz-hook" id="quiz-hook" aria-label="Ваш следующий шаг" hidden>
    <span class="hook-index" aria-hidden="true"></span><div><strong class="hook-title"></strong><p class="hook-copy"></p></div>
  </aside>
  <div class="layout" id="layout" hidden>''')
    replace_once('  </div>\n  <aside class="quiz-hook"', '    ' + timer + '\n  </div>\n  <aside class="quiz-hook"')
    replace_once('        <div id="grant-form-home">', '        ' + timer + '\n        <div id="grant-form-home">')
    replace_once('  const GRANTS_TOTAL = 50;', '''  const GRANTS_TOTAL = 50;
  const marketing = typeof window.QuizMarketing === 'function'
    ? window.QuizMarketing({deadline: CAMPAIGN_END, grantsLeft: GRANTS_LEFT, grantsTotal: GRANTS_TOTAL})
    : {render() {}};''')
    replace_once('      if (event) start.focus();', '      marketing.render(step, TOTAL);\n      if (event) start.focus();')
    replace_once('    placeScene();', '    placeScene();\n    marketing.render(step, TOTAL);')
    if slug == "premiere":
        replace_once('src="../../assets/scenes/first-class.webp" width="1080" height="810"',
                     'src="poster.webp" width="1536" height="1024"')
        replace_once('Преподаватель встречает учеников перед началом занятия в студии йоги',
                     'Анимационные персонажи: будущая преподавательница и ученики в залитой золотым светом студии')
    return page


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
    elif slug == "atlas":
        page = page.replace(
            'src="../../assets/scenes/first-class.webp" width="1080" height="810"',
            'src="plate.webp" width="864" height="1080"',
            1,
        )
        page = page.replace(
            'А если йога станет <span>вашей профессией?</span>',
            'Ваш первый <span>урок йоги</span>',
            1,
        )
        page = page.replace(
            'Преподаватель встречает учеников перед началом занятия в студии йоги',
            'Учитель и ученики в студии на иллюстрации в технике цианотипии',
            1,
        )
    elif slug == "ink":
        page = page.replace(
            'src="../../assets/scenes/first-class.webp" width="1080" height="810"',
            'src="wash.webp" width="864" height="1080"',
            1,
        )
        page = page.replace(
            'А если йога станет <span>вашей профессией?</span>',
            'Проведите <span>первый урок йоги</span>',
            1,
        )
        page = page.replace(
            'Преподаватель встречает учеников перед началом занятия в студии йоги',
            'Преподаватель и ученики на рисунке тушью',
            1,
        )
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

    if slug in MARKETING:
        page = render_marketing(page, slug)
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
