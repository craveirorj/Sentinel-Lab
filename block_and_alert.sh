#!/bin/bash
# Wazuh Active Response — Bloquear IP + Notificar Telegram
# Colocar em: /var/ossec/active-response/bin/block_and_alert.sh
# chmod 750 + chown root:wazuh

read INPUT
SRCIP=$(echo $INPUT | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('srcip',''))" 2>/dev/null)

if [ -n "$SRCIP" ]; then
    iptables -I INPUT   -s $SRCIP -j DROP
    iptables -I FORWARD -s $SRCIP -j DROP
    echo "$(date '+%Y-%m-%d %H:%M:%S') BLOCKED: $SRCIP" >> /var/log/sentinel-blocks.log

    source /opt/sentinel/.env 2>/dev/null
    if [ -n "$TELEGRAM_TOKEN" ] && [ -n "$TELEGRAM_CHAT" ]; then
        MSG="[SENTINEL] IP BLOQUEADO: $SRCIP - $(date '+%d/%m/%Y %H:%M:%S')"
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT}" \
            -d "text=${MSG}" > /dev/null
    fi
fi
