# Módulo 1: Extração e Preparação do PDF
import os
import re
import fitz  # antigo PyMuPDF
import pandas as pd

def extrair_dados_pdf(caminho_pdf: str) -> pd.DataFrame:
    """Lê o catálogo em PDF e retorna um DataFrame com acervo e autor extraídos."""
    if not os.path.exists(caminho_pdf):
        raise FileNotFoundError(f"Arquivo PDF não encontrado no caminho: {caminho_pdf}")

    lista_trabalhos = []
    # Regex captura Autor, Título, Ano e Acervo no padrão do documento
    padrao_bloco = r"([A-ZÀ-ÖØ-Ý]+,\s[A-Z][a-zà-öø-ÿ]+.*?)\.\s(.+?)Recife,\s(\d{4}).*?Ac\.(\d+)"

    with fitz.open(caminho_pdf) as doc:
        for page_num in range(len(doc)):
            for bloco in doc[page_num].get_text("blocks"):
                encontrados = re.findall(padrao_bloco, bloco[4], flags=re.S)
                for autor, _, _, acervo in encontrados:
                    lista_trabalhos.append({
                        "acervo": acervo.strip(),
                        "autor_pdf": autor.strip().replace('\n', ' ')
                    })

    df_pdf = pd.DataFrame(lista_trabalhos)
    # Remove duplicatas caso o mesmo acervo tenha sido lido mais de uma vez
    return df_pdf.drop_duplicates(subset=["acervo"])

