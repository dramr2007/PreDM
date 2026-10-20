#!/usr/bin/env python3
"""Isolated safe adapter for Precision/Recall scene-specific infographics.

Reuses the already verified Piper renderer, replacing only its unsupported
visual fallback in memory. Does not alter other episodes or source files.
"""
import sys
from pathlib import Path

base=Path(__file__).resolve().parent
source=(base/"render_free_episode.py").read_text(encoding="utf-8")
old='    else:\n        for j,(cap,eng) in enumerate([("الجودة","QUALITY"),("الذاكرة","MEMORY"),("السرعة","LATENCY")]):'
new='    elif v.startswith("precision") or v.startswith("recall"):\n        from precision_recall_visuals import draw_visual\n        draw_visual(d,v,ar,en,rect,C)\n    else:\n        for j,(cap,eng) in enumerate([("الجودة","QUALITY"),("الذاكرة","MEMORY"),("السرعة","LATENCY")]):'
if source.count(old)!=1:
    raise RuntimeError("Renderer source changed; cannot safely patch visual branch")
source=source.replace(old,new)
source=source.replace('ID=E["id"]\nOUTPUT=', 'ID=E["id"]\nif len(E.get("segments",[]))!=6: raise ValueError("Expected six segments")\nOUTPUT=',1)
if len(sys.argv)!=2:
    raise SystemExit("Usage: render_precision_recall.py path/to/HAI-C####.json")
exec(compile(source,str(base/"render_free_episode.py"),"exec"),{"__name__":"__main__","__file__":str(base/"render_free_episode.py")})
