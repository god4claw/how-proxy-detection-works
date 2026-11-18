# §12. Где это работает, а где миф

<sub>[Главная](../../README.md) · [Часть 4](README.md) · [← §11](11-stands.md) · [§13. Подгонка стека →](13-tuning.md)</sub>

Глава про сеть — поэтому честно про её место в скоринге.

| Слой | Кто его видит | Роль |
|---|---|---|
| Браузерный: JS, canvas, WebGL, шрифты, UA-CH, тайминги | любой сайт с JS | основной объём решений |
| Репутация IP: ASN, usage type, PTR, списки | любой бэкенд, один API-вызов | высокая и дешёвая |
| Поведение: мышь, ввод, глубина, скорость заполнения | почти все | высокая |
| Сеть: TTL, JA4T, MSS, RTT, джиттер | только тот, кто терминирует TCP | тонкий слой, редко решает в одиночку |
| QUIC/HTTP-3: transport parameters, JA4Q | тот, кто видит UDP | новый слой, пока редко используется в скоринге |
| IPv6: вторая семья адресов | тот, кто видит AAAA/dual-stack | усиливает или ломает картину |

Практические следствия:

- **CDN меняет наблюдателя.** Если сайт за Cloudflare/Akamai/Fastly, TCP-подпись видит CDN, а бэкенд видит уже CDN. На одном периметре exit «невидим», на другом — виден, хотя профиль не менялся. Поэтому «на этом сайте меня не палит» не означает «не палит нигде».
- **JS-сниппет сеть не видит.** Если антифрод встроен как JS/API-скоринг (типичный SaaS), он не читает ни TTL, ни JA4T — для него это просто ещё один IP. Зато он читает Canvas, WebGL, поведение и Client Hints.
- **IP-репутация ≠ сеть.** ipinfo, IPQS, MaxMind, Spur продают метаданные и историю адреса; пакетные пробы — отдельная история и есть не у всех.
- **Порядок работы такой:** сначала браузерный слой, потом репутация, потом сеть. Если у профиля плывёт canvas, подгонка TTL не спасёт — а вот наоборот бывает.
- **Пул важнее подписи.** Плохой пул виден по репутации, скорости и стабильности — это верхние строки таблицы, и они решают больше, чем любая цифра в `/tcp`. Выбор провайдера — в [«Провайдеры и шлюзы»](../1-practice/providers-and-gateways.md).
- **CDN и QUIC.** HTTP/3 часто терминируется на edge CDN; тогда QUIC-фингерпринт видит CDN, а не бэкенд ([§15](../5-gaps/15-http3-quic.md)).

Отсюда главный тезис: **сеть — не «детектор прокси», а проверка консистентности.** Она не ищет плохой IP, она ищет расхождение между двумя машинами. Как только расхождение найдено, дальше решают репутация, поведение и аккаунт — слои, которые к сети не относятся.

---

### Источники

- Cloudflare — [Bot Score](https://developers.cloudflare.com/bots/concepts/bot-score/); Akamai — [HTTP/2 fingerprinting](https://www.akamai.com/blog/security/passive-fingerprinting-of-http-2-clients).
- ValdikSS — [Detecting VPN and its configuration on the server side](https://medium.com/@ValdikSS/detecting-vpn-and-its-configuration-and-proxy-users-on-the-server-side-1bcc59742413).
- Вендорские датасеты: [ipinfo](https://ipinfo.io/data/proxy-vpn-detection), [IPQS](https://www.ipqualityscore.com/documentation/proxy-detection-api/overview), [MaxMind](https://www.maxmind.com/en/geoip-anonymous-ip-database), [Spur](https://docs.spur.us/).

---

<sub>[← §11](11-stands.md) · [Оглавление](../README.md) · [§13. Подгонка стека →](13-tuning.md)</sub>
