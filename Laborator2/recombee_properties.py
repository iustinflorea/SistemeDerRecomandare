import os

import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItemProperty, ListItemProperties
from recombee_api_client.exceptions import APIException

# TODO 1: Configurare credentiale Recombee
# Introduceti datele din contul vostru (Settings -> API Logins in Recombee Admin UI)
DB_NAME = 'unstpb-ro-adidas-nike-lab'
PRIVATE_TOKEN = ''


# Initializarea clientului Recombee
client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region.EU_WEST)

# TODO 2: Configurare dataset propriu
# Descarcati un dataset (CSV) de pe Kaggle/data.world (100-10K de intrari)
# Urcati fisierul in acelasi folder cu acest script si setati numele in variabila de mai jos
PATH_DATASET = 'AdidasVsNike.csv'

# TODO 3: Definirea schemei de date (minim 3 proprietati)
# Adaptati aceasta lista in functie de coloanele din dataset-ul ales
# Tipurile de date suportate de Recombee includ: 'string', 'int', 'double', 'boolean', 'timestamp'
# Ex.: Pentru filme: titlu (string), an (int), rating (double)
PROPRIETATI_CATALOG = [
    {"name": "product_name", "type": "string"},     # coloana "Product Name"
    {"name": "listing_price", "type": "int"},       # coloana "Listing Price"
    {"name": "sale_price", "type": "int"},          # coloana "Sale Price"
    {"name": "discount", "type": "int"},            # coloana "Discount"
    {"name": "brand", "type": "string"},            # coloana "Brand"
    {"name": "description", "type": "string"},      # coloana "Description"
    {"name": "rating", "type": "double"},           # coloana "Rating"
    {"name": "reviews", "type": "int"},             # coloana "Reviews"
    {"name": "last_visited", "type": "timestamp"},  # coloana "Last Visited"
]

def load_dataset():
    """Functie helper care citeste si verifica dataset-ul"""
    try:
        df = pd.read_csv(PATH_DATASET)
        total_randuri = len(df)
        print(f"Dataset incarcat cu succes! Total randuri: {total_randuri}")

        # Verificare numar de randuri (100 - 10K)
        if total_randuri < 100:
            print("ATENTIE: Dataset-ul are sub 100 de produse!")
        elif total_randuri > 10 * 1000:
            print("ATENTIE: Dataset-ul este prea mare! Limitati-l la primele 10K randuri.")

        print("\nPreview primele 3 randuri:")
        print(df.head(3))
        print("-" * 50)
        return df
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{PATH_DATASET}' nu a fost gasit!")
        return None

def set_properties():
    """Functie care trimite structura coloanelor catre Recombee"""
    print(f"\nIncepe definirea proprietatilor pentru baza de date: '{DB_NAME}'...")

    for prop in PROPRIETATI_CATALOG:
        # Validare nume proprietati valide
        if "nume_proprietate" in prop["name"]:
            print("Eroare: Trebuie sa schimbati 'nume_proprietate_x' cu denumirile reale din coloanele fisierul vostru!")
            continue

        try:
            # Request API Recombee pentru adaugarea proprietatii (echivalentul adaugarii unei coloane intr-un tabel)
            client.send(AddItemProperty(prop["name"], prop["type"]))
            print(f"Proprietatea '{prop['name']}' ({prop['type']}) a fost adaugata cu succes.")
        except APIException as e:
            # Recombee returneaza eroare (409) daca proprietatea a fost deja definita la o rulare anterioara
            if getattr(e, "status_code", None) == 409 or "already exists" in str(e).lower():
                print(f"Proprietatea '{prop['name']}' exista deja in Recombee.")
            else:
                print(f"Eroare API la proprietatea '{prop['name']}': {e}")

def verify():
    """Interogheaza API-ul pentru a lista toate proprietatile active din cont"""
    print("\nSe verifica structura finala din Recombee Admin UI...")
    try:
        atribute_active = client.send(ListItemProperties())
        print("Proprietatile configurate in acest moment in baza ta de date:")
        for atribute in atribute_active:
            print(f"- {atribute['name']} => tip de date: {atribute['type']}")
    except APIException as e:
        print(f"Nu s-a putut efectua verificarea. Detalii eroare: {e}")

if __name__ == "__main__":
    # Verificam daca fisierul CSV local se citeste corect
    dataset_ok = load_dataset()

    if dataset_ok is not None:
        # Trimitem proprietatile catre Recombee prin API
        set_properties()

        # Listam ce s-a salvat in baza de date pentru confirmare
        verify()
