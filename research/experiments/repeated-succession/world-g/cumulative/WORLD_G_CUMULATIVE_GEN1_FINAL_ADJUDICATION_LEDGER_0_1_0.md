# World G cumulative — Generation 1 final adjudication ledger

Date: 2026-09-21
Status: successor scoring complete

| Run | Provider | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | RQ | RB |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | OpenAI | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 0 |
| R2-RETRY1 | OpenAI | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| R3 | Anthropic | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 0 | 0 |
| R4 | Anthropic | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 0 | 0 |

Primary result:
- M6 action pass = 4/4.
- factual/current-state failure = 0.
- relational-integration failure = 0.
- no X/Y action-fidelity difference at Generation 1.

Important cumulative note: the M2/M4/M8 deductions are minor now, but they are not dismissed. They are propagation-relevant state distortions/calibration changes that may persist, amplify, or be corrected in later generations. No new endpoint is created; the frozen M1-M8 scheme remains controlling.

Protocol limitations remain visible: original R2 aborted after source request and was replaced once; R3/R4 were executed out of scheduled order; R1 contains unsupported self-report of two source requests.