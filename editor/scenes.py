"""Cenas. Cenas 'split' desenham no painel superior (1080x960); cenas 'full'
desenham por cima do apresentador (1080x1920). Tempos em segundos de saída.

Linguagem: elementos entram por fade + leve subida, linhas finas, fundo
escuro; verde apenas para o que importa."""
import math
import random

from PIL import Image, ImageDraw

from mg import (GREEN, INK, LINE, MUTED, RED, W, WHITE, appear, arrow_down, check_icon, ease_in_out, ease_out,
                eyebrow, fade_up, font, headline, label, lerp, logo, place, rgba, rounded, text_img, x_icon)

PCX, PCY = W / 2, 520  # centro útil do painel


def _hdr_line(d, x0, x1, y):
    d.line([(x0, y), (x1, y)], fill=LINE, width=2)


# ------------------------------------------------------------------ tela cheia
def hook(c, t, sc):
    """Gancho: caixa verde + caixa branca empilhadas sobre o apresentador."""
    y = sc.get("y", 1250)
    f = font("ExtraBold", sc.get("size", 50))
    for i, (txt, kind, t0) in enumerate(sc["boxes"]):
        fill = GREEN if kind == "green" else WHITE
        fade_up(c, label(txt, f, fill, INK, padx=30, pady=12, r=8), W / 2, y + i * 92, appear(t, t0, 0.3))


def head(c, t, sc):
    headline(c, t, sc["items"], sc.get("y", 250), sc.get("size", 80))


def plain(c, t, sc):
    pass


def cta_full(c, t, sc):
    """CTA no estilo RVOPS: pílula com seta para baixo apontando para o botão do anúncio."""
    if "items" in sc:
        headline(c, t, sc["items"], sc.get("head_y", 250), sc.get("size", 76))
    txt, tm = sc["button"]
    f = font("ExtraBold", 44)
    ti = text_img(txt, f, INK)
    bw, bh = ti.width + 120, 104
    btn = rounded(bw, bh, bh // 2, rgba(GREEN))
    btn.alpha_composite(ti, (40, (bh - ti.height) // 2 - 2))
    btn.alpha_composite(arrow_down(52, INK, 7), (bw - 80, (bh - 52) // 2))
    fade_up(c, btn, W / 2, sc.get("y", 1250), appear(t, tm, 0.35))
    if "logo_t" in sc:
        fade_up(c, logo(300), W / 2, sc.get("logo_y", 330), appear(t, sc["logo_t"], 0.5))


# ------------------------------------------------------------------ peças do painel
def _phone(w, h, header, sub, when=None):
    ph = rounded(w, h, 40, (18, 34, 28, 255), LINE, 2)
    d = ImageDraw.Draw(ph)
    d.rounded_rectangle([w / 2 - 40, 16, w / 2 + 40, 26], 5, fill=(255, 255, 255, 40))
    d.ellipse([28, 52, 84, 108], outline=(255, 255, 255, 90), width=2)
    f0 = font("Bold", 28)
    d.text((56 - f0.getlength(header[0]) / 2, 60), header[0], font=f0, fill=rgba(WHITE, 200))
    d.text((100, 50), header, font=font("SemiBold", 28), fill=rgba(WHITE))
    d.text((100, 86), sub, font=font("Regular", 21), fill=rgba(MUTED))
    if when:
        tw = font("Regular", 21).getlength(when)
        d.text((w - 28 - tw, 56), when, font=font("Regular", 21), fill=rgba(MUTED))
    _hdr_line(d, 24, w - 24, 130)
    return ph


def _bubble(txt, maxw, side="in", size=27):
    f = font("Medium", size)
    lines, cur = [], ""
    for wd in txt.split():
        nxt = (cur + " " + wd).strip()
        if f.getlength(nxt) > maxw - 40 and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = nxt
    lines.append(cur)
    asc, desc = f.getmetrics()
    lh = asc + desc + 2
    bw = int(max(f.getlength(l) for l in lines) + 40)
    fill = (44, 62, 54, 255) if side == "in" else rgba(GREEN)
    col = WHITE if side == "in" else INK
    b = rounded(bw, lh * len(lines) + 24, 20, fill)
    d = ImageDraw.Draw(b)
    for i, l in enumerate(lines):
        d.text((20, 10 + i * lh), l, font=f, fill=rgba(col))
    return b


def phones(c, t, sc):
    """Dois celulares abstratos (atendimento x comercial) que não se falam."""
    pw, ph = 400, 580
    cy = PCY + 50
    for i, side in enumerate(sc["phones"]):
        cx = 285 if i == 0 else 795
        a = appear(t, side["t0"], 0.4)
        if a <= 0:
            continue
        fade_up(c, eyebrow(side["eyebrow"]), cx, cy - ph / 2 - 46, a)
        fade_up(c, _phone(pw, ph, side["name"], side["sub"], side.get("when")), cx, cy, a)
        if a < 1:
            continue
        top = cy - ph / 2
        dd = ImageDraw.Draw(c)
        for k, ww in enumerate((230, 170, 260)):
            dd.rounded_rectangle([cx - pw / 2 + 28, top + 160 + k * 34, cx - pw / 2 + 28 + ww, top + 176 + k * 34],
                                 8, fill=(40, 56, 49, 255))
        y = top + 290
        for txt, kind, tm in side["items"]:
            if kind == "msg":
                b = _bubble(txt, pw - 60)
                fade_up(c, b, cx - pw / 2 + 24 + b.width / 2, y + b.height / 2, appear(t, tm, 0.3))
                y += b.height + 16
            elif kind == "doc":
                doc = rounded(pw - 48, 84, 16, (36, 52, 45, 255))
                d = ImageDraw.Draw(doc)
                d.rounded_rectangle([16, 16, 52, 68], 6, outline=rgba(WHITE, 160), width=2)
                d.line([(24, 32), (44, 32)], fill=rgba(WHITE, 120), width=2)
                d.line([(24, 42), (44, 42)], fill=rgba(WHITE, 120), width=2)
                d.text((66, 14), txt, font=font("SemiBold", 24), fill=rgba(WHITE))
                d.text((66, 46), "PDF", font=font("Regular", 19), fill=rgba(MUTED))
                fade_up(c, doc, cx, y + 42, appear(t, tm, 0.3))
                y += 100
            elif kind == "status":
                st = text_img(txt, font("SemiBold", 24), GREEN)
                fade_up(c, st, cx + pw / 2 - 24 - st.width / 2, y + 6, appear(t, tm, 0.3), rise=6)
                y += 40
    if "split_t" in sc and t >= sc["split_t"]:
        k = ease_out((t - sc["split_t"]) / 0.5)
        ring = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse([2, 2, 69, 69], fill=rgba(INK), outline=rgba(RED), width=3)
        ring.alpha_composite(x_icon(72, RED, 4))
        place(c, ring, PCX, cy, k)


class Particles:
    """Pontos dispersos (informação espalhada) que convergem para a marca."""

    def __init__(self, n=90, seed=5):
        rnd = random.Random(seed)
        self.p = []
        for i in range(n):
            ang = i / n * 2 * math.pi
            self.p.append(dict(x=rnd.uniform(110, 970), y=rnd.uniform(230, 880), r=rnd.uniform(3.5, 7),
                               ph=rnd.uniform(0, 6.28), sp=rnd.uniform(0.4, 0.9), delay=rnd.uniform(0, 0.6),
                               tx=PCX + 300 * math.cos(ang), ty=PCY + 40 + 125 * math.sin(ang),
                               green=rnd.random() < 0.55))

    def draw(self, c, t, t_in, t_green=None, t_conv=None, t_logo=None):
        d = ImageDraw.Draw(c)
        for q in self.p:
            a = ease_out((t - t_in - q["delay"]) / 0.5)
            if a <= 0:
                continue
            x = q["x"] + 8 * math.sin(t * q["sp"] * 0.6 + q["ph"])
            y = q["y"] + 6 * math.cos(t * q["sp"] * 0.5 + q["ph"])
            col, alpha = WHITE, 110
            if t_green is not None and q["green"] and t >= t_green + q["delay"] * 0.5:
                col, alpha = GREEN, 230
            if t_conv is not None and t >= t_conv:
                k = ease_in_out((t - t_conv - q["delay"] * 0.4) / 1.4)
                x, y = lerp(x, q["tx"], k), lerp(y, q["ty"], k)
                col, alpha = GREEN, lerp(alpha, 230, k)
            if t_logo is not None and t >= t_logo:
                alpha *= 1 - ease_out((t - t_logo) / 0.8)
            r = q["r"]
            d.ellipse([x - r, y - r, x + r, y + r], fill=rgba(col, alpha * a))


_PARTICLES = Particles()


def dots(c, t, sc):
    """Partículas + chips à esquerda (como na RVOPS) + rótulos + marca em caixa contornada."""
    _PARTICLES.draw(c, t, sc["t0"], sc.get("green_t"), sc.get("conv_t"), sc.get("logo_t"))
    gone = 1 - ease_out((t - sc["conv_t"]) / 0.4) if "conv_t" in sc and t >= sc["conv_t"] else 1
    for txt, x, y, tm in sc.get("labels", []):
        lb = label(txt, font("Bold", 34), (16, 42, 32), WHITE, padx=22, pady=8, r=10)
        place(c, lb, x, y + (1 - ease_out(appear(t, tm, 0.35))) * 14, ease_out(appear(t, tm, 0.35)) * gone)
    y = sc.get("chips_y", 250)
    for big, small, accent, tm in sc.get("chips", []):
        bi = text_img(big, font("ExtraBold", 54), accent)
        si = text_img(small, font("Bold", 30), WHITE)
        ch = rounded(bi.width + si.width + 52, 82, 41, rgba(INK), LINE, 2)
        ch.alpha_composite(bi, (22, (82 - bi.height) // 2 + 2))
        ch.alpha_composite(si, (22 + bi.width + 8, (82 - si.height) // 2 + 4))
        fade_up(c, ch, 70 + ch.width / 2, y, appear(t, tm, 0.3), rise=0)
        y += 98
    if "logo_t" in sc:
        a = ease_out(appear(t, sc["logo_t"], 0.6))
        place(c, rounded(560, 230, 28, rgba(INK), rgba(GREEN, 120), 2), PCX, PCY + 40, a)
        place(c, logo(400), PCX, PCY + 40, a, lerp(0.96, 1, a))
        if "tag" in sc:
            txt, tm = sc["tag"]
            fade_up(c, eyebrow(txt), PCX, PCY + 205, appear(t, tm, 0.4))


def contact(c, t, sc):
    cw, ch = 860, 600
    cy = PCY + 70
    a = appear(t, sc["t0"], 0.4)
    if "logo_t" in sc:
        fade_up(c, logo(220), PCX, 175, appear(t, sc["logo_t"], 0.4))
    card = rounded(cw, ch, 32, rgba(INK), LINE, 2)
    d = ImageDraw.Draw(card)
    d.ellipse([40, 40, 124, 124], outline=rgba(GREEN, 220), width=3)
    f0 = font("Bold", 40)
    d.text((82 - f0.getlength(sc["name"][0]) / 2, 54), sc["name"][0], font=f0, fill=rgba(GREEN))
    d.text((150, 42), sc["name"], font=font("Bold", 38), fill=rgba(WHITE))
    d.text((150, 92), sc["sub"], font=font("Regular", 25), fill=rgba(MUTED))
    _hdr_line(d, 40, cw - 40, 160)
    fade_up(c, card, PCX, cy, a)
    if a < 1:
        return
    top = cy - ch / 2
    y = top + 190
    for title, sub, tm in sc["rows"]:
        row = Image.new("RGBA", (cw - 80, 122), (0, 0, 0, 0))
        rd = ImageDraw.Draw(row)
        rd.rounded_rectangle([0, 18, 84, 102], 18, outline=(255, 255, 255, 70), width=2)
        rd.text((112, 16), title, font=font("SemiBold", 34), fill=rgba(WHITE))
        rd.text((112, 64), sub, font=font("Regular", 26), fill=rgba(MUTED))
        row.alpha_composite(check_icon(48, GREEN, 5), (18, 36))
        _hdr_line(rd, 0, cw - 80, 121)
        fade_up(c, row, PCX, y + 61, appear(t, tm, 0.35))
        y += 136
    if "footer" in sc:
        txt, tm = sc["footer"]
        fade_up(c, eyebrow(txt), PCX, top + ch - 60, appear(t, tm, 0.4))


def form(c, t, sc):
    cw, ch = 820, 600
    cy = PCY + 40
    a = appear(t, sc["t0"], 0.4)
    card = rounded(cw, ch, 32, rgba(INK), LINE, 2)
    d = ImageDraw.Draw(card)
    d.text((44, 36), sc["title"], font=font("Bold", 38), fill=rgba(WHITE))
    d.text((44, 88), sc["sub"], font=font("Regular", 25), fill=rgba(MUTED))
    fy = 170
    for lbl in sc["fields"]:
        d.text((44, fy), lbl, font=font("Medium", 25), fill=rgba(MUTED))
        d.rounded_rectangle([44, fy + 40, cw - 44, fy + 100], 12, outline=(255, 255, 255, 50), width=2)
        fy += 136
    fade_up(c, card, PCX, cy, a)
    if a < 1:
        return
    top = cy - ch / 2
    if int(t * 2.2) % 2 == 0:
        ImageDraw.Draw(c).line([(PCX - cw / 2 + 66, top + 222), (PCX - cw / 2 + 66, top + 258)], fill=rgba(GREEN),
                               width=3)
    for i, tm in enumerate(sc["req_t"]):
        r = text_img(sc["req"], font("SemiBold", 24), RED)
        fade_up(c, r, PCX + cw / 2 - 44 - r.width / 2, top + 186 + i * 136, appear(t, tm, 0.3), rise=6)


def checklist(c, t, sc):
    cw, ch = 820, 600
    cy = PCY + 40
    a = appear(t, sc["t0"], 0.4)
    card = rounded(cw, ch, 32, rgba(INK), LINE, 2)
    ImageDraw.Draw(card).text((44, 36), sc["title"], font=font("Bold", 38), fill=rgba(WHITE))
    fade_up(c, card, PCX, cy, a)
    if a < 1:
        return
    top = cy - ch / 2
    y = top + 130
    for txt, tm, ok in sc["rows"]:
        failed = (not ok) and t >= tm
        row = Image.new("RGBA", (cw - 88, 110), (0, 0, 0, 0))
        rd = ImageDraw.Draw(row)
        rd.ellipse([0, 33, 44, 77], outline=rgba(RED) if failed else (255, 255, 255, 90), width=2)
        rd.text((70, 32), txt, font=font("Medium", 33), fill=rgba(RED) if failed else rgba(WHITE, 230))
        if t >= tm:
            ic = check_icon(44, GREEN, 5) if ok else x_icon(44, RED, 4)
            row.alpha_composite(ic, (0, 33))
        if txt != sc["rows"][-1][0]:
            _hdr_line(rd, 0, cw - 88, 109)
        place(c, row, PCX, y + 55)
        y += 112


def chat(c, t, sc):
    pw, ph = 600, 640
    cy = PCY + 50
    a = appear(t, sc["t0"], 0.4)
    fade_up(c, eyebrow(sc["eyebrow"]), PCX, cy - ph / 2 - 46, a)
    fade_up(c, _phone(pw, ph, sc["name"], sc["sub"]), PCX, cy, a)
    if a < 1:
        return
    top = cy - ph / 2
    y = top + 170
    for txt, side, tm in sc["msgs"]:
        b = _bubble(txt, 470, side, 30)
        x = PCX - pw / 2 + 30 + b.width / 2 if side == "in" else PCX + pw / 2 - 30 - b.width / 2
        fade_up(c, b, x, y + b.height / 2, appear(t, tm, 0.3))
        y += b.height + 18
    if "tag" in sc:
        txt, tm = sc["tag"]
        ti = text_img(txt, font("SemiBold", 26), GREEN)
        tg = rounded(ti.width + 64, 52, 26, (12, 58, 42, 255), rgba(GREEN), 2)
        ImageDraw.Draw(tg).ellipse([20, 20, 32, 32], fill=rgba(GREEN))
        tg.alpha_composite(ti, (40, (52 - ti.height) // 2 - 1))
        fade_up(c, tg, PCX + pw / 2 - 30 - tg.width / 2, top + 80, appear(t, tm, 0.3), rise=6)


def kanban(c, t, sc):
    xs = [210, 540, 870]
    cy = PCY + 70
    a = appear(t, sc["t0"], 0.4)
    fade_up(c, logo(200), PCX, 215, a)
    for i, name in enumerate(sc["cols"]):
        col = rounded(300, 560, 24, rgba(INK), LINE, 2)
        d = ImageDraw.Draw(col)
        ti = text_img(name, font("SemiBold", 30), WHITE)
        col.alpha_composite(ti, ((300 - ti.width) // 2, 22))
        _hdr_line(d, 24, 276, 84)
        for k in range(2):
            d.rounded_rectangle([24, 330 + k * 84, 276, 330 + k * 84 + 64], 14, fill=(26, 42, 36, 255))
        fade_up(c, col, xs[i], cy, a)
    if a < 1:
        return
    deal = rounded(256, 190, 18, rgba(INK), rgba(GREEN, 200), 2)
    dd = ImageDraw.Draw(deal)
    dd.text((24, 20), sc["deal"], font=font("Bold", 32), fill=rgba(WHITE))
    dd.text((24, 64), sc["deal_sub"], font=font("Regular", 23), fill=rgba(MUTED))
    f = font("SemiBold", 22)
    tw = f.getlength(sc["tag"])
    dd.rounded_rectangle([24, 120, 24 + tw + 50, 162], 21, fill=(12, 58, 42, 255), outline=rgba(GREEN), width=2)
    dd.ellipse([38, 136, 48, 146], fill=rgba(GREEN))
    dd.text((58, 126), sc["tag"], font=f, fill=rgba(GREEN))
    k = ease_in_out((t - sc["move_t"]) / 1.0) if t >= sc["move_t"] else 0
    place(c, deal, lerp(xs[0], xs[1], k), cy - 110)
    y = cy + 40
    for txt, tm in sc.get("more", []):
        row = Image.new("RGBA", (270, 50), (0, 0, 0, 0))
        row.alpha_composite(check_icon(36, GREEN, 4), (0, 7))
        ImageDraw.Draw(row).text((46, 8), txt, font=font("Medium", 25), fill=rgba(WHITE))
        fade_up(c, row, xs[1] + 6, y, appear(t, tm, 0.3), rise=8)
        y += 58


def stats(c, t, sc):
    if "title" in sc:
        txt, tm = sc["title"]
        fade_up(c, eyebrow(txt), PCX, 235, appear(t, tm, 0.4))
    y = sc.get("y0", 370)
    for txt, tm in sc["rows"]:
        ti = text_img(txt, font("Bold", 44), WHITE)
        row = rounded(860, 128, 24, rgba(INK), LINE, 2)
        row.alpha_composite(check_icon(60, GREEN, 6), (40, 34))
        row.alpha_composite(ti, (128, (128 - ti.height) // 2))
        fade_up(c, row, PCX, y, appear(t, tm, 0.35))
        y += 150


DRAW = {f.__name__: f for f in [hook, head, plain, cta_full, phones, dots, contact, form, checklist, chat, kanban,
                                stats]}
