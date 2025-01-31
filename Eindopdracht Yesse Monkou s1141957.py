"""
Titel: Eindopdracht BPYT
Auteur: Yesse Monkou (S1141957)
Datum: 03.02.2023

Beschrijving:
Dit programma is een spelletje genaamd woordle. Dit spelletje
is eigenlijk hetzelfde als Lingo. Er wordt een 6-letter woord
gekozen door het programma en de gebruiker moet binnen 6 keer
dit woord raden. Elke keer als de gebruiker een poging doet,
wordt er op het scherm getoond welke letters van dat geraden
woord in het gekozen woord zitten en welke niet. Dit wordt
gedaan door middel van een:
"-": de letter zit niet in het woord
"*": de letter zit in het woord, maar niet op de juiste plek
"+": de letter zit in het woord en op de juiste plek

Het is ook mogelijk om een woord toe te voegen aan de lijst
met mogelijke woorden die je kan krijgen tijdens het spelen
van het spel. Als het woord al in de lijst zit, word je terug
gestuurd naar het hoofdmenu. Als het woord nog niet in de lijst
zit, wordt dit woord op de juiste alfabetische plek in het text-
bestand gezet.

Je kan ook de scores van jezelf of van anderen bekijken. Het
aantal gespeelde, gewonnen en verloren potten worden getoond.
Ook wordt het winstpercentage getoond op het scherm. Na elke
pot die de gebruiker speelt bij woordle, wordt er in een
tekstbestand weggeschreven of de speler heeft gewonnen of verloren.
"""

from random import choice
import re


# KEUZE MAKEN
def keuzemenu() -> str:
    """
    Deze functie vraagt de gebruiker om een keuze te maken uit
    het keuzemenu. Daarna controleert het programma of de
    gebruiker een geldige keuze heeft gemaakt. Als dat het geval
    is, returned het programma de gemaakte keuze. Als de invoer
    onjuist is, vraagt dit programma opnieuw om een keuze. Net
    zolang tot er een juiste invoer is.
    """

    while True:
        km_keuze = input("Opties:\n"
                         "\t1) Woordle spelen\n"
                         "\t2) Woord toevoegen\n"
                         "\t3) Scores bekijken\n"
                         "\t4) Spel sluiten\n"
                         "Voer een keuze in:")

        if km_keuze in "1234" and len(km_keuze) == 1:
            return km_keuze
        else:
            print("Geef een geldige keuze op (1/2/3/4).")


# WOORDLE SPELEN
def naam_vragen_en_formatteren() -> str:
    """
    Deze functie vraagt de gebruiker om zijn naam. De naam mag
    alleen letters en spaties bevatten. Hier wordt ook op
    gecontroleerd. De naam wordt in lowercase gezet en indien de
    naam langer is dan 10 karakters, worden alleen de eerste 10
    karakters gebruikt. Als er niks meer overblijft van de
    uiteindelijke naam, of je hebt geen naam ingevoerd, dan wordt
    de naam "john doe" gebruikt.
    """

    input_naam: str = input("Voer je naam in:").lower()

    gefilterde_naam: str = re.sub("[^a-z\s]", "", input_naam)
    gefilterde_naam: str = gefilterde_naam[0:10]

    if gefilterde_naam == "" or gefilterde_naam == "naam":
        return "john doe"

    return gefilterde_naam


def kies_woord(woorden_bestand: str) -> str:
    """
    Deze functie haalt een willekeurig woord op uit
    het tekstbestand "woordlewoorden.txt". Als dit
    bestand niet bestaat, wordt het woord hachee gebruikt.
    """
    try:
        kw_bestand = open(woorden_bestand, "r")

        woordenlijst = []

        for woorden in kw_bestand:
            woordenlijst.append(woorden)

        kw_bestand.close()

        kw_woord = choice(woordenlijst)
        kw_woord = kw_woord.replace("\n", "")

    except FileNotFoundError:
        kw_woord = "hachee"

    return kw_woord


def print_raster_en_alfabet(prea_raster: list[str], prea_beschikbare_letters:str, prea_geraden_woorden:list[str]):
    """
    Deze functie print het raster en de beschikbare letters.
    Dit staat in een aparte functie omdat de functie woordle_spelen
    anders een te grote chaos werd.
    """
    # Print rasters
    for rasters in range(6):
        if rasters < len(prea_geraden_woorden):
            print("|" + prea_geraden_woorden[rasters] + "|")
            print(prea_raster[rasters])

        else:
            print("|______|")

    # Print beschikbare letters
    for letters in range(len(prea_beschikbare_letters)):
        if letters == 10:  # Plek 10 is waar de "a" hoort te staan
            print(f"\n {prea_beschikbare_letters[letters]}", end=" ")

        elif letters == 19:  # Plek 19 is waar de "z" hoort te staan
            print(f"\n  {prea_beschikbare_letters[letters]}", end=" ")

        else:
            print(prea_beschikbare_letters[letters], end=" ")

    print()


# WORDT GEBRUIKT VOOR WOORDLE SPELEN, WOORD TOEVOEGEN EN SCORES BEKIJKEN
def bestand_uitlezen(bestandsnaam:str) -> str:
    """
    Deze functie leest tekstbestand uit.
    """

    bu_bestand_lezen = open(bestandsnaam, "r")
    bu_bestand_inhoud = bu_bestand_lezen.read()
    bu_bestand_lezen.close()

    return bu_bestand_inhoud


def bestand_wegschrijven(bw_items_speler:list[list[str]], bw_plaats:int, bw_coefficient:int):
    """
    Deze functie update de score van de speler, zet de lijsten in het
    juiste format in een string en schrijft dit weg in
    "woordlescores.txt".
    """

    scores_bestand = "woordlescores.txt"

    bw_items_speler[bw_plaats][bw_coefficient] = str(
        int(bw_items_speler[bw_plaats][bw_coefficient]) + 1)

    tekst = ""

    for rijen in bw_items_speler:
        tekst += ",".join(rijen) + "\n"

    tekst = tekst[:-1]

    bw_bestand_schrijven = open(scores_bestand, "w")
    bw_bestand_schrijven.write(tekst)
    bw_bestand_schrijven.close()


def update_woordlescores(uw_naam:str, uw_geraden:bool, uw_bestand_inhoud:str) -> tuple[list[list[str]], int, int]:
    """
    Deze functie update het woordlescores tekstbestand. Als de speler
    al eerder het spelletje heeft gespeeld, worden zijn statistieken
    aangepast. Als de speler het spelletje nog niet heeft gespeeld,
    wordt er een nieuwe regel voor de speler aangemaakt.
    """
    uw_items_speler = []
    uw_plaats = 0

    for spelers in range(len(uw_bestand_inhoud.split("\n"))):
        uw_items_speler.append(uw_bestand_inhoud.split("\n")[spelers].split(","))
        if uw_naam == uw_items_speler[spelers][0]:
            uw_plaats = spelers

    if uw_geraden:
        uw_coefficient = 1
    else:
        uw_coefficient = 2

    if uw_plaats == 0:
        uw_items_speler.append([uw_naam, "0", "0"])
        uw_plaats = -1

    return uw_items_speler, uw_plaats, uw_coefficient


def woord_opvragen() -> str:
    """"
    Deze functie vraagt een woord op. Als dit woord uit alleen
    letters bestaat en het is 6 tekens lang, dan wordt het
    woord ge-returned.
    """
    woord_test = ""

    while not woord_test.isalpha() or len(woord_test) != 6:
        woord_test = (input("Voer een 6-letter woord in: "))

    return woord_test.lower()


def plusjes_toevoegen(pt_raster:str, pt_voorkomst:dict, pt_woord_raden:str, pt_woord:str) -> tuple[str, dict]:
    """
    Deze functie voegt eventueel de plusjes toe aan het raster. De
    letters uit het ingevoerde woord worden ook in een dictionary
    geplaatst. Dit komt van pas bij het invoeren van de *.
    """
    for letter_plaats in range(6):
        if pt_woord_raden[letter_plaats] not in pt_voorkomst.keys():
            pt_voorkomst[pt_woord_raden[letter_plaats]] = 0
        if pt_woord_raden[letter_plaats] == pt_woord[letter_plaats]:
            pt_raster = pt_raster[:letter_plaats + 1] \
                        + "+" + pt_raster[letter_plaats + 2:]
            pt_voorkomst[pt_woord_raden[letter_plaats]] += 1

    return pt_raster, pt_voorkomst


def sterretjes_minnetjes_toevoegen(smt_raster:str, smt_voorkomst:dict, smt_woord_raden:str, smt_woord:str, smt_beschikbare_letter:str) -> tuple[str, dict, str]:
    """
    Deze functie voegt eventueel * en/of - toe. Er wordt gebruik
    gemaakt van de dictionary smt_voorkomst. Door deze dictionary
    weet de functie of er nog een * kan worden toegevoegd.
    Bijvoorbeeld: het gekozen woord is "hachee". De gebruiker voert
    het woord "ideeen" in. Dan staat er in de dictionary voorkomst
    "e": 3. Voor de 3e "e" rekent het programma dan een -.
    """

    for smt_letter_plaats in range(6):
        if smt_raster[smt_letter_plaats + 1] == "_":
            if (smt_woord_raden[smt_letter_plaats] in smt_woord
                    and smt_woord.count(smt_woord_raden[smt_letter_plaats])
                    > smt_voorkomst[smt_woord_raden[smt_letter_plaats]]):
                smt_voorkomst[smt_woord_raden[smt_letter_plaats]] += 1
                smt_raster = (smt_raster[:smt_letter_plaats + 1]
                              + "*" + smt_raster[smt_letter_plaats + 2:])

            else:
                smt_raster = (smt_raster[:smt_letter_plaats + 1]
                              + "-" + smt_raster[smt_letter_plaats + 2:])
                if smt_voorkomst[smt_woord_raden[smt_letter_plaats]] == 0:
                    if smt_woord_raden[smt_letter_plaats] in smt_beschikbare_letter:
                        smt_beschikbare_letter = smt_beschikbare_letter.replace(
                            smt_woord_raden[smt_letter_plaats], "-")

    return smt_raster, smt_voorkomst, smt_beschikbare_letter


def woordle_spelen(ws_naam: str, ws_woord: str) -> bool:
    """
    Deze functie speelt het spelletje woordle. Eerst wordt
    de naam gevraagd van de gebruiker in een andere functie.
    Daarna wordt er een woord opgehaald om mee te spelen; ook
    dit gebeurt in een andere functie. Het raster en de beschikbare
    letters worden in een andere functie geprint. Hierop wordt de
    functie aangeroepen die het woord ophaalt bij de gebruiker. Er
    wordt de gebruiker net zolang om een woord gevraagd tot het
    ingevoerde woord alleen uit letters bestaat en 6 tekens lang is.
    Er wordt een functie aangeroepen om te checken of de woorden
    overeen komen. Nadat het spel klaar is, word je doorgestuurd naar
    de functie die de score aanpast of toevoegt.
    """

    print(f"Welkom bij woordle, {ws_naam}! "
          f"Je moet het verborgen woord raden.\n"
          "Voer een 6-letter woord in om het woord te raden.\n"
          "Wanneer je een woord raadt, krijg je in de regel eronder een"
          " *, -, of + te zien\n"
          "Een + betekent dat die letter goed is en op de juiste plaats"
          " staat.\n"
          "Een * betekent dat die letter in het woord zit, maar niet op"
          " de juiste plaats staat\n"
          "Een - betekent dat die letter niet in het woord zit.\n"
          "Je hebt 6 pogingen om het 6-letter woord te raden, "
          "veel succes!\n")

    pogingen = 0
    beschikbare_letters = "qwertyuiopasdfghjklzxcvbnm"
    ws_geraden = False
    raster = []
    geraden_woorden = []

    while pogingen < 6 and not ws_geraden:
        print_raster_en_alfabet(raster, beschikbare_letters, geraden_woorden)

        geraden_woorden.append(woord_opvragen())

        voorkomst = {}
        raster.append("|______|")

        if geraden_woorden[-1].lower() == ws_woord:
            raster[-1] = "|++++++|"
            ws_geraden = True
        else:
            raster[-1], voorkomst = plusjes_toevoegen(
                raster[-1], voorkomst, geraden_woorden[-1].lower(), ws_woord)

            raster[-1], voorkomst, \
                beschikbare_letters = sterretjes_minnetjes_toevoegen(
                raster[-1], voorkomst, geraden_woorden[-1].lower(), ws_woord,
                beschikbare_letters)

        pogingen += 1

    if not ws_geraden:
        print(f"Het woord was {ws_woord}. "
              f"Je hebt het jammer genoeg niet geraden!")

    elif ws_geraden:
        print("Gefeliciteerd! Je hebt het woord goed geraden!")

    return ws_geraden


# WOORD TOEVOEGEN
def woord_toevoegen(wt_bestand_woorden: str, wt_toevoeg_woord: str, wt_woordenlijst: str):
    """"
    :param: bestand_woorden: (str)bestand waar de worden in staan.
    :param: wt_toevoeg_woord: (str)woord wat moet worden toegevoegd.
    :return:

    Deze functie vraagt de gebruiker om een geldig woord en stopt dit
    woord in een file (als het woord er nog niet in stond).
    """
    wt_woordenlijst = wt_woordenlijst.split("\n")

    if wt_toevoeg_woord in wt_woordenlijst:
        print(f"{wt_toevoeg_woord} zit al in {wt_bestand_woorden}!")

    elif wt_toevoeg_woord not in wt_woordenlijst:
        wt_woordenlijst.append(wt_toevoeg_woord)
        wt_woordenlijst.sort()

        wt_bestand_schrijven = open(wt_bestand_woorden, "w")
        wt_bestand_schrijven.write("\n".join(wt_woordenlijst))
        wt_bestand_schrijven.close()

        print(f"{wt_toevoeg_woord} toegevoegd aan {wt_bestand_woorden}!")


def scores_bekijken(sb_bestand_inhoud: str):
    """
    Deze functie vraagt de gebruiker van wie hij de scores wil
    bekijken. Vervolgens wordt dit op het scherm getoond met
    het winstpercentage.
    """
    sb_items_speler = []

    print("\nJe kunt uit de volgende spelers kiezen:")

    for sb_spelers in range(len(sb_bestand_inhoud.split("\n"))):
        sb_items_speler.append(
            sb_bestand_inhoud.split("\n")[sb_spelers].split(","))
        if sb_items_speler[-1][0] != "naam":
            print(sb_items_speler[-1][0])

    sb_keuze_speler = ""

    while sb_keuze_speler == "":
        speler_keuze_gebruiker = input("Wiens score wil je zien?")

        for sb_spelers in sb_items_speler:
            if speler_keuze_gebruiker in sb_spelers:
                sb_keuze_speler = sb_spelers

    winstpercentage = round(
        (int(sb_keuze_speler[1]) / (int(sb_keuze_speler[1])
                                    + int(sb_keuze_speler[2])) * 100), 2)

    print(f"Scores van {sb_keuze_speler[0]}\n"
          f"Totaal: {(int(sb_keuze_speler[1]) + int(sb_keuze_speler[2]))}\n"
          f"Gewonnen: {sb_keuze_speler[1]}\n"
          f"Verloren: {sb_keuze_speler[2]}\n"
          f"Winst %: {winstpercentage}\n")


# MAIN
def main():
    """
    De main wordt gebruikt om functies aan te roepen en
    variabelen op te slaan. De loop die functies aanroept,
    blijft net zolang doorgaan tot de gebruiker in het
    keuzemenu kiest om te stoppen.
    """
    
    woorden_bestand = "woordlewoorden.txt"
    scores_bestand = "woordlescores.txt"
    print("\nWelkom bij het beste spel van de wereld: WOORDLE!")

    while True:
        keuze = keuzemenu()

        if keuze == "1":
            naam = naam_vragen_en_formatteren()
            woord = kies_woord(woorden_bestand)
            geraden = woordle_spelen(naam, woord)
            bestand_inhoud_uw = bestand_uitlezen(scores_bestand)
            items_speler, plaats, \
                coefficient = update_woordlescores(naam, geraden, bestand_inhoud_uw)
            bestand_wegschrijven(items_speler, plaats, coefficient)

        elif keuze == "2":
            toevoeg_woord = woord_opvragen()
            woordenlijst = bestand_uitlezen(woorden_bestand)
            woord_toevoegen(woorden_bestand, toevoeg_woord, woordenlijst)

        elif keuze == "3":
            bestand_inhoud_sb = bestand_uitlezen(scores_bestand)
            scores_bekijken(bestand_inhoud_sb)

        elif keuze == "4":
            exit()


if __name__ == "__main__":
    main()
