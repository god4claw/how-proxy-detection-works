# §9. Где антифрод ошибается

<sub>[Главная](../../README.md) · [Часть 3](README.md) · [← §8](08-scoring.md) · [Часть 4. Проверка →](../4-checks/README.md)</sub>

Важно не только то, что детектится, но и то, что детектится **ложно**. Иначе статья превращается в «серебряную пулю», которой не существует.

- **iCloud Private Relay.** Apple проксирует трафик через свои AS — GeoIP и ASN-теги сходят с ума, RTT прыгает, а пользователь самый что ни на есть живой.
- **Google One VPN, корпоративные VPN.** Датацентр-IP при полностью легитимном сценарии.
- **CGNAT мобильных операторов.** Сотни абонентов за одним IP, RTT и джиттер непредсказуемые.
- **Операторы, которые сами проксируют.** Классический пример из статьи ValdikSS — Beeline, который гонял мобильный трафик через Linux-прокси. p0f честно показывал Linux на iPhone.
- **Спутниковый интернет.** Starlink: CGNAT + RTT 20–50 мс + скачки. Эталонный прогон в [§11](../4-checks/11-stands.md) — как раз Starlink: `Usage Corporate / Business`, теги `SATNET/BIZNET`, джиттер `±28.7 мс`, QUIC-RTT `1315 мс`. Наивные правила «Corporate + Satellite + высокий RTT» пометили бы живого пользователя.
- **Антивирусы с MITM.** Kaspersky/ESET подменяют TLS — детектится как MITM, хотя это защита, а не прокси.
- **`no matches` и возраст базы.** Отдельной подписи Windows 10/11 в `p0f.fp` нет; тюнингованный Linux и AmneziaWG тоже дают `no matches`. Если считать это флагом, вы поймаете всех, у кого нестандартный стек ([§3](../2-network/03-p0f-ja4t.md)).
- **Dual-stack.** IPv6-адрес может быть «чистым» и при этом вести напрямую, а IPv4 — через прокси; антифрод, который смотрит только на IPv4, не увидит вторую семью ([§14](../5-gaps/14-ipv6-dualstack.md)).

Обратная сторона: аккуратный residential-exit с совпадающим стеком проходит почти всё. Именно поэтому «списки плохих IP» сами по себе не работают — работает ансамбль.

> [!NOTE]
> Ложные срабатывания — не баг антифрода, а его экономика. Вендоры выбирают порог под допустимый FP: дешевле пропустить часть прокси, чем блокировать платящих клиентов. Поэтому «меня не заблокировали» не доказывает «меня не увидели»: возможно, вы попали в серую зону, а не в чёрный список.

---

### Источники

- ValdikSS — [Detecting VPN and its configuration on the server side](https://medium.com/@ValdikSS/detecting-vpn-and-its-configuration-and-proxy-users-on-the-server-side-1bcc59742413) (пример с Beeline).
- p0f — [p0f.fp](https://github.com/p0f/p0f/blob/master/p0f.fp) (отсутствие подписей Windows 10/11); Zardaxt — [github.com/NikolaiT/zardaxt](https://github.com/NikolaiT/zardaxt).
- BrowserLeaks [/ip](https://browserleaks.com/ip), [/tcp](https://browserleaks.com/tcp).

---

<sub>[← §8](08-scoring.md) · [Оглавление](../README.md) · [Часть 4. Проверка →](../4-checks/README.md)</sub>
