import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re

def extrair_dados_e_salvar(url, nome_pasta, nome_arquivo):
    # Configurar o WebDriver (certifique-se de ter o driver correspondente instalado)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Espera implícita de 10 segundos

    # Vá para a URL
    driver.get(url)

    # Aguarde até que pelo menos um elemento com a div 'title' esteja presente
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'title_907100321807437769'))
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
    hotel_names = [div.text for div in soup.find_all('div', {'data-testid': 'listing-card-title'})]
    hotel_prices = [total.text.replace('Total de', '').strip() for total in soup.find_all('div', class_='_tt122m')]
    hotel_ratings_information = [span.text for span in soup.find_all('span', {'class': 'r1dxllyb dir dir-ltr'})]

    # Duas listas para os valores dentro e fora dos parênteses
    hotel_ratings = []
    hotel_reviews = []

    for rating in hotel_ratings_information:
        match = re.search(r'([\d,.]+)\s*\((\d+)\)', rating)
        if match:
            rating = match.group(1)
            reviews = match.group(2)
        else:
            rating = 'Novo'
            reviews = '0'

        hotel_ratings.append(rating)
        hotel_reviews.append(reviews)

    # Check the lengths of the lists
    print("Length of hotel_names:", len(hotel_names))
    print("Length of hotel_prices:", len(hotel_prices))
    print("Length of hotel_ratings:", len(hotel_ratings))
    print("Length of hotel_ratings:", len(hotel_reviews))

    # Garanta que todas as listas têm o mesmo comprimento
    min_length = min(len(hotel_names), len(hotel_prices), len(hotel_ratings), len(hotel_reviews))
    hotel_names = hotel_names[:min_length]
    hotel_prices = hotel_prices[:min_length]
    hotel_ratings_information = hotel_ratings_information[:min_length]
    hotel_ratings = hotel_ratings[:min_length]
    hotel_reviews = hotel_reviews[:min_length]


    # Criar um DataFrame pandas
    df = pd.DataFrame({'Nome do Hotel': hotel_names, 'Preço': hotel_prices, 'Nota': hotel_ratings, 'Número de avaliações': hotel_reviews})

    # Adicionar data no nome do arquivo e horário
    now = datetime.datetime.now()
    nome_arquivo = nome_arquivo + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'

    # Criar o caminho do arquivo com base no diretório fornecido
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)

    # Salvar o DataFrame em um arquivo CSV com delimitador ponto e vírgula
    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig', sep=';')

    print(f'Dados salvos em "{caminho_arquivo}".')

# Exemplo de uso para duas URLs diferentes
extrair_dados_e_salvar('https://www.airbnb.com.br/s/Copacabana--Rio-de-Janeiro-~-RJ/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&query=Copacabana%2C%20Rio%20de%20Janeiro&place_id=ChIJU5wP0iPVmwARDWteYzJhPGk&date_picker_type=calendar&checkin=2023-12-28&checkout=2024-01-02&adults=2&source=structured_search_input_header&search_type=autocomplete_click', 
                       'airbnb/copacabana', 'copacabana_')
extrair_dados_e_salvar('https://www.airbnb.com.br/s/Fernando-de-Noronha-~-PE/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2023-12-28&checkout=2024-01-02&adults=2&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=5&query=Fernando%20de%20Noronha%20-%20PE&place_id=ChIJPXpJbWZSNgYRFYuX2r9S9oM', 
                       'airbnb/noronha', 'noronha_')
extrair_dados_e_salvar('https://www.airbnb.com.br/s/Gramado-~-RS/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2023-12-28&checkout=2024-01-02&adults=2&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=5&query=Gramado%20-%20RS&place_id=ChIJHzIEeEIyGZURpq7lgfAlHKc', 
                       'airbnb/gramado', 'gramado_')
extrair_dados_e_salvar('https://www.airbnb.com.br/s/Jericoacoara-~-CE/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2023-12-28&checkout=2024-01-02&adults=2&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=5&query=Jericoacoara%20-%20CE&place_id=ChIJhaZBB4iG6QcRB38ggdjaV54',
                       'airbnb/jericoacoara','jericoacoara_')
extrair_dados_e_salvar('https://www.airbnb.com.br/s/B%C3%BAzios-~-RJ/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2023-12-28&checkout=2024-01-02&adults=2&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=5&query=B%C3%BAzios%20-%20RJ&place_id=ChIJ2ZoMxAtVlgARoizhHWfxigI',
                       'airbnb/buzios','buzios_')
extrair_dados_e_salvar('https://www.airbnb.com.br/s/Balne%C3%A1rio-Cambori%C3%BA-~-SC/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2023-12-28&checkout=2024-01-02&adults=2&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=5&query=Balne%C3%A1rio%20Cambori%C3%BA%20-%20SC&place_id=ChIJrSrlwly22JQRxOut5vUEwC0',
                       'airbnb/balneario_camboriu','balneario_camboriu_')