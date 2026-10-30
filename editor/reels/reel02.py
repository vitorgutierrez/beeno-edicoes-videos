"""Reel 02 — O melhor registro é o que ninguém precisa fazer (captura automática).
Bruto: Drive 'Vídeos gravados' / Teleprompter-2026-06-10_15-56-43.mp4"""
from mg import GREEN, RED

TRANSCRIPT = "transcripts/reel02_raw_whisper.json"
OUT_NAME = "BEENO-REEL02-registro-automatico-1.2x.mp4"
SPEED = 1.2
FACE = (580, 980)
SPLIT_ZOOM = 1.0
SPLIT_FRAC = 0.42
CAP_Y = 1600

BANNER = (("PARA GESTORES DE", False), ("TIMES COMERCIAIS", True))

FIXES = [
    ("Bin,", 21.28, "Beeno,"),
    ("Funil", 22.98, "funil"),
    ("agente", 40.90, "agende"),
    ("DM", 41.26, "demo"),
]

KEYWORDS = ["manualmente", "registrar", "CRM", "estranho", "lembrar", "falhar", "capturar", "acontece", "Blip",
            "tag", "classifica", "Beeno", "funil", "existe", "histórico", "consequência", "completo", "cobrança",
            "fiscal", "Saiba", "Mais", "demo", "plataforma"]

CHAPTERS = [5.48, 14.72, 28.50]


def build(m, ev):
    P, X = ev.pop, ev.hit
    return [
        dict(type="hook", layout="full", start=0, nocap=True, y=1420, size=52, boxes=[
            ("O MELHOR REGISTRO", "green", P(m(1.36))),
            ("É AQUELE QUE NINGUÉM", "white", P(m(2.56))),
            ("PRECISA FAZER MANUALMENTE.", "white", P(m(3.28))),
        ]),
        dict(type="form", layout="split", start=m(5.48), t0=m(5.48), title="Registro manual",
             sub="Preencha todos os campos", fields=["Etapa do negócio", "Última conversa", "Próximo passo"],
             req="Obrigatório", req_t=[P(m(6.38)), P(m(6.86)), P(m(7.20))]),
        dict(type="plain", layout="full", start=m(8.02), zoom=1.14),
        dict(type="memory", layout="split", start=m(10.28), t0=m(10.28), title="Depende de alguém lembrar",
             rows=[("Registrar a ligação", P(m(10.58)), True), ("Atualizar a etapa", P(m(11.24)), True),
                   ("Anotar a objeção", P(m(11.80)), True), ("Agendar o follow-up", m(13.22), False)],
             stamp=("VAI FALHAR", X(m(13.22)))),
        dict(type="head", layout="full", start=m(14.72), nocap=True, items=[
            ("O", m(14.72), False), ("CAMINHO", m(14.90), False), ("É", m(15.28), False),
            ("CAPTURAR", m(15.48), True), ("O", m(15.92), False), ("QUE", m(16.08), False),
            ("JÁ", m(16.24), True), ("ACONTECE.", m(16.40), True)]),
        dict(type="chat", layout="split", start=m(17.38), t0=m(17.38), name="Cliente", sub="Blip · Atendimento",
             msgs=[("Quero conhecer os planos para o meu time.", "in", P(m(17.46))),
                   ("Claro! Já te mostro as opções.", "out", P(m(18.84)))],
             tag=("Interessado", X(m(19.34)))),
        dict(type="kanban", layout="split", start=m(21.14), t0=m(21.14), cols=["Novo", "Qualificado", "Proposta"],
             deal="Cliente", deal_sub="Negócio", tag="Interessado", move_t=P(m(22.08)),
             more=[("Tarefa criada", P(m(23.40))), ("Histórico salvo", P(m(23.72)))]),
        dict(type="flow", layout="split", start=m(24.50), sources=[("Conversa", P(m(24.72))),
                                                                   ("Histórico", P(m(25.80)))],
             arrow_t=m(26.94), crm_t=X(m(27.06))),
        dict(type="chips", layout="split", start=m(28.50),
             title=([("REGISTRA", False), ("A", False), ("CONSEQUÊNCIA", True)], P(m(29.50))),
             sub=("NÃO A TAREFA A MAIS", P(m(30.56))), y0=530, dy=165,
             chips=[("check", "DADO COMPLETO", GREEN, P(m(32.36))), ("check", "SEM COBRANÇA", GREEN, P(m(32.98))),
                    ("check", "GESTOR SEM FISCALIZAR", GREEN, X(m(34.70)))]),
        dict(type="head", layout="full", start=m(36.42), size=88, items=[
            ("NINGUÉM", m(37.72), False), ("PRECISA", m(38.02), False), ("LEMBRAR", m(38.32), True),
            ("DE", m(38.66), False), ("FAZER.", m(38.82), True)]),
        dict(type="cta", layout="split", start=m(39.92), t0=m(39.92),
             tagline=([("Vendas", False), ("e", False), ("marketing", False), ("realmente", True),
                       ("integrado.", True)], m(40.06)),
             button=("Saiba mais", X(m(40.20))), sub=("Agende uma demo com o nosso time", P(m(40.90)))),
    ]
