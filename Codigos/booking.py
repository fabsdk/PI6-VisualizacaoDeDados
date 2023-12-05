import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def extrair_dados_e_salvar(url, nome_pasta, nome_arquivo):
    # Configurar o WebDriver (certifique-se de ter o driver correspondente instalado)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Espera implícita de 10 segundos

    # Vá para a URL
    driver.get(url)

    try:
        # Aguarde até que o pop-up esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="title"]'))
        )

        # Lidar com o pop-up (substitua 'xpath_do_botao_fechar' pelo xpath adequado)
        pop_up_close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="b2searchresultsPage"]/div[44]/div/div/div[1]/div[1]/div/button/span/span/svg/path'))
        )
        pop_up_close_button.click()

    except TimeoutException:
        print("Pop-up não encontrado ou não pode ser fechado.")

    # Aguarde até que pelo menos um elemento com a div 'title' esteja presente
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="title"]'))
        )
    except TimeoutException:
        print("title' não encontrado após o tempo de espera.")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]'))
        )
    except TimeoutException:
        print("price-and-discounted-price' não encontrado após o tempo de espera.")

    # Obtenha o conteúdo da página após o carregamento dinâmico
    page_source = driver.page_source

    # Fechar o navegador
    driver.quit()

    # Criar um objeto BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Exemplo de extração de dados (ajuste conforme necessário)
    hotel_names = [div.text for div in soup.find_all('div', {'data-testid': 'title'})]
    hotel_prices = [div.text for div in soup.find_all('span', {'data-testid': 'price-and-discounted-price'})]
    hotel_notes = [div.text.strip() if div else 'N/A' for div in soup.find_all('div', {'class': 'a3b8729ab1 d86cee9b25'})]
    hotel_room = [h4.text.strip() for h4 in soup.find_all('h4', {'class': 'abf093bdfe e8f7c070a7'})]
    hote_number_of_avaliations = [div.text.strip() if div else 'N/A' for div in soup.find_all('div', {'class': 'abf093bdfe f45d8e4c32 d935416c47'})]
    
    # Garanta que todas as listas têm o mesmo comprimento
    min_length = min(len(hotel_names), len(hotel_prices), len(hotel_notes), len(hotel_room), 
                     len(hote_number_of_avaliations)) 
    hotel_names = hotel_names[:min_length]
    hotel_prices = hotel_prices[:min_length]
    hotel_notes = hotel_notes[:min_length]
    hotel_room = hotel_room[:min_length]
    hote_number_of_avaliations = hote_number_of_avaliations[:min_length]


    print(f'Número de notas {nome_arquivo}: {len(hotel_notes)}')
    print(f'Número de nomes {nome_arquivo}: {len(hotel_names)}')
    print(f'Número de preços {nome_arquivo}: {len(hotel_prices)}')
    print(f'Número de quartos {nome_arquivo}: {len(hotel_room)}')
    print(f'Número de avaliações {nome_arquivo}: {len(hote_number_of_avaliations)}')

    # Criar um DataFrame pandas
    df = pd.DataFrame({'Nome do Hotel': hotel_names, 'Preço': hotel_prices, 'Nota': hotel_notes,
                       'Quarto': hotel_room, 'Número de avaliações': hote_number_of_avaliations})

    # Adicionar data no nome do arquivo e horário
    now = datetime.datetime.now()
    nome_arquivo = nome_arquivo + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'

    # Criar o caminho do arquivo com base no diretório fornecido
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)

    # Salvar o DataFrame em um arquivo CSV com delimitador ponto e vírgula
    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig', sep=';')
    
    print(f'Dados salvos em "{caminho_arquivo}".')

# Exemplo de uso para duas URLs diferentes
extrair_dados_e_salvar('https://www.booking.com/searchresults.pt-br.html?ss=Copacabana%2C+Rio+de+Janeiro%2C+Estado+do+Rio+de+Janeiro%2C+Brasil&map=1&ssne=Rio+de+Janeiro&ssne_untouched=Rio+de+Janeiro&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAS24ARfIAQ_YAQHoAQGIAgGoAgO4Avj39KoGwAIB0gIkYzkyZTc3YWUtMmEzNi00NWM0LWFmZDYtNGE3ODA0ZTA2NmE42AIF4AIB&sid=79d7018dd7d3d4b19c0301afb395f669&aid=304142&lang=pt-br&sb=1&src_elem=sb&src=index&dest_id=1792&dest_type=district&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=b343a48278fd00c4&ac_meta=GhBiMzQzYTQ4Mjc4ZmQwMGM0IAAoATICeGI6BGNvcGFAAEoAUAA%3D&checkin=2023-12-28&checkout=2024-01-02&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure#map_closed', 
                       'booking/copacabana', 'copacabana_')
extrair_dados_e_salvar('https://www.booking.com/searchresults.pt-br.html?ss=Fernando+de+Noronha%2C+Pernambuco%2C+Brasil&ssne=Gramado&ssne_untouched=Gramado&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAS24ARfIAQ_YAQHoAQGIAgGoAgO4Avj39KoGwAIB0gIkYzkyZTc3YWUtMmEzNi00NWM0LWFmZDYtNGE3ODA0ZTA2NmE42AIF4AIB&sid=79d7018dd7d3d4b19c0301afb395f669&aid=304142&lang=pt-br&sb=1&src_elem=sb&src=searchresults&dest_id=900048482&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=537a864afa1502a5&ac_meta=GhA1MzdhODY0YWZhMTUwMmE1IAAoATICeGI6CGZlcm5hbmRvQABKAFAA&checkin=2023-12-28&checkout=2024-01-02&group_adults=2&no_rooms=1&group_children=0', 
                       'booking/noronha', 'noronha_')
extrair_dados_e_salvar('https://www.booking.com/searchresults.pt-br.html?ss=Gramado%2C+Rio+Grande+do+Sul%2C+Brasil&ssne=Copacabana&ssne_untouched=Copacabana&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAS24ARfIAQ_YAQHoAQGIAgGoAgO4Avj39KoGwAIB0gIkYzkyZTc3YWUtMmEzNi00NWM0LWFmZDYtNGE3ODA0ZTA2NmE42AIF4AIB&sid=79d7018dd7d3d4b19c0301afb395f669&aid=304142&lang=pt-br&sb=1&src_elem=sb&src=searchresults&dest_id=-645052&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=d7ff8645b38904bf&ac_meta=GhBkN2ZmODY0NWIzODkwNGJmIAAoATICeGI6A2dyYUAASgBQAA%3D%3D&checkin=2023-12-28&checkout=2024-01-02&group_adults=2&no_rooms=1&group_children=0', 
                       'booking/gramado', 'gramado_')
extrair_dados_e_salvar('https://www.booking.com/searchresults.pt-br.html?ss=Jericoacoara%2C+Cear%C3%A1%2C+Brasil&ssne=Fernando+de+Noronha&ssne_untouched=Fernando+de+Noronha&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAS24ARfIAQ_YAQHoAQGIAgGoAgO4Avj39KoGwAIB0gIkYzkyZTc3YWUtMmEzNi00NWM0LWFmZDYtNGE3ODA0ZTA2NmE42AIF4AIB&sid=79d7018dd7d3d4b19c0301afb395f669&aid=304142&lang=pt-br&sb=1&src_elem=sb&src=searchresults&dest_id=-649321&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=5f4c865901b006da&ac_meta=GhA1ZjRjODY1OTAxYjAwNmRhIAAoATICeGI6Bmplcmljb0AASgBQAA%3D%3D&checkin=2023-12-28&checkout=2024-01-02&group_adults=2&no_rooms=1&group_children=0',
                       'booking/jericoacoara','jericoacoara_')
extrair_dados_e_salvar('https://www.booking.com/searchresults.pt-br.html?ss=B%C3%BAzios%2C+Estado+do+Rio+de+Janeiro%2C+Brasil&ssne=Ubatuba&ssne_untouched=Ubatuba&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAS24ARfIAQ_YAQHoAQGIAgGoAgO4Avj39KoGwAIB0gIkYzkyZTc3YWUtMmEzNi00NWM0LWFmZDYtNGE3ODA0ZTA2NmE42AIF4AIB&sid=79d7018dd7d3d4b19c0301afb395f669&aid=304142&lang=pt-br&sb=1&src_elem=sb&src=searchresults&dest_id=-626254&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=e0508670e4da0391&ac_meta=GhBlMDUwODY3MGU0ZGEwMzkxIAAoATICeGI6AmJ1QABKAFAA&checkin=2023-12-28&checkout=2024-01-02&group_adults=2&no_rooms=1&group_children=0',
                       'booking/buzios','buzios_')
extrair_dados_e_salvar('https://www.booking.com/searchresults.pt-br.html?ss=Balne%C3%A1rio+Cambori%C3%BA%2C+Santa+Catarina%2C+Brasil&ssne=B%C3%BAzios&ssne_untouched=B%C3%BAzios&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAS24ARfIAQ_YAQHoAQGIAgGoAgO4Avj39KoGwAIB0gIkYzkyZTc3YWUtMmEzNi00NWM0LWFmZDYtNGE3ODA0ZTA2NmE42AIF4AIB&sid=79d7018dd7d3d4b19c0301afb395f669&aid=304142&lang=pt-br&sb=1&src_elem=sb&src=searchresults&dest_id=-627380&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=3&search_selected=true&search_pageview_id=5c06867a3ff0051a&ac_meta=GhA1YzA2ODY3YTNmZjAwNTFhIAAoATICeGI6BWJhbG5lQABKAFAA&checkin=2023-12-28&checkout=2024-01-02&group_adults=2&no_rooms=1&group_children=0',
                       'booking/balneario_camboriu','balneario_camboriu_')