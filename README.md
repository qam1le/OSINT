OSINT įrankis
Įrankis skirtas rinkti finansinę informaciją apie organizacijas, iš organizacijų svetainių rinkti kontaktinius duomenis.

Įdedu ir executable, kad nereikėtų įsirašinėti python bibliotekų, kiek testavau ant kitų sistemų ir kompiuterių, viskas veikia.
Iš Python kodo į executable, naudojantis: auto-py-to-exe


Naudojamos duomenų rinkmenos iš : https://data.gov.lt/datasets

def tycinisBankrotas()
Pirmasis šaltinis, pasitelkiamas rasti įmonės finansinę būklę/istoriją.
URL: https://data.gov.lt/dataset/duomenys-apie-tycinius-bankrotus

def viesiejiPirkimai()
Antrasis šaltinis - viešųjų pirkimų informacija
URL: https://data.gov.lt/dataset/nauja-duomenu-baze
*Kadangi viešųjų pirkimų JSON failas yra ganėtinai didelis, jį iš karto pridedu, tačiau jį galima ir parsisiųsti/atnaujinti išsikvietus funkciją.

def contactScraper()
Funkcija skirta pagal HTML dokumente automatiškai rasti el. paštą ir numerį, kuris įprastai yra esančiose žymėse (angl. tags): "mailto" ir "tel"

def json_csv()
Surinktos informacijos iš JSON failų, išsaugojimas .csv failą. 

def textFile(contactList)
Išsaugojimas į .txt failą


ATSISKAITYMO REIKALAVIMAI:
1. Vienas arba daugiau lietuviškų informacijos šaltinių
    Naudojami du lietuviški informacijos šaltiniai.
2.  Informacijos rinkimas, išsaugojimas ir atvaizdavimas
    Informacijos saugojimas .csv ir .txt formatais, atvaizdavimas konsolėje.
3. Rezultatų ataskaitos išsaugojimas
    Informacijos saugojimas .csv ir .txt formatais, atvaizdavimas konsolėje.
4. Išeities kodo pateikimas
    def tycinisBankrotas(), def viesiejiPirkimai(), def contactScraper(), funkcijos kodą išveda į konsolę.