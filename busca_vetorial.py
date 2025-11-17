# busca_vetorial.py
import math
from utils import carregar_indice, carregar_armazenamento, carregar_stopwords, preprocessar_texto_bruto, criar_mapa_arquivo_para_docid, normalizar_texto
from collections import defaultdict

# Carrega índice já com idf calculado (arquivo indice.json que você gerou)
# Estrutura esperada em indice.json:
# { "indice_invertido": { termo: { "Artigo_01.json": tf, ... } , ... },
#   "idf": { termo: idf_value, ... } }

def construir_vetores_documentos(indice):
    idf = indice.get("idf", {})
    invert = indice.get("indice_invertido", {})
    docs_vet = {}          # docId -> {termo: tfidf}
    norma_doc = {}         # docId -> norma (sqrt soma squares)
    # primeiro, precisamos converter nomes de arquivo para docId fora deste módulo (quem chama fará)
    # aqui retornamos vetores indexados por nome de arquivo
    for termo, docs in invert.items():
        termo_idf = idf.get(termo, 0.0)
        for arquivo, tf in docs.items():
            if arquivo not in docs_vet:
                docs_vet[arquivo] = {}
            peso = tf * termo_idf
            docs_vet[arquivo][termo] = peso

    # calcular normas
    for arquivo, vec in docs_vet.items():
        s = 0.0
        for w in vec.values():
            s += w * w
        norma = math.sqrt(s) if s > 0 else 0.0
        norma_doc[arquivo] = norma

    return docs_vet, norma_doc

def buscar_vetorial(query, indice_path="indice.json", armazenamento_path="armazenamento.json", stop_path="stop.txt", top_k=20):
    indice = carregar_indice(indice_path)
    armazenamento = carregar_armazenamento(armazenamento_path)
    stopwords = carregar_stopwords(stop_path)
    arquivo_para_docid = criar_mapa_arquivo_para_docid(armazenamento)

    # construir vetores (por arquivo)
    docs_vet, norma_doc = construir_vetores_documentos(indice)
    idf = indice.get("idf", {})

    # pré-processar consulta
    tokens = preprocessar_texto_bruto(query, stopwords)
    if not tokens:
        return []

    # TF da query
    tf_q = {}
    for t in tokens:
        tf_q[t] = tf_q.get(t, 0) + 1

    # construir vetor tf-idf da query
    vec_q = {}
    s_q = 0.0
    for termo, tf in tf_q.items():
        termo_idf = idf.get(termo, None)
        if termo_idf is None:
            # termo não está no vocabulário do corpus -> ignorar
            continue
        peso = tf * termo_idf
        vec_q[termo] = peso
        s_q += peso * peso
    norma_q = math.sqrt(s_q) if s_q > 0 else 0.0
    if norma_q == 0.0:
        return []

    # calcular cosseno por iteração sobre termos da consulta
    scores = {}  # arquivo -> dot product
    for termo, peso_q in vec_q.items():
        # para cada documento que contém termo, somar peso_q * peso_doc
        docs_contendo = indice.get("indice_invertido", {}).get(termo, {})
        for arquivo in docs_contendo.keys():
            peso_doc = docs_vet.get(arquivo, {}).get(termo, 0.0)
            if peso_doc == 0.0:
                continue
            scores[arquivo] = scores.get(arquivo, 0.0) + peso_q * peso_doc

    # normalizar pelos modulos
    ranked = []
    for arquivo, dot in scores.items():
        denom = norma_q * (norma_doc.get(arquivo, 0.0) or 1e-9)
        sim = dot / denom if denom != 0 else 0.0
        docid = arquivo_para_docid.get(arquivo)
        ranked.append((arquivo, docid, sim))

    # ordenar por similaridade decrescente
    ranked.sort(key=lambda x: x[2], reverse=True)
    # retornar top_k (arquivo, docid, score)
    return ranked[:top_k]
