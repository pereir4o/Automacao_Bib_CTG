# 📚 Automação de Extração e Indexação de Dados Bibliográficos | CTG-UFPE

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green.svg)](https://www.selenium.dev/)
[![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-API%20v4-yellow.svg)](https://developers.google.com/sheets/api)

Solução ponta a ponta (End-to-End) desenvolvida para otimizar o fluxo de tratamento de dados da Biblioteca do Centro de Tecnologia e Geociências (CTG) da Universidade Federal de Pernambuco (UFPE).

O projeto surgiu de um pedido feito por minha ex chefe (fui bolsista PROGEPE na Bib. CTG) e resolveu um gargalo operacional massivo na auditoria de mais de 3.000 trabalhos acadêmicos (Teses e Dissertações) destinados ao processo de descarte institucional, substituindo semanas de conferência manual por um processamento automatizado de alta precisão.

---

## 🎯 Impacto e Resultados

- **96% de Taxa de Sucesso:** Validação e indexação automática de acervos diretamente no portal institucional.
- **Redução Drástica de Tempo:** Processo reduzido de várias semanas de esforço manual para poucas horas de execução em segundo plano.
- **Precisão Institucional:** Direcionamento do capital humano (bibliotecários) apenas para o tratamento de exceções (4% de casos complexos ou não cadastrados no sistema legado).

---

## ⚙️ Arquitetura da Solução

O ecossistema foi estruturado em 4 grandes etapas integradas:

1. **Mineração de Documentos Não Estruturados (PDF):** Utilização da biblioteca `PyMuPDF (fitz)` aliada a Expressões Regulares (`Regex`) para ler mais de 200 páginas do catálogo bruto e extrair autor, título, ano e código de acervo.
2. **Integração em Nuvem (Google Sheets API):** Conexão via `gspread` e `Service Account` para ler a base de dados de trabalho colaborativa e mapear lacunas (células vazias ou pendentes).
3. **Automação Web & RPA (Selenium WebDriver):** Navegação autônoma no sistema Pergamum (portal de acervo da UFPE) para pesquisar códigos de acervo, filtrar bibliotecas específicas (Tecnologia e Geociências) e capturar metadados atualizados em tempo real.
4. **Atualização em Bloco (Batch Update):** Otimização de chamadas de API (reduzindo verbosidade e latência) ao preencher os dados validados de forma simultânea nas planilhas de auditoria.

**Recomendo fortemente a leitura do READM me na pasta src, onde explico a estrutura dos módulos de 1 à 4.**

---

## 🛠️ Tech Stack

- **Linguagem Principal:** Python
- **Manipulação de PDFs e Texto:** `PyMuPDF`, `re` (Regex)
- **Engenharia de Dados & Mapeamento:** `Pandas`
- **Automação Web / Web Scraping:** `Selenium WebDriver` (Microsoft Edge)
- **Integração com APIs:** `gspread`, `oauth2client`

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Navegador Microsoft Edge (e seu respectivo WebDriver compatível com a versão instalada).
- Conta de Serviço (Service Account) configurada no Google Cloud Platform com acesso à API do Google Sheets e Drive.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/pereir4o/automacao-biblioteca-ctg.git](https://github.com/pereir4o/automacao-biblioteca-ctg.git)
cd automacao-biblioteca-ctg