# Extrator de Itens de NF-e

Projeto pessoal - UC9 SENAC SP
Automação para extrair código, nome, quantidade e unidade de Notas Fiscais Eletrônicas e exportar para Excel.

### O problema
Digitação manual de itens de DANFE em PDF para planilha. Lento e sujeito a erro.

### V1 - PDF
`teste_codigo.py` - Lê PDFs com `pdfplumber`, extrai via regex. 
Aprendizado real: descrição quebrada em 2 linhas, vírgula brasileira `2.251,6000`, duplicação de itens, protocolo sendo lido como código de produto. Tudo debugado na mão.

### V2 - XML
`teste_em_xml.py` - Lê o XML da SEFAZ direto. Sem regex. 
`<cProd>`, `<xProd>`, `<qCom>`, `<uCom>` - 100% fiel.

### Tecnologias
Python, pdfplumber, pandas, xml.etree, openpyxl

### Como usar
1. Coloque os .xml ou .pdf na pasta `PASTA_NOTAS`
2. `python teste_em_xml.py`
3. Sai `lista_materiais_xml.xlsx`

---
Desenvolvido com Python básico + pair programming com IA. Eu guiei o processo, validei cada saída e corrigi os bugs. A IA acelerou, o domínio fiscal foi meu.
