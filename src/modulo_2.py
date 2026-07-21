# Módulo 2: Conexão Google Sheets com google-auth
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials  # <-- Importação correta e moderna

def conectar_planilha(caminho_credencial: str, nome_planilha: str):
    """Autentica na API do Google usando google-auth e retorna a planilha e o DataFrame."""
    if not os.path.exists(caminho_credencial):
        raise FileNotFoundError(
            f"❌ Chave JSON não encontrada no caminho: '{caminho_credencial}'.\n"
            f"Dica: O script está rodando a partir da pasta '{os.getcwd()}'."
        )

    escopos = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        creds = Credentials.from_service_account_file(caminho_credencial, scopes=escopos)
        client = gspread.authorize(creds)
        
        sheet = client.open(nome_planilha).sheet1
        df_planilha = pd.DataFrame(sheet.get_all_records())
        df_planilha.columns = [str(c).strip().lower() for c in df_planilha.columns]
        
        return sheet, df_planilha

    except AttributeError as e:
        raise RuntimeError(
            "❌ Erro de método na biblioteca: Você provavelmente está usando o import antigo da 'oauth2client'. "
            "Substitua por: 'from google.oauth2.service_account import Credentials'."
        ) from e

    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(
            f"❌ O arquivo '{caminho_credencial}' foi encontrado, mas o conteúdo não é um JSON válido "
            "ou o arquivo está corrompido. Baixe uma nova chave no Google Cloud."
        ) from e

    except gspread.exceptions.SpreadsheetNotFound as e:
        raise RuntimeError(
            f"❌ A planilha '{nome_planilha}' não foi encontrada ou o e-mail da conta de serviço "
            "(client_email dentro do JSON) não foi adicionado como editor na planilha do Google Drive."
        ) from e

def salvar_em_lotes(sheet, lote_atualizacoes: list):
    """Envia uma lista de atualizações de uma única vez (Batch Update)."""
    if not lote_atualizacoes:
        return
    try:
        sheet.batch_update(lote_atualizacoes)
        print(f" -> [LOTE SALVO COM SUCESSO] {len(lote_atualizacoes)} registros gravados no Google Sheets.")
    except Exception as e:
        print(f" -> [ERRO NO BATCH UPDATE] Falha ao gravar lote na planilha: {str(e)}")
