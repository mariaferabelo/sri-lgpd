# utils.py
import re
import json
import os

# ----------------------------------------------------------
# Carregar stopwords (arquivo stop.txt)
# ----------------------------------------------------------
def carregar_stopwords(caminho="stop.txt"):
    with open(caminho, "r", encoding="utf-8") as f:
        stopwords = set([linha.strip() for linha in f if linha.strip()])
    return stopwords

# ----------------------------------------------------------
# Normalizar mantendo acentuação e hífens como letra
# ----------------------------------------------------------
def normalizar_texto(texto):
    texto = texto.lower()
    # manter letras (incluindo acentos), números, hífen e espaço
    texto = re.sub(r"[^a-záéíóúàãõâêôç0-9\- ]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# ----------------------------------------------------------
# Tokenizar (separar por espaços; hífen mantido)
# ----------------------------------------------------------
def tokenizar(texto):
    if not texto:
        return []
    return texto.split()

# ----------------------------------------------------------
# Remover stopwords
# ----------------------------------------------------------
def remover_stopwords(tokens, stopwords):
    return [t for t in tokens if t not in stopwords]

# ----------------------------------------------------------
# Pré-processa uma consulta / resumo: normalizar -> tokenizar -> filtrar stopwords
# ----------------------------------------------------------
def preprocessar_texto_bruto(texto, stopwords):
    norm = normalizar_texto(texto)
    tokens = tokenizar(norm)
    tokens_filtrados = remover_stopwords(tokens, stopwords)
    return tokens_filtrados

# ----------------------------------------------------------
# Carregar indice.json e armazenamento.json
# ----------------------------------------------------------
def carregar_indice(caminho="indice.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_armazenamento(caminho="armazenamento.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------------------------------------
# Mapear nome de arquivo -> docId (usando armazenamento.json)
# ----------------------------------------------------------
def criar_mapa_arquivo_para_docid(armazenamento):
    mapa = {}
    tabela = armazenamento.get("tabela_documentos", {})
    for docid_str, meta in tabela.items():
        # em armazenamento criámos docId como inteiro keys; quando foi salvo em JSON, as chaves viraram strings
        try:
            docid = int(docid_str)
        except:
            docid = docid_str
        arquivo = meta.get("arquivo")
        mapa[arquivo] = docid
    return mapa
