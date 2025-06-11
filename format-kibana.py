import json

def decode_escaped_string(s):
    return s.encode('utf-8').decode('unicode_escape')

with open("akasaka.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("kibana_bulk.json", "w", encoding="utf-8") as f_out:
    for gateway_ip, info in data.items():
        nome_rede_raw = info.get("nome_rede") or ["", ""]
        if not isinstance(nome_rede_raw, list) or len(nome_rede_raw) < 2:
            nome_rede_raw = ["", ""]
        nome_rede = decode_escaped_string(nome_rede_raw[1])

        dispositivos_lan = info.get("dispositivos_lan") or []
        dados_ppp = info.get("dados_ppp") or []

        for dispositivo in dispositivos_lan:
            meta = { "index": { "_index": "redes" } }
            doc = {
                "gateway": gateway_ip,
                "nome_rede": nome_rede,
                "tipo": "dispositivo_lan",
                **dispositivo
            }
            f_out.write(json.dumps(meta) + "\n")
            f_out.write(json.dumps(doc, ensure_ascii=False) + "\n")

        for ppp in dados_ppp:
            meta = { "index": { "_index": "redes" } }
            doc = {
                "gateway": gateway_ip,
                "nome_rede": nome_rede,
                "tipo": "dados_ppp",
                **ppp
            }
            f_out.write(json.dumps(meta) + "\n")
            f_out.write(json.dumps(doc, ensure_ascii=False) + "\n")

print("Arquivo 'kibana_bulk.json' gerado para _bulk do Elasticsearch.")
