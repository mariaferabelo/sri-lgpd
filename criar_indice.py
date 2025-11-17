import os
import json
import math

# ---------------------------------------------------------
# Carrega todos os arquivos JSON (Artigo_XX.json)
# ---------------------------------------------------------
def carregar_documentos(pasta="."):
    documentos = {}
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".json") and arquivo.startswith("Artigo_"):
            with open(os.path.join(pasta, arquivo), "r", encoding="utf-8") as f:
                conteudo = json.load(f)
                documentos[arquivo] = conteudo
    return documentos

# ---------------------------------------------------------
# Criar índice invertido (TERM → {doc: tf})
# ---------------------------------------------------------
def criar_indice(documentos):
    indice = {}

    for doc, dados in documentos.items():
        termos = dados["frequencia_termos"]
        for termo, freq in termos.items():
            if termo not in indice:
                indice[termo] = {}
            indice[termo][doc] = freq
    
    return indice

# ---------------------------------------------------------
# Calcular IDF para o modelo vetorial
# ---------------------------------------------------------
def calcular_idf(indice, total_docs):
    idf = {}
    for termo, docs in indice.items():
        df = len(docs)                    # documentos que contêm o termo
        idf[termo] = math.log(total_docs / df)
    return idf

# ---------------------------------------------------------
# Salvar tudo em um arquivo JSON único
# ---------------------------------------------------------
def salvar_indice(indice, idf, caminho="indice.json"):
    estrutura = {
        "indice_invertido": indice,
        "idf": idf
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=4, ensure_ascii=False)
    print("Arquivo índice.json criado com sucesso!")


# ---------------------------------------------------------
# EXECUÇÃO
# ---------------------------------------------------------
if __name__ == "__main__":
    documentos = carregar_documentos(".")
    indice = criar_indice(documentos)
    idf = calcular_idf(indice, len(documentos))
    salvar_indice(indice, idf)
