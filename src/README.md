# ⚙️ Arquitetura e Módulos do Sistema (`/src`)

Este diretório contém o código-fonte da aplicação, estruturado de forma modular para garantir manutenibilidade, legibilidade e facilidade na execução e nos testes de integração. Também serviu de aprendizagem para estruturas modulares.

A arquitetura foi desenhada para isolar as etapas do pipeline de dados: mineração de documentos não estruturados, processamento tabular, RPA/web scraping e sincronização em nuvem. Abaixo está a representação da estrutura da pasta, seguida pelo detalhamento técnico de cada módulo do sistema.

---

## 🗂️ Estrutura de Arquivos

```text
src/
├── main.py        # Onde acontece a automação e o controle de fluxo
├── modulo_1.py    # Extração e parsing do catálogo institucional em PDF
├── modulo_2.py    # Autenticação e requisições em lote no Google Sheets API
├── modulo_3.py    # Tratamento tabular e merge com Pandas
└── modulo_4.py    # Web Scraping e RPA no sistema Pergamum (com Selenium WebDriver)