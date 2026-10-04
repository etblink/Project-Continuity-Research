# NotebookLM Seven-Project Blueprint — Complete Transcript Provenance 0.1.0

Date preserved: 2026-10-04  
Status: **DERIVED REFERENCE ARTIFACT — COMPLETE — NONAUTHORITATIVE**

## 1. Source audio

Primary secondary-synthesis audio:

```text
filename = Evan_Kotler_s_Seven_Project_Blueprint.m4a
duration_seconds = 2257.699410
duration_approx = 00:37:37.699
sha256 = 6c59de01b791e04b7e103241f993763755fdd435043c01467c984bbe9b106494
```

Governing audio source record:

`sources/NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_SOURCE_2026_10_04.md`

## 2. Transcription service

```text
service = TurboScribe.ai
date = 2026-10-04
```

The first free-tier transcription stopped at approximately 30 minutes, so the remaining audio was separately transcribed from a deliberately overlapping clip.

No claim is made that automatic speech recognition is verbatim-perfect.

## 3. First transcript segment

Original uploaded files:

```text
TXT = Evan Kotler s Seven Project Blueprint(1).txt
TXT size_bytes = 30406
TXT sha256 = 168c6cf64c9bfdafb062028653fa8948abe458a696989a966f5821a7d86e94ca

SRT = Evan Kotler s Seven Project Blueprint.srt
SRT size_bytes = 60154
SRT sha256 = 799258866ae382e4bf967cf017efda708e275494130682522852473c3ced50cf
```

Previously frozen partial artifacts remain immutable:

- `NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_RAW_PARTIAL_0_1_0.txt`
- `NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_TIMESTAMPED_PARTIAL_0_1_0.srt`
- `NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_PROVENANCE_0_1_0.md`

The first SRT ends with a truncated cue:

```text
861
00:29:55,830 --> 00:29:58,970
Mathematical physics, specifically NFC, derives...
```

## 4. Remainder audio and transcript

Remainder audio was cut from the original beginning at:

```text
00:29:50.000
```

The overlap is intentional so the merge can be anchored to shared spoken text rather than an inferred hard cut.

Remainder audio identity:

```text
filename = NotebookLM_Seven_Project_Blueprint_REMAINDER_FROM_29m50s.m4a
sha256 = 67a170ca204955abf46d801244f796f49c9b9d4497bfbb9e7ef8a797aeaad7e6
```

Original uploaded remainder transcript files:

```text
TXT = NotebookLM Seven Project Blueprint REMAINDER FROM 29m50s.txt
TXT size_bytes = 7732
TXT sha256 = 639b3d15fd7a6bd154355d48446da41830fce2fb4eb84afd255bab4c33fcfa70

SRT = NotebookLM Seven Project Blueprint REMAINDER FROM 29m50s.srt
SRT size_bytes = 14572
SRT sha256 = 2575f89daa1cdf0b22f90686e4e577d8cb34e658d1dc4fba734b4f9aa38f075b
```

Frozen remainder artifacts:

- `sources/NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_REMAINDER_RAW_0_1_0.txt`
- `sources/NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_REMAINDER_TIMESTAMPED_0_1_0.srt`

## 5. SRT export settings

The same TurboScribe SRT settings were used:

```text
max_words_per_segment = 8
max_duration_per_segment_seconds = 10
max_characters_per_segment = 80
sentence_aware_segmentation = enabled
```

## 6. Mechanical merge rule

The complete transcript is a derived mechanical splice.

### TXT

1. Preserve first-part transcript through:
   `Let's trace the logic.`
2. Drop the first-part truncated sentence:
   `Mathematical physics, specifically NFC, derives...`
3. Drop the TurboScribe 30-minute paywall/truncation notice.
4. In the remainder transcript, skip the deliberately duplicated overlap and begin at the full sentence:
   `Mathematical physics, specifically NFC, derives physical invariance from finite relational structures.`
5. Drop the second TurboScribe service notice at the end.

The first TurboScribe service notice at the beginning remains present because it was part of the first raw transcript export.

### SRT

1. Preserve first-part cues 1 through 860.
2. Drop truncated cue 861.
3. Drop remainder cues 1 through 3 because they duplicate the overlap:
   - key to actualizing the global universe;
   - Lay it on me;
   - Let's trace the logic.
4. Preserve remainder cues 4 through 202.
5. Add exactly `00:29:50.000` to all retained remainder timestamps.
6. Renumber the merged cues consecutively.

Result:

```text
merged_cue_count = 1059
first_retained_remainder_timestamp = 00:29:55,810
final_transcript_timestamp = 00:37:37,370
source_audio_end = approximately 00:37:37.699
```

The ~0.329-second difference between final SRT cue end and audio duration is ordinary subtitle boundary slack, not missing transcript content.

## 7. Complete derived artifacts

### Searchable text

`sources/NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_COMPLETE_0_1_0.txt`

```text
size_bytes = 37753
sha256 = 22374939741fe1e927ffc4f96f7d82c7dd5c69d4b03f845e12c4d98f2682c5ec
```

### Timestamped transcript

`sources/NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_TRANSCRIPT_TIMESTAMPED_COMPLETE_0_1_0.srt`

```text
size_bytes = 74560
sha256 = 739f3c238976bf543a6be8feef21d797605d9b6a1c973a6b2ecd765b941e3b94
```

## 8. Supersession rule

The complete artifacts supersede the PARTIAL transcript **for convenience of reference only**.

They do not delete, rewrite, or invalidate the partial artifacts. The partial transcript remains historical evidence of the first transcription pass and its 30-minute truncation.

No audio-source authority is transferred to either transcript.

## 9. Epistemic hierarchy

```text
PROJECT-NATIVE EVIDENCE / CANON
    >
NOTEBOOKLM SECONDARY AUDIO SYNTHESIS
    >
TURBOSCRIBE DERIVED TRANSCRIPT
```

The transcript is useful to establish what the NotebookLM synthesis said.

It is not evidence that NotebookLM's claims about any project are correct.

## 10. Particularly important caution

The completed tail contains strong claims that CPI-0 has already treated as speculative or rejected, including:

- HiVenues/Hive as a physical empirical sensor array for NFC/PGH;
- a requirement to force one `state.yaml` model across all repositories;
- upgrading Project Observatory directly into an active cross-project control plane.

Preserving these statements faithfully is important precisely because the transcript is a source artifact, not a corrected research summary.

CPI-0 adjudications remain separate.

## 11. Stage-6B boundary

Completing this transcript does not execute or contaminate Stage 6B.

The Stage-6B independent evaluator may use this transcript only as a secondary source when relevant and must not substitute it for native repository evidence.
