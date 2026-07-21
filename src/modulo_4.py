# Módulo 4: Scraping com Captura Real de Erros
# 
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def buscar_metadados_pergamum(driver, wait: WebDriverWait, acervo: str):
    """Navega no Pergamum e extrai os metadados com tratamento de erros descritivo."""
    driver.get("https://biblioteca.ufpe.br")
    
    try:
        # Passo 1: Busca pelo Código do Acervo
        dropdown = Select(wait.until(EC.presence_of_element_located((By.NAME, "for"))))
        dropdown.select_by_visible_text("Código do Acervo")
        driver.find_element(By.NAME, "q").send_keys(f"{acervo}{Keys.ENTER}")

        # Passo 2: Acessa os detalhes do trabalho
        link_xpath = f"//a[contains(@href, '/acervo/{acervo}')]"
        link = wait.until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
        titulo = link.text.strip()
        driver.execute_script("arguments[0].click();", link)

    except Exception as e:
        raise RuntimeError(f"Acervo não localizado ou erro na busca inicial ({str(e).splitlines()[0]})")

    # Passo 3: Captura de Autor e Ano (Com fallbacks resilientes)
    try:
        autor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.link.hover1.f500"))).text.strip()
    except Exception:
        autor = "Não encontrado no portal"

    try:
        ano = re.search(r'(\d{4})\.', driver.page_source).group(1)
    except Exception:
        ano = "N/A"

    # Passo 4: Filtro de Biblioteca CTG e Captura de Exemplar
    try:
        btn_ex = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Exemplares')]")))
        driver.execute_script("arguments[0].click();", btn_ex)

        filtro = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='Filtrar biblioteca']")))
        filtro.send_keys("Bib. Tecnologia e Geociencias")

        opcao_ctg = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Bib. Tecnologia e Geociencias')]")))
        driver.execute_script("arguments[0].click();", opcao_ctg)

        celula_xpath = "//td[starts-with(text(), '1011')] | //table//tr[contains(., 'Ex. 1')]//td[last()-1]"
        exemplar = wait.until(EC.presence_of_element_located((By.XPATH, celula_xpath))).text.strip()

    except Exception as e:
        raise RuntimeError(f"Exemplar do CTG não disponível ou estruturação de tabela diferente ({str(e).splitlines()[0]})")

    return exemplar, autor, titulo, ano
