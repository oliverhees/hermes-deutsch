# Herkunft und Prüfstand

## Locale

- Ursprung: [NousResearch/hermes-agent PR #51762](https://github.com/NousResearch/hermes-agent/pull/51762)
- Enthaltener Locale-Hash (SHA-256):

  ```text
  b4c7d38fc6de07ead7f89506ecde19e5ec89f1f72d6333922d4600b7104eaf43
  ```

## Lokaler Prüfstand

- Hermes Agent: `v0.21.3 (2026.9.14)`
- Upstream-Commit beim Installertest: `db1f3f4564`
- Getestet am: 21. September 2026

## Verifizierter Ablauf

1. Installation in einen isolierten Hermes-Home-Ordner gegen einen frischen `origin/main`-Worktree.
2. Wiederholte Reparatur ohne Änderung erkannt die vorhandene Locale korrekt als aktuell.
3. Simuliertes Hermes-Update setzte den i18n-Ordner auf den Upstream-Zustand zurück.
4. `repair.py` spielte die Locale erneut und vollständig ein.
5. `uninstall.py` stellte `types.ts`, `catalog.ts` und `languages.ts` bytegleich zum Upstream-Zustand wieder her, entfernte `de.ts` sowie den separaten Hook.

Die Prüfung umfasst keinen vollständigen Electron-Desktop-Build. Der normale Installer führt diesen Build standardmäßig aus; der Test verwendete bewusst `--no-build`, damit er keine reale lokale Desktop-Installation verändert.
