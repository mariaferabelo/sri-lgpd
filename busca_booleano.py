# busca_booleano.py
from utils import carregar_indice, carregar_armazenamento, carregar_stopwords, preprocessar_texto_bruto, normalizar_texto, criar_mapa_arquivo_para_docid
import re

# ---------------------------------------------------------
# Tokenizador de queries
# ---------------------------------------------------------
def tokenize_query(query):
    # Mantém operadores e parênteses separados
    pattern = r'(\bAND\b|\bOR\b|\bNOT\b|\(|\))'
    parts = re.split(pattern, query, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------
# Shunting-yard: infix → postfix
# ---------------------------------------------------------
def infix_to_postfix(tokens):
    prec = {"NOT": 3, "AND": 2, "OR": 1}
    out = []
    stack = []

    for t in tokens:
        up = t.upper()
        if up in prec:  # operador
            while stack and stack[-1] != "(" and prec.get(stack[-1], 0) >= prec[up]:
                out.append(stack.pop())
            stack.append(up)
        elif t == "(":
            stack.append(t)
        elif t == ")":
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            stack.pop()  # remove "("
        else:
            out.append(t)  # termo normal

    while stack:
        out.append(stack.pop())

    return out


# ---------------------------------------------------------
# Avaliar postfix com pré-processamento correto
# ---------------------------------------------------------
def avaliar_postfix(postfix, indice, armazenamento, stopwords, arquivo_para_docid):
    invert = indice["indice_invertido"]

    # universo de documentos
    universo = set(int(k) for k in armazenamento["tabela_documentos"].keys())

    stack = []

    for tok in postfix:
        up = tok.upper()

        # -------------------------------------------
        # OPERADORES
        # -------------------------------------------
        if up == "NOT":
            a = stack.pop() if stack else set()
            stack.append(universo - a)
            continue

        if up == "AND":
            b = stack.pop() if stack else set()
            a = stack.pop() if stack else set()
            stack.append(a & b)
            continue

        if up == "OR":
            b = stack.pop() if stack else set()
            a = stack.pop() if stack else set()
            stack.append(a | b)
            continue

        # -------------------------------------------
        # TERMO (com pré-processamento padrão)
        # -------------------------------------------
        termo = preprocessar_texto_bruto(tok, stopwords)

        if not termo:
            stack.append(set())
            continue

        # Cada termo vira um conjunto, intersectamos todos
        docs_sets = []
        for t in termo:
            if t in invert:
                docs = set(arquivo_para_docid[arq] for arq in invert[t])
            else:
                docs = set()
            docs_sets.append(docs)

        if not docs_sets:
            stack.append(set())
        else:
            s = docs_sets[0]
            for d in docs_sets[1:]:
                s = s & d
            stack.append(s)

    return stack[0] if stack else set()


# ---------------------------------------------------------
# Função pública
# ---------------------------------------------------------
def buscar_booleano(query,
                    indice_path="indice.json",
                    armazenamento_path="armazenamento.json",
                    stop_path="stop.txt"):

    indice = carregar_indice(indice_path)
    armazenamento = carregar_armazenamento(armazenamento_path)
    stopwords = carregar_stopwords(stop_path)
    mapa = criar_mapa_arquivo_para_docid(armazenamento)

    tokens = tokenize_query(query)
    postfix = infix_to_postfix(tokens)
    resultado = avaliar_postfix(postfix, indice, armazenamento, stopwords, mapa)

    return sorted(resultado)
