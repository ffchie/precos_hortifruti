'''
Descobrir a quantide de páginas disponíveis
    Percorrer todas as páginas
        Todos os produtos
Pegar o nome do produto
Pagar o valor do produto
Pegar o fabricante
Pegar a % de desconto do produto
Salvar em um arquivo xlsx
'''

from bs4 import BeautifulSoup
import requests
import openpyxl

def ConsultarQuantidadePagina(url):
    resposta = requests.get(url)

    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        pagina = soup.find('div', class_ = 'page-template') # find retorna o primeiro resultado
        div = pagina.find_all('div', class_ = 'text-center pt-3' ) # find_all retorna todos os resultados
        div = div[-1].text # o -1 mostra a última página, de 0 a frente mostra as paginas em sentido crescente
        qntd = div.split(' ')[-1]
        return qntd

def ConsultarProdutosPaginas(url):
    resposta = requests.get(url)

    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        pagina = soup.find('div', class_ = 'list-products page-content')
        produtos = pagina.find_all('div', class_ = 'desc position-relative')
        lista_produtos = []
        for item in produtos:
            nome = item.find('h2', class_ = 'title').text.strip()
            fabricante = item.find('span', class_ = 'font-size-11 text-primary font-weight-bold').text.strip()

            
            if bool(item.find('p', class_ = 'sale-price')):
                valor = item.find('p', class_ = 'sale-price').text.strip()
            else:
                valor = 'Sem estoque'      


            if bool(item.find('span', class_ = 'discount')):
                desconto = item.find('span', class_ = 'discount').text.strip()
            else:
                desconto = ' '

            lista_produtos.append([
                nome,
                valor,
                fabricante,
                desconto
            ])
        return lista_produtos
           
def GravarArquivosXLSX(dados, nome_arquivo):
    try:
        excel = openpyxl.Workbook()
        planilha = excel.active
        
        for linha in dados:
            planilha.append(linha)

        excel.save(nome_arquivo + '.xlsx')
        print('Dados salvos com sucesso no arquivo {}.xlsx'.format(nome_arquivo))
    except Exception as ex:
        print('Error: {}'.format(ex))

area = 'hortifruti'       

url = 'https://www.superpaguemenos.com.br/{}/'.format(area)
qntd = ConsultarQuantidadePagina(url)
print(qntd, 'páginas totais')

produtos = []
for i in range(1, int(qntd) +1):
    new_url = url + '?p=' + str(i)
    print(new_url)
    produtos = produtos + ConsultarProdutosPaginas(new_url)

GravarArquivosXLSX(produtos, area)