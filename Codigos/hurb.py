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
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div:nth-child(3) > div > section > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(1) > h3'))

        )
    except TimeoutException:
        print("title' não encontrado após o tempo de espera.")

    # Obtenha o conteúdo da página após o carregamento dinâmico
    page_source = driver.page_source

    # Fechar o navegador
    driver.quit()

    # Criar um objeto BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Exemplo de extração de dados (ajuste conforme necessário)
    hotel_names = [h3.text for h3 in soup.find_all('h3', {'class': 'h-3j9r7h'})]
    hotel_prices = [strong.text for strong in soup.find_all('strong', {'class': 'h-88jtai'})]
    hotel_notes = [span.text for span in soup.find_all('span', {'class': 'h-t8lbg4'})]

    # Garanta que todas as listas têm o mesmo comprimento
    min_length = min(len(hotel_names), len(hotel_prices), len(hotel_notes)) 
    hotel_names = hotel_names[:min_length]
    hotel_prices = hotel_prices[:min_length]    
    hotel_notes = hotel_notes[:min_length]

    # Criar um DataFrame pandas
    df = pd.DataFrame({'Nome do Hotel': hotel_names, 'Preço': hotel_prices, 'Nota': hotel_notes})

    # Adicionar data no nome do arquivo e horário
    now = datetime.datetime.now()
    nome_arquivo = nome_arquivo + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'

    # Criar o caminho do arquivo com base no diretório fornecido
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)

    # Salvar o DataFrame em um arquivo CSV com delimitador ponto e vírgula
    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig', sep=';')

    print(f'Dados salvos em "{caminho_arquivo}".')

# Exemplo de uso para duas URLs diferentes
extrair_dados_e_salvar('https://www.hurb.com/br/search/hotels?q=Copacabana%2C+Rio+de+Janeiro%2C+Rio+de+Janeiro&tab=hotels&checkin=2023-12-28&checkout=2024-01-02&rooms=2&neighborhoods=neighborhood_copacabana%2Ccity_rio_de_janeiro%2Cstate_rio_de_janeiro%2Ccountry_brasil', 
                       'hurb/copacabana', 'copacabana_')
extrair_dados_e_salvar('https://www.hurb.com/br/search/hotels?q=Fernando+de+Noronha%2C+Pernambuco%2C+Brasil&tab=hotels&checkin=2023-12-28&checkout=2024-01-02&rooms=2&cities=city_fernando_de_noronha%2Cstate_pernambuco%2Ccountry_brasil', 
                       'hurb/noronha', 'noronha_')
extrair_dados_e_salvar('https://www.hurb.com/br/search/hotels?q=gramado&tab=hotels&checkin=2023-12-28&checkout=2024-01-02&rooms=2&search_type=open_search', 
                       'hurb/gramado', 'gramado_')
extrair_dados_e_salvar('https://www.hurb.com/br/search/hotels?q=Jericoacoara%2C+Jijoca+de+Jericoacoara%2C+Cear%C3%A1&tab=hotels&checkin=2023-12-28&checkout=2024-01-02&rooms=2&neighborhoods=neighborhood_jericoacoara%2Ccity_jijoca_de_jericoacoara%2Cstate_ceara%2Ccountry_brasil',
                       'hurb/jericoacoara','jericoacoara_')
extrair_dados_e_salvar('https://www.hurb.com/br/search/hotels?q=BUZIOS%2C+Rio+de+Janeiro%2C+Brasil&tab=hotels&checkin=2023-12-28&checkout=2024-01-02&rooms=2&cities=city_buzios%2Cstate_rio_de_janeiro%2Ccountry_brasil',
                       'hurb/buzios','buzios_')
extrair_dados_e_salvar('https://www.hurb.com/br/search/hotels?q=Balne%C3%A1rio+Cambori%C3%BA%2C+Santa+Catarina%2C+Brasil&tab=hotels&checkin=2023-12-28&checkout=2024-01-02&rooms=2&cities=city_balneario_camboriu%2Cstate_santa_catarina%2Ccountry_brasil',
                       'hurb/balneario_camboriu','balneario_camboriu_')