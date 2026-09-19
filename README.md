# Kilogram website

Статический сайт Рината Абидуллина на английском и русском: HTML, CSS и небольшой JavaScript
только для года copyright. Документы, контакты и навигация доступны без JavaScript.
Сборка, npm, фреймворки, внешние шрифты и серверная обработка данных не нужны.

Документы первоначально подготовлены 16 сентября 2026 года. Текущая версия Privacy Policy
датирована 19 сентября 2026 года. Русские переводы сохраняют даты исходного содержания.
`Prepared` обозначает дату подготовки версии документа, а не вступление условий в силу.
Privacy Policy, Terms и правила поддержки ранее утверждены владельцем; legal URLs в iOS
настроены, `documentsApproved = true`. Основания — в [RELEASE_REVIEW.md](RELEASE_REVIEW.md).
Текущее обновление локальное: push и публикация этой версии не выполнялись.

## Языковые версии

Английские страницы остаются в корне, русские размещены в `ru/` с теми же маршрутами:
главная, `privacy/`, `terms/`, `support/`, `data-sources/` и `licenses/`.
Переключатель English / Русский открывает перевод текущей страницы; остальные ссылки
сохраняют язык. Переключение работает без JavaScript и автоматических перенаправлений.
У каждой версии есть собственный canonical и взаимные hreflang-ссылки.
Общая `404.html` содержит сообщение и ссылки для обоих языков.

Правила синхронного обновления переводов находятся в [AGENTS.md](AGENTS.md).
Маршруты и языки перечислены в `scripts/site_config.py`; этот список используют
preview-сервер и валидатор. Новые страницы добавляйте сразу для всех языков.

## Локальная проверка

Из корня репозитория, Python 3.9 или новее:

```sh
python3 scripts/check_site.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/serve.py --port 8000
```

Открыть [английский сайт](http://127.0.0.1:8000/kilogram-site/)
или [русский сайт](http://127.0.0.1:8000/kilogram-site/ru/).
В другом терминале:

```sh
python3 scripts/check_site.py --http http://127.0.0.1:8000
git diff --check
```

Скрипт проверяет 13 HTML-страниц, локальные ссылки, фрагменты, mailto, assets,
плейсхолдеры и параметры PNG. Также проверяются полнота языковых пар, `lang`,
canonical, hreflang, переключатели, сохранение языка в навигации, структура разделов,
даты документов и соответствие ссылок в содержимом переводов. Незарегистрированные
HTML-страницы считаются ошибкой. Смысл переводов нужно проверять вручную.
Режим `--http` дополнительно проверяет двуязычные ответы 404 на вложенных путях.
`--icon-source /path/to/original.png` дополнительно
сравнивает иконку побайтно с оригиналом. Список внешних URL в выводе —
инвентаризация; их доступность нужно проверять отдельно без авторизации.

В браузере проверить все страницы при ширине 320 px и на широком экране,
обе темы, увеличение текста до 200%, Tab/Enter и отключённый JavaScript.
Обновление вложенных страниц и переход на несуществующий путь должны работать.

Preview-сервер обслуживает только публичные страницы и assets под `/kilogram-site/`.
На неизвестных путях он возвращает HTTP 404 с `404.html`.
В исходном `404.html` используются полные адреса GitHub Pages, чтобы CSS, иконка
и переход домой работали на любой глубине отсутствующего URL без JS.
Только при локальной отдаче 404 сервер заменяет этот адрес на localhost.
На остальных страницах навигация и ресурсы используют относительные ссылки,
а SEO-метаданные — полные публичные адреса; `<base>` не используется.

## Адреса для приложения и App Store Connect

| Назначение | Публичный адрес |
| --- | --- |
| Privacy Policy | https://rinatabidullin.github.io/kilogram-site/privacy/ |
| Support | https://rinatabidullin.github.io/kilogram-site/support/ |
| Marketing | https://rinatabidullin.github.io/kilogram-site/ |
| Terms page | https://rinatabidullin.github.io/kilogram-site/terms/ |
| Apple Standard EULA | https://www.apple.com/legal/internet-services/itunes/dev/stdeula/ |
| Data sources | https://rinatabidullin.github.io/kilogram-site/data-sources/ |
| Licenses | https://rinatabidullin.github.io/kilogram-site/licenses/ |

Контакт поддержки и приватности: [rinatabidullin@gmail.com](mailto:rinatabidullin@gmail.com).

Русская главная: https://rinatabidullin.github.io/kilogram-site/ru/.
Русские документы доступны по тем же путям внутри `ru/`, например
https://rinatabidullin.github.io/kilogram-site/ru/privacy/ и
https://rinatabidullin.github.io/kilogram-site/ru/support/.

## Публикация владельцем

1. Проверить diff и локальную валидацию. Поддерживать документы в соответствии
   с фактическим поведением приложения и практикой разработчика; при изменении текста
   обновлять `Prepared` / «Дата подготовки» у изменённых документов во всех языках.
   При правке только перевода, навигации или оформления сохранять дату содержания.
2. Закоммитить и отправить проверенные изменения
   в [rinatabidullin/kilogram-site](https://github.com/rinatabidullin/kilogram-site),
   затем дождаться GitHub Pages deployment. Сохранить `.nojekyll`.
3. После deployment открыть адреса выше в приватном браузере без авторизации:
   проверить новый текст Privacy Policy, навигацию, вложенные 404 и скачивание OFF-пакета
   без входа в Google.
4. Использовать Privacy Policy / Support URL выше в App Store Connect и проверить
   соответствующие поля магазина. Повторная настройка legal URLs или `documentsApproved`
   в iOS не требуется. Полный checklist выпуска ведётся в проекте Kilogram.

При обновлении OFF брать URL и версию из актуального `DataSourcesConfiguration.live`,
сверять метаданные и скачанный ZIP. SQLite и ZIP не хранить в репозитории сайта.
Исходная иконка `assets/kilogram-app-icon.png` — неизменённый PNG 1024×1024 с alpha;
её также используют favicon и apple-touch-icon.
