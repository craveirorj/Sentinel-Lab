#!/bin/bash
# Gerar ficheiro .ovpn para cliente OpenVPN
# Uso: ./gen_ovpn.sh <nome_cliente>
# Correr no LXC OpenVPN (192.168.1.105)

CLIENT=$1
EASYRSA='/etc/openvpn/easy-rsa'
SERVER_DOMAIN='vpnlab.duckdns.org'
SERVER_PORT='1194'

if [ -z "$CLIENT" ]; then
    echo "Uso: $0 <nome_cliente>"
    exit 1
fi

cd $EASYRSA
./easyrsa build-client-full $CLIENT nopass

cat > /root/${CLIENT}.ovpn << OVPN
client
dev tun
proto udp
remote $SERVER_DOMAIN $SERVER_PORT
resolv-retry infinite
nobind
persist-key
persist-tun
cipher AES-256-CBC
verb 3
<ca>
$(cat ${EASYRSA}/pki/ca.crt)
</ca>
<cert>
$(cat ${EASYRSA}/pki/issued/${CLIENT}.crt)
</cert>
<key>
$(cat ${EASYRSA}/pki/private/${CLIENT}.key)
</key>
<tls-auth>
$(cat /etc/openvpn/ta.key)
</tls-auth>
key-direction 1
OVPN

echo "Ficheiro gerado: /root/${CLIENT}.ovpn"
echo "Copiar para o PC: scp root@192.168.1.105:/root/${CLIENT}.ovpn ."
