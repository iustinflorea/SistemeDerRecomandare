import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
DB_NAME = 'unstpb-ro-adidas-nike-lab'
PRIVATE_TOKEN = 'v3lIOJ75ZXxHdcG8T2jES0vTsrU8TlZGnZuKTpBJ8VhDdgOGYlY0tQoesZrZnpro'

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region.EU_WEST)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = 'AdidasVsNike.csv'

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")
    
    requests = []
    
    for index, row in df.iterrows():
        # TODO 3: Extrageti ID-ul unic al produsului din coloana corespunzatoare din CSV
        item_id = str(row['Product ID'])
        
        # TODO 4: Mapati proprietatile definite anterior cu valorile din randul curent
        # Exemplu:
        properties = {
           "product_name": str(row['Product Name']),
           "listing_price": int(row['Listing Price']),
           "sale_price": int(row['Sale Price']),
           "discount": int(row['Discount']),
           "brand": str(row['Brand']),
           "description": str(row['Description']) if pd.notna(row['Description']) else "",
           "rating": float(row['Rating']) if pd.notna(row['Rating']) else 0.0,
           "reviews": int(row['Reviews']) if pd.notna(row['Reviews']) else 0,
           "last_visited": str(row['Last Visited'])
       }
        
        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))
        
        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            client.send(Batch(requests))
            requests = []
            print("S-a trimis un lot de 100 item-uri...")
            
    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        client.send(Batch(requests))
        print("S-a trimis ultimul lot de item-uri.")
        
    print("Toate item-urile au fost trimise cu succes!")

if __name__ == "__main__":
    send_items()