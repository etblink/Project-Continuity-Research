# Incident Corpus Schema

Version: 0.1.0
Status: Working research instrument; not a frozen standard.

## Purpose

This schema is used to reconstruct concrete long-horizon human-AI project incidents before deriving a final failure taxonomy or architecture.

The corpus must distinguish **what happened** from **how we interpret it**.

## Evidence status

Each incident receives one evidence status:

- `R0 — recollection only`: remembered, but no recoverable supporting record has yet been located.
- `R1 — cross-chat reconstruction`: supported by retained conversation history or successor summaries, but not yet checked against the original raw turn sequence.
- `R2 — artifact corroborated`: supported by a repository artifact, issue, PR, handoff, state file, test output, or other durable record.
- `R3 — transcript corroborated`: checked against the relevant raw conversation turns.
- `R4 — multiply corroborated`: independently supported by both transcript and durable project evidence.

Evidence status describes **corroboration**, not importance.

## Incident fields

### Identity

- `Incident ID`
- `Project`
- `Approximate date / phase`
- `Evidence status`
- `Confidence`

### Reconstruction

1. **Observed incident** — What concretely happened?
2. **Local model frame / working assumption** — What did the AI appear to be optimizing for or treating as true? Avoid claims about inaccessible internal mental states.
3. **Authoritative reality** — What was actually true, current, frozen, demonstrated, or governing?
4. **Human intervention** — What did the human notice, challenge, reframe, authorize, or correct?
5. **Outcome** — What changed after the intervention?

### Interpretation

6. **Candidate failure dimensions** — Non-exclusive provisional labels only.
7. **Logos relevance** — Did representation drift from evidence, authority, truth, or valid inference?
8. **Agape relevance** — Did execution drift from the human/community purpose the work existed to serve?
9. **Missing executive/metacognitive function** — What function had to be supplied externally?
10. **Possible architectural implication** — What mechanism might externalize that function?
11. **Counterfactual detection question** — What could the system have checked to catch this itself?

### Verification queue

12. **Primary evidence to retrieve next** — transcript, issue, commit, handoff, test output, etc.
13. **Open uncertainty** — What remains unknown or interpretive?

## Discipline

- Do not force incidents into Logos/Agape. `Neither`, `unclear`, and `other` are valid.
- Do not infer an AI's private mental state. Describe observable working assumptions, outputs, or optimization behavior.
- Do not convert a recurring pattern into a taxonomy class until multiple incidents support it.
- A machine-green result is evidence, not automatic acceptance.
- Historical evidence and current authority are distinct.
- Intended state, claimed state, demonstrated state, qualified state, and canonical state must remain distinguishable.
- The `Other` category remains mandatory throughout early coding.
