# Сверка kilogram-site перед релизом

Подготовка: 16 сентября 2026 года. Проверки завершены 17 сентября 2026 года
(Asia/Yekaterinburg). Документы ещё не утверждены владельцем и не опубликованы.

Проверен текущий Kilogram, commit `66378dc3785545c7cb5e861b3d2f1e9c02e53794`.
Оба рабочих дерева были чистыми до начала. Изменён только kilogram-site;
iOS-код, базы, entitlements, покупки и `PaywallLegalConfiguration.json` не изменялись.
Сборка и тесты iOS не запускались: задача меняет только статический сайт.

## Основания существенных утверждений

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
- `Prepared: September 16, 2026` — фиксированная дата подготовки, не дата вступления
  условий в силу. JavaScript изменяет только год copyright, имеющий HTML fallback.

## Проверки

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

## Проверка производного OFF-пакета

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

## Решения владельца до публикации

1. Подтвердить фактические правила обработки поддержки: Gmail, использование писем
   для ответа и расследования обращений, отсутствие подписки на рассылку, хранение
   только необходимое время и исполнение запросов доступа/исправления/удаления.
   Это обязательства из подготовленной Privacy Policy, которые нельзя доказать кодом.
   Если практика отличается, сначала исправить соответствующие абзацы.
2. Закрыть вопросы происхождения и прав: разделение исходного импорта/обработки OFF
   от остальных источников и согласование EULA с открытыми лицензиями уже отмечены
   в `Kilogram/RELEASE_CHECKLIST.md`. Дополнительно подтвердить допустимость использования
   справочных материалов собственного каталога. Сайт сохраняет права открытых лицензий
   и не объявляет эти вопросы автоматически решёнными.
3. Проверить в App Store Connect фактическую настройку трёх продуктов Pro и
   применение Standard EULA. В исходниках подтверждена модель, но не опубликованные
   предложения/цены/доступность продуктов. Локальный `.storekit` этого не доказывает.

Название разработчика, email, дата USDA и описание ручного составления каталога
уже предоставлены владельцем; повторное подтверждение этих сведений не запрашивается.
Не добавлены вымышленные адрес, компания, представитель, возрастной порог или сертификат.
После одобрения документов владелец отдельно выбирает дату утверждения и публикацию.

Текущая iOS-конфигурация по-прежнему содержит `privacyPolicyURL: null`,
`termsOfUseURL: null`, `documentsApproved: false`. Настройка URL, включение флага,
проверки реального HealthKit на устройстве и выпуск приложения — отдельные действия;
они не выполнены в этой задаче. Адреса для последующей настройки приведены в README.
