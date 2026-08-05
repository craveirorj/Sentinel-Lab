from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import anthropic, os, httpx
from dotenv import load_dotenv
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()

app = FastAPI(
    title="SENTINEL API",
    description="Blue Team AI-powered security analysis"
)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def ask_claude(system: str, prompt: str) -> str:
    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text


async def get_wazuh_alerts(limit: int = 20):
    auth = (os.getenv("WAZUH_USER"), os.getenv("WAZUH_PASS"))
    url = f"https://{os.getenv('WAZUH_HOST')}:{os.getenv('WAZUH_PORT')}"
    async with httpx.AsyncClient(verify=False) as h:
        r = await h.get(f"{url}/alerts", auth=auth,
            params={"limit": limit, "sort": "-timestamp"})
    return r.json().get("data", {}).get("affected_items", [])


@app.get("/health")
async def health():
    return {"status": "online", "service": "SENTINEL API"}


@app.post("/analyst")
async def analyst(data: dict):
    """Análise geral de logs e eventos de segurança"""
    r = ask_claude(
        "És um analista SOC. Analisa eventos de segurança de forma clara e objectiva. "
        "Identifica ameaças, classifica por severidade e recomenda acções.",
        data.get("query", ""))
    return {"response": r}


@app.post("/incident")
async def incident(data: dict):
    """Guia de resposta a incidentes passo a passo"""
    r = ask_claude(
        "És um especialista em resposta a incidentes (IR). "
        "Fornece guia passo a passo: contenção, erradicação, recuperação e lições aprendidas.",
        data.get("query", ""))
    return {"response": r}


@app.post("/ioc")
async def ioc(data: dict):
    """Análise de Indicadores de Compromisso"""
    r = ask_claude(
        "És um analista de Threat Intelligence. "
        "Analisa IOCs (IPs, hashes, domínios, URLs) e classifica o risco.",
        data.get("query", ""))
    return {"response": r}


@app.post("/hardening")
async def hardening(data: dict):
    """Recomendações de hardening de sistemas"""
    r = ask_claude(
        "És um especialista em hardening de sistemas Linux e Windows. "
        "Fornece recomendações práticas e específicas com comandos prontos a usar.",
        data.get("query", ""))
    return {"response": r}


@app.post("/wazuh")
async def wazuh_analysis():
    """Fetch automático dos últimos alertas Wazuh + análise IA"""
    alerts = await get_wazuh_alerts(20)
    r = ask_claude(
        "És um analista SOC. Resume os alertas Wazuh, "
        "identifica ameaças prioritárias e recomenda acções imediatas.",
        f"Alertas Wazuh (últimos 20): {alerts}")
    return {"analysis": r, "alert_count": len(alerts)}


@app.post("/report")
async def generate_report():
    """Gerar relatório PDF de incidente com análise IA"""
    alerts = await get_wazuh_alerts(50)
    analysis = ask_claude(
        "És analista SOC. Gera relatório estruturado em português com: "
        "1) Sumário Executivo "
        "2) IPs Atacantes Identificados "
        "3) Técnicas MITRE ATT&CK Detectadas "
        "4) Timeline dos Eventos "
        "5) IOCs Identificados "
        "6) Recomendações de Mitigação",
        f"Alertas Wazuh para análise: {alerts}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"/tmp/sentinel_report_{ts}.pdf"

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("SENTINEL LAB — Relatório de Incidente", styles["Title"]),
        Paragraph(
            f"Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            styles["Normal"]),
        Spacer(1, 16),
    ]
    for line in analysis.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 4))

    doc.build(story)
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=f"sentinel_report_{ts}.pdf"
    )
