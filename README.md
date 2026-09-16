# Kilogram website

Статический английский сайт Rinat Abidullin: HTML, CSS и небольшой JavaScript
только для года copyright. Документы, контакты и навигация доступны без JavaScript.
Сборка, npm, фреймворки, внешние шрифты и серверная обработка данных не нужны.

Документы подготовлены 16 сентября 2026 года по текущему коду Kilogram.
`Prepared` обозначает дату подготовки, а не утверждение или вступление условий в силу.
Результаты сверки и решения владельца — в [RELEASE_REVIEW.md](RELEASE_REVIEW.md).
Изменения локальные: push и публикация не выполнялись.

## Локальная проверка

Из корня репозитория, Python 3.9 или новее:

```sh
python3 scripts/check_site.py
python3 scripts/serve.py --port 8000
```

Открыть [локальный сайт](http://127.0.0.1:8000/kilogram-site/).
В другом терминале:

```sh
python3 scripts/check_site.py --http http://127.0.0.1:8000
git diff --check
```

Скрипт проверяет семь HTML-страниц, локальные ссылки, фрагменты, mailto, assets,
плейсхолдеры и параметры PNG. `--icon-source /path/to/original.png` дополнительно
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
Остальные страницы используют относительные ссылки; `<base>` не используется.

## Адреса для приложения и App Store Connect

| Назначение | Адрес после публикации |
| --- | --- |
| Privacy Policy | https://rinatabidullin.github.io/kilogram-site/privacy/ |
| Support | https://rinatabidullin.github.io/kilogram-site/support/ |
| Marketing | https://rinatabidullin.github.io/kilogram-site/ |
| Terms page | https://rinatabidullin.github.io/kilogram-site/terms/ |
| Apple Standard EULA | https://www.apple.com/legal/internet-services/itunes/dev/stdeula/ |
| Data sources | https://rinatabidullin.github.io/kilogram-site/data-sources/ |
| Licenses | https://rinatabidullin.github.io/kilogram-site/licenses/ |

Контакт поддержки и приватности: [rinatabidullin@gmail.com](mailto:rinatabidullin@gmail.com).

## Публикация владельцем

1. Проверить diff, отчёт и принять обязательства документов; при изменении текста
   явно обновить дату подготовки/утверждения. Проверить фактические настройки продуктов
   и лицензии приложения в App Store Connect.
2. Самостоятельно закоммитить и отправить одобренные изменения
   в [rinatabidullin/kilogram-site](https://github.com/rinatabidullin/kilogram-site).
3. В GitHub Settings → Pages выбрать Deploy from a branch, нужную опубликованную ветку
   и `/(root)`. Сохранить `.nojekyll`. Не запускать публикацию до одобрения документов.
4. После успешного Pages deployment открыть адреса выше, проверить реальные
   вложенные 404 и скачивание OFF-пакета без входа в Google.
5. Отдельно настроить URL в iOS/App Store Connect и утвердить `documentsApproved`.
   Эта задача не изменяет iOS-проект или настройки магазина.

При обновлении OFF брать URL и версию из актуального `DataSourcesConfiguration.live`,
сверять метаданные и скачанный ZIP. SQLite и ZIP не хранить в репозитории сайта.
Исходная иконка `assets/kilogram-app-icon.png` — неизменённый PNG 1024×1024 с alpha;
её также используют favicon и apple-touch-icon.
