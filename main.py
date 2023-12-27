import httpx
import socks

def read_proxies_from_file(file_path):
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def test_proxies_with_api(proxies):
    api_url = "https://api.ipify.org/?format=json" # api para verificar o ip
    verified_proxies = []
    mismatch_proxies = []

    for proxy in proxies:
        url = "https://www.roblox.com" # url que será testado os proxys
        try:
            with httpx.Client(proxies={"http://": f"socks5://{proxy}", "https://": f"socks5://{proxy}"}, timeout=5) as client:
                response = client.get(url) # metodo da verificação em socks5, apenas use socks5

                if response.status_code == 200:
                    api_response = client.get(api_url).json()
                    proxy_ip = proxy.split(":")[0]
                    api_ip = api_response.get("ip")

                    if proxy_ip == api_ip:
                        print(f"[{proxy}] | OK") # ambos estão certos, então ok proxy funciona
                        verified_proxies.append(proxy)
                    else:
                        print(f"[{proxy}] | Mismatch - IP da API: {api_ip}") # se o proxy é diferente que está na api
                        mismatch_proxies.append(proxy)
                else:
                    print(f"[{proxy}] | N/A - Proxy retornou um código de status {response.status_code}.") # codigo que o proxy retornou
        except httpx.RequestError as e:
            print(f"[{proxy}] | N/A - Erro ao conectar ao proxy: {e}") # erro na hora de estabelecer uma conexão

    with open("proxyVerified.txt", "w") as file: # onde vai salvar os proxy que deram ok.
        file.write("\n".join(verified_proxies))
    
    with open("proxyMismatch.txt", "w") as file:
        file.write("\n".join(mismatch_proxies))

if __name__ == "__main__":
    proxy_file_path = "proxy.txt" # onde vai estar a lista de proxy.
    proxies_list = read_proxies_from_file(proxy_file_path)

    if proxies_list:
        test_proxies_with_api(proxies_list)
    else:
        print("Lista de proxies vazia. Verifique o arquivo de proxies.")
