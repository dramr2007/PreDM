# Hakim AI free male narration audition — 2026-10-22

Purpose: test a new, commercial-use-permitted **synthetic** male Arabic voice after the user rejected low-clarity narrators. This request authorizes only producing a private-review audio audition on the isolated experiment branch, not creating a public social post, not paid services, and not reuploading any published video.

Episode material: HAI-C0069 Confidence Interval, existing reviewed script.
Delivery: fluent MSA, clear fast pacing with pitch preserved, -16 LUFS, automated signal and Arabic-ASR checks, then human audio review required before publication. This does not supersede HAI-C0040 as the preferred reference until approved.

## Prior Audar attempts — blocked

The Audar-TTS V1 Flash attempts did not reach synthesis:
1. dependency conflict,
2. gated `neuphonic/neucodec` checkpoint,
3. `neuphonic/distill-neucodec` also returned gated 401.

No authentication bypass, token substitution, payment, or public posting is authorized.

## Habibi MSA public-weight audition — 2026-10-23

Test `SWivid/Habibi-TTS` Specialized/MSA only. The official model card states the specialized MSA weights use Apache-2.0; code uses MIT. Use the publicly distributed Audar `demo_male_1` synthetic sample only as a male reference prompt, not a recording of a real person. Produce an independent private sample and `QA_HABIBI_MSA.json`; do not publish it to social accounts.

Sources:
- https://huggingface.co/SWivid/Habibi-TTS
- https://github.com/SWivid/Habibi-TTS
- https://huggingface.co/audarai/Audar-TTS-V1-Flash
