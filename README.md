# Swish 123

*(This concerns Swedes and people living in Sweden, hence written in Swedish)*

Detta är ett försök att skapa en datakälla med alla kända och okända Swish 123-nummer, enligt Swish använder [306 234](https://www.swish.nu/about-swish#Swish_in_numbers) företag/organisationer Swish-platformen för betalningar. Det vore därför trevligt att kunna bygga API eller bara kunna kolla vem/vilka som har ett Swish 123-nummer.

Detta lilla projekt drivs på fritiden av en privatperson och på hobby-basis.

Önskar du tillägg eller förändringar, skapa en PR så infogas detta "ASAP" (när jag har tid) - var vänlig gör endast en förändring per PR för att göra det överskådligt och enkelt för mig att verifiera förändringar.





## Vad är ett Swish 123-nummer?

Listan innehåller Swish 123-nummer som samlats och kunnat knytas till en organisation med organisationsnummer - i de fall 123-nummret innehas av enskild företagare to utelämnas detta eftersom det då skulle utgöra problem med GDPR på grund av företagarens personnummer.



## Swish 1239XX

Speciella serier av 1239XX (900-999) är allokerade till organisationer med så kallade 90-konton genom Insammlingskontroll.

Några populära exempel:

* Radio Hjälpen, Plusgiro 90 1950-6, med Swish nummer 1239019506 ibland uttryckt som 901 95 06
* Läkare Utan Gränser, Plusgiro 90 0603-2, med Swish nummer 1239006032 ibland uttryckt som 900 60 32
* Human Rights Watch Scandinavia, Plusgiro 90 0454-0, med Swish nummer 1239004540 ibland uttryckt som 900 45 40



## Varför?

Initiativet startades medan huvudet var fullt med snor och lätt febrig, 2021-12-30 12:30 ungefär efter att ha letat på nätet efter Swish nummer att skicka betalning till. Detta skulle kunna användas som data-källa för ett eventuellt API eller som katalog att inkludera i en App. [Swish](https://swish.nu/) själva verkar inte exponera eller tillhandahålla dessa nummer själva. 



### TODO:

* Bryta upp listor i separata filer med "grupp nummer", ex. swish-123-901.xml för nummer som börjar med 123901*
* Komplettera kategoriseringar för stöd i tex. filtreringar.