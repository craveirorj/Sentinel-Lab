# 🛡️ SENTINEL LAB

> **SOC doméstico completo — Blue Team & Red Team**
> Deteção, threat intelligence, resposta automática e análise de tráfego em tempo real, construídos em hardware de consumidor.

🇬🇧 *A home Security Operations Center built on Proxmox, OpenWRT, Wazuh and Suricata: full-network traffic mirroring (GRETAP), firewall and threat-intel logs in the SIEM, automatic network-wide blocking with Telegram alerts, honeypots and an isolated vulnerable lab. The full manual (in Portuguese) documents every component, every mistake and how it was fixed.*

---

## 📘 Manual

**[SENTINEL-LAB-Manual-v2.pdf](SENTINEL-LAB-Manual-v2.pdf)** — 89 páginas, 26 capítulos (edição pública).

| Parte | Conteúdo |
|---|---|
| I — Fundamentos | A ideia, os conceitos de rede essenciais, o equipamento |
| II — Construção | Proxmox, OpenWRT, AdGuard, Wazuh + Suricata, honeypots, alvos vulneráveis, OpenVPN, SENTINEL AI, Hack The Box |
| III — Visibilidade e resposta | Túnel de espelhamento GRETAP, DHCP, firewall com logs no SIEM, banIP, Active Response na rede inteira, redução de ruído |
| IV — Operar e analisar | Rotina de análise em tempo real, como ler Wazuh / Suricata / Wireshark / AdGuard, playbooks, investigações reais, teste de falha de luz |
| V — Consulta rápida | Cábula de comandos, lista de erros e correções, próximos passos |

Todos os IPs, MACs e domínios são **fictícios**. Nenhum segredo real está neste repositório.

---

## 🏗️ Arquitetura

```
                        INTERNET
                            │
                 Router do operador (dupla NAT)
                            │  UDP 1194 (VPN)
                 Router OpenWRT ── firewall · DHCP · banIP (~33k IPs maliciosos)
                 │          │          │      · logs → Wazuh · espelhamento GRETAP
        WiFi SENTINEL    Switch    WiFi SENTINELAB (testes, isolada)
                            │
                  Proxmox VE (Dell OptiPlex 5040)
   ┌──────────┬──────────┬──────────┬──────────┬──────────────────┐
 Wazuh +    AdGuard     OpenVPN   Honeypots   SENTINEL AI   Rede isolada (vmbr1)
 Suricata   Home (DNS)            Cowrie +    (FastAPI +    Metasploitable2
   ▲                              OpenCanary   Claude)      Kioptrix · DVWA
   └── recebe a cópia do tráfego da casa toda
```

## 🔄 Deteção e resposta

```
Suricata (IDS) ─┐
Firewall OpenWRT ┼─► Wazuh (decoders + regras próprias) ─┬─► Bloqueio no router, rede inteira (24h)
banIP ──────────┤                                        └─► Alerta no Telegram
Honeypots ──────┘
```

- **Lista branca dupla:** as máquinas de ataque do próprio lab nunca são bloqueadas.
- **Quarentena automática** de aparelhos que façam varrimentos na rede de testes.
- **Chave SSH restrita:** o SIEM só consegue pedir bloqueios ao router, nada mais.

## 🧩 Stack

| Camada | Ferramentas |
|---|---|
| Virtualização | Proxmox VE (VMs + contentores LXC) |
| Rede / firewall | OpenWRT 25.12 (fw4/nftables), banIP, túnel GRETAP + `tc mirred` |
| SIEM / XDR | Wazuh 4.14 (decoders e regras próprias, Active Response em Python) |
| IDS | Suricata 8 (Emerging Threats Open + regras próprias) |
| DNS | AdGuard Home (perfis por rede) |
| Engano | Cowrie, OpenCanary (FTP, HTTP, MySQL, SMB) |
| Acesso remoto | OpenVPN com PKI (um certificado por dispositivo, CRL) |
| Análise | Wireshark ao vivo sobre o túnel, `jq` sobre o `eve.json` |
| IA | SENTINEL AI — FastAPI + Claude API |
| Treino ofensivo | Kali Linux, VulnHub, Hack The Box |

## 📁 Repositório

| Ficheiro | Descrição |
|---|---|
| `SENTINEL-LAB-Manual-v2.pdf` | O manual completo (edição pública) |
| `main.py`, `requirements.txt`, `.env.example` | Backend SENTINEL AI (FastAPI) |
| `gen_ovpn.sh` | Montagem de perfis `.ovpn` por dispositivo |
| `duckdns_update.sh` | Atualização do DNS dinâmico |
| `architecture.png` | Diagrama de arquitetura |

## 📈 Histórico

- **v1 (set/2026):** construção do lab — Proxmox, rede segmentada, Wazuh + Suricata, honeypots, alvos, VPN.
- **v2 (nov/2026):** visibilidade da rede inteira, logs da firewall e do banIP no SIEM, threat intelligence, Active Response refeito (bloqueio na rede inteira + Telegram), menos 25 mil falsos alertas por dia, teste de falha de luz, guia de análise e playbooks.

---

**Autor:** Craveiro · [GitHub](https://github.com/craveirorj) · [LinkedIn](https://linkedin.com/in/ricardo-craveiro-751512150)
