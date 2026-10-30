"""Cenas de motion graphics. Cada função desenha no canvas RGBA:
- cenas 'split': canvas = painel superior (1080x960)
- cenas 'full' : canvas = quadro inteiro (1080x1920), por cima do apresentador
Todos os tempos já estão em tempo de saída (segundos)."""
from PIL import Image, ImageDraw

from mg import (GREEN, GREEN_50, GREEN_600, INK, INK_600, INK_700, MUTED, RED, W, WHITE, appear, arrow_icon,
                avatar, bubble, card, check_icon, chip, clamp01, ease_back, ease_in_out, ease_out, font, headline,
                label_box, lerp, logo, icon, place, pop, rgba, rounded, stamp, stamp_anim, text_img, typing, x_icon)

PCX, PCY = W / 2, 560  # centro útil do painel (abaixo do banner/progresso)


# ------------------------------------------------------------------ full
def hook(c, t, sc):
    """Caixas de gancho empilhadas sobre o apresentador (como o hook da referência)."""
    y = sc.get("y", 1250)
    for i, (txt, kind, t0) in enumerate(sc["boxes"]):
        f = font("ExtraBold", sc.get("size", 54))
        fill, col = (GREEN, INK) if kind == "green" else (WHITE, INK)
        box = label_box(txt, f, fill, col, padx=34, pady=16, r=14)
        pop(c, box, W / 2, y + i * 104, appear(t, t0, 0.3), rotate=sc.get("rot", -2) if i == 0 else 0)


def head(c, t, sc):
    headline(c, t, sc["items"], sc.get("y", 260), sc.get("size", 92), align_top=True)
    for st in sc.get("stamps", []):
        stamp_anim(c, stamp(st["text"], st.get("color", GREEN), st.get("size", 70), st.get("rot", -7)),
                   st.get("x", W / 2), st["y"], t, st["t"])


def stamp_full(c, t, sc):
    stamp_anim(c, stamp(sc["text"], sc.get("color", GREEN), sc.get("size", 84), sc.get("rot", -7)),
               sc.get("x", W / 2), sc.get("y", 420), t, sc["t"])


def plain(c, t, sc):
    pass


# ------------------------------------------------------------------ split
def _card_header(cd, x, y, letter, name, sub, size=84, letter_bg=GREEN):
    cd.alpha_composite(avatar(size, letter, letter_bg), (x, y))
    cd.alpha_composite(text_img(name, font("Bold", 38), WHITE), (x + size + 22, y + 2))
    cd.alpha_composite(text_img(sub, font("Medium", 27), MUTED), (x + size + 22, y + 48))


def chat(c, t, sc):
    cw, ch = 860, sc.get("h", 600)
    base = card(cw, ch)
    cd = base
    p0 = 40  # padding do glow
    _card_header(cd, p0 + 36, p0 + 30, sc.get("letter", "C"), sc["name"], sc["sub"])
    ImageDraw.Draw(cd).line([(p0 + 30, p0 + 140), (p0 + cw - 30, p0 + 140)], fill=(255, 255, 255, 30), width=2)
    a = appear(t, sc["t0"], 0.35)
    place(c, cd, PCX, PCY + 20 + (1 - ease_out(a)) * 60, 1, ease_out(a * 1.5))
    if a <= 0:
        return
    top = PCY + 20 - ch / 2
    y = top + 170
    left = PCX - cw / 2 + 36
    right = PCX + cw / 2 - 36
    for txt, side, tm in sc["msgs"]:
        b = bubble(txt, side, maxw=700, size=42)
        if side == "in" and tm - 0.55 <= t < tm:
            ty = typing(t)
            place(c, ty, left + ty.width / 2, y + ty.height / 2)
        if t >= tm:
            x = left + b.width / 2 if side == "in" else right - b.width / 2
            pop(c, b, x, y + b.height / 2, appear(t, tm, 0.3), from_scale=0.8, rise=20)
        y += b.height + 18
    if "tag" in sc:
        txt, tm = sc["tag"]
        tg = label_box(txt, font("Bold", 30), GREEN, INK, padx=24, pady=8, r=22)
        pop(c, tg, PCX + cw / 2 - 40 - tg.width / 2, top + 72, appear(t, tm, 0.3), from_scale=1.6, rise=0)
    if "stamp" in sc:
        txt, tm = sc["stamp"]
        stamp_anim(c, stamp(txt, GREEN, 60, -6), PCX + 170, 255, t, tm)


def proposal(c, t, sc):
    cw, ch = 860, 520
    cd = card(cw, ch)
    p0 = 40
    # ícone de envelope
    env = Image.new("RGBA", (84, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(env)
    d.ellipse([0, 0, 83, 83], fill=rgba(INK_600))
    d.rounded_rectangle([18, 26, 66, 58], 5, outline=rgba(GREEN), width=4)
    d.line([(20, 29), (42, 46), (64, 29)], fill=rgba(GREEN), width=4)
    cd.alpha_composite(env, (p0 + 36, p0 + 30))
    cd.alpha_composite(text_img(sc["name"], font("Bold", 38), WHITE), (p0 + 142, p0 + 32))
    cd.alpha_composite(text_img(sc["sub"], font("Medium", 27), MUTED), (p0 + 142, p0 + 80))
    ImageDraw.Draw(cd).line([(p0 + 30, p0 + 140), (p0 + cw - 30, p0 + 140)], fill=(255, 255, 255, 30), width=2)
    cd.alpha_composite(text_img("Assunto", font("Medium", 28), MUTED), (p0 + 40, p0 + 172))
    cd.alpha_composite(text_img(sc["title"], font("ExtraBold", 50), WHITE), (p0 + 40, p0 + 208))
    att = rounded(470, 76, 18, rgba(INK_600))
    ad = ImageDraw.Draw(att)
    ad.rounded_rectangle([18, 16, 58, 60], 6, fill=rgba(RED))
    ad.text((24, 26), "PDF", font=font("Bold", 16), fill=rgba(WHITE))
    ad.text((76, 19), sc["file"], font=font("Medium", 28), fill=rgba(WHITE))
    cd.alpha_composite(att, (p0 + 40, p0 + 300))
    a = appear(t, sc["t0"], 0.35)
    place(c, cd, PCX, PCY + 20 + (1 - ease_out(a)) * 60, 1, ease_out(a * 1.5))
    if "sent" in sc:
        txt, tm = sc["sent"]
        bx = label_box(txt, font("ExtraBold", 36), GREEN, INK, padx=26, pady=10, r=24)
        pop(c, bx, PCX + 250, PCY + 20 + 175, appear(t, tm, 0.3), from_scale=1.5, rise=0)
    if "stamp" in sc:
        txt, tm = sc["stamp"]
        stamp_anim(c, stamp(txt, GREEN, 60, -6), PCX + 170, 255, t, tm)


def disconnect(c, t, sc):
    """Dois cartões (departamentos) desconectados com X vermelho no meio."""
    for i, (title, sub, tm) in enumerate(sc["cards"]):
        cw, ch = 400, 300
        cd = card(cw, ch)
        p0 = 40
        ic = avatar(80, title[0], GREEN if i == 0 else GREEN_600)
        cd.alpha_composite(ic, (p0 + (cw - 80) // 2, p0 + 40))
        ti = text_img(title, font("ExtraBold", 38), WHITE)
        cd.alpha_composite(ti, (p0 + (cw - ti.width) // 2, p0 + 140))
        si = text_img(sub, font("Medium", 28), MUTED)
        cd.alpha_composite(si, (p0 + (cw - si.width) // 2, p0 + 200))
        x = 270 if i == 0 else 810
        pop(c, cd, x, PCY, appear(t, tm, 0.35), from_scale=0.8)
    tl = sc["link_t"]
    if t >= tl:
        k = ease_out((t - tl) / 0.4)
        d = ImageDraw.Draw(c)
        x0, x1 = 470, lerp(470, 610, k)
        xx = x0
        while xx < x1:
            d.line([(xx, PCY), (min(xx + 14, x1), PCY)], fill=rgba(WHITE, 160), width=5)
            xx += 26
    if t >= sc["x_t"]:
        pop(c, x_icon(120, WHITE, RED, 12), PCX, PCY, appear(t, sc["x_t"], 0.3), from_scale=1.8, rise=0)
    if "label" in sc:
        txt, tm = sc["label"]
        lb = label_box(txt, font("ExtraBold", 40), WHITE, INK, padx=28, pady=12, r=12)
        pop(c, lb, PCX, PCY + 250, appear(t, tm, 0.3))


def chips(c, t, sc):
    if "title" in sc:
        items, tm = sc["title"]
        f = font("ExtraBold", 46)
        x_total = sum(f.getlength(w) for w, _ in items) + f.getlength(" ") * (len(items) - 1)
        x = W / 2 - x_total / 2
        a = appear(t, tm, 0.35)
        for w_, hi in items:
            im = text_img(w_, f, GREEN if hi else WHITE)
            place(c, im, x + im.width / 2, sc.get("title_y", 285) + (1 - ease_out(a)) * 20, 1, ease_out(a))
            x += f.getlength(w_) + f.getlength(" ")
    if "sub" in sc:
        txt, tm = sc["sub"]
        lb = label_box(txt, font("ExtraBold", 34), WHITE, INK, padx=24, pady=10, r=12)
        pop(c, lb, W / 2, sc.get("sub_y", 375), appear(t, tm, 0.3))
    y = sc.get("y0", 420)
    for big, small, accent, tm in sc["chips"]:
        big_img = None
        if big == "check":
            big_img = check_icon(84, INK, accent, 10)
        elif big == "x":
            big_img = x_icon(84, INK, accent, 10)
        ch = chip(big, small, accent, big_img=big_img)
        p = appear(t, tm, 0.3)
        if p > 0:
            place(c, ch, W / 2 + (1 - ease_out(p)) * -80, y, lerp(0.85, 1, ease_back(p)), ease_out(p * 1.5))
        y += sc.get("dy", 150)


def brand(c, t, sc):
    t0 = sc["t0"]
    a = appear(t, t0, 0.45)
    glow = rounded(700, 260, 130, (0, 0, 0, 0), glow=rgba(GREEN, 70))
    place(c, glow, PCX, 470, 1, ease_out(a))
    pop(c, logo(sc.get("w", 600)), PCX, 470, a, from_scale=0.7, rise=0)
    if "tag" in sc:
        txt, tm = sc["tag"]
        lb = rounded(10, 10, 5, (0, 0, 0, 0))
        f = font("Bold", 32)
        ti = text_img(txt, f, GREEN)
        lb = rounded(ti.width + 80, 66, 33, rgba(INK, 220), rgba(GREEN, 170), 2)
        ImageDraw.Draw(lb).ellipse([28, 27, 40, 39], fill=rgba(GREEN))
        lb.alpha_composite(ti, (54, (66 - ti.height) // 2 - 1))
        pop(c, lb, PCX, 690, appear(t, tm, 0.3))


def contact(c, t, sc):
    cw, ch = 880, 640
    cd = card(cw, ch)
    p0 = 40
    _card_header(cd, p0 + 36, p0 + 32, "C", sc["name"], sc["sub"], 92)
    ImageDraw.Draw(cd).line([(p0 + 30, p0 + 150), (p0 + cw - 30, p0 + 150)], fill=(255, 255, 255, 30), width=2)
    a = appear(t, sc["t0"], 0.35)
    place(c, cd, PCX, PCY + 30 + (1 - ease_out(a)) * 60, 1, ease_out(a * 1.5))
    top = PCY + 30 - ch / 2
    y = top + 230
    for title, sub, color, tm in sc["rows"]:
        row = rounded(800, 120, 24, rgba(INK_600, 255), rgba(color, 150), 2)
        d = ImageDraw.Draw(row)
        d.rounded_rectangle([24, 24, 96, 96], 18, fill=rgba(color))
        row.alpha_composite(text_img(title, font("Bold", 36), WHITE), (122, 18))
        row.alpha_composite(text_img(sub, font("Medium", 27), MUTED), (122, 64))
        row.alpha_composite(check_icon(48, INK, None, 7), (36, 36))
        p = appear(t, tm, 0.35)
        if p > 0:
            place(c, row, PCX + (1 - ease_out(p)) * 140, y, 1, ease_out(p * 1.4))
        y += 140
    if "footer" in sc:
        txt, tm = sc["footer"]
        lb = label_box(txt, font("ExtraBold", 36), GREEN, INK, padx=26, pady=10, r=24)
        pop(c, lb, PCX, top + ch - 20, appear(t, tm, 0.3), from_scale=1.4, rise=0)


def form(c, t, sc):
    cw, ch = 860, 620
    cd = card(cw, ch)
    p0 = 40
    cd.alpha_composite(text_img(sc["title"], font("ExtraBold", 42), WHITE), (p0 + 40, p0 + 34))
    cd.alpha_composite(text_img(sc["sub"], font("Medium", 27), MUTED), (p0 + 40, p0 + 92))
    d = ImageDraw.Draw(cd)
    fy = p0 + 160
    for lbl in sc["fields"]:
        d.text((p0 + 40, fy), lbl, font=font("Medium", 26), fill=rgba(MUTED))
        d.rounded_rectangle([p0 + 40, fy + 38, p0 + cw - 40, fy + 38 + 58], 12, fill=rgba(INK), outline=(255, 255, 255, 40), width=2)
        fy += 110
    a = appear(t, sc["t0"], 0.35)
    cy = PCY + 30
    place(c, cd, PCX, cy + (1 - ease_out(a)) * 60, 1, ease_out(a * 1.5))
    if a < 1:
        return
    top = cy - ch / 2
    # cursor piscando no primeiro campo
    if int(t * 2.4) % 2 == 0:
        ImageDraw.Draw(c).line([(PCX - cw / 2 + 64, top + 210), (PCX - cw / 2 + 64, top + 244)], fill=rgba(GREEN), width=4)
    for i, tm in enumerate(sc["req_t"]):
        b = label_box(sc.get("req", "Pendente"), font("Bold", 24), RED, WHITE, padx=16, pady=4, r=14)
        pop(c, b, PCX + cw / 2 - 60 - b.width / 2, top + 227 + i * 110, appear(t, tm, 0.25), from_scale=1.5, rise=0)
    if "stamp" in sc:
        txt, tm = sc["stamp"]
        stamp_anim(c, stamp(txt, RED, 62, -6), PCX + 150, 250, t, tm)


def memory(c, t, sc):
    cw, ch = 860, 600
    cd = card(cw, ch)
    p0 = 40
    cd.alpha_composite(text_img(sc["title"], font("ExtraBold", 40), WHITE), (p0 + 40, p0 + 34))
    a = appear(t, sc["t0"], 0.35)
    cy = PCY + 40
    place(c, cd, PCX, cy + (1 - ease_out(a)) * 60, 1, ease_out(a * 1.5))
    top = cy - ch / 2
    y = top + 150
    for txt, tm, ok in sc["rows"]:
        row = rounded(780, 92, 20, rgba(INK_600))
        row.alpha_composite(text_img(txt, font("SemiBold", 34), WHITE if (t < tm or ok) else RED), (100, 20))
        d = ImageDraw.Draw(row)
        d.ellipse([28, 24, 72, 68], outline=(255, 255, 255, 120), width=3)
        if t >= tm:
            k = ease_back((t - tm) / 0.3)
            ic = (check_icon(44, INK, GREEN, 6) if ok else x_icon(44, WHITE, RED, 6))
            if k > 0.05:
                ic = ic.resize((max(1, int(44 * k)), max(1, int(44 * k))))
                row.alpha_composite(ic, (int(50 - ic.width / 2), int(46 - ic.height / 2)))
        place(c, row, PCX, y + 46, 1, ease_out(a * 1.5))
        y += 108
    if "stamp" in sc:
        txt, tm = sc["stamp"]
        stamp_anim(c, stamp(txt, RED, 56, -7), PCX + 240, top + 30, t, tm)


def kanban(c, t, sc):
    cols = sc["cols"]
    a = appear(t, sc["t0"], 0.35)
    xs = [200, 540, 880]
    for i, name in enumerate(cols):
        col = rounded(310, 560, 26, rgba(INK_700, 240), rgba(GREEN, 70), 2)
        d = ImageDraw.Draw(col)
        ti = text_img(name, font("Bold", 32), WHITE)
        col.alpha_composite(ti, ((310 - ti.width) // 2, 26))
        d.line([(24, 88), (286, 88)], fill=rgba(GREEN, 120 if i == 1 else 40), width=3)
        for k in range(2):
            d.rounded_rectangle([24, 380 + k * 80, 286, 380 + k * 80 + 60], 14, fill=(255, 255, 255, 12))
        place(c, col, xs[i], PCY + 70 + (1 - ease_out(appear(t, sc["t0"] + i * 0.08, 0.35))) * 50, 1,
              ease_out(appear(t, sc["t0"] + i * 0.08, 0.35) * 1.5))
    place(c, logo(190), PCX, 250, 1, ease_out(a))
    # cartão do negócio que se move
    deal = rounded(270, 190, 20, rgba(INK_600), rgba(GREEN, 220), 3, glow=rgba(GREEN, 80))
    dd = ImageDraw.Draw(deal)
    dd.text((62, 54), sc["deal"], font=font("Bold", 34), fill=rgba(WHITE))
    dd.text((62, 98), sc["deal_sub"], font=font("Medium", 24), fill=rgba(MUTED))
    tg = label_box(sc["tag"], font("Bold", 24), GREEN, INK, padx=14, pady=4, r=14)
    deal.alpha_composite(tg, (62, 138))
    tm = sc["move_t"]
    k = ease_in_out((t - tm) / 0.55) if t >= tm else 0
    lift = 1 + 0.08 * (1 - abs(2 * k - 1)) if 0 < k < 1 else 1
    p = appear(t, sc["t0"] + 0.25, 0.3)
    pop(c, deal, lerp(xs[0], xs[1], k), PCY + 70 - 120 - (lift - 1) * 120, p, from_scale=0.8) if p < 1 else \
        place(c, deal, lerp(xs[0], xs[1], k), PCY + 70 - 120 - (lift - 1) * 120, lift)
    y = PCY + 70 + 30
    for txt, tm2 in sc.get("more", []):
        b = label_box(txt, font("Bold", 26), WHITE, INK, padx=18, pady=8, r=18)
        bb = Image.new("RGBA", (b.width + 44, b.height), (0, 0, 0, 0))
        bb.alpha_composite(check_icon(40, INK, GREEN, 5), (0, (b.height - 40) // 2))
        bb.alpha_composite(b, (44, 0))
        pop(c, bb, xs[1], y + 30, appear(t, tm2, 0.3))
        y += 80


def flow(c, t, sc):
    y_mid = PCY + 20
    for i, (txt, tm) in enumerate(sc["sources"]):
        bx = rounded(380, 150, 26, rgba(INK_700, 245), rgba(GREEN, 120), 2, glow=rgba(GREEN, 40))
        bx.alpha_composite(check_icon(64, INK, GREEN, 8), (40 + 30, 40 + 43))
        bx.alpha_composite(text_img(txt, font("ExtraBold", 40), WHITE), (40 + 112, 40 + 44))
        pop(c, bx, 270, y_mid - 110 + i * 220, appear(t, tm, 0.35))
    ta = sc["arrow_t"]
    if t >= ta:
        k = ease_out((t - ta) / 0.45)
        d = ImageDraw.Draw(c)
        for yy in (y_mid - 110, y_mid + 110):
            x0, y0, x1, y1 = 470, yy, 650, y_mid
            xe, ye = lerp(x0, x1, k), lerp(y0, y1, k)
            d.line([(x0, y0), (xe, ye)], fill=rgba(GREEN), width=7)
        if k > 0.9:
            place(c, arrow_icon(70, GREEN, 9), 640, y_mid)
    tc = sc["crm_t"]
    bx = rounded(330, 330, 40, rgba(INK, 250), rgba(GREEN, 230), 3, glow=rgba(GREEN, 110))
    bx.alpha_composite(icon(120), (40 + 105, 40 + 55))
    ti = text_img(sc.get("crm", "CRM"), font("ExtraBold", 48), WHITE)
    bx.alpha_composite(ti, (40 + (330 - ti.width) // 2, 40 + 196))
    pop(c, bx, 860, y_mid, appear(t, tc, 0.35), from_scale=0.6, rise=0)


def cta(c, t, sc):
    t0 = sc["t0"]
    a = appear(t, t0, 0.45)
    glow = rounded(640, 240, 120, (0, 0, 0, 0), glow=rgba(GREEN, 60))
    place(c, glow, PCX, 370, 1, ease_out(a))
    pop(c, logo(520), PCX, 370, a, from_scale=0.7, rise=0)
    if "tagline" in sc:
        items, tm = sc["tagline"]
        f = font("Bold", 40)
        total = sum(f.getlength(w) for w, _ in items) + f.getlength(" ") * (len(items) - 1)
        x = W / 2 - total / 2
        p = appear(t, tm, 0.35)
        for w_, hi in items:
            im = text_img(w_, f, GREEN if hi else WHITE)
            place(c, im, x + im.width / 2, 545 + (1 - ease_out(p)) * 20, 1, ease_out(p))
            x += f.getlength(w_) + f.getlength(" ")
    txt, tm = sc["button"]
    f = font("ExtraBold", 46)
    ti = text_img(txt, f, INK)
    bw, bh = ti.width + 170, 120
    btn = rounded(bw, bh, bh // 2, rgba(GREEN), glow=rgba(GREEN, 150))
    btn.alpha_composite(ti, (40 + 56, 40 + (bh - ti.height) // 2 - 2))
    btn.alpha_composite(arrow_icon(56, INK, 7), (40 + bw - 100, 40 + (bh - 56) // 2))
    p = appear(t, tm, 0.35)
    if p > 0:
        import math
        pulse = 1 + 0.035 * math.sin((t - tm) * 5.5) if p >= 1 else 1
        pop(c, btn, PCX, 720, p, from_scale=0.6, rise=0) if p < 1 else place(c, btn, PCX, 720, pulse)
    if "sub" in sc:
        txt, tm = sc["sub"]
        im = text_img(txt, font("Medium", 32), (190, 210, 200))
        p = appear(t, tm, 0.35)
        place(c, im, PCX, 840 + (1 - ease_out(p)) * 16, 1, ease_out(p))


DRAW = {f.__name__: f for f in [hook, head, stamp_full, plain, chat, proposal, disconnect, chips, brand, contact,
                                form, memory, kanban, flow, cta]}
