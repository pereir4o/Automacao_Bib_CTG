# Módulo 3: O Merge Analítico com Pandas

import pandas as pd

def cruzar_planilha_com_pdf(df_planilha: pd.DataFrame, df_pdf: pd.DataFrame) -> pd.DataFrame:
    """Realiza o merge entre a Planilha e o PDF apontando para o nome exato da coluna do Google Sheets."""
    
    # Padroniza a chave 'acervo' como string para o merge não falhar por conflito de tipos (texto vs número)
    df_planilha['acervo'] = df_planilha['acervo'].astype(str).str.strip()
    df_pdf['acervo'] = df_pdf['acervo'].astype(str).str.strip()

    # Merge Left: Mantém toda a estrutura original da planilha e acopla os dados do PDF onde o acervo bater
    df_merge = pd.merge(df_planilha, df_pdf, on='acervo', how='left')

    # Nome exato da coluna de autor após passar pelo .strip().lower() na etapa de conexão
    coluna_autor = 'autor (sobrenome, nome)'

    # Se a extração do PDF trouxe o 'autor_pdf', preenchemos as lacunas da coluna oficial da planilha
    if 'autor_pdf' in df_merge.columns:
        df_merge[coluna_autor] = df_merge[coluna_autor].replace(['', 'nan', 'Não encontrado', 'None'], pd.NA)
        df_merge[coluna_autor] = df_merge[coluna_autor].fillna(df_merge['autor_pdf'])
        df_merge = df_merge.drop(columns=['autor_pdf']) # Descarta a coluna temporária que veio do PDF

    return df_merge
