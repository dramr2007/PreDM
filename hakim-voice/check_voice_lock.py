"""Validate the user-approved voice for new HAKIM AI episodes before publishing.

A verified provider voice ID does not bypass HeyGen licensing or confirm that a
different TTS engine is perceptually identical. Never publish private reference
audio or other user assets to GitHub.
"""
import argparse, json
from pathlib import Path

LOCK = json.loads(Path(__file__).with_name("VOICE_LOCK.json").read_text(encoding="utf-8"))

def check(episode, engine, voice_id="", authorized=False, qa_passed=False):
    if episode <= 50:
        return "Legacy episode: do not create a duplicate Metricool post."
    if engine == "heygen":
        if voice_id != LOCK["exact_voice_id"]:
            raise SystemExit("VOICE LOCK FAIL: incorrect HeyGen voice ID")
        if not authorized:
            raise SystemExit("VOICE LOCK FAIL: voice rights/credits not verified")
    elif engine == "validated_clone":
        if not authorized or not qa_passed:
            raise SystemExit("VOICE LOCK FAIL: authorized reference + A/B voice QC required")
    else:
        raise SystemExit("VOICE LOCK FAIL: unapproved voice engine (including Nabra/Piper)")
    if not qa_passed:
        raise SystemExit("VOICE LOCK FAIL: audio/visual QA missing")
    return "VOICE LOCK PASS: verify Metricool duplicates and publication rules next"

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--episode", type=int, required=True)
    ap.add_argument("--engine", required=True)
    ap.add_argument("--voice-id", default="")
    ap.add_argument("--authorized", action="store_true")
    ap.add_argument("--qa-passed", action="store_true")
    a=ap.parse_args()
    print(check(a.episode,a.engine,a.voice_id,a.authorized,a.qa_passed))
