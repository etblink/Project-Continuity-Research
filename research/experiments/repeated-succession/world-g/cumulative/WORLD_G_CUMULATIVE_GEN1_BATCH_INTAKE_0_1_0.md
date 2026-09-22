# World G Cumulative — Generation 1 Batch Intake 0.1.0

Date: 2026-09-21
Status: RAW MATERIAL FROZEN BEFORE SCORING

Four operator-supplied artifacts were received together.

| Run | Packet blob | Artifact type | Upload SHA-256 | Bytes |
|---|---|---|---|---:|
| WG-CUM-G1-R1 | `1e036d804f2ff484760267a1c66ce248864e7db8` | RAW_FINAL_RESPONSE | `e84f8e353485c0370d0414c22ed88b599b205bda6b16a05b02ffb89324869123` | 3618 |
| WG-CUM-G1-R2 | `21fe74186323ced6d1e0c984c2edb679e0318a31` | ORACLE_REQUEST_CHECKPOINT | `908366ddbbcbb426c6c300d22a4a8ca65a37fd727b11c6dc281b8e67a6762941` | 101 |
| WG-CUM-G1-R3 | `0712fa8ac888ed1171f3b43050978ef234faabe3` | RAW_FINAL_RESPONSE_PREMATURE_ORDER | `75a1cf18a14ae282b258446a85fe8afaf4cdae262c04b7a082577207805d52bb` | 4809 |
| WG-CUM-G1-R4 | `975bb22eb7df3c178fb350cce6e09156e9d18ef4` | RAW_FINAL_RESPONSE_PREMATURE_ORDER | `731cfb4785cad75a8738d5c316ed46f3d21892410335419259674c54ae18ff77` | 4415 |

## Protocol observations frozen before adjudication

- R1 is a final response. Its text says two historical records were requested, but the supplied artifact contains no valid `SOURCE_REQUEST:` command and no oracle return. Treat the claim as unsupported interaction metadata until adjudication.
- R2 is not a final response. It requests exact G-01 and G-02 records and therefore must receive the frozen oracle response before the same context may finalize.
- R3 and R4 are final responses, but were supplied before R2 completed even though the preregistered Generation-1 execution order is R1 -> R2 -> R3 -> R4. They are frozen now but quarantined from scoring pending explicit protocol-deviation adjudication.
- No score, condition interpretation, or compiler step is included here.
