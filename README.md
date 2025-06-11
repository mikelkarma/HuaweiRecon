# HuaweiRecon

![Logo](https://raw.githubusercontent.com/mikelkarma/HuaweiRecon/refs/heads/main/screenshot.png)


O script permite acessar dados como IPs, endereços MAC e o nome da rede (SSID), oferecendo uma visão detalhada sobre os dispositivos conectados.

## Funcionalidades

- Realiza login em roteadores Huawei e outras marcas.

- Exibe informações de dispositivos conectados, incluindo IPs e MAC addresses.

- Recupera o nome da rede (SSID).

## Como Usar

Exemplo de Uso:

1. Para rodar o script, execute no terminal:
```
python hwdump.py --target 192.168.1.0/24 --devices --offline --log
```

2. Ou, se preferir, use a opção de IP inicial e final:
```
python hwdump.py --start-ip 192.168.1.1 --end-ip 192.168.1.254 --devices --offline --log
```

## Opções Disponíveis:

--target <host ou rede>: Especifica o alvo (ex.: 192.168.1.0/24).

--start-ip <IP inicial>: Define o início do intervalo de IPs.

--end-ip <IP final>: Define o fim do intervalo de IPs.

--devices: Lista apenas dispositivos conectados (clientes).

--offline: Lista dispositivos online e offline.

--log: Ativa o log detalhado das operações.

--ssl: Utiliza protocolo HTTPS (SSL) para as requisições.

--help: Exibe todas as opções e descrições completas.


