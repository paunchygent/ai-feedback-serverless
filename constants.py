# constants.py

import os

# Constants for folder IDs
INPUT_FOLDER_ID = os.getenv('INPUT_FOLDER_ID', '1m_v4M41nRvskbz2vdQQCY6xDZo9fpfnu')
OUTPUT_FOLDER_ID = os.getenv('OUTPUT_FOLDER_ID', '1uYZMU_abYzEMiSa4F1MIq-9Xuqqk5OaI')

ESSAY_INSTRUCTION = """Skrivuppgift: Uppsats om ungas läsning
Uppgiftsbeskrivning: Du har fått i uppgift att skriva ett personligt och reflekterande inlägg för en webbplats som diskuterar samhälls- och skolfrågor. Ditt inlägg ska handla om ungas minskade läsning och läsförmåga. Utgå från dina personliga erfarenheter, men koppla dem också till de bredare perspektiv som presenteras i de angivna källorna.
Ditt inlägg ska först och främst väcka intresse för frågan om ungas minskande läsning. Det är viktigt att ge läsarna perspektiv på ämnet genom att resonera kring varför läsningen minskar och om detta är något vi bör vara oroade över. Du ska också diskutera möjliga lösningar på problemet och presentera relevant information från de angivna källorna för att stärka dina resonemang och ge läsarna en bredare förståelse.
De här frågorna måste din text besvara:
•	Utifrån dina erfarenheter och de källor du läst, vad anser du om ungas läsning idag?
•	Vilka hot och möjligheter ser du för ungas läsning i framtiden?
Följande frågor är enbart inspiration till ditt skrivande:
•	Vad betyder läsning för dig personligen?
•	Hur har din relation till läsning förändrats över tid?
•	Vilken roll spelar läsning i ditt liv nu?
•	Hur tror du att din läsning kommer att utvecklas framöver?
Inkludera två exempel från de angivna texterna som stöd för dina resonemang. Tänk på: att dina läsare inte har läst texterna.
Kom ihåg att ditt inlägg ska vara engagerande och relevant för en bred publik som är intresserad av samhälls- och skolfrågor.

Rubrik: Ungas läsning – hot och möjligheter
Omfång: 400–600 ord
Tid: ca 120 minuter

Bedömning: Vi kommer att fokusera:
•	Textens struktur, sammanhang och förmåga att väcka intresse
•	Din förmåga att reflektera över din egen läsning och koppla den till det större sammanhanget
•	Hur väl du resonerar kring orsakerna till minskad läsning och potentiella lösningar
•	Tydligheten i din åsikt om ungas läsning
•	Användning och källhänvisning av exempel från de angivna källorna

När du källhänvisar till artiklarna nedan ska du göra fullständiga källhänvisningar i brödtext. Lyft gärna in fullständiga datum inom parenteser (år-månad-dag för tidningar och år för tryckta böcker och rapporter). Om du anser att det förenklar din meningsbyggnad kan du även lyfta in var källan är publicerad i parentesen, men det är frivilligt.

PS! Glöm inte bort att använda referatmarkörer!

Namn på tidningar, så som *Dagens Nyheter* kan kursiveras.

Bjärvall, Katarina. 2011-05-31. ”Godis för hjärnan”. Lärarnas Nyheter.

Letmark, Peter. 2017-09-24. ”En läsande hjärna formas i tidig ålder”. Dagens Nyheter.

Lindberg, Gisela. 2017-08-31. ”Unga allt sämre på svåra ord”. Forskning.se

Magnusson, Lisa. 2020-08-27. ”Om skolan inte prioriterar läsning och skrivande kommer inget annat heller att fungera”. Dagens Nyheter.

Nordlund, Anna. Svedjedal, Johan. 2020. Läsandets årsringar. Rapport och reflektion om läsningens aktuella tillstånd i Sverige. Förläggarföreningen."""