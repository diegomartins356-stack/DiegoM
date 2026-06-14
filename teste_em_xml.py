import os
import pandas as pd
import xml.etree.ElementTree as ET

PASTA_NOTAS = r"C:\Users\Computador PC\OneDrive - SENAC - SP\Documentos\UC 9\Projeto Pessoal Python"
ARQUIVO_SAIDA = os.path.join(PASTA_NOTAS, "lista_materiais_xml.xlsx")

def extrair_itens_xml(caminho_xml):
    itens = []
    tree = ET.parse(caminho_xml)
    root = tree.getroot()
    
    # NF-e usa namespace, funciona tanto pra nfeProc quanto pra NFe solta
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
    for det in root.findall('.//nfe:det', ns):
        prod = det.find('nfe:prod', ns)
        if prod is None:
            continue
            
        codigo = prod.findtext('nfe:cProd', '', ns)
        nome = prod.findtext('nfe:xProd', '', ns)
        qtd = prod.findtext('nfe:qCom', '0', ns)
        un = prod.findtext('nfe:uCom', '', ns)
        
        try:
            quantidade = float(qtd)
        except:
            quantidade = 0.0
        
        itens.append({
            "arquivo_nfe": os.path.basename(caminho_xml),
            "codigo_produto": codigo,
            "nome_produto": nome,
            "quantidade": quantidade,
            "unidade": un
        })
    return itens

def main():
    todos_itens = []
    xmls = [f for f in os.listdir(PASTA_NOTAS) if f.lower().endswith(".xml")]
    
    print(f"Encontrados {len(xmls)} XMLs em {PASTA_NOTAS}")
    
    for arquivo in xmls:
        caminho = os.path.join(PASTA_NOTAS, arquivo)
        try:
            itens = extrair_itens_xml(caminho)
            todos_itens.extend(itens)
            print(f"{arquivo}: {len(itens)} itens")
            for it in itens:
                print(f"  {it['codigo_produto']} -> {it['quantidade']} {it['unidade']}")
        except Exception as e:
            print(f"Erro em {arquivo}: {e}")
    
    if not todos_itens:
        print("Nenhum item encontrado. Coloque os .xml na pasta.")
        return
    
    df = pd.DataFrame(todos_itens)
    df.to_excel(ARQUIVO_SAIDA, index=False)
    print(f"\nPronto! {len(df)} linhas extraídas.")
    print(f"Salvo em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()
    