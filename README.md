# SRI-LGPD: Sistema de Recuperação de Informações Simplificado sobre a LGPD

**Disciplina:** Organização e Recuperação da Informação  
**Tema:** Lei Geral de Proteção de Dados (LGPD)  
**Grupo:**

- Alan Cézar 
- Carlos Eduardo
- Gildo Rodrigues
- Maria Fernanda 

## Descrição do Projeto

Este repositório contém a implementação de um **Sistema de Recuperação de Informações (SRI) simplificado**, desenvolvido como trabalho acadêmico com foco na **Lei Geral de Proteção de Dados (LGPD)**. O sistema é dividido em **três módulos principais**:

1. **Indexação de artigos científicos**
2. **Armazenamento estruturado**
3. **Recuperação de informações** com suporte aos modelos **Booleano** e **Espaço Vetorial**


## Objetivo

Construir um SRI funcional que:
- Indexa 20 artigos científicos sobre LGPD
- Armazena metadados e frequências de termos de forma estruturada
- Permite consultas via interface gráfica com dois modelos de recuperação:
  - **Booleano** (AND, OR, NOT)
  - **Espaço Vetorial** (similaridade cosseno)


## Funcionalidades Implementadas

### 1. **Preparação da Base (Indexação)**
- Extração de: Título, Autor(es), Filiação, Resumo, Palavras-chave
- Processamento do **resumo**:
  - Tokenização (hífen como letra)
  - Normalização: minúsculas + acentuação preservada
  - Remoção de stop-words
  - Cálculo de **TF (Term Frequency)** por documento


### 2. **Recuperação de Informações**
- **Interface gráfica** para inserção de consultas
- Pré-processamento idêntico à indexação
- Dois modelos de busca:
  - **Booleano**: suporta `AND`, `OR`, `NOT`
  - **Espaço Vetorial**: ranking por similaridade cosseno
- Resultados ordenados por relevância
- Clique para ver detalhes completos do artigo


## Tecnologias Utilizadas

- **Linguagem**: Python
- **Bibliotecas**:
  - `re` (expressões regulares)
  - `json` / `pickle` (persistência)
  - `numpy` (cálculo de similaridade)
  - `tkinter` ou `streamlit` (interface gráfica)
- **Formato de dados**: JSON ou estruturas em memória com persistência

## Base de Dados

- **20 artigos científicos** sobre LGPD
- Fontes: IEEE, SciELO, Google Scholar, Repositórios institucionais
- Temas: privacidade, conformidade, impacto na saúde, educação, tecnologia, etc.
