"""
projekt_3.py: třetí projekt

author: Valterová Kristina
email: valte06367@mot.sps-dopravni.cz
discord: @justt.cattiwo 

"""

import sys
import csv
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 3:
        print("Chyba: Skript vyžaduje 2 argumenty: <odkaz_na_uzemni_celek> <jmeno_vystupniho_souboru.csv>")
        print("Ukázka: python projekt_3.py \"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103\" vysledky.csv")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not url.startswith("https://volby.cz/pls/ps2017nss/"):
        print("Chyba: Zadaný odkaz není platný odkaz na volby.cz pro rok 2017.")
        sys.exit(1)

    print(f"STAHUJI DATA Z VYBRANÉHO ODKAZU: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba při komunikaci se serverem: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    municipalities = []
    tables = soup.find_all('table', class_='table')
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[2:]:
            cols = row.find_all('td')
            if len(cols) >= 3:
                a_tag = cols[0].find('a')
                if a_tag:
                    code = a_tag.text.strip()
                    name = cols[1].text.strip()
                    link = "https://volby.cz/pls/ps2017nss/" + a_tag['href']
                    municipalities.append({'code': code, 'name': name, 'link': link})

    if not municipalities:
        print("Chyba: Na zadaném odkazu nebyly nalezeny žádné obce. Zkontrolujte prosím URL.")
        sys.exit(1)

    print(f"NALEZENO {len(municipalities)} OBCÍ. STAHUJI DETAILY...")

    all_data = []
    party_names_set = []

    for mun in municipalities:
        mun_data = {
            'code': mun['code'],
            'location': mun['name']
        }
        
        try:
            detail_resp = requests.get(mun['link'])
            detail_resp.raise_for_status()
            detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')

            td_registered = detail_soup.find('td', headers=lambda x: x and 'sa2' in x)
            td_envelopes = detail_soup.find('td', headers=lambda x: x and 'sa3' in x)
            td_valid = detail_soup.find('td', headers=lambda x: x and 'sa6' in x)

            mun_data['registered'] = td_registered.text.replace('\xa0', '').replace(' ', '') if td_registered else ""
            mun_data['envelopes'] = td_envelopes.text.replace('\xa0', '').replace(' ', '') if td_envelopes else ""
            mun_data['valid'] = td_valid.text.replace('\xa0', '').replace(' ', '') if td_valid else ""

            detail_tables = detail_soup.find_all('table', class_='table')
            for dt in detail_tables:
                headers_text = [th.text for th in dt.find_all('th')]
                if any("Kandidující strana" in h or "strana" in h.lower() for h in headers_text):
                    dt_rows = dt.find_all('tr')
                    for r in dt_rows[2:]:
                        dt_cols = r.find_all('td')
                        if len(dt_cols) >= 3:
                            party_name = dt_cols[1].text.strip()
                            votes = dt_cols[2].text.replace('\xa0', '').replace(' ', '')
                            if party_name and party_name != "-":
                                mun_data[party_name] = votes
                                if party_name not in party_names_set:
                                    party_names_set.append(party_name)
                                    
        except Exception as e:
            print(f"Varování: Nepodařilo se stáhnout data pro obec {mun['name']} ({e})")
            
        all_data.append(mun_data)

    print(f"UKLÁDÁM DATA DO SOUBORU: {output_file}")

    header = ['code', 'location', 'registered', 'envelopes', 'valid'] + party_names_set

    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
            writer.writeheader()
            for d in all_data:
                row_data = {h: d.get(h, '0') for h in header}
                writer.writerow(row_data)
    except Exception as e:
        print(f"Chyba při ukládání souboru: {e}")
        sys.exit(1)

    print("HOTOVO. UKONČUJI PROGRAM.")

if __name__ == '__main__':
    main()
