import os
import re
import pdfplumber
import pandas as pd

PASTA_NOTAS = r"C:\Users\Computador PC\OneDrive - SENAC - SP\Documentos\UC 9\Projeto Pessoal Python"
ARQUIVO_SAIDA = "lista_materiais.xlsx"

def parse_quantidade(valor_str):
    if not valor_str:
        return 0.0
    s = str(valor_str).strip().replace(" ", "")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except:
        return 0.0

def extrair_itens_pdf(caminho_pdf):
    itens = []
    vistos = set()
    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            texto = page.extract_text(x_tolerance=1.5) or ""
            # 1. código 4 a 8 dígitos, não pega protocolo
            # 2. descrição para antes do próximo código
            # 3. quantidade aceita 700 / 100 / 2.251,6000
            padrao = re.compile(
                r'(?<!\d)(\d{4,8})(?!\d)\s+((?:(?!\b\d{4,8}\b).)+?)\s+(\d{8})\s+\d{3}\s+\d{4}\s+(KG|UN|PC|CX|T|M|M2|L)\s+([\d\.,]+)',
                re.DOTALL | re.IGNORECASE
            )
            for m in padrao.finditer(texto):
                codigo, descricao, ncm, un, quant_str = m.groups()
                descricao = re.sub(r'\s+', ' ', descricao).strip()

                # descarta cabeçalho se ainda escapar
                if any(x in descricao.upper() for x in ["INSCRIÇÃO", "CNPJ", "PROTOCOLO", "DESTINATÁRIO"]):
                    continue

                quantidade = parse_quantidade(quant_str)
                if quantidade == 0:
                    continue

                chave = (codigo, quantidade, un.upper())
                if chave in vistos:
                    continue
                vistos.add(chave)

                itens.append({
                    "arquivo_nfe": os.path.basename(caminho_pdf),
                    "codigo_produto": codigo,
                    "nome_produto": descricao[:150],
                    "quantidade": quantidade,
                    "unidade": un.upper()
                })
    return itens

def main():
    todos_itens = []
    for arquivo in os.listdir(PASTA_NOTAS):
        if arquivo.lower().endswith(".pdf"):
            caminho = os.path.join(PASTA_NOTAS, arquivo)
            try:
                itens = extrair_itens_pdf(caminho)
                todos_itens.extend(itens)
                print(f"{arquivo}: {len(itens)} itens")
                for it in itens:
                    print(f"  {it['codigo_produto']} -> {it['quantidade']} {it['unidade']}")
            except Exception as e:
                print(f"Erro em {arquivo}: {e}")

    if not todos_itens:
        print("Nenhum item encontrado.")
        return

    df = pd.DataFrame(todos_itens)
    df.to_excel(ARQUIVO_SAIDA, index=False)
    print(f"\nPronto! {len(df)} linhas extraídas.")
    print(f"Salvo em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()