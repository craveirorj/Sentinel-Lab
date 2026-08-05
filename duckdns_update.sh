#!/bin/bash
# Actualizar IP público no DuckDNS
# Adicionar ao cron: */5 * * * * /opt/duckdns_update.sh > /dev/null 2>&1

source /opt/sentinel/.env 2>/dev/null

DOMAINS="sentinel,vpnlab"
curl -s "https://www.duckdns.org/update?domains=${DOMAINS}&token=${DUCKDNS_TOKEN}&ip=" \
    >> /var/log/duckdns.log 2>&1

echo "$(date): DuckDNS actualizado" >> /var/log/duckdns.log
