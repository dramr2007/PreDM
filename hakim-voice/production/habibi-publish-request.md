# HAI-C0069 full production request — 2026-10-23

Authorised by user: produce and publish a complete, factual, high-quality, 9:16 Hakim AI educational short on Confidence Interval, with clear, slightly quick, distinctive male Arabic narration and six scene-appropriate visuals.

Approved *technical trial*, not approval of identical prior timbre: GitHub run 39910185773 successfully synthesized Habibi-TTS Specialized MSA Apache-2.0 Arabic speech; trial QA duration 8.24 sec, peak 0.5519, low level 0.293. The run's final commit step failed only because a concurrent commit changed the repository; audio is safely archived in GitHub Action artifact 12481649835. The production renderer exists as hakim-voice/render_habibi_episode.py; validated source episode in hakim-voice/audar-episodes/HAI-C0069.json.

Run exactly one complete free CPU render now. Do not use Piper, SILMA, paid HeyGen, gated codecs, or restricted Unified/SAU/UAE weights. Store produced MP4 and QA in isolated experiment branch. Only publish after verifying actual output, Arabic speech and full video; social publishing separately via Metricool, no duplicates, respect YouTube quota and platform posting gaps.

## Correction run — 2026-10-23 13:43 Riyadh
The prior HAI-C0069 MP4 was intentionally blocked by QA for incorrect Arabic pronunciation and square-glyph titles. Replaced long clauses with shorter, pronunciation-friendly full MSA text; removed accelerated tempo, raised denoising steps, removed mixed Arabic/Latin numerals from headline/subtitles, and added per-scene faster-whisper source-audio intelligibility gate. Rerender only in isolated experimental branch. Do not publish if speech QA fails. Author request: publish repaired fully checked episode on connected social platforms as soon as actually ready, without duplicating prior episodes.
