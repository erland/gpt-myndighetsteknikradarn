# Runtime build

Chat ZIP är primär runtime för Myndighetsteknikradarn.

Bygg med:

```bash
python scripts/build_chat_runtime.py --project-root . --version <version>
```

Bygget kompilerar canonical instruktionens utvecklingsvägar till runtimevägar och inkluderar endast filer som behövs vid körning.
