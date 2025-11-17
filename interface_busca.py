# interface_busca.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from busca_booleano import buscar_booleano
from busca_vetorial import buscar_vetorial
from utils import carregar_armazenamento, carregar_indice
import json
import os

# Carregar armazenamento para exibir metadados
armazenamento = carregar_armazenamento("armazenamento.json")
indice = carregar_indice("indice.json")

# criar mapa docId -> metadados
tabela = armazenamento.get("tabela_documentos", {})
docid_para_meta = {}
for k, v in tabela.items():
    try:
        docid = int(k)
    except:
        docid = k
    docid_para_meta[docid] = v

# janela principal
root = tk.Tk()
root.title("SRI - Busca (Booleano / Vetorial)")
root.geometry("850x600")

# entrada de consulta
frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill="x")

lbl = ttk.Label(frame_top, text="Consulta:")
lbl.pack(side="left")

entry_query = ttk.Entry(frame_top, width=70)
entry_query.pack(side="left", padx=8)

# opções do modelo
model_var = tk.StringVar(value="vetorial")
rb1 = ttk.Radiobutton(frame_top, text="Espaço Vetorial", variable=model_var, value="vetorial")
rb2 = ttk.Radiobutton(frame_top, text="Booleano", variable=model_var, value="booleano")
rb1.pack(side="left", padx=6)
rb2.pack(side="left")

# botão buscar
def on_buscar():
    query = entry_query.get().strip()
    if not query:
        messagebox.showwarning("Aviso", "Digite uma consulta.")
        return
    model = model_var.get()
    lst_results.delete(0, tk.END)
    details_txt.delete(1.0, tk.END)
    if model == "booleano":
        try:
            docids = buscar_booleano(query, indice_path="indice.json", armazenamento_path="armazenamento.json", stop_path="stop.txt")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na busca booleana:\n{e}")
            return
        if not docids:
            lst_results.insert(tk.END, "Sem resultados.")
            return
        # exibir título e autor
        for d in docids:
            meta = docid_para_meta.get(d, {})
            titulo = meta.get("titulo", "—")
            autor = meta.get("autor", meta.get("autor", "—"))
            display = f"[Doc {d}] {titulo} — {autor}"
            lst_results.insert(tk.END, display)
    else:
        # vetorial
        try:
            ranked = buscar_vetorial(query, indice_path="indice.json", armazenamento_path="armazenamento.json", stop_path="stop.txt", top_k=50)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na busca vetorial:\n{e}")
            return
        if not ranked:
            lst_results.insert(tk.END, "Sem resultados relevantes.")
            return
        for arquivo, docid, score in ranked:
            meta = docid_para_meta.get(docid, {})
            titulo = meta.get("titulo", "—")
            autor = meta.get("autor", meta.get("autor", "—"))
            display = f"[{docid}] {titulo} — {autor}  (score={score:.4f})"
            lst_results.insert(tk.END, display)
        # salvar os ranked no contexto para permitir detalhes ao clicar
        root.ranked = ranked

btn_search = ttk.Button(frame_top, text="Buscar", command=on_buscar)
btn_search.pack(side="left", padx=8)

# lista de resultados
frame_mid = ttk.Frame(root, padding=10)
frame_mid.pack(fill="both", expand=True)

lst_results = tk.Listbox(frame_mid, height=12)
lst_results.pack(side="left", fill="both", expand=True)

# detalhes
frame_right = ttk.Frame(frame_mid, padding=10)
frame_right.pack(side="right", fill="both", expand=True)

lbl_det = ttk.Label(frame_right, text="Detalhes")
lbl_det.pack(anchor="w")

details_txt = scrolledtext.ScrolledText(frame_right, wrap=tk.WORD, width=60, height=20)
details_txt.pack(fill="both", expand=True)

# ao clicar em um resultado, mostrar detalhes (título, autores, resumo)
def on_select(event):
    sel = lst_results.curselection()
    if not sel:
        return
    idx = sel[0]
    text = lst_results.get(idx)
    # extrair docId entre colchetes no começo [DocId]
    m = None
    import re
    m = re.match(r"\[(\d+)\]", text)
    if not m:
        # talvez o formato vetorial use [docid] sem "Doc "
        m = re.match(r"\[(\d+)\]", text)
    if not m:
        details_txt.delete(1.0, tk.END)
        details_txt.insert(tk.END, "Não foi possível identificar o documento selecionado.")
        return
    docid = int(m.group(1))
    meta = docid_para_meta.get(docid, {})
    arquivo = meta.get("arquivo")
    # ler o Artigo_XX.json para pegar resumo original e outros metadados
    if arquivo:
        caminho = arquivo
        if not os.path.exists(caminho):
            # talvez arquivo está com extensão .json e nome diferente; tentar procurar
            # procurar por arquivo no diretório com prefixo 'Artigo_' e docid no nome
            found = None
            for f in os.listdir("."):
                if f.startswith("Artigo_") and f.endswith(".json"):
                    found = f
                    break
            caminho = found
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except Exception as e:
            details_txt.delete(1.0, tk.END)
            details_txt.insert(tk.END, f"Erro ao abrir {caminho}: {e}")
            return
        # mostrar metadados e resumo
        details_txt.delete(1.0, tk.END)
        details_txt.insert(tk.END, f"Título: {dados.get('titulo','—')}\n")
        details_txt.insert(tk.END, f"Autores: {dados.get('autores','—')}\n")
        details_txt.insert(tk.END, f"Filiação: {dados.get('filiacao','—')}\n")
        details_txt.insert(tk.END, f"Palavras-chave: {dados.get('palavras_chave','—')}\n\n")
        details_txt.insert(tk.END, "Resumo original:\n")
        details_txt.insert(tk.END, dados.get("resumo_original","—"))
    else:
        details_txt.delete(1.0, tk.END)
        details_txt.insert(tk.END, "Metadados do documento não encontrados.")

lst_results.bind("<<ListboxSelect>>", on_select)

# rodar
root.mainloop()
