"""Reel 02 — O melhor registro é o que ninguém precisa fazer (captura automática).
Bruto: Drive 'Vídeos gravados' / Teleprompter-2026-06-10_15-56-43.mp4"""

TRANSCRIPT = "transcripts/reel02_raw_whisper.json"
OUT_NAME = "BEENO-REEL02-registro-automatico.mp4"
SPEED = 1.1
FACE = (580, 980)
SPLIT_ZOOM = 1.0
SPLIT_FRAC = 0.42
CAP_Y = 1600

FIXES = [
    ("Bin,", 21.28, "Beeno,"),
    ("Funil", 22.98, "funil"),
    ("agente", 40.90, "agende"),
    ("DM", 41.26, "demo"),
]

KEYWORDS = ["manualmente", "registrar", "CRM", "estranho", "lembrar", "falhar", "capturar", "acontece", "Blip",
            "tag", "classifica", "Beeno", "funil", "existe", "histórico", "consequência", "completo", "cobrança",
            "fiscal", "Saiba", "Mais", "demo", "plataforma"]

# no máximo um punch-in suave por bloco de tela cheia (tempo do bruto)
PUNCH = [5.48, 15.48, 28.50, 37.72]


def build(m):
    return [
        dict(type="hook", layout="full", start=0, nocap=True, y=1420, size=48, boxes=[
            ("O MELHOR REGISTRO", "green", m(1.36)),
            ("É AQUELE QUE NINGUÉM", "white", m(2.56)),
            ("PRECISA FAZER MANUALMENTE.", "white", m(3.28)),
        ]),
        dict(type="plain", layout="full", start=m(5.48)),
        dict(type="checklist", layout="split", start=m(10.28), t0=m(10.28), title="Depende de alguém lembrar",
             rows=[("Registrar a ligação", m(10.42), True), ("Atualizar a etapa", m(11.04), True),
                   ("Anotar a objeção", m(11.80), True), ("Agendar o follow-up", m(13.22), False)]),
        dict(type="head", layout="full", start=m(14.72), nocap=True, size=76, items=[
            ("O", m(14.72), False), ("CAMINHO", m(14.90), False), ("É", m(15.28), False),
            ("CAPTURAR", m(15.48), True), ("O", m(15.92), False), ("QUE", m(16.08), False),
            ("JÁ", m(16.24), True), ("ACONTECE.", m(16.40), True)]),
        dict(type="chat", layout="split", start=m(17.38), t0=m(17.38), eyebrow="ATENDIMENTO NA BLIP",
             name="Cliente", sub="WhatsApp",
             msgs=[("Quero conhecer os planos para o meu time.", "in", m(17.46)),
                   ("Claro! Já te mostro as opções.", "out", m(18.84))],
             tag=("Interessado", m(19.34))),
        dict(type="kanban", layout="split", start=m(21.14), t0=m(21.14), cols=["Novo", "Qualificado", "Proposta"],
             deal="Cliente", deal_sub="Negócio", tag="Interessado", move_t=m(22.08),
             more=[("Tarefa criada", m(23.40)), ("Histórico salvo", m(23.72))]),
        dict(type="plain", layout="full", start=m(24.50)),
        dict(type="stats", layout="split", start=m(31.76), title=("REGISTRANDO A CONSEQUÊNCIA", m(31.76)),
             rows=[("Dado completo", m(32.36)), ("Sem cobrança", m(32.98)),
                   ("Gestor deixa de ser fiscal", m(34.14))]),
        dict(type="plain", layout="full", start=m(36.42)),
        dict(type="cta_full", layout="full", start=m(37.72), cap_from=m(39.92), y=1450, size=84, items=[
            ("NINGUÉM", m(37.72), False), ("PRECISA", m(38.02), False), ("LEMBRAR", m(38.32), True),
            ("DE", m(38.66), False), ("FAZER.", m(38.82), True)],
             button=("Saiba mais", m(40.20))),
    ]
