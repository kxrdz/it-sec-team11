# Kryptoübung: RSA

Ziel der Aufgabe ist die Implementation eines einfachen Demonstration
des hinlänglich bekannten Algorithmus von Rivest, Shamir und Adleman für
hinlänglich große Zahlen.

Die Kommunikation erfolgt dabei wie in den Übungen vorgestellt:

### Protokollskizze

#### Server Ankündigung

Baut eine TCP/IP-Verbindung zur Adresse ``10.42.1.23:3033`` auf. Sendet
eine Portnummer auf der euer ETP-Server arbeitet. Die Nachricht besteht
ausschließlich aus einer ASCII-codierten Zahl in Dezimalschreibweise.
Beispiel: Die Nachricht ``12345``, für den Port 12345 auf dem Host, von
dem aus die Nachrichht gesendet wird.

Wenn eure Nachricht verstanden wurde, sendet euch der Server ein ``Ok``
zurück und öffnet eine TCP-Verbindung zu eurem Host unter der
angegebenen Portnummer. Dort sollte dann ein Server bereits auf die
Anfrage warten und das wie folgt beschriebene Protokoll verstehen.

#### Example Transmission Protocol (ETP)

Der Protokollablauf ist wie folgt skizziert. Dabei steht S für Server
und C für Client in der Kommunikation. Der Server sollte zunächst ein
RSA Schlüsselpaar erzeugt haben. Die Blockgröße der
Nachrichtenkommunikation ist 512 Bit, die Nachrichten sind ggf. mit
Null-Bytes auf volle Blockgröße zu padden bevor sie verschlüsselt
werden.

1. C -> S: ``GET pubkey ETP/2025``
2. S -> C: ``pub: <pubkey>\nN: <modul>\n``
3. C -> S: ``<ciphertext>``

Dabei MUSS der Server sicherstellen, dass er keine anderen Kommandos
akzeptiert als das oben definierte. Insbesondere MUSS sichergestellt
werden, dass in der Antwort niemals der private Schlüssel gesendet wird. 
Der Server SOLLTE mit unterschiedlichen Fehlermeldungen auf 
unterschiedliche Fehler (Kommando, Ressource oder Protokoll) reagieren.

Alle Nachrichten sind als ASCII-Text zu kodieren.

Der Server MUSS auf eine korrekte Anfrage mit einer Nachricht wie unter
2 angegeben Antworten. Dabei ist ``<pubkey>`` eine Hexadezimalzahl 
(Big-Endian) die als ASCII-Text kodiert ist. ``<modul>`` ist durch das
Modul des verwendeten Schlüssels zu ersetzen und ebenso zu kodieren. Das
Modul sollte als Binärzahl kodiert 512 Bit lang sein. Das Modul MUSS
diese Länge nicht überschreiten. Ein Beispiel mit unzureichender Länge:

```
p: a4f452ab3
N: 341221315
```

Der öffentliche Schlüsselteil SOLLTE nach bestem Wissen "sicher"
ausgewählt werden. Die Gründe für die gewählte Erzeugung des
öffentlichen (und zugehörigen privaten) Schlüsselteils sollten begründet
werden können.

Der ``<ciphertext>`` in der dritten Nachricht enthält eine
verschlüsselte Nachricht die auf ein vielfaches der Blockgröße (512 Bit)
am Ende der Nachricht mit Null-Bytes aufgefüllt ist (Padding). Die
Nachricht ist mit dem Schlüssel des Servers verschlüsselt. Der Server
MUSS die entschlüsselte Nachricht auf ``stdout`` ausgeben. Der Server
KANN die Nachricht in ein Log schreiben und KANN prüfen ob die Nachricht
erkennbar wohlgeformt ist. Die unverschlüsselte Nachricht enthält, bis
auf Padding, UTF-8 Text.

## Anforderungen/Bewertung

Volle 10 Punkte gibt es für eine Implementierung, die meine Nachricht
korrekt anzeigt und für welche das Modul 512 Bit Länge haben kann. Es
dürfen Bibliotheken für beliebig große Integer (``bignum``) für die
Zahldarstellung, Addition und Multiplikation verwendet werden.  
Teillösungen werden wie folgt bewertet:

- Implementierung von RSA mit 512-Bit Blocklänge (5 Punkte)
- Abfangen und Rückmelden von Protokollfehlern (1 Punkt)
- Funktionale Implementation des ETP (3 Punkte)
- Eigene Implementierung von ``modpow`` (1 Punkt)

Punktabzüge gibt es für fehlende oder fehlerhafte Skripte (siehe
Abgabe), hart-kodierte Lösungen (z.B. Schlüssel), mangelhafte Erklärung
von Code in der Vorstellung, oder Ressourcenverschwendung (z.B. das Öffnen
des Servers auf mehr als einem Port). Eine verspätete Abgabe wird mit
einem Punkt pro Woche geahndet.

### Ausgleichspunkte

Desweiteren können fehlende Punkte ausgeglichen werden durch:

- 2 Punkte: Eigene Implementierung des Euklidischen Algorithmus für 
  ``bignum`` zur Bestimmung des öffentlichen Schlüssels 
  (des multiplikativen Inversen des ersten, zufällig gewählten Schlüssels)
- Einmalig einen Punkt für das Team welches eine Schwachstelle in meiner
  Serverimplementierung findet. Ein Denial-of-Service Angriff gilt dann,
  wenn er nicht nur ein Überlastungsangriff ist, sondern mein Programm
  zum abstürzen bringt. 

Beachtet die Labornutzungsordnung!

### Bonuspunkte

Teams mit mindestens 5 erreichten Punkten — erst müssen die minimalen
Anforderungen erfüllt werden — können zudem Bonuspunkte
gewinnen die über erreichbare Maximalpunktzahl hinausgehen:

- 2 Punkte: einfaches Spoofing, bringt meinen Client dazu mit dem
  falschen ETP-Server zu reden. Kurzum: Ihr demonstriert mir, wie ihr
  von eurem Host aus eine (oder mehrere) Nachrichten sendet, die mich
  dazu bringen eine ETP-Kommunikation mit einem beliebigen anderen Host
  zu sprechen.
- Zusätzlich dazu 2 weitere Punkte, wenn ihr dabei dann auch die
  Nachricht lesen könnt die mir der andere Server schickt. Das Stichwort
  für diesen Angriff ist Machine-in-the-Middle (MitM).
- Einen weiteren zusätzlichen Punkt könnt ihr gewinnen, wenn ihr ein
  umsetzbares Konzept entwickeln könnt, damit der MitM-Angriff nicht
  mehr möglich ist.


## Abgabe

Ein gezipptes tar-Archiv mit dem Dateinamen ``team<teamnr>-etp.tar.gz``.
Inhalt des Archives ist die folgende Verzeichnisstruktur:

- ``team<teamnr>``
  + ``install.sh``
  + ``build.sh``
  + ``run.sh``
  + ``src``

Dabei sind die aufgeführten Skripte ausführbare(!) Bash-Skripte welche
euer Programm 

- aus diesem Verzeichnis auf eurem Host installieren (``install.sh
  <host-ip>`` ausgeführt auf Rechner mit Wireguard-Zugang zum Labor,
  ``<host-ip>`` ist dabei durch eine IP-Adresse des Zielhostes zu
  ersetzen), 
- wenn notwendig das Programm (auf einem Standard-Labor-Host) kompilieren (``build.sh``), 
- das Programm ausführen (``run.sh``).

Diese Skripte helfen euch ausserdem dabei die Grundanforderungen des
Labor nach schnellem "Recovery" nach einem Totalausfall zu erfüllen.

Dabei ist ``<teamnr>`` jeweils durch die zweistellige(!) Nummer des
Teams zu ersetzen. Falls ihr euch nicht erinnern könnt, das ist das
letzte Oktett der IP-Adresse eures Teamhosts minus 100.
