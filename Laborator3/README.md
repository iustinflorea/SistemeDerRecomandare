Am incarcat produsele Adidas si Nike in Recombee folosind Python, pandas, SDK-ul oficial Recombee si cereri Batch, in loturi de cate 100.

Randuri initiale: 3.268
ID-uri unice (Product ID): 3.179
ID-uri lipsa: 0

Diferenta provine din 89 de randuri cu ID-uri duplicate. Recombee identifica produsele prin itemId, deci ID-urile repetate nu reprezinta item-uri distincte.
Scriptul recombee_items.py citeste CSV-ul, mapeaza proprietatile definite si le trimite catre Recombee folosind SetItemValues si Batch.
Incarcarea a fost verificata în Recombee Admin UI, sectiunea Items, unde catalogul afisează 3.179 de item-uri si proprietatile acestora.
