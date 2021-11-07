
import pdfkit, webbrowser, os, time, clipboard
import PySimpleGUI as sg
from markdown import markdown
# 
#          ____  _____    _    ____  __  __ _____                 _ 
#         |  _ \| ____|  / \  |  _ \|  \/  | ____|  _ __ ___   __| |
#         | |_) |  _|   / _ \ | | | | |\/| |  _|   | '_ ` _ \ / _` |
#         |  _ <| |___ / ___ \| |_| | |  | | |___ _| | | | | | (_| |
#         |_| \_\_____/_/   \_\____/|_|  |_|_____(_)_| |_| |_|\__,_|
#                                                                   
#                   _ _ _             
#           ___  __| (_) |_ ___  _ __ 
#          / _ \/ _` | | __/ _ \| '__|
#         |  __/ (_| | | || (_) | |   
#          \___|\__,_|_|\__\___/|_|   
#                                     


arquivo_md = 'README.md'

class MarkdownEditor: 
    
    def salvar_md(self, conteudo, arquivo_md):
        self.conteudo = conteudo
        self.arquivo_md = arquivo_md
        # salva o arquivo markdown
        with open(arquivo_md, 'w', encoding='utf8') as f:
            f.write(conteudo)
    
    def salvar_html(self, conteudo, arquivo_html):
        self.conteudo = conteudo
        self.arquivo_html = arquivo_html       
        # salva o arquivo markdown em um arquivo temporario
        with open('.temp.md', 'w', encoding='utf8') as f:
            f.write(conteudo)
        # Converte o arquivo markdown em html
        with open('.temp.md', 'r', encoding='utf8') as f:
            html_text = markdown(f.read(), output_format='html4')
        # salva o arquivo html    
        with open(arquivo_html, 'w', encoding='utf8') as f:
            f.write(html_text)
    
    def visualizar(self, conteudo):
        self.conteudo = conteudo
        # salva o arquivo markdown em um arquivo temporario
        with open('.temp.md', 'w', encoding='utf8') as f:
            f.write(conteudo)
        # Converte o arquivo markdown em html
        with open('.temp.md', 'r', encoding='utf8') as f:
            html_text = markdown(f.read(), output_format='html4')
        # salva o arquivo html temporariamente    
        with open('.temp.html', 'w') as f:
            f.write(html_text)
        # abre o arquivo
        webbrowser.open('.temp.html')
        # apaga os arquivos após 15 segundos
        time.sleep(15)
        os.remove('.temp.md')
        os.remove('.temp.html')
    
    def salvar_pdf(self, conteudo, arquivo_pdf):        
        self.arquivo_pdf = arquivo_pdf        
        self.conteudo = conteudo
        # salva o arquivo markdown em um arquivo temporario
        with open('.temp.md', 'w', encoding='utf8') as f:
            f.write(conteudo)
        # Converte o arquivo markdown em html
        with open('.temp.md', 'r', encoding='utf8') as f:
            html_text = markdown(f.read(), output_format='html4')        
        # Converte em PDF
        options = {            
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'no-outline': None
        }
        
        pdfkit.from_string(html_text, arquivo_pdf, options=options)
        
# interface gráfica com pysimplegui

sg.theme('Reddit')

menu = [
    ['&Arquivo',
     ['&Novo Arquivo',
      '&Abrir Arquivo',
      '&Salvar',
      ['&Markdown *.md',
       '&HTML *.html',
       '&PDF *.pdf'],
      '&Sair']
     ],            
    ['&Editar',
     ['&Inserir imagem',
      '&Inserir Link',
      'Inserir Código',
      '&Inserir Lista Simples',
      '&Inserir Lista Numerada',
      '&Inserir Tabela',
      '&Copiar Texto',
      '&Colar Texto']
     ],
    ['&Visualizar',
     ['&Visualizar no Browser']
     ],
    ['&Sobre o Autor',
     ['&Linkedin',
      '&GitHub'
      ]      
     ]
    ]

layout = [
    [sg.Menu(menu, tearoff=False, pad=(200, 1))],
    [sg.Stretch(),
     sg.Multiline('', key='-output-', font=('any', 12), size=(400, 150), autoscroll=True),
     sg.Stretch()]
    ]

window = sg.Window(f'{arquivo_md} - Markdown editor', layout, size=(640, 400), resizable=True)
arquivo = MarkdownEditor()

while True:
    event, values = window.read()
    
    if event in ('Linkedin'):
        webbrowser.open_new_tab('https://www.linkedin.com/in/elizeu-barbosa-abreu-69965b218/') 
    
    elif event in ('Novo Arquivo'):
        window['-output-'].update('')
    
    elif event in ('Abrir Arquivo'):
        arquivo_md = sg.popup_get_file('Abrir Arquivo de Texto',
                                       title='Abrir Arquivo',
                                       file_types=(("Markdown","*.md"),("Texto", "*.txt"),),
                                       )
        
        with open(arquivo_md, 'r') as f:
            conteudo = f.read()
        window['-output-'].update(str(conteudo))
    
    elif event in ('Markdown *.md'):
        conteudo = values['-output-']
        arquivo_md = sg.popup_get_file('Salve seu arquivo',
                                       title='Salvar Arquivo',
                                       file_types=(("Markdown","*.md"),),
                                       save_as = True,)
        arquivo.salvar_md(conteudo, arquivo_md)
        
    
    elif event in ('Visualizar no Browser'):
        conteudo = values['-output-']
        arquivo.visualizar(conteudo)        
    
    elif event in ('HTML *.html'):
        conteudo = values['-output-']
        arquivo_html = sg.popup_get_file('Salve seu arquivo',
                                       title='Salvar Arquivo',
                                       file_types=(("Web HTML","*.html"),),
                                       save_as = True,)
        arquivo.salvar_html(conteudo, arquivo_html)       
    
    elif event in ('PDF *.pdf'):
        conteudo = values['-output-']
        sg.popup_timed('ATENÇÃO: Recurso em Teste', 'Resultado pode não ser satistatório!!!')  
        arquivo_pdf = sg.popup_get_file('Salve seu arquivo',
                                       title='Salvar Arquivo',
                                       file_types=(("PDF Reader","*.pdf"),),
                                       save_as = True,)
        arquivo.salvar_pdf(conteudo, arquivo_pdf)   
             
    elif event in ('Inserir imagem'):
        conteudo = values['-output-']
        imagem = sg.popup_get_file('Escolha a imagem para inserir aqui',
                                       title='Adicionar imagem',
                                       file_types=(("imagem JPG","*.jpeg, *.jpeg"),("Imagem PNG","*.png")),
                                       )
        texto = f'![Imagem]({imagem})'
        conteudo += f'\n{texto} \n'
        window['-output-'].update(conteudo)
        
    elif event in ('Inserir Link'):
        conteudo = values['-output-']
        link = sg.popup_get_text('Inserir link ou url', 'Inserir link ou url')
        texto = f'[Texto do Link]({link})'
        conteudo += f'\n{texto} \n'
        window['-output-'].update(conteudo)
        
    
    elif event in ('Inserir Lista Simples'):
        conteudo = values['-output-']
        conteudo += '''
* Item 1
* Item 2
* Item 3 editar

'''
        window['-output-'].update(conteudo)
        
    elif event in ('Inserir Lista Numerada'):
        conteudo = values['-output-']
        conteudo += '''
1. Item 1
2. Item 2
2. Item 3 editar

'''
        window['-output-'].update(conteudo)
            
    elif event in ('Copiar Texto'):
        conteudo = values['-output-']
        clipboard.copy(conteudo)
        sg.Popup('CTRL+C CTRL+V', 'Conteúdo Copiado para área de Transferência')
            
    elif event in ('Colar Texto'):
        conteudo = values['-output-']
        text = clipboard.paste()
        conteudo += f' {text} '
        window['-output-'].update(conteudo)
        
    elif event in ('Inserir Tabela'):
        conteudo = values['-output-']
        sg.popup_timed('ATENÇÃO: Recurso em Teste', 'Só funciona no README.md do GitHub!!!') 
        text = '\n\n'
        col = int(sg.popup_get_text('Quantidade de colunas da talela', 'Quantidade de colunas da talela'))
        row = int(sg.popup_get_text('Quantidade de linhas da talela', 'Quantidade de linhas da talela'))
        # Gera as colunas da tabela        
        text += ('| TEXTO ' * col) + '|\n' + ('| --- ' * col) + '|\n'
        # gera as linhas da tabela
        for r in range(row-1):
            text += ('| TEXTO ' * col) + '|\n'            
            
        text += '\n\n'        
           
        conteudo += f'{text}'
        window['-output-'].update(conteudo)  
    
    elif event in ('Inserir Código'):
        conteudo = values['-output-']
        sg.popup_timed('ATENÇÃO', 'Recurso só funciona no GitHub!!!')        
        text = '''
~~~python

Edite este texto
aqui com seu código

~~~
'''
        conteudo += f'\n {text} \n'
        window['-output-'].update(conteudo)
    
    elif event in ('GitHub'):
        webbrowser.open_new_tab('https://github.com/elizeubarbosaabreu') 
    
    elif event in (sg.WINDOW_CLOSED or 'Sair'):
        break

window.close()
