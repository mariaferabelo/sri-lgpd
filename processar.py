import os
import json
import re

# -------------------------------------------------------------
# 1. Carregar stopwords
# -------------------------------------------------------------
def carregar_stopwords(caminho_stopwords):
    with open(caminho_stopwords, "r", encoding="utf-8") as f:
        stopwords = set([linha.strip() for linha in f.readlines() if linha.strip()])
    return stopwords


# -------------------------------------------------------------
# 2. Extrair apenas o resumo do arquivo Artigo_XX.txt
# -------------------------------------------------------------
def extrair_resumo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.readlines()

    resumo = ""

    for linha in texto:
        if linha.lower().startswith("resumo:"):
            resumo = linha[len("resumo:"):].strip()
            break

    return resumo


# -------------------------------------------------------------
# 3. Normalização e limpeza do texto
# -------------------------------------------------------------
def normalizar_texto(texto):
    texto = texto.lower()                         # manter acentos, apenas minúsculas
    texto = re.sub(r"[^a-záéíóúàãõâêôç0-9\- ]", " ", texto)  # manter letras, números e hífen
    texto = re.sub(r"\s+", " ", texto)            # remover múltiplos espaços
    return texto.strip()


# -------------------------------------------------------------
# 4. Tokenização (separar palavras)
# -------------------------------------------------------------
def tokenizar(texto):
    return texto.split()


# -------------------------------------------------------------
# 5. Remover stopwords
# -------------------------------------------------------------
def remover_stopwords(tokens, stopwords):
    return [t for t in tokens if t not in stopwords]


# -------------------------------------------------------------
# 6. Calcular frequência de termos (TF)
# -------------------------------------------------------------
def calcular_tf(tokens):
    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    return tf


# -------------------------------------------------------------
# 7. Extrair metadados do Artigo_XX.txt (título, autores…)
# -------------------------------------------------------------
def extrair_metadados(caminho):
    dados = {
        "titulo": "",
        "autores": "",
        "filiacao": "",
        "palavras_chave": ""
    }

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.lower().startswith("título:"):
                dados["titulo"] = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("autor("):
                dados["autores"] = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("filiação"):
                dados["filiacao"] = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("palavras"):
                dados["palavras_chave"] = linha.split(":", 1)[1].strip()

    return dados


# -------------------------------------------------------------
# 8. Processar TODOS os artigos de uma pasta
# -------------------------------------------------------------
def processar_todos(pasta=".", stopwords_file="stop.txt"):
    stopwords = carregar_stopwords(stopwords_file)

    # processar todos arquivos no formato Artigo_XX.txt
    for arquivo in os.listdir(pasta):
        if arquivo.startswith("Artigo_") and arquivo.endswith(".txt"):
            caminho = os.path.join(pasta, arquivo)
            print(f"Processando {arquivo}...")

            # extrair dados principais
            resumo = extrair_resumo(caminho)
            metadados = extrair_metadados(caminho)

            # pré-processamento
            texto_normalizado = normalizar_texto(resumo)
            tokens = tokenizar(texto_normalizado)
            tokens_filtrados = remover_stopwords(tokens, stopwords)
            tf = calcular_tf(tokens_filtrados)

            # estrutura final
            dados_final = {
                "arquivo": arquivo,
                "titulo": metadados["titulo"],
                "autores": metadados["autores"],
                "filiacao": metadados["filiacao"],
                "palavras_chave": metadados["palavras_chave"],
                "resumo_original": resumo,
                "tokens_filtrados": tokens_filtrados,
                "frequencia_termos": tf
            }

            # salvar JSON
            nome_json = arquivo.replace(".txt", ".json")
            caminho_json = os.path.join(pasta, nome_json)

            with open(caminho_json, "w", encoding="utf-8") as out:
                json.dump(dados_final, out, indent=4, ensure_ascii=False)

            print(f"→ Criado {nome_json}")

    print("\nProcessamento concluído!")


# -------------------------------------------------------------
# 9. Executar automaticamente
# -------------------------------------------------------------
if __name__ == "__main__":
    processar_todos(".", "stop.txt")
