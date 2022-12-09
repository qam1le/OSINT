#qam1le 2022
from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from colorama import Fore
import time
import requests

#================================FUNKCIJA SKIRTA ISGAUTI DUOMENIS IS API SU TYCINIU BANKROTU DUOMENIMIS
#================================IR GRAZINTI REIKIAMUS/PASIRINKTUS
def tycinisBankrotas():
    org = input(Fore.RESET + "Irasykite imones pavadinima \n").upper()
    response = urlopen('https://get.data.gov.lt/datasets/gov/avnt/tyciniai_bankrotai/TycinisBankrotas/:format/json')
    json_data = json.loads(response.read())
    data = {
            "imones_bankroto_duomenys" : []
        }
    try:
        for i in json_data:
            for j in json_data[i]:
                if org in j['imones_pavadinimas']:
                    data_dict = {
                        "imones_kodas" : j['imones_kodas'],
                        "imones_pavadinimas" : j['imones_pavadinimas'],
                        "imones_bankroto_pradzia" : j['bankroto_pradzia'],
                        "imones_likvidavimas" : j['likvidavimo_data'],
                        "imones_tycinis_bankrotas" : j['tycinis_bankrotas'],
                        "imones_pabaiga" : j['isregistravimo_data']
                    }
                    data['imones_bankroto_duomenys'].append(data_dict)
                else:
                    print(Fore.RED + "Imones nera sarase, griztama i meniu \n")
                    menu()
        if not data["imones_bankroto_duomenys"]:
            return ''
        else:
            return data
    except:
        print(Fore.RED + "Klaida")
        menu()


#================================FUNKCIJA SKIRTA ISGAUTI DUOMENIS IS API SU VIESUJU PIRKIMU DUOMENIMIS
#================================IR GRAZINTI REIKIAMUS/PASIRINKTUS
# funkcija veikia salyginai letai del didesnio json failo dydzio
def viesiejiPirkimai():
    file_name = 'vpt.json'
    if os.path.isfile(file_name) == False:
        print(Fore.MAGENTA + "Kraunasi duomenys")
        start = time.process_time()
        response = urlopen('https://get.data.gov.lt/datasets/gov/vpt/new/Atn3/:format/json')
        json_data = json.loads(response.read())
        print("Krovimo laikas: " + str(time.process_time() - start) + "\n") #iprastai uztrunka 30sek
        dwnInput = input(Fore.BLUE + "Ar noretumet parsisiusti faila, greitesnei prieigai? t/n \n").lower()
        if dwnInput == 't':
            response = requests.get('https://get.data.gov.lt/datasets/gov/vpt/new/Atn3/:format/json')
            json_data = response.json()
            with open(file_name, "w") as file:
                json.dump(json_data, file)
            file.close()
            print(Fore.LIGHTGREEN_EX + "Failas buvo sekmingai sukurtas \n")
        elif dwnInput == 'n':
            pass
        else:
            print(Fore.RED + "Neteisinga ivestis bandykite dar karta \n")
            viesiejiPirkimai()

    elif os.path.isfile(file_name) == True:
        kbrInput = input(Fore.BLUE + "Ar norite atnaujinti " + file_name + " ? t/n \n").lower() 
        if kbrInput == 't':
            response = requests.get('https://get.data.gov.lt/datasets/gov/vpt/new/Atn3/:format/json')
            json_data = response.json()
            with open(file_name, "w") as file:
                json.dump(json_data, file)
            file.close()
            print(Fore.GREEN + "Failas buvo sekmingai atnaujintas \n")
        elif kbrInput == 'n':
            with open(file_name, 'r') as file:
                json_data = json.load(file)
        else:
            print(Fore.RED + "Netinkama ivestis, bandykite dar karta \n")
            viesiejiPirkimai()
    else:
        pass
    search_item = ''
    data = {
            "imones_vp_duomenys" : []
        }
    org = ""
    kbrInput = input(Fore.RESET + "Imones ieskojimas pagal: 1 - Koda, 2 - Pavadinima ")
    if kbrInput == '1':
        org = str(input("Irasykite imones koda \n"))
        search_item = 'legal_entity_code_1'
    elif kbrInput == '2':
        org = str(input("Irasykite imones pavadinima \n")).upper()
        search_item = 'official_name_1'
    else:
        print(Fore.RED + "Netinkama ivestis, bandykite dar karta")
        viesiejiPirkimai()

    try:
        for i in json_data:
            for j in json_data[i]:
                if org in str(j[search_item]).upper():
                    data_dict = {
                        "dok_irasymo_data" :  j['insert_date'],
                        "imones_kodas" : j['legal_entity_code_1'],
                        "imones_pavadinimas" : j['official_name_1'],
                        "imones_adresas" : j['postal_address_1'],
                        "imones_pasto_kodas" : j['postal_code_1'],
                        "imones_viesieji_url" : j['url_buyer_1']
                    }
                    data['imones_vp_duomenys'].append(data_dict)
                else:
                    print(Fore.RED + "Nera duomenu apie imone, griztama i meniu \n")
                    menu()
        if not data["imones_vp_duomenys"]:
            return ''
        else:
            return data
    except:
        print(Fore.RED + "Klaida, griztama i meniu")
        time.sleep(1.0)
        menu()
#================================FUNKCIJA SKIRTA IS DUOTO URL ISGAUTI EL PASTA IR NUMERI, JUOS GRAZINTI
#funkcija yra lucky guess, dazniausiai html failuose el pasta galima rasti po mailto eilutes, bet ne visada. 
#ir veikia tik duotame url'e, nevaiksto po direktorijas, del ko neverta webscrapper pavadinimo
def contactScraper():
    kbrInput = input(Fore.RESET + "Iveskite tinklapio URL \n")
    ref = 'http://'
    ref1 = 'https://'
    if ref not in kbrInput or ref1 not in kbrInput:
        try:
            req = requests.get(''.join((ref,kbrInput)))
        except:
            try:
                req = requests.get(''.join((ref1,kbrInput)))
            except:
                print(Fore.RED + "Neimanoma prisijungti \n")
                return ''
    data = req.text
    mail = ""
    tel = ""
    soup = BeautifulSoup(data, "html.parser")

    for i in soup.find_all(href=re.compile("mailto")):
        if str(i.string) and str(i.string).split(): 
            if "@" in str(i.string):
                mail = ''.join(str(i.string))
        else:
            mail = "Nerastas el pastas"
    for i in soup.find_all(href=re.compile("tel")):
        if str(i.string) and str(i.string).split():
            if "+" in str(i.string) or (str(i.string).replace(" ", "")).isdigit():
                tel = ''.join(str(i.string))
        else:
            tel = " Nerastas tel numeris"
    return (mail, tel) 
#=================================ISGAUTU JSON DUOMENU I CSV TIPO FAILA IRASYMAS
def json_csv(data):
    new_dict = []
    dict_name = list(data)[0]
    imone = ''
    for i in data[dict_name]:
        new_dict = i
        imone = i['imones_pavadinimas']
    fn = input(Fore.RESET + "Iveskite failo, kuriame norite issaugoti informacija, pavadinima \n")
    file_name = (''.join(fn)) + '.csv'
    if os.path.isfile(file_name) == False:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(imone + "\n")
            for key in new_dict.keys():
                file.write("%s, %s\n" % (key, new_dict[key]))
            file.write("\n")
        file.close()
        print(Fore.LIGHTGREEN_EX + "Duomenys sekmingai isaugoti \n")
        menu()
    if os.path.isfile(file_name) == True and os.stat(file_name).st_size != 0:
        kbrInput = input("Failas egzistuoja ir nera tuscias, ar norite sujungti sugeneruotus duomenis? t/n ").lower()
        if kbrInput == 't':
            with open(file_name, 'a', encoding='utf-8') as file:
                file.write("NAUJI DUOMENYS \n")
                file.write(imone + "\n")
                for key in new_dict.keys():
                    file.write("%s, %s\n" % (key, new_dict[key]))
                file.write("\n")
            file.close()
            print(Fore.LIGHTGREEN_EX + "Duomenys sekmingai isaugoti \n")
            menu()
        if kbrInput == 'n':
            print(Fore.GREEN + "Baigiamas darbas, griztama i meniu")
            time.sleep(1.0)
            menu()
        else:
            print(Fore.RED + "Netinkama ivestis, iseinama \n")
            menu()

    else:
        print(Fore.RED + "Failas neisaugotas, griztama i meniu")
        menu()


#=================================ISGAUTU DUOMENU I TXT TIPO FAILUS IRASYMAS
def textFile(contactList):
    fn = input(Fore.RESET + "Iveskite failo pavadinima \n")
    file_name = (' '.join(fn)) + ".txt"
    if os.path.isfile(file_name) == False:
        with open(file_name, "w") as file:
            file.write(' '.join(contactList))
            file.close()
    elif os.path.isfile(file_name) == True and os.stat(file_name).st_size != 0:
        kbrInput = input(Fore.LIGHTMAGENTA_EX + "Failas egzistuoja, bet nera tuscias ar norite papildyti? t/n \n").lower()
        if kbrInput == 't':
            with open(file_name, "a") as file:
                #for i in contactList:
                file.write(' '.join(contactList))
                file.close()
    else:
        print(Fore.RED + "Nepavyko sukurti failo\n")
        menu()
    print(Fore.LIGHTGREEN_EX + "Sekmingai sukurtas failas \n", file_name)
    print(Fore.BLUE + "Griztama i meniu\n")
    time.sleep(1.0)
    menu()


#=======================================================KONSOLES MENIU
def menu():
    kbrInput = input(Fore.RESET + 
    """===========SVEIKI===========\n
    1. Tycinio bankroto duomenys
    2. Duomenys is VMI
    3. Kontaktiniu duomenu isgavimas
    0. Baigti darba

    Iveskite pasirinkima:""")
    print("\n")
    if kbrInput == '1':
        bank = tycinisBankrotas()
        if len(bank) == 0:
            print(Fore.RED + "Grazinama tuscia eilute, informacijos nepavyko surasti, bandykite dar karta \n")
            bank = tycinisBankrotas()
        print(Fore.LIGHTGREEN_EX + "Gauti duomenys")
        print(bank)
        json_csv(bank)
    elif kbrInput == '2':
        vp = viesiejiPirkimai()
        if len(vp) == 0:
            print(Fore.RED + "Informacija nebuvo rasta, bandykite dar karta")
            vp = tycinisBankrotas()
        print(Fore.LIGHTGREEN_EX + "Gauti duomenys \n")
        print(vp)
        json_csv(vp)
    elif kbrInput == '3':
        web = contactScraper()
        if len(web) != 0:
            if  not (web[0] and web[0].strip()) and not (web[1] and web[1].strip()):# == "" and web[1] == "":
                print(Fore.RED + "Nepavyko rasti duomenu \n")
                web = contactScraper()
            elif (web[0] and web[0].strip()) and (web[1] and web[1].strip()):
                print(Fore.LIGHTGREEN_EX + "Gauti duomenys")
                print(Fore.RESET, web)
                textFile(web)
            else:  
                if web[0] and web[0].strip():
                    print(Fore.LIGHTGREEN_EX + "Gautas el. pastas")
                    print(Fore.RESET, web[0])
                    textFile(web[0])
                elif web[1] and web[1].strip():
                    print(Fore.LIGHTGREEN_EX + "Gautas numeris")
                    print(Fore.RESET, web[1])
                    textFile(web[1])
                else:
                    print(Fore.RED + "Nepavyko rasti duomenu, badykite dar karta\n")
                    web = contactScraper()
        else:
            print(Fore.RED + "Ivyko klaida \n")
            menu()
    elif kbrInput == '0':
        sys.exit()
    else:
        print(Fore.RED + "Tokio pasirinkimo nera, bandykite dar karta")
        menu()
menu()
#===============================================================
