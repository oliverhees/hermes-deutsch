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
- Hermes liegt im Standardpfad seines Betriebssystems oder im konfigurierten `HERMES_HOME`.

| Betriebssystem | Standard für `HERMES_HOME` | Hermes-Checkout | Installationsdaten |
| --- | --- | --- | --- |
| Linux / macOS | `~/.hermes` | `~/.hermes/hermes-agent` | `~/.hermes/hermes-deutsch` |
| Windows | `%LOCALAPPDATA%\hermes` | `%LOCALAPPDATA%\hermes\hermes-agent` | `%LOCALAPPDATA%\hermes\hermes-deutsch` |

Wenn `HERMES_HOME` gesetzt ist, ersetzt es diese Standardpfade auf allen Plattformen. Bei einem abweichenden Checkout-Pfad wird `--agent-dir` verwendet.

## Installation

### Empfohlen: direkt in Hermes installieren

Öffne einen normalen Hermes-Chat und sende **genau diesen Satz**. Du brauchst kein Terminal und keinen Git-Befehl:

> Bitte installiere **Hermes Deutsch v0.1.0** aus dem öffentlichen Repository `oliverhees/hermes-deutsch`. Prüfe zuerst die README und die enthaltenen Python-Dateien. Lade das Repository in einen temporären lokalen Arbeitsordner, führe anschließend den Installer mit dem Python aus, das Hermes verwendet, aus und zeige mir jede Ausgabe. Verwende keinen `curl | python`-Befehl. Baue Hermes Desktop nach der Installation neu und sage mir danach, ob Deutsch erfolgreich installiert wurde.

Hermes führt die technische Arbeit lokal aus. Der Installer sichert die Originaldateien, installiert den optionalen Gateway-Hook und baut die Desktop-App neu. Das kann einige Minuten dauern.

> [!IMPORTANT]
> **Danach Hermes vollständig beenden und neu starten.** Wähle anschließend in Hermes unter den Spracheinstellungen **Deutsch** aus.
>
> Ein Gateway-Neustart oder ein Plugin-Reload allein reicht für die sichtbare Desktop-Oberfläche nicht zuverlässig aus.

<details>
<summary>Profi-Alternative: Installation im Terminal</summary>

Repository klonen oder als ZIP herunterladen und entpacken:

```bash
git clone https://github.com/oliverhees/hermes-deutsch.git
cd hermes-deutsch
```

**Linux / macOS**

```bash
python3 install.py
```

**Windows (PowerShell)**

```powershell
py -3 install.py
```

</details>

### Abweichender Hermes-Checkout

**Linux / macOS**

```bash
python3 install.py --agent-dir /pfad/zu/hermes-agent
```

**Windows (PowerShell)**

```powershell
py -3 install.py --agent-dir "C:\Pfad\zu\hermes-agent"
```

### Nur installieren, später selbst bauen

**Linux / macOS**

```bash
python3 install.py --no-build
python3 -m hermes_cli.main desktop --build-only --force-build
```

**Windows (PowerShell)**

```powershell
py -3 install.py --no-build
py -3 -m hermes_cli.main desktop --build-only --force-build
```

## Nach einem Hermes-Update reparieren

Wenn Deutsch nach einem Update fehlt oder die Desktop-App ohne Gateway gestartet wurde, nutze zuerst wieder Hermes selbst.

### Empfohlen: direkt in Hermes reparieren

Öffne einen Hermes-Chat und sende **genau diesen Satz**:

> Bitte repariere meine Installation von **Hermes Deutsch v0.1.0** nach dem Hermes-Update. Prüfe zuerst, ob die deutsche Locale vollständig und in der erwarteten Version vorhanden ist. Wenn etwas fehlt, führe den Reparaturhelfer aus, baue Hermes Desktop neu und zeige mir die vollständige Ausgabe. Verwende keinen `curl | python`-Befehl. Sage mir abschließend klar, ob Deutsch wieder installiert und der Desktop-Neubau erfolgreich war.

Hermes prüft dabei zuerst den Zustand. Nur wenn die Locale fehlt, beschädigt ist oder nicht zum mitgelieferten Stand passt, werden Dateien erneut eingespielt und der Desktop neu gebaut.

<details>
<summary>Profi-Alternative: Reparatur im Terminal</summary>

**Linux / macOS**

```bash
python3 ~/.hermes/hermes-deutsch/repair.py --rebuild
```

**Windows (PowerShell)**

```powershell
py -3 "$env:LOCALAPPDATA\hermes\hermes-deutsch\repair.py" --rebuild
```

Bei einem abweichenden Hermes-Home ersetze den Pfad durch `$HERMES_HOME/hermes-deutsch/repair.py` beziehungsweise den entsprechenden Windows-Pfad.

</details>

> [!IMPORTANT]
> Nach einer erfolgreichen Reparatur Hermes vollständig beenden und neu starten. Wähle bei Bedarf erneut **Deutsch** in den Spracheinstellungen aus.

## Deinstallation / Notausstieg

**Linux / macOS**

```bash
python3 ~/.hermes/hermes-deutsch/uninstall.py
```

**Windows (PowerShell)**

```powershell
py -3 "$env:LOCALAPPDATA\hermes\hermes-deutsch\uninstall.py"
```

Dadurch werden die bei der Installation gesicherten Originaldateien wiederhergestellt, `de.ts` entfernt und der Gateway-Hook gelöscht. Falls keine vollständigen Original-Sicherungen vorhanden sind, beendet sich der Rückbau ohne Änderung.

## Datenschutz und Sicherheit

- Keine Telemetrie, keine Netzwerkaufrufe, keine Zugangsdaten.
- Der Installer verändert ausschließlich den lokalen Hermes-Checkout und den eigenen Ordner `~/.hermes/hermes-deutsch/` (Linux/macOS) beziehungsweise `%LOCALAPPDATA%\hermes\hermes-deutsch\` (Windows) samt optionalem Hook.
- Die Installation ist offen lesbar; es gibt bewusst keinen `curl | python`-Befehl.

## Quellen und Anerkennung

- Deutsche Locale: ursprüngliche Arbeit aus [PR #51762](https://github.com/NousResearch/hermes-agent/pull/51762).
- Der aktuelle enthaltene Stand wurde gegen den Hermes-`main`-Stand getestet.
- Hermes Agent ist ein Projekt von Nous Research; dieses Repository ist ein unabhängiges Community-Projekt.

## Lizenz

MIT – siehe [LICENSE](LICENSE). Die enthaltene Locale bleibt mit ihrem Hermes-Upstream-Kontext und den jeweiligen Autor:innen verbunden.
