# BIBLIOTECA DO CTG
#RELAÇÃO DE DISSERTAÇÕES E TESES PARA DESCARTE 2026
#%% - Importação das bibliotecas
# Automação 
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Importando de nossos módulos
from modulo_1 import extrair_dados_pdf
from modulo_2 import conectar_planilha, salvar_em_lotes
from modulo_3 import cruzar_planilha_com_pdf
from modulo_4 import buscar_metadados_pergamum

print('\nSucesso!')
#%%
if __name__ == "__main__":
    print("--- INICIANDO AUTOMAÇÃO DE AUDITORIA BIBLIOTECÁRIA (UFPE) ---")

    # 1. CONFIGURAÇÕES EM CAIXA ALTA (Boas práticas de Environment Variables)
    CAMINHO_PDF = os.getenv("CAMINHO_PDF", os.path.join("..", "data", "TESES E DISSERTACOES.pdf"))
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", os.path.join("..", "data", "credenciais_gcp.json"))    
    NOME_PLANILHA = os.getenv("NOME_PLANILHA", "RELAÇÃO DE DISSERTAÇÕES E TESES PARA DESCARTE 2026")
    TAMANHO_DO_LOTE = 20  # Grava no Google Sheets a cada 20 itens processados

    # 2. EXTRAÇÃO DO PDF E MERGE COM A PLANILHA
    print("1/4 -> Extraindo catálogo original em PDF...")
    df_pdf = extrair_dados_pdf(CAMINHO_PDF)

    print("2/4 -> Conectando ao Google Sheets e cruzando dados...")
    sheet, df_planilha = conectar_planilha(GOOGLE_APPLICATION_CREDENTIALS, NOME_PLANILHA)
    df_alvo = cruzar_planilha_com_pdf(df_planilha, df_pdf)

    # 3. INICIALIZAÇÃO DO WEBDRIVER
    print("3/4 -> Abrindo navegador para validação no Pergamum...")
    opcoes = Options()
    opcoes.add_argument("--log-level=3")
    # opcoes.add_argument("--headless") # Descomente para rodar oculto no GitHub Actions
    driver = webdriver.Edge(options=opcoes)
    wait = WebDriverWait(driver, 10)

    lote_atualizacoes = []

    try:
        # 4. LOOP DE ENRIQUECIMENTO
        print("4/4 -> Iniciando varredura. Processando apenas pendências...")
        for i, row in df_alvo.iterrows():
            acervo = str(row['acervo']).strip()
            exemplar_atual = str(row.get('exemplar', '')).strip()

            # Pula os registros que já foram validados ou preenchidos anteriormente
            if exemplar_atual not in ["", "Não encontrado", "Manual", "nan", "0"]:
                continue

            try:
                exemplar, autor, titulo, ano = buscar_metadados_pergamum(driver, wait, acervo)
                print(f"[{i+1}/{len(df_alvo)}] Acervo: {acervo} | OK -> Ex: {exemplar} | Ano: {ano}")

                # Prepara o payload para gravação em lote (Linha na planilha = índice + 2)
                linha_planilha = i + 2
                lote_atualizacoes.append({
                    'range': f'C{linha_planilha}:F{linha_planilha}',
                    'values': [[exemplar, autor, titulo, ano]]
                })

                # Quando o lote atinge 20 itens, faz o disparo para a API de uma vez só!
                if len(lote_atualizacoes) >= TAMANHO_DO_LOTE:
                    salvar_em_lotes(sheet, lote_atualizacoes)
                    lote_atualizacoes.clear()

            except Exception as e:
                # Captura clara do erro sem interromper a execução do restante da lista
                print(f"[{i+1}/{len(df_alvo)}] Acervo: {acervo} | FALHA -> {str(e)}")
                continue

        # Envia qualquer registro restante que não completou um lote de 20
        if lote_atualizacoes:
            salvar_em_lotes(sheet, lote_atualizacoes)

    finally:
        driver.quit()
        print("\n--- AUTOMAÇÃO CONCLUÍDA COM SUCESSO ---")
# %%
