import os
import requests
from tqdm import tqdm  # Para a barra de progresso
from colorama import Fore, init  # Para cores no terminal

# Inicializa o colorama para habilitar cores no terminal
init(autoreset=True)

# Função para exibir a arte ASCII
def exibir_arte_ascii():
    arte = """
 ######   ##  ##   ######    #####     ####     ##
  ##  ##  ##  ##    ##  ##  ##   ##   ##  ##   ####
  ##  ##  ##  ##    ##  ##  ##   ##  ##       ##  ##
  #####    ####     #####   ##   ##  ##       ##  ##
  ##        ##      ## ##   ##   ##  ##       ######
  ##        ##      ##  ##  ##   ##   ##  ##  ##  ##
 ####      ####    #### ##   #####     ####   ##  ##
    """
    print(Fore.CYAN + arte)

# Função para criar a pasta de destino
def criar_pasta_destino():
    pasta_destino = "Pyroca Downloads"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(Fore.CYAN + f"Pasta '{pasta_destino}' criada com sucesso.")
    return pasta_destino

# Função para tentar baixar novamente um arquivo que falhou
def tentar_novamente(url, pasta_destino):
    while True:
        escolha = input(Fore.YELLOW + f"Deseja tentar baixar novamente o arquivo de {url}? (s/n): ").strip().lower()
        if escolha == 's':
            return baixar_arquivo(url, pasta_destino)
        elif escolha == 'n':
            print(Fore.RED + f"Download de {url} cancelado.")
            return False
        else:
            print(Fore.YELLOW + "Opção inválida. Digite 's' para sim ou 'n' para não.")

# Função para baixar um arquivo individual
def baixar_arquivo(url, pasta_destino):
    try:
        print(Fore.CYAN + f"Iniciando download de: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Extrai o nome do arquivo da URL
        filename = url.split("/")[-1]
        caminho_completo = os.path.join(pasta_destino, filename)

        # Obtém o tamanho total do arquivo em bytes
        total_size = int(response.headers.get('content-length', 0))

        # Configura a barra de progresso
        with open(caminho_completo, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET),  # Barra colorida
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))  # Atualiza a barra de progresso

        print(Fore.GREEN + f"Download de {filename} concluído com sucesso!")
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao baixar {url}: {e}")
        return False

# Função principal para baixar os arquivos
def baixar_arquivos(url_file):
    # Cria a pasta de destino
    pasta_destino = criar_pasta_destino()

    # Abre o arquivo de texto e lê as URLs
    with open(url_file, 'r') as file:
        urls = file.readlines()

    # Remove espaços em branco e quebras de linha das URLs
    urls = [url.strip() for url in urls if url.strip()]

    # Contador de downloads concluídos
    total_downloads = len(urls)
    downloads_concluidos = 0

    # Loop para baixar cada URL
    for url in urls:
        if not url.startswith(('http://', 'https://')):
            print(Fore.YELLOW + f"URL inválida: {url}. Certifique-se de que a URL começa com 'http://' ou 'https://'.")
            continue  # Pula para a próxima URL

        sucesso = baixar_arquivo(url, pasta_destino)
        if not sucesso:
            if tentar_novamente(url, pasta_destino):
                downloads_concluidos += 1
        else:
            downloads_concluidos += 1

        print(Fore.BLUE + f"Progresso: {downloads_concluidos}/{total_downloads} downloads concluídos.\n")

if __name__ == "__main__":
    # Exibe a arte ASCII
    exibir_arte_ascii()

    # Solicita o caminho do arquivo .txt com as URLs
    url_file = input("Digite o caminho do arquivo .txt com as URLs: ")

    # Chama a função para baixar os arquivos
    baixar_arquivos(url_file)
