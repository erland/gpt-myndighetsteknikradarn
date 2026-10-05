# OpenAI Plugin-runtime

Myndighetsteknikradarn distribueras från GPT Byggaren 1.5.1 även som en skills-first OpenAI Plugin.

## Paket

Releaseartefakten heter `myndighetsteknikradarn-plugin-<version>.zip` och har `plugin.json` direkt i ZIP-roten. Huvudskillen ligger i `skills/myndighetsteknikradarn/SKILL.md`.

Skillen innehåller canonical instruktion som reference, relevanta policies, modeller, workflows, templates och knowledge samt en explicit allowlist av runtime-skript. Test-, eval-, CI-, build- och releaseverktyg paketeras inte.

## Stateful paritet

Projektet är stateful. Full paritet kräver ett persistent skrivbart workspace/filesystem där `ResearchRun` kan vara auktoritativ state och checkpoints kan bevaras mellan batcher/sessioner.

Om persistent state saknas fungerar kärnmetoden för en sammanhängande körning, men cross-session resume får inte beskrivas som garanterad. Runtimen är därför `ready_runtime_dependent`, inte identisk med OpenCode.

## Hostberoenden

- Web krävs för färsk myndighets-, teknik-, upphandlings- och kontaktpersonsresearch.
- Filesystem krävs för full persistent ResearchRun/checkpoint-paritet.
- Code execution rekommenderas för deterministisk state, scoring, coverage, deduplicering, rendering och export.
- PyYAML används av YAML-baserade Python-resurser.

## MCP

Pluginen genererar ingen MCP-wrapper. Runtime-skripten är resurser i skillen och används bara när hosten erbjuder kompatibel code execution.
