import json
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "YOUR-PASSWORD"))

with open("kibana_bulk.json", "r", encoding="utf-8") as f:
    linhas = f.readlines()

documentos = []
for i in range(0, len(linhas), 2):
    if i + 1 < len(linhas):
        doc = json.loads(linhas[i + 1])
        documentos.append(doc)

def inserir(tx, doc):
    if doc["tipo"] == "dispositivo_lan" and "mac" in doc:
        tx.run("""
            MERGE (r:Rede {gateway: $gateway})
            MERGE (d:Dispositivo {mac: $mac})
            SET d += $props
            MERGE (r)-[:TEM]->(d)
        """, gateway=doc["gateway"], mac=doc["mac"], props=doc)

    elif doc["tipo"] == "dados_ppp":
        tx.run("""
            MERGE (r:Rede {gateway: $gateway})
            CREATE (p:DadoPPP)
            SET p += $props
            MERGE (r)-[:USA]->(p)
        """, gateway=doc["gateway"], props=doc)


with driver.session() as session:
    for doc in documentos:
        session.write_transaction(inserir, doc)

print("Dados importados no Neo4j.")
