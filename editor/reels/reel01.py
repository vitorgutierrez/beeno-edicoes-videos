"""Reel 01 — Atendimento x Vendas no mesmo contato (CRM integrado).
Bruto: Drive 'Vídeos gravados' / Teleprompter-2026-06-10_15-50-07.mp4"""
from mg import RED

TRANSCRIPT = "transcripts/reel01_raw_whisper.json"
OUT_NAME = "BEENO-REEL01-atendimento-vendas-1.2x.mp4"
SPEED = 1.2
FACE = (560, 810)       # centro do rosto no bruto (px)
SPLIT_ZOOM = 1.0
SPLIT_FRAC = 0.42       # posição do rosto na metade de baixo do split
CAP_Y = 1480            # legenda no modo tela cheia

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
            "lados", "prática", "plataforma", "departamentos", "deveria"]


def build(m):
    return [
        dict(type="hook", layout="full", start=0, nocap=True, y=1250, boxes=[
            ("ISSO AQUI JÁ ACONTECEU", "green", m(3.32)),
            ("NA SUA OPERAÇÃO.", "white", m(5.20)),
        ]),
        dict(type="phones", layout="split", start=m(6.68), split_t=m(14.24), phones=[
            dict(t0=m(6.68), eyebrow="ATENDIMENTO", name="Cliente", sub="WhatsApp", when="Seg 09:12",
                 items=[("Oi, estou com um problema no meu pedido.", "msg", m(9.18)),
                        ("Ticket aberto", "status", m(9.92))]),
            dict(t0=m(10.84), eyebrow="COMERCIAL", name="Cliente", sub="E-mail", when="Ter 10:40",
                 items=[("Proposta de renovação", "doc", m(12.18)), ("Enviada", "status", m(12.76))]),
        ]),
        dict(type="head", layout="full", start=m(18.60), nocap=True, size=72, items=[
            ("PRO", m(18.60), False), ("CLIENTE,", m(18.88), False), ("É", m(19.08), False),
            ("UMA", m(19.22), False), ("EMPRESA", m(19.26), True), ("SÓ.", m(19.52), True)]),
        dict(type="plain", layout="full", start=m(20.16), zoom=1.1),
        dict(type="dots", layout="split", start=m(22.24), t0=m(22.24), chips_y=260,
             labels=[("Atendimento", 300, 660, m(22.42)), ("Vendas", 800, 440, m(23.04))],
             chips=[("−", "TEMPO", RED, m(26.08)), ("−", "ARGUMENTO", RED, m(27.38)),
                    ("−", "O CLIENTE", RED, m(28.54))]),
        dict(type="dots", layout="split", start=m(30.02), t0=m(22.24), conv_t=m(30.02), logo_t=m(30.68),
             tag=("CRM DE VENDAS E MARKETING", m(30.9))),
        dict(type="contact", layout="split", start=m(31.44), t0=m(31.44), name="Cliente",
             sub="1 contato · histórico completo",
             rows=[("Ticket · Atendimento", "Reclamação no WhatsApp", m(31.54)),
                   ("Negócio · Comercial", "Proposta de renovação", m(32.62))],
             footer=("OS DOIS LADOS, ANTES DE FALAR", m(36.58))),
        dict(type="head", layout="full", start=m(38.76), nocap=True, size=72, items=[
            ("O", m(38.76), False), ("SEU", m(38.88), False), ("CLIENTE", m(39.02), False),
            ("ENXERGA", m(39.34), False), ("UMA", m(39.70), False), ("EMPRESA", m(39.84), True),
            ("SÓ.", m(40.12), True)]),
        dict(type="plain", layout="full", start=m(40.46)),
        dict(type="head", layout="full", start=m(42.88), nocap=True, size=76, items=[
            ("QUER", m(42.88), False), ("VER", m(42.98), False), ("ISSO", m(43.12), False),
            ("NA", m(43.30), False), ("PRÁTICA?", m(43.54), True)]),
        dict(type="cta_full", layout="full", start=m(44.40), y=1340, logo_t=m(44.40), logo_y=330,
             button=("Agendar demonstração", m(44.94))),
    ]
