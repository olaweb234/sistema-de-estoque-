from PyQt6 import uic,QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem,QFileDialog
from PyQt6.QtWidgets import QMessageBox,QTreeWidgetItem
import datetime
import csv

usuarios=[]
usuario_logado = " "
chefe = False

def logar():
    global usuario_logado, chefe
    nome=principal.line_nome.text()
    senha= principal.line_senha.text()
    if nome ==  'admin' and senha == 'admin':
        chefe= True
        usuario_logado = nome
        principal.close()
        main.show()
        main.bt_salvar.clicked.connect(salvar)
        main.bt_excluir.clicked.connect(excluir)
        main.bt_abrir.clicked.connect(abrir_arquivo)
        main.bt_saida.clicked.connect(saida)
        main.bt_estorno.clicked.connect(estorno)
        main.bt_home.clicked.connect(bthome)
        return
    for usuario in usuarios:
        if usuario['nome']== nome and usuario['senha'] == senha:
            chefe= False
            main.bt_abrir.clicked.connect(abrir_arquivo)
            main.bt_saida.clicked.connect(saida)
            main.bt_estorno.clicked.connect(estorno)
            main.bt_home.clicked.connect(bthome)
            principal.close()
            main.show()
            return
    
    QMessageBox.warning(principal,'ERRO','Senha ou nome errado')


def salvar():
    nome=main.line_nome.text()
    senha=main.line_senha.text()
    confimar=main.line_confimacao.text()
    if senha != confimar:
        QMessageBox.warning(main,'ERRO','Senhas diferentes')
        
    else:
      usuarios.append({'nome': nome,'senha':senha,'criado_por':usuario_logado})
      QMessageBox.warning(main,'SUCESSO','salvo')
      mostrar_user()

def excluir ():
    item = main.pg_user.currentItem()
    if item:
        nome = item.text(0)
        data_criacao = item.text(1)
        criado_por = item.text(2)
        data_exclusao = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Remove o usuário da lista interna
        global usuarios
        usuarios = [user for user in usuarios if user['nome'] != nome]
        
        # Remove o item da interface
        main.pg_user.takeTopLevelItem(main.pg_user.indexOfTopLevelItem(item))
        
        # Exibe uma mensagem com detalhes da exclusão
        QMessageBox.information(main, 'Usuário Excluído', 
                                f"Nome: {nome}\nData de Criação: {data_criacao}\nCriado por: {criado_por}\nData de Exclusão: {data_exclusao}")
    else:
        QMessageBox.warning(main, 'ERRO', 'Selecione um usuário para excluir')
def mostrar_user():
    main.pg_user.clear()
    for usuario in usuarios:
        item = QTreeWidgetItem([usuario['nome'],'Data de criação', usuario['criado_por']])
        main.pg_user.addTopLevelItem(item) 
        usuario_item =QtWidgets.QTreeWidgetItem(main.pg_user)
        data_criacao = datetime.datetime.now().strftime('%Y-%m-%d')
        usuario_item.setText(1,data_criacao)
        
def abrir_arquivo():
    file_name, _= QFileDialog.getOpenFileName(main,'Abrir Aquivo','','Aquivos CSV(*.csv);;Todos os arquivos(*)')            
    if file_name:
        carregar(file_name)

def saida():
     item_selecionado = main.pg_estoque.currentItem()

     if item_selecionado:
        # Pega os dados do item selecionado
        user = item_selecionado.text(0)
        serie = item_selecionado.text(1)
        nf = item_selecionado.text(2)
        
        # Remove o item da pg_estoque
        index = main.pg_estoque.indexOfTopLevelItem(item_selecionado)
        main.pg_estoque.takeTopLevelItem(index)

        # Adiciona o item removido na pag_saida com a data atual
        data_saida = datetime.datetime.now().strftime('%Y-%m-%d')
        novo_item_saida = QTreeWidgetItem([nf, data_saida])
        main.pag_saida.addTopLevelItem(novo_item_saida)

        # Mostra uma mensagem de sucesso
        QMessageBox.information(main, 'Sucesso', 'Item movido para SAIDA')
     else:
        QMessageBox.warning(main, 'Erro', 'Nenhum item selecionado na lista de estoque')

def estorno():
    item= main.pag_saida.currentItem()
    if item:
         # Remove o item da pag_saida
        index = main.pag_saida.indexOfTopLevelItem(item)
        item_removido = main.pag_saida.takeTopLevelItem(index)
        
        # Adiciona o item removido de volta ao pg_estoque
        main.pg_estoque.addTopLevelItem(item_removido)
        
        QMessageBox.warning(main, 'SUCESSO', 'item devovido ao estoque')
    else:
        QMessageBox.warning(main,'ERRO','Nenhum item selecionado')
        


def carregar(file_name):
    main.pg_estoque.clear()
    with open(file_name , newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            item = QTreeWidgetItem(row)
            main.pg_estoque.addTopLevelItem(item)

def bthome():
    main.close()
    principal.show()
    principal.line_senha.clear()
    principal.line_nome.clear()


app=QtWidgets.QApplication([])
principal=uic.loadUi('tela_de_acessor.ui')
main=uic.loadUi("tela_principal.ui")
principal.Bt_logar.clicked.connect(logar)
principal.show()
app.exec()

