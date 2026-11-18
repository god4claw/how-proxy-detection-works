# §16. Headless-артефакты вне сети

<sub>[Главная](../../README.md) · [Часть 5](README.md) · [← §15](15-http3-quic.md) · [Оглавление](../README.md)</sub>

Сеть — только один слой. Если браузер headless или им управляет автоматизация, профиль проигрывает ещё до того, как сайт посмотрит на TTL. Именно поэтому антипример в [§11](../4-checks/11-stands.md) — «худший случай»: там UA подменён, но сам браузер не тот.

## Сначала важная оговорка: headless больше не один

- **Старый headless** — отдельный бинарник `chrome-headless-shell` (выделен в Chrome 132): обрезанные кодеки, шрифты, плагины, поведение, отличное от обычного Chrome.
- **Новый headless** (Chrome 112+) — это тот же браузер, который создаёт невидимые окна; официально «no limitations», и по JS/сети он куда ближе к обычному Chrome.
- **Автоматизация** (Puppeteer/Playwright/CDP) может быть и в headful-режиме — и тогда артефакты автоматизации есть, а «headless» нет.

Поэтому «headless = detected» — такое же упрощение, как «TTL = Windows». Смотреть надо на конкретные артефакты.

## Артефакты, которые видит JS

| Артефакт | Что означает | Насколько надёжен |
|---|---|---|
| `navigator.webdriver === true` | Chrome ставит его при `--enable-automation`, `--headless` и `--remote-debugging-port=0` | **сильный**: спецификация, один бит |
| `HeadlessChrome` в UA | старый headless добавляет префикс в product token | сильный, но легко подменяется |
| `window.chrome` / `chrome.runtime` | в старом headless и shell части API отсутствуют | средний, зависит от сборки |
| `navigator.plugins.length === 0` | по спецификации при поддержке inline PDF их должно быть 5 | средний: зависит от сборки/настроек |
| `WebGL` vendor/renderer | `Google SwiftShader`/software-рендер выдают отсутствие GPU | средний: бывает и на живых VM |
| `Notification.permission === "denied"` при `permissions.query()` → `prompt` | классическое расхождение старого headless | средний (описано Intoli ещё в 2018) |
| `window.outerWidth/outerHeight === 0` | у невидимого окна нет геометрии | эмпирический, не задокументирован |
| `Intl`/TZ/locale по умолчанию `UTC`/`en-US` | контейнер не наследует локаль хоста | эмпирический |
| Кодеки/шрифты | shell не содержит часть проприетарных кодеков и шрифтов | эмпирический, для shell |
| Поведение ввода | нет реальной мыши/клавиатуры, тайминги «идеальные» | эмпирический, но сильный в сумме |

Источники по каждому пункту — внизу; пункты, помеченные «эмпирический», официальной документации не имеют и в разных сборках ведут себя по-разному. Это важно: тесты на headless устаревают вместе с Chrome.

## CDP и следы автоматизации

Когда браузером управляют через DevTools Protocol, появляются косвенные следы: включение домена `Runtime` меняет поведение некоторых JS-механизмов, `ChromeDriver` оставляет переменные вида `cdc_…`, Puppeteer/Playwright добавляют свои объекты. Это гонка вооружений: конкретные имена меняются, но сам факт «браузером управляют» часто виден по совокупности.

Практический вывод: **не полагайтесь на «stealth-плагины» как на решение**. Они чинят отдельные проверки, но не делают профиль согласованным: сеть, TLS, CH и поведение всё равно должны сходиться ([§13](../4-checks/13-tuning.md)).

## Почему это важно для разбора сети

Антипример в [§11](../4-checks/11-stands.md) снят headless-браузером на Linux с UA-подменой на Windows. Он честно показывает расхождение **сетевого** слоя, но не доказывает, что «антифрод поймал прокси по p0f»: такой же расхождение даст UA-подмена на Linux без прокси. Headless-артефакты — вторая причина, по которой этот профиль не жилец.

Правильный тест — **headful-браузер на самом exit-хосте** (или на машине, чей стек вы честно реплицируете), с реальным профилем и без автоматизации. Тогда `/tcp`, `/tls`, `/client-hints` и `/webrtc` показывают то, что увидит сайт, а не то, что вы ему рассказали.

## Мини-чек-лист

1. `navigator.webdriver` — `false`.
2. UA и Client Hints согласованы, версия одна и та же ([§7](../3-browser/07-browser-layer.md)).
3. `WebGL` vendor/renderer — не SwiftShader/software (или объяснимо).
4. `navigator.plugins`, `languages`, `Intl` — как у живой системы.
5. `Notification.permission` и `permissions.query()` не противоречат друг другу.
6. Геометрия окна (`outerWidth/Height`, `screen`) — ненулевая и правдоподобная.
7. Нет CDP-следов (по крайней мере очевидных).
8. Поведение ввода и тайминги — не «идеальные».
9. Тест из-под прокси на exit-машине, а не с dev-хоста.

---

### Источники

- Chrome — [Headless mode](https://developer.chrome.com/docs/automation-and-testing/headless), [Headless shell](https://developer.chrome.com/docs/automation-and-testing/headless-chrome-shell); Puppeteer — [Headless modes](https://pptr.dev/guides/headless-modes).
- MDN — [`navigator.webdriver`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/webdriver), [`navigator.plugins`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/plugins), [`Notification.permission`](https://developer.mozilla.org/en-US/docs/Web/API/Notification/permission_static), [`WEBGL_debug_renderer_info`](https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_debug_renderer_info), [`window.outerWidth`](https://developer.mozilla.org/en-US/docs/Web/API/Window/outerWidth).
- Intoli — [Detecting Chrome headless](https://intoli.com/blog/not-possible-to-block-chrome-headless/) (канонический список проверок 2018 года, часть уже неактуальна).

---

<sub>[← §15](15-http3-quic.md) · [Оглавление](../README.md) · [Источники →](../references.md)</sub>
