# Hermes Deutsch

**Deutsche Oberfläche für Hermes Desktop – jetzt, ohne auf einen Upstream-Merge zu warten.**

> **Status: Kompatibilitäts-Patch.** Dieses Projekt ist **kein offizielles Hermes-Sprachpaket** und kein Bestandteil von Nous Research. Es ergänzt gezielt vier Dateien im lokalen Hermes-Checkout, bis Deutsch nativ in Hermes verfügbar ist.

Die deutsche Locale basiert auf [Hermes-Agent PR #51762](https://github.com/NousResearch/hermes-agent/pull/51762). Ziel dieses Repositorys ist nur die sichere, eigenständige Übergangsverteilung.

## Was es macht

- installiert die deutsche Locale `de.ts`;
- ergänzt die Locale-Registrierung in `types.ts`, `catalog.ts` und `languages.ts`;
- legt vor der ersten Änderung Original-Sicherungen mit der Endung `.aiianer-orig` an;
- arbeitet wiederholbar: erneutes Installieren aktualisiert nur die deutsche Datei;
- bricht bei unbekannter Hermes-Struktur ab, statt blind Dateien umzuschreiben;
- installiert optional einen kleinen Gateway-Hook, der nach einem Gateway-Start prüft, ob ein Hermes-Update Deutsch entfernt hat.

## Wichtige Grenze

Hermes stellt derzeit **keinen offiziellen Desktop-Update-Hook für Community-Sprachen** bereit.

Der beiliegende Hook reagiert daher auf `gateway:startup`. Wenn du Hermes ausschließlich über das Desktop-App-Symbol startest und dabei kein Gateway startet, kann nach einem Hermes-Update ein manueller Reparaturschritt nötig sein. Das ist bewusst dokumentiert – dieses Projekt verspricht keine Automatik, die Hermes nicht technisch auslöst.

## Voraussetzungen

- Hermes Desktop ist installiert.
- Python 3 ist verfügbar (bei einer normalen Hermes-Installation bereits vorhanden).
- Hermes liegt im Standardpfad `~/.hermes/hermes-agent` (Linux/macOS) beziehungsweise im konfigurierten `$HERMES_HOME`.

Bei abweichendem Checkout-Pfad wird `--agent-dir` verwendet.

## Installation

1. Repository klonen oder als ZIP herunterladen und entpacken:

   ```bash
   git clone https://github.com/oliverhees/hermes-deutsch.git
   cd hermes-deutsch
   ```

2. Installer starten:

   ```bash
   python3 install.py
   ```

   Der Installer sichert die mitgelieferten Dateien nach `~/.hermes/hermes-deutsch/`, installiert den Gateway-Hook und baut Hermes Desktop neu. Der Neubau kann einige Minuten dauern.

3. Hermes vollständig beenden und neu starten.

4. In Hermes die Sprache auf **Deutsch** stellen.

### Abweichender Hermes-Checkout

```bash
python3 install.py --agent-dir /pfad/zu/hermes-agent
```

### Nur installieren, später selbst bauen

```bash
python3 install.py --no-build
python3 -m hermes_cli.main desktop --build-only --force-build
```

## Nach einem Hermes-Update reparieren

Wenn Deutsch nach einem Update fehlt oder die Desktop-App ohne Gateway gestartet wurde:

```bash
python3 ~/.hermes/hermes-deutsch/repair.py --rebuild
```

Bei einem abweichenden Hermes-Home gilt entsprechend `$HERMES_HOME/hermes-deutsch/repair.py`.

Der Befehl prüft zuerst, ob die deutsche Locale bereits vollständig und in der erwarteten Version vorhanden ist. Nur bei einer Abweichung wird gepatcht und neu gebaut.

## Deinstallation / Notausstieg

```bash
python3 ~/.hermes/hermes-deutsch/uninstall.py
```

Dadurch werden die bei der Installation gesicherten Originaldateien wiederhergestellt, `de.ts` entfernt und der Gateway-Hook gelöscht. Falls keine vollständigen Original-Sicherungen vorhanden sind, beendet sich der Rückbau ohne Änderung.

## Datenschutz und Sicherheit

- Keine Telemetrie, keine Netzwerkaufrufe, keine Zugangsdaten.
- Der Installer verändert ausschließlich den lokalen Hermes-Checkout und den eigenen Ordner `~/.hermes/hermes-deutsch/` samt optionalem Hook.
- Die Installation ist offen lesbar; es gibt bewusst keinen `curl | python`-Befehl.

## Quellen und Anerkennung

- Deutsche Locale: ursprüngliche Arbeit aus [PR #51762](https://github.com/NousResearch/hermes-agent/pull/51762).
- Der aktuelle enthaltene Stand wurde gegen den Hermes-`main`-Stand getestet.
- Hermes Agent ist ein Projekt von Nous Research; dieses Repository ist ein unabhängiges Community-Projekt.

## Lizenz

MIT – siehe [LICENSE](LICENSE). Die enthaltene Locale bleibt mit ihrem Hermes-Upstream-Kontext und den jeweiligen Autor:innen verbunden.
