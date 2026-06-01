# Volební skraper

## O co jde v projektu?

Tento skript umožňuje získat výsledky parlamentních voleb z roku 2017 pro konkrétní okres z [této webové stránky](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) (vyberte si okres ve sloupci *Výběr obce*) a uložit je do CSV souboru.

## Jak na to?

Před spuštěním projektu si nainstalujte potřebné knihovny uvedené v souboru `requirements.txt`. Skript spustíte z příkazového řádku pomocí následujícího příkazu:

`python volby17_RK.py <odkaz_uzemniho_celku> <vystupni_soubor>`

Výstupem bude soubor .csv s výsledky voleb pro daný okres.

## Jak to vypadá v praxi?

Například pro okres Cheb:

1. Odkaz -> https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101
2. Název výstupního souboru -> `cheb_volby17.csv`
