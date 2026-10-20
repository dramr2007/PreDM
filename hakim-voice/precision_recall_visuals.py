"""Educational, scene-specific vector infographics for Precision and Recall episodes.
Called by render_free_episode.py; no external assets or third-party illustrations.
"""

def draw_visual(d, v, ar, en, rect, C):
    green, red, yellow, pale, blue = C['teal'], C['orange'], C['yellow'], C['pale'], C['blue']
    def grid(total, good, neutral=False, fade_good=False, label=''):
        ar(d, 'توقعات إيجابية' if total == 10 else 'حالات إيجابية فعلية', 360, 444, 32, pale, True)
        cols = 5
        step_x = 97
        step_y = 76 if total == 20 else 114
        top = 516 if total == 20 else 550
        for i in range(total):
            x = 124 + (i % cols) * step_x
            y = top + (i // cols) * step_y
            ok = i < good
            color = '#356B78' if neutral or (fade_good and ok) else (green if ok else red)
            rect(d, (x, y, x+74, y+61), color, 13)
            en(d, '?' if neutral else ('+' if ok else '!'), x+37, y+30, 28,
               '#FFFFFF' if not fade_good or not ok else '#A6D4D5', True)
        ar(d, label, 360, 929, 29, yellow, True)
    def formula(title, expression, example, explanation):
        en(d, title, 360, 455, 42, blue, True)
        rect(d, (103, 533, 617, 788), '#20546A', 24, '#2C768A', 2)
        en(d, expression, 360, 610, 33, pale, True)
        d.line((165, 650, 555, 650), fill=yellow, width=5)
        en(d, example, 360, 722, 51, yellow, True)
        ar(d, explanation, 360, 882, 31, green, True)
    if v == 'precisionalerts':
        grid(10, 0, neutral=True, label='عشرة إنذارات تحتاج مراجعة')
    elif v == 'precisioncards':
        grid(10, 8, label='ثمانية صحيحة وإنذاران كاذبان')
    elif v == 'precisionerrors':
        grid(10, 8, fade_good=True, label='إنذاران كاذبان من عشرة')
    elif v == 'precisionformula':
        formula('PRECISION', 'TP / (TP + FP)', '8 / 10 = 80%', 'صحة التنبؤات الإيجابية')
    elif v == 'precisionvsrecall':
        for y, term, label, border in [
            (460, 'PRECISION', 'كم إنذارًا إيجابيًا صحيح؟', green),
            (680, 'RECALL', 'كم حالة إيجابية اكتشفنا؟', red)]:
            rect(d, (107, y, 613, y+168), '#1D5369', 20, border, 3)
            en(d, term, 360, y+53, 34, yellow, True)
            ar(d, label, 360, y+112, 30, pale, True)
    elif v == 'precisiontakeaway':
        ar(d, 'من عشرة إنذارات', 360, 475, 36, pale, True)
        en(d, '8 CORRECT', 360, 602, 51, green, True)
        en(d, '2 FALSE', 360, 708, 49, red, True)
        en(d, 'PRECISION = 80%', 360, 877, 34, yellow, True)
    elif v == 'recallcards':
        grid(20, 18, label='اكتشفنا 18 وفاتتنا حالتان')
    elif v == 'recallmissed':
        grid(20, 18, fade_good=True, label='حالتان إيجابيتان لم تُكتشفا')
    elif v == 'recallformula':
        formula('RECALL', 'TP / (TP + FN)', '18 / 20 = 90%', 'اكتشاف الحالات الإيجابية الفعلية')
    elif v == 'recallthreshold':
        ar(d, 'عتبة القرار تغيّر النتائج', 360, 470, 33, pale, True)
        d.line((128, 644, 590, 644), fill=blue, width=13)
        d.ellipse((324, 615, 383, 674), fill=yellow)
        en(d, 'LOW', 153, 717, 26, green, True)
        en(d, 'HIGH', 558, 717, 26, red, True)
        rect(d, (107, 790, 613, 887), '#1D5369', 18)
        ar(d, 'وازن بين المكتشف والفائت', 360, 837, 29, yellow, True)
    elif v == 'recalltakeaway':
        en(d, '18 / 20', 360, 548, 75, green, True)
        en(d, 'RECALL = 90%', 360, 715, 47, yellow, True)
        ar(d, 'الحساسية لا تكفي وحدها', 360, 882, 31, pale, True)
    else:
        raise ValueError('Unsupported Precision/Recall visual: ' + v)
