import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extrair_dados_e_salvar(url, nome_pasta, nome_arquivo):
    # Configurar o WebDriver (certifique-se de ter o driver correspondente instalado)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Espera implícita de 10 segundos

    # Vá para a URL
    driver.get(url)

    # Aguarde até que pelo menos um elemento com a div 'title' esteja presente
    try:
        # Espera explícita por um elemento específico
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.c1eQ2-hotel-name .c1eQ2-big-name'))
        )
    except TimeoutException:
        print("title' não encontrado após o tempo de espera.")

    # Obtenha o conteúdo da página após o carregamento dinâmico
    page_source = driver.page_source

    # Fechar o navegador
    driver.quit()

    # Criar um objeto BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    test_selector = soup.select('.c1eQ2-hotel-name .c1eQ2-big-name')
    print(test_selector)

    # Exemplo de extração de dados (ajuste conforme necessário)
    hotel_names = []
    hotel_links = []

    for hotel_div in soup.find_all('div', {'class': 'c1eQ2-hotel-name'}):
        hotel_name = hotel_div.find('a', {'class': 'c1eQ2-big-name'}).text
        hotel_link = hotel_div.find('a', {'class': 'c1eQ2-big-name'}).get('href')
        hotel_names.append(hotel_name)
        hotel_links.append(hotel_link)

    # Criar um DataFrame pandas
    df = pd.DataFrame({'Nome do Hotel': hotel_names, 'Link do Hotel': hotel_links})


    # Adicionar data no nome do arquivo e horário
    now = datetime.datetime.now()
    nome_arquivo = nome_arquivo + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'

    # Criar o caminho do arquivo com base no diretório fornecido
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)

    # Salvar o DataFrame em um arquivo CSV com delimitador ponto e vírgula
    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig', sep=';')

    print(f'Dados salvos em "{caminho_arquivo}".')

# Exemplo de uso para duas URLs diferentes
extrair_dados_e_salvar('https://www.kayak.com.br/hotels/Praia-de-Copacabana,Rio-de-Janeiro,Brasil-c24146-l159298/2023-12-23/2024-01-03/2adults?sort=distance_a',
                       'kayak/copacabana', 'copacabana_')