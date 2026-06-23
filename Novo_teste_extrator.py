import os
import pandas as pd
import xmltodict

# Pasta onde o script está
PASTA_NOTAS = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_SAIDA = os.path.join(PASTA_NOTAS, "lista_materiais_xml.xlsx")
ARQUIVO_BUSCA = os.path.join(PASTA_NOTAS, "lista_materiais_busca.xlsx")

def extrair_itens_xml(caminho_xml):
    with open(caminho_xml, 'r', encoding='utf-8') as f:
        doc = xmltodict.parse(f.read())

    # NF-e pode vir como nfeProc/NFe ou direto NFe
    nfe = doc.get('nfeProc', {}).get('NFe', doc.get('NFe'))
    inf = nfe['infNFe']

    numero_nota = inf['ide']['nNF']

    # det pode ser lista ou um único dict
    dets = inf['det']
    if not isinstance(dets, list):
        dets = [dets]

    itens = []
    for det in dets:
        prod = det['prod']
        codigo = prod.get('cProd', '')
        nome = prod.get('xProd', '')
        qtd = str(prod.get('qCom', '0')).replace(',', '.')
        un = prod.get('uCom', '')

        try:
            quantidade = float(qtd)
        except:
            quantidade = 0.0

        itens.append({
            "numero_nota": numero_nota,
            "codigo_produto": codigo,
            "nome_produto": nome,
            "quantidade": quantidade,
            "unidade": un
        })
    return itens

def buscar_por_codigo(codigo_busca):
    xmls = [f for f in os.listdir(PASTA_NOTAS) if f.lower().endswith(".xml")]
    resultados = []

    if not xmls:
        print("Nenhum XML encontrado na pasta.")
        return resultados

    print(f"\nBuscando: {codigo_busca}")
    print("-" * 40)

    for arquivo in xmls:
        caminho = os.path.join(PASTA_NOTAS, arquivo)
        try:
            itens = extrair_itens_xml(caminho)
            for it in itens:
                if it["codigo_produto"].strip() == codigo_busca.strip():
                    print(f"NF {it['numero_nota']} | {it['nome_produto']} | {it['quantidade']} {it['unidade']}")
                    resultados.append(it)
        except Exception as e:
            print(f"Erro em {arquivo}: {e}")

    if not resultados:
        print("Nada encontrado.")
    print("-" * 40)
    return resultados

def main():
    while True:
        print("\n=-=- Extrator NF-e - Saintsteel -=-=")
        print("1 - Extrair itens de TODAS as NF-e")
        print("2 - Buscar produtos por código")
        print("3 - Sair")
        op = input("Opção: ").strip()

        if op == "3":
            print("Saindo...")
            break

        if op == "2":
            itens_busca = []
            print("\nDigite um código por vez. Digite 'sair' para gerar a planilha.")
            while True:
                codigo = input("Código: ").strip()
                if codigo.lower() == 'sair':
                    break
                if not codigo:
                    continue
                achados = buscar_por_codigo(codigo)
                itens_busca.extend(achados)

            if itens_busca:
                df_busca = pd.DataFrame(itens_busca)
                df_busca["codigo_produto"] = df_busca["codigo_produto"].astype(str)
                df_busca.to_excel(ARQUIVO_BUSCA, index=False)
                print("\n" + "="*30)
                print(f"Planilha de busca criada: {len(df_busca)} linhas")
                print(f"Arquivo: {ARQUIVO_BUSCA}")
                print("="*30)
            else:
                print("\nNenhum item encontrado. Planilha não criada.")
            continue

        if op!= "1":
            print("Opção inválida")
            continue

        xmls = [f for f in os.listdir(PASTA_NOTAS) if f.lower().endswith(".xml")]
        print("-" * 30)
        print(f"Encontrei {len(xmls)} XMLs")
        print("-" * 30)

        todos_itens = []
        for arquivo in xmls:
            caminho = os.path.join(PASTA_NOTAS, arquivo)
            try:
                itens = extrair_itens_xml(caminho)
                todos_itens.extend(itens)
                num = itens[0]["numero_nota"] if itens else "?"
                print(f"NF {num}: {len(itens)} itens")
            except Exception as e:
                print(f"Erro em {arquivo}: {e}")

        if not todos_itens:
            print("Nenhum material encontrado.")
            continue

        df = pd.DataFrame(todos_itens)
        df["codigo_produto"] = df["codigo_produto"].astype(str)
        df.to_excel(ARQUIVO_SAIDA, index=False)
        print(f"\nPlanilha completa salva em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()