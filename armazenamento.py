import os
import json

# -------------------------------------------------------
# 1. Carrega todos os JSONs Artigo_XX.json
# -------------------------------------------------------
def carregar_documentos(pasta="."):
    docs = {}
    for arquivo in os.listdir(pasta):
        if arquivo.startswith("Artigo_") and arquivo.endswith(".json"):
            with open(os.path.join(pasta, arquivo), "r", encoding="utf-8") as f:
                docs[arquivo] = json.load(f)
    return docs


# -------------------------------------------------------
# 2. Criar dicionário global de termos (total corpus)
# -------------------------------------------------------
def criar_dicionario_termos(documentos):
    dicionario = {}
    for doc, dados in documentos.items():
        for termo, freq in dados["frequencia_termos"].items():
            dicionario[termo] = dicionario.get(termo, 0) + freq
    return dicionario


# -------------------------------------------------------
# 3. Criar tabela de documentos <DocId, Título, Autor, TotalTermos>
# -------------------------------------------------------
def criar_tabela_documentos(documentos):
    tabela = {}
    doc_id = 1

    for nome, dados in documentos.items():
        total_termos = sum(dados["frequencia_termos"].values())
        tabela[doc_id] = {
            "arquivo": nome,
            "titulo": dados["titulo"],
            "autor": dados["autores"],
            "total_termos": total_termos
        }
        doc_id += 1

    return tabela, doc_id - 1


# -------------------------------------------------------
# 4. Registro <DocId, TotPal>
# -------------------------------------------------------
def criar_registro(doc_id_final, dicionario_termos):
    total_palavras_significativas = sum(dicionario_termos.values())
    return {
        "ultimo_doc_id": doc_id_final,
        "total_palavras_significativas": total_palavras_significativas
    }


# -------------------------------------------------------
# 5. Salvar módulo 2
# -------------------------------------------------------
def salvar_armazenamento(dic_termos, tabela_docs, registro, saida="armazenamento.json"):
    estrutura = {
        "dicionario_termos": dic_termos,
        "tabela_documentos": tabela_docs,
        "registro": registro
    }
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=4, ensure_ascii=False)

    print("Arquivo armazenamento.json criado com sucesso!")


# -------------------------------------------------------
# Execução principal
# -------------------------------------------------------
if __name__ == "__main__":
    documentos = carregar_documentos(".")
    dic_termos = criar_dicionario_termos(documentos)
    tabela_docs, ultimo_id = criar_tabela_documentos(documentos)
    registro = criar_registro(ultimo_id, dic_termos)
    salvar_armazenamento(dic_termos, tabela_docs, registro)
