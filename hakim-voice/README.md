# Hakim AI — Free Arabic Speech Trial

This is an **isolated experimental branch** dedicated to generating AI educational voiceover using Piper. It does not alter the PreDM main branch.

- Clip: HAI-C0041 Overfitting, from the user's existing 1000-script educational series.
- Piper model: `ar_JO-kareem-medium`; publicly available through `rhasspy/piper-voices` under repository MIT terms. Check the individual model card and any dataset terms before monetization.
- This branch uses **GitHub Actions on a public repository** (standard runner free under GitHub policy). It needs no paid TTS API or service credentials.
- The input and resulting artifact are PUBLIC. Never add passwords, patient information, private voice recordings, or sensitive material.
- Final video publishing remains via Metricool; this workflow generates audio only, and must pass Arabic pronunciation and technical QA before publication.
- After a run, download the `hakim-c0041-arabic-voice` Actions artifact.
- Voice should not be represented as the user's personal voice or the exact voice from HeyGen video HAI-C0040.

Sources:
https://huggingface.co/rhasspy/piper-voices/blob/main/ar/ar_JO/kareem/medium/MODEL_CARD
https://github.com/rhasspy/piper/blob/master/VOICES.md
