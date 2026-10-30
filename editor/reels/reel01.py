"""Reel 01 — Atendimento x Vendas no mesmo contato (CRM integrado).
Bruto: Drive 'Vídeos gravados' / Teleprompter-2026-06-10_15-50-07.mp4"""
from mg import GREEN, GREEN_300, RED

TRANSCRIPT = "transcripts/reel01_raw_whisper.json"
OUT_NAME = "BEENO-REEL01-atendimento-vendas-1.2x.mp4"
SPEED = 1.2
FACE = (560, 810)       # centro do rosto no bruto (px)
SPLIT_ZOOM = 1.0
SPLIT_FRAC = 0.42       # posição do rosto na metade de baixo do split
CAP_Y = 1480            # legenda no modo tela cheia

BANNER = (("PARA EMPRESAS QUE", False), ("VENDEM E ATENDEM", True), ("PELO WHATSAPP", False))

# (palavra transcrita, tempo aprox. no bruto, texto correto)
FIXES = [
    ("chamar", 8.38, "chamado"),
    ("whatsapp", 8.70, "WhatsApp"),
    ("Para", 15.74, "Pra"),
    ("empresas", 15.94, "empresa"),
    ("para", 18.60, "pro"),
    ("o", 18.76, ""),
    ("time,", 26.30, "tempo,"),
]

KEYWORDS = ["WhatsApp", "problema", "comercial", "proposta", "renovação", "nenhum", "desorganizada", "atendimento",
            "vendas", "diferentes", "tempo", "argumento", "CRM", "integrado", "tickets", "negócios", "contato",
            "lados", "prática", "plataforma", "departamentos"]

CHAPTERS = [6.68, 22.24, 30.02]


def build(m, ev):
    P, X = ev.pop, ev.hit
    return [
        dict(type="hook", layout="full", start=0, nocap=True, y=1250, boxes=[
            ("ISSO AQUI JÁ ACONTECEU", "green", P(m(3.32))),
            ("NA SUA OPERAÇÃO.", "white", P(m(5.20))),
        ]),
        dict(type="chat", layout="split", start=m(6.68), t0=m(6.68), name="Cliente", sub="WhatsApp · Atendimento",
             stamp=("SEGUNDA", X(m(6.86))),
             tag=("Ticket aberto", P(m(8.38))),
             msgs=[("Oi! Estou com um problema no meu pedido.", "in", P(m(9.18))),
                   ("Alguém pode me ajudar?", "in", P(m(9.92)))]),
        dict(type="proposal", layout="split", start=m(10.70), t0=m(10.70), name="Comercial", sub="para: Cliente",
             title="Proposta de renovação", file="proposta-renovacao.pdf",
             stamp=("TERÇA", X(m(10.84))), sent=("ENVIADA", P(m(12.76)))),
        dict(type="disconnect", layout="split", start=m(13.92),
             cards=[("ATENDIMENTO", "Ticket aberto", P(m(13.92))), ("COMERCIAL", "Proposta enviada", P(m(14.06)))],
             link_t=m(14.24), x_t=X(m(14.62)), label=("DOIS DEPARTAMENTOS", P(m(16.64)))),
        dict(type="head", layout="full", start=m(18.60), nocap=True, items=[
            ("PRO", m(18.60), False), ("CLIENTE,", m(18.88), False), ("É", m(19.08), False),
            ("UMA", m(19.22), False), ("EMPRESA", m(19.26), True), ("SÓ.", m(19.52), True)],
             stamps=[dict(text="DESORGANIZADA", color=RED, y=1280, t=X(m(20.82)), size=72, rot=-6)]),
        dict(type="chips", layout="split", start=m(22.24),
             title=([("ATENDIMENTO", True), ("×", False), ("VENDAS", True)], P(m(22.42))),
             sub=("EM LUGARES DIFERENTES", P(m(24.44))), y0=530, dy=165,
             chips=[("−", "TEMPO", RED, P(m(26.08))), ("−", "ARGUMENTO", RED, P(m(27.38))),
                    ("−", "O CLIENTE", RED, X(m(28.54)))]),
        dict(type="brand", layout="split", start=m(30.02), t0=m(30.02), tag=("CRM INTEGRADO", P(m(30.68)))),
        dict(type="contact", layout="split", start=m(31.44), t0=m(31.44), name="Cliente",
             sub="1 contato · histórico completo",
             rows=[("Ticket · Atendimento", "Reclamação no WhatsApp", GREEN, P(m(31.54))),
                   ("Negócio · Comercial", "Proposta de renovação", GREEN_300, P(m(32.62)))],
             footer=("VÊ OS DOIS LADOS", P(m(36.58)))),
        dict(type="head", layout="full", start=m(38.76), items=[
            ("UMA", m(39.70), False), ("EMPRESA", m(39.84), True), ("SÓ.", m(40.12), True)]),
        dict(type="head", layout="full", start=m(42.88), nocap=True, zoom=1.08, items=[
            ("QUER", m(42.88), False), ("VER", m(42.98), False), ("ISSO", m(43.12), False),
            ("NA", m(43.30), False), ("PRÁTICA?", m(43.54), True)]),
        dict(type="cta", layout="split", start=m(44.40), t0=m(44.40),
             tagline=([("Vendas", False), ("e", False), ("marketing", False), ("realmente", True),
                       ("integrado.", True)], m(44.62)),
             button=("Agendar demonstração", X(m(44.94))), sub=("beeno.ai", P(m(45.72)))),
    ]
