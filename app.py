from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import atexit
import os
import traceback
from datetime import datetime

# --- Configuração do Flask ---
app = Flask(__name__, template_folder='templates')

# --- Cache do driver ---
driver = None

def init_webdriver():
    """Inicializa a instância global do WebDriver manualmente."""
    global driver
    if driver is None:
        print("Iniciando uma nova instância do WebDriver (modo manual)...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            driver_path = os.path.join(script_dir, 'chromedriver.exe')
            if not os.path.exists(driver_path):
                print("ERRO: 'chromedriver.exe' não encontrado. Coloque-o ao lado de 'app.py'.")
                return
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("WebDriver iniciado com sucesso.")
        except Exception as e:
            print(f"Erro ao iniciar o WebDriver: {e}")
            driver = None

def close_webdriver():
    """Fecha a instância do WebDriver."""
    global driver
    if driver:
        print("Fechando o WebDriver...")
        driver.quit()

init_webdriver()
atexit.register(close_webdriver)

def scrape_live_stock_data(ticker_code):
    """Busca os dados em tempo real de uma ação."""
    # ... (código existente para dados em tempo real, sem alterações) ...
    if driver is None:
        return {'error': 'O WebDriver não está disponível.'}
    url = f"https://finance.yahoo.com/quote/{ticker_code.upper()}.SA"
    try:
        print(f"Acessando {url} para dados em tempo real...")
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        try:
            consent_iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Consent Management Platform"]')))
            driver.switch_to.frame(consent_iframe)
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar') or contains(., 'Accept all')]")))
            accept_button.click()
            driver.switch_to.default_content()
        except TimeoutException:
            pass # Continua se não houver pop-up
        price_selector = f"fin-streamer[data-symbol='{ticker_code.upper()}.SA'][data-field='regularMarketPrice']"
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
        title_element = driver.find_element(By.CSS_SELECTOR, "h1")
        change_selector = f"fin-streamer[data-symbol='{ticker_code.upper()}.SA'][data-field='regularMarketChange']"
        percent_change_selector = f"fin-streamer[data-symbol='{ticker_code.upper()}.SA'][data-field='regularMarketChangePercent']"
        change_element = driver.find_element(By.CSS_SELECTOR, change_selector)
        percent_change_element = driver.find_element(By.CSS_SELECTOR, percent_change_selector)
        data = {
            'ticker': f"{ticker_code.upper()}.SA",
            'company_name': title_element.text.split('(')[0].strip(),
            'price': price_element.get_attribute('value'),
            'change': change_element.get_attribute('value'),
            'percent_change': percent_change_element.get_attribute('value').strip('()'),
        }
        print(f"Dados em tempo real coletados: {data}")
        return data
    except Exception:
        # ... (código de tratamento de erro existente) ...
        return {'error': 'Não foi possível coletar os dados em tempo real.'}


def scrape_historical_stock_data(ticker_code, start_date_str, end_date_str):
    """Busca os dados históricos de uma ação em um período."""
    if driver is None:
        return {'error': 'O WebDriver não está disponível.'}

    # Converte as datas para timestamps Unix, que a URL do Yahoo usa
    start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    period1 = int(start_dt.timestamp())
    period2 = int(end_dt.timestamp())
    
    url = f"https://finance.yahoo.com/quote/{ticker_code.upper()}.SA/history?period1={period1}&period2={period2}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    
    try:
        print(f"Acessando {url} para dados históricos...")
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Espera a tabela de dados históricos carregar
        table_selector = "table[data-test='historical-prices']"
        print(f"Aguardando a tabela ({table_selector}) carregar...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, table_selector)))
        print("Tabela carregada.")

        # Coleta os dados da tabela
        table = driver.find_element(By.CSS_SELECTOR, table_selector)
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        historical_data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            # Ignora linhas que não são de dados (ex: dividendos, que têm menos colunas)
            if len(cols) == 7:
                historical_data.append({
                    "date": cols[0].text,
                    "open": cols[1].text,
                    "high": cols[2].text,
                    "low": cols[3].text,
                    "close": cols[4].text,
                    "adj_close": cols[5].text,
                    "volume": cols[6].text,
                })
        
        print(f"Coletados {len(historical_data)} registros históricos.")
        return historical_data

    except Exception:
        print("\n--- ERRO NO SCRAPING HISTÓRICO ---")
        print(traceback.format_exc())
        screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_screenshot_historical.png')
        driver.save_screenshot(screenshot_path)
        print(f"Uma captura de tela foi salva em: {screenshot_path}")
        return {'error': 'Não foi possível coletar os dados históricos.'}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-data')
def get_data():
    """Endpoint para dados em tempo real."""
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'O código da ação é obrigatório.'}), 400
    
    data = scrape_live_stock_data(ticker)
    
    if 'error' in data:
        return jsonify(data), 404
        
    return jsonify(data)

@app.route('/api/get-historical-data')
def get_historical_data():
    """Novo endpoint para dados históricos."""
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not all([ticker, start_date, end_date]):
        return jsonify({'error': 'Ticker, data de início e data de fim são obrigatórios.'}), 400

    data = scrape_historical_stock_data(ticker, start_date, end_date)

    if isinstance(data, dict) and 'error' in data:
        return jsonify(data), 404
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

