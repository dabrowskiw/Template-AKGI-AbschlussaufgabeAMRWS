# Abschlussaufgabe

In der Abschlussaufgabe erweitern Sie den Mapper um k-mer-Spektrum basierte Fehlerkorrektur, um trotz Sequenzierfehlern im Datensatz belastbare Aussagen treffen zu können. Dann nutzen Sie Ihren Code, um bei vier Infektionen jeweils die zur Behandlung einsetzbaren Antibiotika vorzuschlagen. 

Sie finden zu diesem Zweck in dem repository bereits die Musterlösung für die Mapping-Aufgabe. Sie können diese aber sehr gerne durch Ihre eigene Lösung aus der letzten Aufgabe ersetzen - ich denke, es macht mehr Spaß, am eigenen Code zu arbeiten! 

## Benotung

Zunächst aber die für Sie vermutlich besonders interessante Information, wo Sie Ihre Punkte herbekommen. Neben der Implementation gibt es Punkte für:

* Die Tablet-Aufgabe beim SAM-Export: Für die Identifikation der korrekten Basenaustausche in dem Mapping gibt es 5 Punkte.
* Für die erste Antibiotika-Empfehlung gibt es 10 Punkte (2.5 pro Person)
* Für die zweite Antibiotika-Empfehlung gibt es 10 Punkte (2.5 pro Person)
* Für die Erklärung der Unterschiede gibt es 10 Punkte

Insgesamt gibt es also für den Verständnisteil 35 Punkte zu bekommen, die restlichen 65 Punkte bekommen Sie für die Implementation.

## Visualisierung von Mappings

Mappen Sie zunächst die Datei [data/fluA_reads.fasta](data/fluA_reads.fasta) auf [data/fluA_reads.fasta](data/fluA.fasta) und speichern Sie das Ergebnis als fluA_mapping.sam. 

Laden Sie dann das Programm [Tablet](https://ics.hutton.ac.uk/tablet/) herunter und öffnen Sie (Klick auf den Button "Open Assembly" oben links) die Dateien fluA_mapping.sam sowie die Referenz [data/fluA_reads.fasta](data/fluA.fasta). Sie müssten dann eine Ansicht erhalten wie in diesem Bild:

![t1](Bilder/Tablet1.png)

Sie erkennen oben eine schematische Ansicht der gesamten Referenz mit den darauf gemappten Reads, dadrunter sehen Sie eine Detailansicht: Zuerst die in Aminosäuren translatierte Sequenz, dann die Nukleotidsequenz der Referenz, und dann die einzelnen Reads.

Wenn Sie den Mauszeiger über eine Base halten, bekommen Sie eine Information über den Read. Auf der Koordinatenachse zwischen Referenzsequenz und Reads wird zudem in roter Farbe die Position angezeigt - in diesem Fall ist zu erkennen, dass die erste Base "T" aus dem Read "Read_95" an Position 10 der Referenzsequenz gemappt wurde.

Wählen Sie im Reiter "Color Schemes" die Option "Variants", werden alle Basen der Reads, die mit der Referenzsequenz übereinstimmen, ausgegraut:

![t2](Bilder/Tablet2.png)

Sie erkennen nun oben in der Übersicht zwei rote Streifen, die Unterschiede zu der Referenzsequenz anzeigen. Bitte beachten Sie, dass es mehr Basen in der Referenz gibt als Pixelspalten auf dem Bildschirm und somit nicht zwingender Maßen alle Unterschiede in dieser Übersicht sichtbar sind!

### Tablet-Aufgabe

Tragen Sie hier bitte in dem Format ```<Referenz-Base><Position><Neue Base>``` ein, welche Mutationen Sie in dem Mapping erkennen können (```T10A``` würde also beispielsweise bedeuten, dass in der Referenz an Position 10 die Base T steht, es aber laut der Reads an dieser Position eine Mutation zu A gibt):

```text
Mutation 1:
Mutation 2:
...
Mutation n:
```

## Antibiotika-Resistenzen

Eine Aufgabe, bei der die Erkennung solcher Mutationen besonders wichtig ist, ist die Behandlung bekterieller Infektionen. Bakterien können Resistenzen gegen Antibiotika entwickeln - die Gabe solcher Antibiotika kann dann nicht mehr zur Heilung beitragen. Es gibt aber mittlerweile viele gut untersuchte Zusammenhänge zwischen Mutationen in bestimmten Genen und dadurch vermittelten Antibiotikaresistenzen. Entsprechend kann vor einer Behandlung eine Sequenzierung des Bakteriums erfolgen, und anhand der vorhandenen Mutationen kann eine Behandlungsentscheidung getroffen werden.

Ein besonders prominentes Beispiel ist das Bakterium Staphylococcus aureus, welches schnell Antibiotikaresistenzen ansammelt. Infektionen mit multiresistenten S. aureus (MRSA) stellen die Medizin vor eine große Herausforderung, da im schlimmsten Fall keine der verfügbaren Antibiotika mehr gegen sie funktionieren (bzw. nur noch sogenannte "drugs of last resort" funktionieren - Antibiotika, die für besonders schwere Fälle zurückgehalten werden, da durch einen stark reglementierten Einsatz Bakterien noch keinem Evolutionsdruck ausgesetzt wurden, um gegen diese Resistenzen zu entwickeln). 

In dieser Aufgabe untersuchen Sie die Proben von 4 mit S. aureus infizierten Personen auf Mutationen im rpoB-Gen des Bakteriums. Es stehen zur Behandlung die folgenden zwei Antibiotika zur Verfügung - in Klammern steht jeweils die Priorität, mit der sie eingesetzt werden sollten, wenn möglich sollte das Antibiotikum mit der höchsten Priorität eingesetzt werden:

* Daptomycin (1)
* Rifampicin (2)

Es sind Ihnen zudem die folgenden drei Mutationen bekannt, die Resistenzen vermitteln:

* C1862A: Resistenz gegen Daptomycin
* T2858G: Resistenz gegen Daptomycin
* C1402A: Resistenz gegen Rifampicin

Mappen Sie die Read-Sequenzen der 4 Personen ([data/patient1.fasta](data/patient1.fasta) - [data/patient4.fasta](data/patient4.fasta)) auf die rpoB-Referenz ([data/rpoB.fasta](data/rpoB.fasta)) und tragen Sie hier ein, welche Mutation(en) Sie identifizieren konnten und welches Antibiotikum Sie empfehlen würden:

```text
Person 1 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
Person 2 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
Person 3 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
Person 4 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
```

Lassen Sie sich bitte von Unterschieden zur Referenzsequenz, die nur in einzelnen Reads vorkommen, nicht verwirren - das ist ein realistischer Datensatz und die Reads enthalten Sequenzierfehler.

## Fehlerkorrektur

Wie Ihnen in der Identifikation der Antibiotikaresistenzen aufgefallen sein könnte, sind die realen Reads mit Sequenzierfehlern behaftet. Diese können die Analyse erschweren oder gar zu Fehlinterpretationen der Daten führen.

Eine Möglichkeit zur Korrektur dieser Fehler ist das k-mer-Spektrum. Dabei wird davon ausgegangen, dass durch eine große Coverage mit großteils korrekten Reads jedes sequenzierte k-mer mehrmals in unterschiedlichen Reads repräsentiert sein sollte. Kommt ein k-mer deutlich seltener vor, als die anderen k-mere, ist es vermutlich nicht auf eine Mutation (die ja von mehreren Reads abgedeckt sein sollte und deren k-mer entsprechend mehrmals vorkommen sollte) sondern auf einen Sequenzierfehler zurückzuführen.

Nehmen wir als Beispiel ein kurzes Genom, welches fehlerfrei sequenziert wird, und das 3-mer-Spektrum dazu: 

![sp1](Bilder/Spectrum1.png)

In diesem Fall wurde das Genom mit 5 fehlerfreien Reads abgedeckt, es ergeben sich 4 3-mere mit den Häufigkeiten 2, 4, 4 und 2.

Enthält aber einer der Reads einen Fehler (in diesem Fall wird die 3. Base von Read 2 fehlerhafter Weise als C gelesen), verändert sich das Spektrum:

![sp2](Bilder/Spectrum2.png)

Es kommen durch den Fehler drei neue k-mere hinzu, die jeweils nur ein Mal auftreten.

Anhand dieser Information kann eine Korrektur erfolgen: Es wird ein Schwellenwert definiert, ab dem ein k-mer als potenziell fehelrhaft eingestuft wird. Für jedes k-mer, welches seltener als dieser Schwellenwert vorkommt, werden folgende Schritte durchlaufen:

* Für jede Base X aus dem k-mer:
    * Für jede mögliche Base Y (A, G, T und C):
        * Generiere ein Kandidaten-k-mer indem die Base X durch die Base Y ersetzt wird
        * Falls das Kandidaten-k-mer auch im Datensatz vorkommt und zwar häufiger als der Schwellenwert: Merke es als mögliche Korrektur
* Falls Kandidaten-k-mere gefunden wurden: Ersetze das k-mer durch das Kandidaten-k-mer welches am häufigsten im Datensatz vorkommt (bei zwei Kandidaten-k-meren mit der gleichen Häufigkeit wähle zufällig eins davon)

Für das Mapping müssen die so identifizierten korrigierbaren k-mere in allen Reads ersetzt werden, in denen sie vorkommen.

### Implementation

Implementieren Sie die k-mer-Spektrum-Fehlerkorrektur wie folgt.

Implementieren Sie zunächst eine Klasse ```ReadPolisher``` mit den folgenden Methoden:
* ```__init__(self, kmerlen)```: Constructor, bekommt die zu verwendende k-mer-Länge
* ```add_read(self, readseq)```: Fügt die übergebene Readsequenz dem k-mer-Spektrum hinzu
* ```get_replacements(self, minfreq)```: Berechnet für die k-mere, die seltener als ```minfreq``` im k-mer-Spektrum vorkommen, die mögliche Korrektur und gibt ein entsprechendes dictionary zurück. Darin sind keys die korrigierbaren k-mere, values sind die Korrekturen (in dem obigen Beispiel wäre also z.B. bei minfreq=2 ein mögliches key-value-Paar "GCT":"GTT", welches aussagt, dass das k-mer "GCT" durch das k-mer "GTT" ersetzt werden soll)
  
Erweitern Sie zudem die Klasse ```Read``` um die Methode ```replace_kmers(self, replacements)```, welche die dictionary aus ```get_replacements``` bekommt und alle darin als key vorkommenden k-mere, die in dem Read vorhanden sind, durch den jeweiligen value ersetzt. Das ist zwar nicht die effizienteste Variante (effizienter wäre es, sich in ```ReadPolisher``` die Information zu merken, in welchen Reads welche k-mere vorkommen und dann nur dort die Ersetzungen vorzunehmen), aber das würde die Abschlussaufgabe zu lang machen.

### Anwendung

Verwenden Sie Ihre Read-Korrektur, um nochmal die Read-Sequenzen der 4 Personen ([data/patient1.fasta](data/patient1.fasta) - [data/patient4.fasta](data/patient4.fasta)) auf die rpoB-Referenz ([data/rpoB.fasta](data/rpoB.fasta)) zu mappen. Sehen Sie einen Unterschied? Welche k-mer-Längen und cutoffs erscheinen Ihnen sinnvoll? 

Tragen Sie hier ein, welche Mutation(en) Sie identifizieren konnten und welches Antibiotikum Sie nun empfehlen würden (verwenden Sie die Parameter, die Sie am sinnvollsten finden, probieren Sie aber zumindest ein Mal bei [data/patient2.fasta](data/patient2.fasta) eine k-mer-Länge von 15 und einen frequency cutoff von 3 aus):

```text
Person 1 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
Person 2 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
Person 3 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
Person 4 - Mutation(en): <IHRE MUTATIONEN>, Empfehlung: <IHRE ANTIBIOTIKUMS-EMPFEHLUNG> 
```

Sehen Sie einen Unterschied in den Empfehlungen zu denen, die Sie ohne Fehlerkorrektur gegeben haben? Beschreiben Sie kurz, was der Unterschied ist, und wie dieser durch die Fehlerkorrektur zustande gekommen ist (kein Roman, 5-6 Sätze reichen aus):

```text
Der Unterschied...
```