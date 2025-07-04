import requests
import html

# ====== CONFIGURAÇÕES DO TELEGRAM ======
TELEGRAM_TOKEN = "8074493778:AAFjvuV7O3lV7iIeebmCt0-G2H6Et7ukE2k"
CHAT_ID = "-1002861597708"


def send_telegram_alert(nome, url, status_erro):
    if TELEGRAM_TOKEN.startswith("COLOQUE") or CHAT_ID.startswith("COLOQUE"):
        print("[AVISO] Configure o TELEGRAM_TOKEN e o CHAT_ID para receber alertas no Telegram.")
        return
    # Sanitiza o status_erro para evitar problemas com o Telegram
    status_erro_sanitizado = str(status_erro).replace('\n', ' ').replace('\r', ' ')
    status_erro_sanitizado = html.escape(status_erro_sanitizado)[:400]  # Limita tamanho e escapa HTML
    mensagem = (
        "🚨 <b>Alerta de Erro no Graylog</b> 🚨\n\n"
        f"<b>Ambiente:</b> {nome}\n"
        f"<b>Link:</b> <a href='{url}'>{url}</a>\n"
        f"<b>Status:</b> <code>{status_erro_sanitizado}</code>"
    )
    url_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        response = requests.post(url_api, data=data, timeout=10)
        print(f"[DEBUG] Telegram API status: {response.status_code}, resposta: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar alerta para o Telegram: {e}")

urls = [
    ("https://graylog-prod-inovacarreira.santoro.in/welcome", "Graylog Inovacarreira Produção"),
    ("https://graylog-stage-inovacarreira.santoro.in/", "Graylog Inovacarreira Stage"),
    ("https://graylog.piwi.com.br/", "Graylog Piwi"),
    ("https://signoz.piwi.com.br/", "Signoz Piwi"),
    ("http://smallgrafana.santoro.in:3000/login", "Grafana Small"),
    ("https://monitor.santoro.in/?orgId=1&from=now-6h&to=now&timezone=browser", "Grafana SantoroIN"),
    ("https://grafana-aws.tray.net.br", "Grafana Tray"),
    ("https://inframonitor.agrinvest.agr.br", "Grafana Agrinvest"),
    ("http://futmonitor.santoro.in:3000", "Grafana FutFanatics"),
    ("https://inframonitor.happy.com.br/login", "Grafana Happy"),
    ("https://grafana.com/auth/sign-in/", "Grafana Piwi"),
    ("http://senior-monitor.santoro.in:3000", "Grafana Senior"),
    ("http://186.227.40.91:3051/", "Grafana Wepass")
]

# Lista de mensagens de erro comuns em páginas web
erros_comuns = [
    "Internal Server Error",
    "502 Bad Gateway",
    "503 Service Unavailable",
    "504 Gateway Timeout",
    "404 Not Found",
    "Erro",
    "Error",
    "exception",
    "not available",
    "temporarily unavailable"
]

def contem_erro(texto):
    texto_lower = texto.lower()
    for erro in erros_comuns:
        if erro.lower() in texto_lower:
            return True
    return False

print("\n==============================")
print("   STATUS DAS CONTAS GRAYLOG  ")
print("==============================\n")

for url, nome in urls:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if contem_erro(response.text):
                status_erro = "Acessível, mas contém mensagem de erro na página!"
                print(f"❌ {nome.ljust(28)} | {url}\n    ↳ Acessível, mas contém mensagem de erro na página!\n")
                send_telegram_alert(nome, url, status_erro)
            else:
                print(f"✅ {nome.ljust(28)} | {url}\n    ↳ Acessível e sem mensagens de erro.\n")
        else:
            status_erro = f"Retornou status {response.status_code}."
            print(f"❌ {nome.ljust(28)} | {url}\n    ↳ Retornou status {response.status_code}.\n")
            send_telegram_alert(nome, url, status_erro)
    except Exception as e:
        status_erro = f"Não foi possível acessar: {e}"
        print(f"❌ {nome.ljust(28)} | {url}\n    ↳ Não foi possível acessar: {e}\n")
        send_telegram_alert(nome, url, status_erro)

print("==============================\n") 