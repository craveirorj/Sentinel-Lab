# 🛡️ SENTINEL LAB

> **Blue Team + Red Team Home Laboratory**  
> Detecção, Resposta e Relatórios Automáticos com IA em Tempo Real

![SENTINEL LAB Architecture](docs/architecture.png)

---

## 📋 Sobre o Projecto

O **SENTINEL LAB** é um laboratório de cibersegurança doméstico completo, construído sobre Proxmox VE, que combina um ambiente isolado de Red Team com uma stack Blue Team profissional. O objectivo é praticar pentesting em máquinas vulneráveis enquanto se monitoriza e responde aos ataques em tempo real.

### O que este lab permite fazer

- **Red Team** — atacar máquinas vulneráveis num ambiente completamente isolado
- **Blue Team** — detectar ataques com Suricata IDS + Wazuh SIEM/XDR
- **Active Response** — bloquear IPs atacantes automaticamente via iptables
- **IA integrada** — analisar alertas e gerar relatórios de incidentes com Claude AI
- **VPN** — aceder ao lab remotamente de qualquer lado (ideal para demonstrações)

---

## 🏗️ Arquitectura

```
Internet
    │
[Router Xiaomi AX3200 — OpenWRT]  ← WiFi Principal + Guest (AdGuard filtrado)
    │
[Switch Hisource Hi-S21-8G]
    │
[Mini PC — Proxmox VE — 192.168.1.100]
    │
    ├── LAN Principal (192.168.1.0/24)
    │   ├── SENTINEL API  (LXC 101) — FastAPI + Claude AI
    │   ├── Kali Linux    (VM  102) — Máquina de ataque
    │   ├── OpenVPN       (LXC 105) — Acesso remoto ao lab
    │   ├── Wazuh+Suricata(VM  106) — SIEM + IDS
    │   └── AdGuard Home  (LXC 108) — DNS + Controlo Parental
    │
    └── Rede Isolada Lab (10.10.10.0/24)
        ├── Metasploitable 2  (10.10.10.11)
        ├── Kioptrix          (10.10.10.10)
        └── DVWA              (10.10.10.4)
```

---

## 🔄 Fluxo Blue Team

```
Ataque detectado
      │
      ▼
[Suricata IDS] — analisa pacotes em tempo real
      │
      ▼
[Wazuh Manager] — correlaciona eventos + regras
      │
      ├──────────────────────────────┐
      ▼                              ▼
[Active Response]           [Alerta Telegram]
bloqueia IP (iptables)      notifica em segundos
      │
      ▼
[SENTINEL API + Claude AI]
analisa alertas, identifica IOCs
      │
      ▼
[Relatório PDF gerado automaticamente]
```

---

## 🧩 Componentes

### Hardware
| Componente | Modelo |
|---|---|
| Router | Xiaomi AX3200 (OpenWRT) |
| Switch | Hisource Hi-S21-8G |
| Hypervisor | Mini PC — Dell OptiPlex / Lenovo ThinkCentre |

### Stack Blue Team
| Componente | Função |
|---|---|
| **Proxmox VE** | Hypervisor — gere todas as VMs e LXCs |
| **Suricata IDS** | Detecção de intrusão em tempo real (regras Emerging Threats) |
| **Wazuh SIEM/XDR** | Correlação de eventos, dashboards, MITRE ATT&CK |
| **SENTINEL API** | Backend FastAPI com Claude AI para análise e relatórios |
| **AdGuard Home** | Filtro DNS — controlo parental e bloqueio de publicidade |
| **OpenVPN** | Acesso remoto seguro ao lab |
| **Cowrie + OpenCanary** | Honeypots SSH e multi-serviço |
| **Cloudflare Tunnel** | Exposição segura de serviços sem abrir portos |

### Stack Red Team (Rede Isolada)
| VM | IP | Descrição |
|---|---|---|
| Metasploitable 2 | 10.10.10.11 | Alvo multi-serviço vulnerável |
| Kioptrix | 10.10.10.10 | Máquina CTF-style |
| DVWA | 10.10.10.4 | Aplicação web vulnerável |
| Kali Linux | 192.168.1.102 | Máquina de ataque (dual NIC) |

---

## 🤖 SENTINEL API

Backend FastAPI com integração Claude AI que expõe 6 endpoints:

| Endpoint | Função |
|---|---|
| `POST /analyst` | Análise geral de logs e eventos de segurança |
| `POST /incident` | Guia de resposta a incidentes |
| `POST /ioc` | Análise de IOCs (IPs, hashes, domínios) |
| `POST /hardening` | Recomendações de hardening |
| `POST /wazuh` | Fetch automático de alertas Wazuh + análise IA |
| `POST /report` | Geração de relatório PDF de incidente com IA |

### Exemplo de uso

```bash
# Análise de um alerta
curl -X POST http://192.168.1.101:8000/analyst \
  -H 'Content-Type: application/json' \
  -d '{"query": "ET SCAN Nmap SYN Scan detectado de 10.10.10.50"}'

# Gerar relatório de incidente
curl -X POST http://192.168.1.101:8000/report \
  -H 'Content-Type: application/json' \
  -d '{}' -o relatorio.pdf
```

---

## 📁 Estrutura do Repositório

```
sentinel-lab/
├── README.md
├── docs/
│   ├── architecture.png          ← diagrama de arquitectura
│   └── SENTINEL_LAB_Manual.pdf   ← manual completo (instalação + operação + ferramentas)
├── sentinel-api/
│   ├── main.py                   ← FastAPI + endpoints
│   ├── requirements.txt
│   └── .env.example              ← variáveis de ambiente (sem credenciais)
├── configs/
│   ├── suricata/
│   │   └── suricata.yaml         ← configuração Suricata
│   ├── wazuh/
│   │   ├── ossec.conf            ← configuração Wazuh Manager
│   │   └── local_rules.xml       ← regras personalizadas
│   └── openvpn/
│       └── server.conf           ← configuração servidor OpenVPN
└── scripts/
    ├── gen_ovpn.sh               ← gerar ficheiros .ovpn para clientes
    ├── block_and_alert.sh        ← Active Response + notificação Telegram
    └── duckdns_update.sh         ← actualização automática DNS
```

---

## 🚀 Instalação Rápida

Ver o manual completo em `docs/SENTINEL_LAB_Manual.pdf`.

Sequência de instalação:

```
1. Configurar Switch (IP 192.168.1.2)
2. Instalar OpenWRT no AX3200 + fix dual partition
3. Configurar WiFi principal + guest + AdGuard
4. Instalar Proxmox VE no mini PC
5. Criar bridges vmbr0 (LAN) e vmbr1 (rede isolada)
6. Criar LXCs: SENTINEL, OpenVPN, AdGuard
7. Criar VMs: Kali, Wazuh+Suricata, Metasploitable, Kioptrix, DVWA
8. Configurar Suricata + integração Wazuh
9. Configurar Active Response + Telegram
10. Configurar Cloudflare Tunnel + DuckDNS
```

---

## ⚙️ Configuração

Copiar `.env.example` para `.env` e preencher:

```bash
cp sentinel-api/.env.example sentinel-api/.env
```

```env
ANTHROPIC_API_KEY=sk-ant-...
WAZUH_HOST=192.168.1.106
WAZUH_PORT=55000
WAZUH_USER=wazuh
WAZUH_PASS=your_password
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT=your_chat_id
```

---

## 📊 Acesso aos Serviços

| Serviço | URL | Credenciais |
|---|---|---|
| Proxmox VE | https://192.168.1.100:8006 | root / [instalação] |
| Wazuh Dashboard | https://192.168.1.106 | admin / [installer] |
| SENTINEL API | http://192.168.1.101:8000 | — |
| AdGuard Home | http://192.168.1.108:3000 | admin / [instalação] |

> ⚠️ IPs privados — apenas acessíveis dentro da rede local.

---

## 🔐 Segurança

- VMs vulneráveis em rede completamente isolada (vmbr1) sem acesso à Internet ou LAN
- DNS forçado na rede guest — impossível contornar o AdGuard
- Cloudflare Tunnel — sem portos expostos directamente na Internet
- Active Response — bloqueio automático de IPs atacantes
- Honeypots — Cowrie (SSH) + OpenCanary (multi-serviço)

---

## 📖 Documentação

O manual completo está em `docs/SENTINEL_LAB_Manual.pdf` e inclui:

- **Parte 1** — Instalação e configuração de todos os componentes (16 fases)
- **Parte 2** — Guia de Operação — como usar Wazuh, Suricata, SENTINEL, AdGuard, OpenVPN
- **Parte 3** — Guia de Ferramentas — Nmap, Metasploit, Burp Suite, Wireshark, Nessus e mais

---

## 👤 Autor

**Ricardo Craveiro**  
[github.com/craveirorj](https://github.com/craveirorj)  
[linkedin.com/in/ricardo-craveiro-751512150](https://linkedin.com/in/ricardo-craveiro-751512150)

---

## ⚠️ Aviso

Este laboratório destina-se exclusivamente a fins educativos e de investigação em ambiente controlado.  
Todas as máquinas vulneráveis estão numa rede isolada sem acesso à Internet.  
Não utilizar técnicas aqui descritas em sistemas sem autorização explícita.

---

*Blue Team + Red Team Home Laboratory — 2026*
