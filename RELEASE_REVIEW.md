# Сверка kilogram-site перед релизом

Первоначальная подготовка: 16 сентября 2026 года; исходные проверки завершены
17 сентября 2026 года (Asia/Yekaterinburg). Дополнение по Apple reports и текущей
legal-конфигурации: 17 сентября 2026 года.

## Согласование веб-иконки и валидатора — 20 сентября 2026 года

Коммит `77d7b9057e720f16d427f1c58ecb25f915ce3f63` от 19 сентября
(«Уменьшена иконка приложения») намеренно заменил PNG 1024×1024
на веб-ресурс 128×128, сократив размер с 1 910 832 до 41 966 байт.
Проверка продолжала требовать прежнее разрешение. Исправлен её контракт:
128×128, 8 бит на канал, RGBA; неполный или неверный PNG-заголовок теперь
выдаёт понятную ошибку. Сравнение с эталоном через `--icon-source` сохранено.

PNG оставлен побайтно неизменным. Текущий SHA-256:

```text
e2ee56e3f7d1bb7042368aedb42d20a2c0547cc60d2839b23178477cf373e533
```

Оригинал 1024×1024 доступен в истории Git до `77d7b90`; сведения об оригинале
в разделе первоначальных проверок ниже относятся к той версии. README обновлён
для текущего веб-ресурса. HTML, CSS, EN/RU, публичные адреса, юридические тексты,
даты документов, условия покупок, права и источники данных не изменены.

Проверки этого изменения:

- `python3 scripts/check_site.py` — PASS, 13 HTML-страниц, 16 локальных целей.
- `python3 -m unittest discover -s scripts -p 'test_*.py' -v` — PASS, 14 тестов,
  включая 9 прежних проверок локализации и 5 проверок контракта иконки.
- Локальный `scripts/serve.py --port 8000` и проверка `--http http://127.0.0.1:8000` —
  PASS под `/kilogram-site/`, включая двуязычный HTTP 404 на вложенном русском пути.
- Все 39 ссылок на иконку (изображение, favicon, apple-touch-icon на 13 страницах)
  разрешаются в `https://rinatabidullin.github.io/kilogram-site/assets/kilogram-app-icon.png`.
- Headless Chrome 153.0.8010.48 — PASS, 208 сценариев: 12 страниц EN/RU и вложенная
  404 × 320/1280 px × светлая/тёмная тема × JS on/off × текст 100/200%.
  Увеличение текста эмулировано удвоением вычисленных размеров шрифта.
  При 320 px использовалась плотность 3×, при 1280 px — 2×.
  PNG загружается как 128×128; HTML width/height и фактический размер — 40×40,
  `object-fit: contain`. Растяжения пропорций, увеличения растра при этих плотностях
  и горизонтального переполнения не обнаружено.
- Tab, видимый фокус и Enter на skip-link — PASS во всех 208 сценариях.
  Отдельно без JS проверены переключение EN → RU на `/support/`, переход внутри RU
  на `/privacy/`, перезагрузка вложенных страниц, переключение обратно в EN
  и возврат на русскую главную с вложенной 404 с помощью клавиатуры.
- Визуально просмотрены четыре скриншота: EN/RU главные на 320 px в светлой/тёмной
  темах, английская Privacy на 1280 px в тёмной теме и русская Support на 1280 px
  в светлой теме с текстом 200%. Иконка видна целиком, пропорции сохранены.
- `git diff --check` — PASS.

Скрипт браузерной проверки, результаты JSON и скриншоты сохранены локально
в `/private/tmp/kilogram-site-icon-check-20260920/`, вне репозитория.
Retina проверена эмуляцией плотности в Chrome; Safari на физическом iPhone и
создаваемый ОС значок apple-touch-icon не проверялись. Новых зависимостей нет.
Push и deploy не выполнялись. Внешние ссылки только перечислены валидатором;
доступность опубликованной версии и внешних сервисов в этой задаче не проверялась.

## Актуальное состояние на 17 сентября 2026 года

Для этого обновления прочитан Kilogram на commit `2af9e91dfef20d146c76a3a8401523b1f5621dcc`.
Источники относительно корня iOS-проекта: `Documentation/AppStorePrivacyAnswers.md`,
`Documentation/ReleaseDocumentationSync.md`, `Documentation/LegalPrivacyVerification.md`,
`Kilogram/Resources/PaywallLegalConfiguration.json` и
`Kilogram/Application/Configuration/PaywallLegalConfiguration.swift`.
Последний commit актуализирует release-документацию; более новой формулировки Apple reports
в текущем рабочем дереве не найдено.

Privacy Policy, Terms и правила Gmail-поддержки ранее утверждены владельцем, что зафиксировано
в `LegalPrivacyVerification.md`. Доступность опубликованных документов подтверждена
в `ReleaseDocumentationSync.md`; это результат предыдущей проверки iOS-проекта.
Новое уточнение Privacy Policy в этой задаче подготовлено локально; push и deploy не выполнялись.

| Параметр | Подтверждённое состояние |
| --- | --- |
| `privacyPolicyURL` | `https://rinatabidullin.github.io/kilogram-site/privacy/` |
| `termsOfUseURL` | `https://www.apple.com/legal/internet-services/itunes/dev/stdeula/` — Apple Standard EULA |
| `supportURL` | `https://rinatabidullin.github.io/kilogram-site/support/` |
| `documentsApproved` | `true` |
| `isReadyForCheckout` | `true`: документы утверждены и оба обязательных HTTPS URL валидны |

Legal-конфигурация больше не блокирует checkout. Остальные проверки StoreKit сохранены;
наличие реальных продуктов, покупки/Restore через Apple и прохождение App Store Review
этим не подтверждаются. `/terms/` остаётся страницей дополнительных условий Pro,
а Terms of Use в приложении ведёт на Apple Standard EULA.

В `privacy/index.html` после абзаца об отсутствии сторонних advertising/tracking/analytics SDK
добавлен текст из `ReleaseDocumentationSync.md`: разработчик использует aggregate usage reports
Apple App Analytics для понимания использования и улучшения функций, а crash/performance reports
Apple — для диагностики сбоев, повышения надёжности и производительности. Доступность зависит
от сервисов Apple и sharing settings. Отчёты не используются для рекламы или tracking;
это не автоматическая отправка дневника или локальных diagnostic files разработчику.
Прежняя условная формулировка об Apple заменена этим явным описанием; добровольная отправка
диагностики в поддержку сохранена отдельным абзацем. `Prepared` обновлён на 17 сентября.

Сверены все разделы Privacy Policy: локальное хранение, HealthKit, diagnostics, support,
exports, покупки, tracking и реклама. Противоречий с новым описанием Apple reports не найдено.
На `/support/`, `/terms/`, `/data-sources/` и `/licenses/` очевидных устаревших плейсхолдеров
или противоречий не найдено; эти страницы не изменены. README больше не предлагает
повторно настроить legal URLs, подтвердить документы или настроить уже работающий Pages.

Оба рабочих дерева были чистыми до начала обновления. Изменён только kilogram-site;
iOS-проект использован только для чтения. Сборка и тесты iOS не запускались.

Проверки этого обновления:

| Проверка | Результат |
| --- | --- |
| `python3 scripts/check_site.py` | PASS: 7 HTML-страниц, 10 локальных targets; ссылки, фрагменты, mailto, assets, PNG и отсутствие плейсхолдеров |
| `python3 scripts/serve.py --port 8000` и `python3 scripts/check_site.py --http http://127.0.0.1:8000` | PASS: локальный preview запущен, все страницы и ресурсы возвращают HTTP 200 |
| `git diff --check` | PASS |
| `git -C ../Kilogram status --porcelain=v1` и `rev-parse HEAD` | Чистое рабочее дерево, исходный commit `2af9e91dfef20d146c76a3a8401523b1f5621dcc`; iOS не изменён |

Внешние URL перечислены валидатором, но повторно по сети не проверялись.
Проверка опубликованного обновления остаётся шагом после отдельного deploy.

## Основания исходной проверки сайта

Первоначальная проверка ниже относится к Kilogram на commit
`66378dc3785545c7cb5e861b3d2f1e9c02e53794`, до подключения legal URLs.
Актуальное состояние конфигурации приведено выше.

Пути относительно соседнего репозитория Kilogram. Production-код — основной источник;
roadmap и `.storekit` не подтверждают выпущенные функции или предложения магазина.

| Утверждение в документах | Файл / символ |
| --- | --- |
| Дневник и каталоги локальные, отдельная пользовательская SQLite | `Kilogram/Application/AppDependencyFactory.swift`, `prepareStorage`, `makeDependencies`; `Kilogram/Data/Repositories/ProductRepository.swift` |
| Возраст, пол, рост, вес, активность калькулятора сохраняются локально | `Kilogram/Data/Repositories/GoalCalculatorPreferencesRepository.swift`, `load`, `save` |
| Три поставляемых каталога OFF, USDA, Kilogram | `Kilogram/Application/Configuration/ProductCatalogConfiguration.swift`, `bundled`; ресурсы `Kilogram.xcodeproj/project.pbxproj` |
| Версия OFF и текущая ссылка Google Drive | `Kilogram/Application/Configuration/DataSourcesConfiguration.swift`, `live`; `Artifacts/OFF/CATALOG_METADATA.json`, `manifest.json`; `DB/offdb.sqlite3`, `catalog_metadata` |
| HealthKit: запись четырёх показателей без общего чтения чужих данных | `Kilogram/Data/HealthKit/HealthKitNutritionStore.swift`, `requestWriteAuthorization` (`read: []`); `HealthKitNutritionObjectFactory.makeSample` |
| Чтение/обновление/удаление собственных объектов, включая прежний app source FoodDiary | `HealthKitNutritionStore.readOwn`, `ownDayObjects`, `deleteDayObjects`, `ownPredicate`; ограничение `HKSource.default()` |
| Включение и повторное включение обрабатывают всю историю, включая будущие записи | `Kilogram/Domain/UseCases/HealthKitNutritionSyncCoordinator.swift`, `setAutomatic`; `Kilogram/Data/Database/DiaryDatabase+HealthKitDaySync.swift`, `enqueueAllHealthKitDays`; временные отметки фабрики объектов |
| Выключение передачи не удаляет записи Health; фоновая передача не гарантируется | `HealthKitNutritionSyncCoordinator.setAutomatic`, `setRuntimeAvailable`; выключение отменяет задачи и меняет настройку |
| Локальные копии миграции, техническая история, диагностика | `Kilogram/Data/LegacyMigration/LegacyFoodDiaryBackupService.swift`, `createBackup`; `LegacyMigrationDiagnosticReportWriter.swift`; `Kilogram/Data/Repositories/HealthKitDiagnosticsRepository.swift`; `DiaryDatabase+DataChanges.swift` |
| Widget App Group, snapshot исключён из backup | `WidgetShared/Storage/WidgetSnapshotFileStore.swift`, `appGroup`, `write`; `Kilogram/Kilogram.entitlements`; `widget.privacy.*` в `Localizable.xcstrings` |
| CSV/JSON бесплатно, PDF требует Pro; импорт и полное восстановление не реализованы | `Kilogram/Domain/Models/FeatureAccess/ProFeature.swift`, `requiresPro`; `Kilogram/Data/Export/ExportFileStore.swift`, `writeRaw`, `readme`; `Kilogram/Presentation/Export/ExportView.swift` |
| Временные экспорты удаляются при release; оставшиеся старше 24 часов — при maintenance | `ExportFileStore.release`, `maintenance`; `ExportFileProtection.apply` исключает их из backup |
| Monthly / Annual — месяц / год, Lifetime — non-consumable | `Kilogram/Domain/Models/Purchases/StoreProductIdentifiers.swift`; `ProProductCatalog.validates`; `Kilogram/Data/StoreKit/StoreKitPurchaseClient.swift` |
| Прежняя FoodDiary Pro / Remove Ads даёт Lifetime при допустимой покупке; local fallback не гарантирует перенос | `ProProductCatalog.plan`, `ProEntitlement.verifiedLifetimeProductIDs`, `source`; `Kilogram/Domain/UseCases/PurchaseInteractor.swift`, `refreshEntitlement`, `blockFallback`; `StoreKitPurchaseClient.restorePurchases` |
| Названия путей поддержки | `Kilogram/Presentation/Settings/Views/SettingsView.swift`, `Presentation/HealthKit/Views/HealthKitSettingsView.swift`, `Presentation/Export/ExportView.swift`, `Localizable.xcstrings` |

Поиск сетевого кода, импортов, SDK, ресурсов, project.pbxproj и entitlements не выявил
собственного backend, аккаунтов, CloudKit/iCloud sync, сторонней аналитики или рекламы.
`NetworkAvailabilityRepository` использует `NWPathMonitor` для доступности сети;
покупки обращаются к Apple через StoreKit. Внешние сайты открываются явным действием.
Это вывод по проверенной версии исходников, а не утверждение о настройках Apple или Gmail.

## Зависимости и лицензии

Проверены tracked-файлы и bundle-ресурсы приложения и widget extension, импорты Swift,
зависимости и link phases Xcode, возможные manifests/lockfiles, vendored C/Objective-C,
frameworks и лицензионные notices. Дополнительного стороннего кода, требующего
отдельного уведомления, не обнаружено. Используется системный SQLite3 и Apple SDK.
У сайта только собственные HTML/CSS/JS и предоставленная иконка, без CDN и npm.
Системные SDK не представлены как сторонние пакеты; пустая software-секция удалена.

Оставлены ODbL 1.0, DbCL 1.0 и CC0 1.0 со ссылками на точные условия,
атрибуцией и разграничением прав данных, приложения и иконки. Не назначена общая
MIT/ODbL/CC0-лицензия всему приложению или каталогу Kilogram.

Правила данных сверены с [документацией OFF](https://openfoodfacts.github.io/openfoodfacts-server/api/)
и [USDA FoodData Central](https://fdc.nal.usda.gov/). Текст об IP-логах — с
[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection).
Лицензия приложения — ссылка на [Apple Standard EULA](https://www.apple.com/legal/internet-services/itunes/dev/stdeula/),
без копирования полного текста. Сверены официальные страницы Apple об
[отмене](https://support.apple.com/en-us/118428), [возвратах](https://support.apple.com/en-us/118223),
[подписках](https://developer.apple.com/app-store/subscriptions/) и
[применении EULA](https://developer.apple.com/help/app-store-connect/manage-app-information/provide-a-custom-license-agreement/).

## Уточнения относительно предоставленной основы

- Существенного противоречия состава каталогов не найдено: Пятёрочка и Жизньмарт
  уже отсутствуют в production-конфигурации поставляемых каталогов. Исторические
  источники в пользовательских данных и миграции не изменялись.
- Вместо неопределённого «экспорт не обязательно является backup» явно указано
  отсутствие импорта и полного восстановления. Отмечены бесплатный CSV/JSON и Pro PDF.
- Уточнены backup-исключения только для файлов, где они реализованы;
  миграционные копии и дневник не объявлены исключёнными из системных backup.
- Уточнены очистка временных экспортов, ограничения удаления всех локальных копий,
  поведение Lock Screen widgets и local fallback старой покупки.
- HealthKit не назван системой без чтения: описано чтение собственных записей,
  повторная обработка истории и отсутствие гарантии непрерывной фоновой передачи.
- OFF содержит обработанные и усреднённые данные, не точные копии этикеток. Дата
  исходного снимка неизвестна; дата подготовки пакета не выдана за эту дату.
  Фотографий в схеме/пакете нет. Иконка не связана с лицензией изображений OFF.
- USDA: дата 10 октября 2023 года сохранена именно как предоставленная разработчиком.
- `Prepared` — фиксированная дата подготовки версии, не дата вступления условий в силу.
  В исходной версии это `September 16, 2026`; Privacy Policy теперь датирована
  `September 17, 2026`. JavaScript изменяет только год copyright, имеющий HTML fallback.

## Проверки исходной версии сайта

Ниже сохранены результаты первоначальной проверки. Они не означают повторного выполнения
всей браузерной матрицы и проверки внешних URL после уточнения Apple reports.

| Проверка | Результат |
| --- | --- |
| `python3 scripts/check_site.py` | PASS: 7 страниц, 10 локальных targets, фрагменты, mailto, assets, отсутствие плейсхолдеров и редакторских инструкций |
| `python3 scripts/check_site.py --http http://127.0.0.1:8000` | PASS: прямые адреса с `/kilogram-site/`, все локальные HTTP responses 200 |
| Оригинал и `assets/kilogram-app-icon.png` | Побайтно равны; 1024×1024 RGBA, alpha сохранена |
| Headless Google Chrome / доступный Playwright вне репозитория | PASS: 112 случаев — 7 страниц × 2 темы × 320/1280 px × JS on/off × текст 100/200% |
| Браузер: прямой переход и reload, overflow, загрузка PNG | PASS; горизонтального скролла нет, object-fit contain, border-radius 0 |
| Tab / видимый focus / Enter на Skip to content | PASS на всех страницах, focus переходит в main; ошибки JS и внешние автоматические requests отсутствуют |
| Последовательный Tab по всем ссылкам при 320/1280 px | PASS: 274 перехода, видимый outline и прокрутка к ссылке; проверка ждёт завершения плавной прокрутки |
| Вложенный отсутствующий URL | HTTP 404, рабочие иконка/CSS и кнопка возврата; также без JS |
| Визуальная проверка скриншотов | Просмотрены узкая светлая главная и широкая тёмная Privacy; иконка видна целиком |
| 12 внешних URL из HTML | Все ответили HTTP 200 без авторизации; непроверенных внешних адресов из HTML не осталось |
| `git diff --check` | PASS |
| Состояние Kilogram после работы | Чистое рабочее дерево, тот же commit; iOS не изменён |

Проверки не являются полным аудитом доступности или тестом Safari на физическом iPhone.
Браузерные результаты и скриншоты находятся в локальном `/tmp/kilogram-site-checks/`;
они не добавлены в Git и могут исчезнуть при очистке временных файлов.
Новые зависимости в проект не устанавливались.

У 404 намеренно абсолютные production URL: GitHub отдаёт его на произвольной глубине.
Локальный сервер при отдаче 404 меняет production адрес на preview адрес.
Проверка реального GitHub Pages после публикации остаётся отдельным шагом.

## Исходная проверка производного OFF-пакета

[Публичная страница файла](https://drive.google.com/file/d/1NzUM6jaEcSZrMdNPCFFt3goFEkJGOzcD)
без входа показала `kilogram-off-data-1848f4170a38b9c2.zip`.
После стандартного предупреждения Google о размере архива скачан сам ZIP,
52 473 789 байт, HTTP 200, без авторизации. Он находится только во временной папке.

SHA-256 скачанного ZIP совпал с локальным релизным ZIP:

```text
b7be449d690318c38b5ea652292f279c977e97a50214577994f4f622606e1a81
```

Прочитаны все элементы локального ZIP, CRC без ошибок. Metadata внутри архива,
`Artifacts/OFF/CATALOG_METADATA.json` и публикационные поля `catalog_metadata`
в текущей `DB/offdb.sqlite3` совпали. База внутри ZIP и база проекта имеют один SHA-256:

```text
7a8913b819ae6a62866b4b94eb57ace74e22885d69b4d9d224fb5af3a5841cad
```

Архив содержит только OFF SQLite, metadata, schema, manifest, validation, checksum и notices.
Фотографии, пользовательские дневники, другие каталоги и исходники в нём отсутствуют.
Равенство байтов подтверждает доступный пакет, но не историю исходного импорта,
права на другие каталоги или точность каждого продукта.

SHA-256 иконки:

```text
71926ac33f0ae1de3bb7f5c72fad668ae072c0c34060b30462b275fc413f05d8
```

## Подтверждённые решения и оставшиеся ручные шаги

Правила поддержки уже подтверждены владельцем: Gmail, ответы и расследование обращений,
отсутствие рассылок, необходимый срок хранения и исполнение запросов доступа/исправления/удаления.
Основание — `Documentation/LegalPrivacyVerification.md` проекта Kilogram.
Повторное утверждение документов и включение `documentsApproved` не требуются.

1. Перед публикацией сверить поля реально используемых Apple reports, как указано в
   `Documentation/AppStorePrivacyAnswers.md`. Политика не объявляет все отчёты анонимными
   или безусловно не связанными с устройствами. Если практика отличается от описания,
   согласовать текст и App Privacy; изменения iOS/магазина выполняются отдельно.
2. Закрыть вопросы происхождения и прав: разделение исходного импорта/обработки OFF
   от остальных источников и согласование EULA с открытыми лицензиями уже отмечены
   в `Kilogram/RELEASE_CHECKLIST.md`. Дополнительно подтвердить допустимость использования
   справочных материалов собственного каталога. Сайт сохраняет права открытых лицензий
   и не объявляет эти вопросы автоматически решёнными.
3. Проверить в App Store Connect фактическую настройку трёх продуктов Pro и
   применение Standard EULA. В исходниках подтверждена модель, но не опубликованные
   предложения/цены/доступность продуктов. Локальный `.storekit` этого не доказывает.
4. Опубликовать обновление сайта отдельным действием; затем проверить новый текст Privacy Policy,
   ссылки и страницы без авторизации. Проверить Privacy Policy / Support URL в App Store Connect.
   Адреса и порядок публикации приведены в README.

Название разработчика, email, дата USDA и описание ручного составления каталога
уже предоставлены владельцем; повторное подтверждение этих сведений не запрашивается.
Не добавлены вымышленные адрес, компания, представитель, возрастной порог или сертификат.
Проверки реального HealthKit на устройстве и полный checklist выпуска остаются
в release-документации Kilogram; эта задача их не выполняет и не закрывает.
