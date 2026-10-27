# PUBLISHING HOLD — HAI-M0006

Status checked: 2026-10-27 06:23 Asia/Riyadh.

Do **not** publish `HAI-M0006-female.mp4`.

The GitHub Actions run [40431924572](https://github.com/dramr2007/PreDM/actions/runs/40431924572) completed technically, but the output is rejected for publication despite the automatic PASS flag:

- exact word recall: `0.545`
- automatic transcript contains material pronunciation distortions in medical/technical Arabic
- human listening review: `not_performed`
- visual review: `pending`
- Metricool HAI-M0006 post found: `false`

Publication remains blocked until the manual female-voice repair finishes and a new version passes:

1. human listening review of the full narration;
2. medical term pronunciation review;
3. stronger ASR verification without treating a low threshold as approval;
4. representative and full visual review;
5. full decode, audio level, silence and synchronization QA;
6. fresh Metricool duplicate/queue check.

No parallel render or publication was started by this check.
