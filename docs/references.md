# Источники

Ссылки сгруппированы по темам. В тексте источники указаны в конце каждой главы; здесь — полный список.

## Инструменты и тесты

- [BrowserLeaks](https://browserleaks.com/): [/ip](https://browserleaks.com/ip) · [/tcp](https://browserleaks.com/tcp) · [/webrtc](https://browserleaks.com/webrtc) · [/dns](https://browserleaks.com/dns) · [/tls](https://browserleaks.com/tls) · [/http2](https://browserleaks.com/http2) · [/quic](https://browserleaks.com/quic) · [/client-hints](https://browserleaks.com/client-hints) · [/proxy](https://browserleaks.com/proxy)
- [quic.browserleaks.com](https://quic.browserleaks.com/) — сырые данные QUIC-теста.
- [test-ipv6.com](https://test-ipv6.com/) — независимая проверка dual-stack.
- [check.torproject.org/torbulkexitlist](https://check.torproject.org/torbulkexitlist) — список Tor exit-узлов.

## p0f, Satori, Zardaxt, JA3/JA4

- p0f — [исходники и документация](https://github.com/p0f/p0f), [база подписей p0f.fp](https://github.com/p0f/p0f/blob/master/p0f.fp).
- Satori — [github.com/xnih/satori](https://github.com/xnih/satori).
- Zardaxt — [github.com/NikolaiT/zardaxt](https://github.com/NikolaiT/zardaxt) (обученный relay-классификатор).
- JA4+ — [github.com/FoxIO-LLC/ja4](https://github.com/FoxIO-LLC/ja4), [о JA4T](https://foxio.io/blog/ja4t-tcp-fingerprinting).
- JA3 — [github.com/salesforce/ja3](https://github.com/salesforce/ja3), [статья Salesforce Engineering](https://engineering.salesforce.com/tls-fingerprinting-with-ja3-and-ja3s-247362855967/).
- Akamai — [Passive fingerprinting of HTTP/2 clients](https://www.akamai.com/blog/security/passive-fingerprinting-of-http-2-clients) (страница может отдавать 403 автоматическим клиентам; открывайте в браузере).

## Спецификации

- TCP: [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) (TCP), [RFC 7323](https://www.rfc-editor.org/rfc/rfc7323) (window scale, timestamps), [RFC 879](https://www.rfc-editor.org/rfc/rfc879) (MSS), [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681) (congestion control), [RFC 6298](https://www.rfc-editor.org/rfc/rfc6298) (RTT).
- IP: [RFC 791](https://www.rfc-editor.org/rfc/rfc791) (IPv4, TTL), [RFC 1191](https://www.rfc-editor.org/rfc/rfc1191) (PMTU), [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200) (IPv6, в т.ч. MSS −60), [RFC 6864](https://www.rfc-editor.org/rfc/rfc6864) (IP ID).
- IPv6: [RFC 8305](https://www.rfc-editor.org/rfc/rfc8305) (Happy Eyeballs v2), [RFC 8981](https://www.rfc-editor.org/rfc/rfc8981) (приватные адреса; заменил RFC 4941), [RFC 6877](https://www.rfc-editor.org/rfc/rfc6877) (464XLAT), [RFC 6052](https://www.rfc-editor.org/rfc/rfc6052) (NAT64), [RFC 7721](https://www.rfc-editor.org/rfc/rfc7721) (угрозы и корреляция в IPv6, §4 о префиксе).
- PPPoE: [RFC 2516](https://www.rfc-editor.org/rfc/rfc2516) (MTU 1492).
- TLS: [RFC 9849](https://www.rfc-editor.org/rfc/rfc9849) (ECH), [RFC 9848](https://www.rfc-editor.org/rfc/rfc9848) (SVCB/HTTPS), [RFC 9180](https://www.rfc-editor.org/rfc/rfc9180) (HPKE).
- QUIC/HTTP: [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) (QUIC), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001) (TLS over QUIC), [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114) (HTTP/3), [RFC 9113](https://www.rfc-editor.org/rfc/rfc9113) (HTTP/2), [RFC 9369](https://www.rfc-editor.org/rfc/rfc9369) (QUIC v2).
- DNS: [RFC 8484](https://www.rfc-editor.org/rfc/rfc8484) (DoH), [RFC 7858](https://www.rfc-editor.org/rfc/rfc7858) (DoT).
- WebRTC: [MDN: connectivity](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity), [MDN: RTCIceCandidate](https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/candidate), [mDNS ICE candidates (IETF draft)](https://datatracker.ietf.org/doc/draft-ietf-mmusic-mdns-ice-candidates/).
- Client Hints: [WICG UA-CH](https://wicg.github.io/ua-client-hints/), [MDN `userAgentData`](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/userAgentData).

## Вендорская документация

- Microsoft: [TCP/IP performance tuning — autotuning, окна, RTT, MSS](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-tcpip-performance-tuning).
- Linux: [ip-sysctl](https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html); `iptables-extensions(8)` — [TTL и TCPMSS](https://man7.org/linux/man-pages/man8/iptables-extensions.8.html); `tc-netem(8)` — [delay/jitter](https://man7.org/linux/man-pages/man8/tc-netem.8.html).
- WireGuard: [wg-quick(8)](https://git.zx2c4.com/wireguard-tools/plain/src/man/wg-quick.8); OpenVPN: [reference manual, mssfix](https://openvpn.net/community-resources/reference-manual-for-openvpn-2-6/).
- Chrome: [Headless mode](https://developer.chrome.com/docs/automation-and-testing/headless), [Headless shell](https://developer.chrome.com/docs/automation-and-testing/headless-chrome-shell), [UA Client Hints](https://developer.chrome.com/docs/privacy-security/user-agent-client-hints/), [Network Quality Estimator](https://developer.chrome.com/docs/capabilities/network-quality), [Chromium `user_agent_utils.cc`](https://source.chromium.org/chromium/chromium/src/+/main:components/embedder_support/user_agent_utils.cc).
- Puppeteer: [Headless modes](https://pptr.dev/guides/headless-modes).
- Cloudflare: [Bot Score](https://developers.cloudflare.com/bots/concepts/bot-score/).
- Датасеты репутации: [ipinfo Proxy & VPN Detection](https://ipinfo.io/data/proxy-vpn-detection) · [IPQualityScore Proxy Detection](https://www.ipqualityscore.com/documentation/proxy-detection-api/overview) · [MaxMind Anonymous IP](https://www.maxmind.com/en/geoip-anonymous-ip-database) · [Spur Context API](https://docs.spur.us/) · [Spamhaus](https://www.spamhaus.org/).

## Исследования и разборы

- ValdikSS — [Detecting VPN (and its configuration!) and proxy users on the server side](https://medium.com/@ValdikSS/detecting-vpn-and-its-configuration-and-proxy-users-on-the-server-side-1bcc59742413).
- Intoli — [Detecting Chrome headless](https://intoli.com/blog/not-possible-to-block-chrome-headless/).
- Krebs on Security — [Residential proxy service 911](https://krebsonsecurity.com/2022/07/a-deep-dive-into-the-residential-proxy-service-911/) · [Aisuru botnet](https://krebsonsecurity.com/2025/10/aisuru-botnet-shifts-from-residential-proxies/).

## Право и этика

- США: [18 U.S.C. §1030](https://www.law.cornell.edu/uscode/text/18/1030) (Computer Fraud and Abuse Act).
- Великобритания: [Computer Misuse Act 1990](https://www.legislation.gov.uk/ukpga/1990/18/contents).
- ЕС: [GDPR, Regulation (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679).
- ToS и consent: разбирается в материалах Krebs выше; для конкретного провайдера читайте его договор и abuse-политику.

## Лицензия

- [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/), полный текст — в [LICENSE](../LICENSE).

---

<sub>[← Оглавление](README.md) · [На главную](../README.md)</sub>
