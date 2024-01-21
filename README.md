# Swish 123

*(This concerns Swedes and people living in Sweden, hence written in Swedish)*

Detta är ett försök att skapa en datakälla med alla kända och okända Swish 123-nummer, enligt Swish använder [319412](https://www.swish.nu/about-swish#Swish_in_numbers) företag/organisationer Swish-platformen för betalningar. Det vore därför trevligt att kunna bygga API eller bara kunna kolla vem/vilka som har ett Swish 123-nummer.

Detta lilla projekt drivs på fritiden av en privatperson och på hobby-basis.

Önskar du tillägg eller förändringar, skapa en PR så infogas detta "ASAP" (när jag har tid) - var vänlig gör endast en förändring per PR för att göra det överskådligt och enkelt för mig att verifiera förändringar.



[Aktuell lista med Swish 123-nummer](https://github.com/cisene/swish-123/blob/master/swish-123.md) (Eye-candy)

[JSON](https://github.com/cisene/swish-123/blob/master/json/swish-123-datasource.json)

[TSV](https://github.com/cisene/swish-123/blob/master/text/swish-123-datasource.tsv)

[CSV](https://github.com/cisene/swish-123/blob/master/text/swish-123-datasource.csv)

[XML](https://github.com/cisene/swish-123/blob/master/xml-data/swish-123-datasource.xml)



## Samlade nummer

I aktuell samling av Swish-nummer har vi ***6945*** verifierade nummer. Dessa utgör bara en del av den fulla mängden existerande Swish-nummer, vi samlar och verifierar hela tiden nya och lägger dessa till samlingarna.

## Distribution av Swish-nummer

```mermaid
pie title Distribution
    "123 00x xx xx" : 118
    "123 01x xx xx" : 80
    "123 02x xx xx" : 102
    "123 03x xx xx" : 110
    "123 04x xx xx" : 127
    "123 05x xx xx" : 84
    "123 06x xx xx" : 82
    "123 07x xx xx" : 129
    "123 08x xx xx" : 120
    "123 09x xx xx" : 98
    "123 10x xx xx" : 104
    "123 11x xx xx" : 92
    "123 12x xx xx" : 113
    "123 13x xx xx" : 112
    "123 14x xx xx" : 122
    "123 15x xx xx" : 93
    "123 16x xx xx" : 91
    "123 17x xx xx" : 118
    "123 18x xx xx" : 98
    "123 19x xx xx" : 81
    "123 20x xx xx" : 76
    "123 21x xx xx" : 106
    "123 22x xx xx" : 119
    "123 23x xx xx" : 116
    "123 24x xx xx" : 63
    "123 25x xx xx" : 76
    "123 26x xx xx" : 108
    "123 27x xx xx" : 109
    "123 28x xx xx" : 83
    "123 29x xx xx" : 86
    "123 30x xx xx" : 91
    "123 31x xx xx" : 69
    "123 32x xx xx" : 100
    "123 33x xx xx" : 98
    "123 34x xx xx" : 84
    "123 35x xx xx" : 105
    "123 36x xx xx" : 89
    "123 37x xx xx" : 74
    "123 38x xx xx" : 111
    "123 39x xx xx" : 90
    "123 40x xx xx" : 66
    "123 41x xx xx" : 78
    "123 42x xx xx" : 90
    "123 43x xx xx" : 69
    "123 44x xx xx" : 101
    "123 45x xx xx" : 99
    "123 46x xx xx" : 73
    "123 47x xx xx" : 57
    "123 48x xx xx" : 56
    "123 49x xx xx" : 93
    "123 50x xx xx" : 75
    "123 51x xx xx" : 140
    "123 52x xx xx" : 94
    "123 53x xx xx" : 97
    "123 54x xx xx" : 87
    "123 55x xx xx" : 96
    "123 56x xx xx" : 95
    "123 57x xx xx" : 95
    "123 58x xx xx" : 90
    "123 59x xx xx" : 73
    "123 60x xx xx" : 91
    "123 61x xx xx" : 87
    "123 62x xx xx" : 100
    "123 63x xx xx" : 67
    "123 64x xx xx" : 86
    "123 65x xx xx" : 73
    "123 66x xx xx" : 86
    "123 67x xx xx" : 95
    "123 68x xx xx" : 83
    "123 69x xx xx" : 80
    "123 86x xx xx" : 1
    "123 90x xx xx" : 445
```

## Användning av information från Swish 123

Användning av [Swish 123](https://github.com/cisene/swish-123) data kan skådas på bland annat [Swish-Katalogen](https://b19.se/swish-katalogen/) där dessa data exponeras i en enkel söktjänst genom tagg-moln och fritext sökning.



## Vad är ett Swish 123-nummer?

Swish 123-nummer är 10-ställiga nummer som har begynnelsesiffror "123". Detta ger en nummer-rymd om 9999999, nära 10 miljoner nummer. Bland dessa nummer finns serier allokerade för specifika ändamål. 

Listan innehåller Swish 123-nummer som samlats och kunnat knytas till en organisation med organisationsnummer - i de fall 123-nummret innehas av enskild företagare to utelämnas detta eftersom det då skulle utgöra problem med GDPR på grund av företagarens personnummer.



## Swish 1239XX

Speciella serier av 1239XX (900-909) är allokerade till organisationer med så kallade 90-konton genom [Insammlingskontroll](https://www.insamlingskontroll.se/90-konto-organisationer/). För tillfället är 445 organisationer under kontroll.

Några populära exempel:

* Radio Hjälpen, pg 90 1950-6, med Swish nummer **[1239019506](https://b19.se/swish-katalogen/1239019506)** ibland uttryckt som 901 95 06
* Läkare Utan Gränser, pg 90 0603-2, med Swish nummer **[1239006032](https://b19.se/swish-katalogen/1239006032)** ibland uttryckt som 900 60 32
* Human Rights Watch Scandinavia, pg 90 0454-0, med Swish nummer **[1239004540](https://b19.se/swish-katalogen/1239004540)** ibland uttryckt som 900 45 40

Dessa kan även hittas i Swish-Katalogen under kategorin [insamlingskontroll](https://b19.se/swish-katalogen/k/insamlingskontroll).



## Varför?

Initiativet startades medan huvudet var fullt med snor och lätt febrig, 2021-12-30 12:30 ungefär efter att ha letat på nätet efter Swish nummer att skicka betalning till. Detta skulle kunna användas som data-källa för ett eventuellt API eller som katalog att inkludera i en App. [Swish](https://swish.nu/) själva verkar inte exponera eller tillhandahålla dessa nummer själva. 



### TODO:

* Skapa script för QA-kontroller av information (saknade eller felaktigt formatterade uppgifter)


### Support/Stöd

Att bidra till projektet uppskattas, det betalar lite av kostnaderna att hålla servrar igång, domännamn och annat.

Några som bidragit är:
* Maria B
