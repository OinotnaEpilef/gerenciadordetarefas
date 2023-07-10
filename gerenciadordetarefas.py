import hashlib
from pickle import *


class Tarefa:
    def __init__(self, titulo, descricao, prioridade, ID):
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.ID = ID


def menu():
    print(' 1. Cadastrar novo usuário')
    print(' 2. Logar no sistema')
    print(' 3. Sair do sistema')


def submenu():
    print(' 1. Cadastrar nova tarefa')
    print(' 2. Visualizar tarefa')
    print(' 3. Editar tarefa')
    print(' 4. Excluir tarefa')
    print(' 5. Sair')


def hash():  # Encriptar a senha e adicionar ao arquivo
    senha = input('Digite sua senha: ')
    senha_hash = hashlib.md5(senha.encode('utf-8')).hexdigest()
    arquivo.write(senha_hash + '\n')


def checar_usuario(n):  # Checa a existência do usuário, para ser usado no item "A" e no "B"
    for linha in arquivo:
        if linha.startswith(n):
            return True


def ordenar(lista):  # Faz a ordenação da lista por prioridade e por ID
    for i in range(len(lista) - 1, 0, -1):
        for j in range(i):
            if lista[j].prioridade > lista[j + 1].prioridade:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                if lista[j].ID > lista[j + 1].ID:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]


def buscar(lista, chave):  # Faz a busca do objeto cuja ID é dita pelo usuário
    for i in range(len(lista)):
        if lista[i].ID == chave:
            return i
    return -1


opcao = 0
tarefas = []

while True:  # Mostra a o menu, uma função escrita mais acima, e solicia a opção do usuário
    opcao2 = 0
    menu()
    opcao = int(input(' Digite sua opção: '))

    if opcao == 1:  # Cadastro do usuário, checando se ele já existe
        novo_usuario = input('Digite seu nome de usuário: ')
        with open('usuarios.txt', 'r+', encoding='utf8') as arquivo:
            while checar_usuario(novo_usuario):
                print('Nome de usuário já existente. Por favor, digite outro nome')
                novo_usuario = input('Digite seu nome de usuário: ')
                arquivo.seek(0)
            arquivo.write(novo_usuario + ' ')
            hash()

    elif opcao == 2:  # Login do usuário no sistema, checando usuário inexistente e senha incorreta
        usuario = input('Digite seu nome de usuário: ')
        with open('usuarios.txt', 'r+', encoding='utf8') as arquivo:
            while not checar_usuario(usuario):
                print('Nome de usuário inexistente. Por favor, digite outro nome')
                usuario = input('Digite seu nome de usuário: ')
    # Encontra o usuário, a barra de espaço entre este e o seu hash, e fatia a linha inteira para deixar apenas o hash,
    # para ser comparado com o da senha digitada para efetuar o login
        texto = usuario
        with open('usuarios.txt', encoding='utf8') as arquivo:
            for linha1 in arquivo:
                if linha1.startswith(texto):
                    hash_e_usuario = linha1
        chave = ' '
        coluna = 0
        for coluna in range(len(hash_e_usuario) - len(chave)):
            hash_do_usuario = hash_e_usuario[len(hash_e_usuario) - coluna + 1:-1]
        # Efetua a comparação, retornando uma mensagem de erro caso a senha esteja incorreta
        senha_inserida = input('Digite sua senha: ')
        hash_inserido = hashlib.md5(senha_inserida.encode('utf-8')).hexdigest()
        while hash_do_usuario != hash_inserido:
            print('Senha incorreta!')
            senha_inserida = input('Digite sua senha: ')
            hash_inserido = hashlib.md5(senha_inserida.encode('utf-8')).hexdigest()
        # Mostra o submenu e solicita a opção ao usuário
        while True:
            submenu()
            opcao2 = int(input('Digite sua opção: '))

            if opcao2 == 1:  # Cria a tarefa e a adiciona ao arquivo binário do usuário, adiciona a ID dentro de um
                # arquivo para ID como um contador do tamanho do arquivo
                ID = 0
                with open(usuario + '.txt', 'a') as arquivo:
                    arquivo.write('0')
                with open(usuario + '.txt', 'r') as arquivo:
                    ID = len(arquivo.read())
                tarefa = Tarefa(titulo=input('Digite o titulo da tarefa: '),
                                descricao=input('Digite a descrição da tarefa: '),
                                prioridade=int(input('Digite o número da prioridade: (1. Alta, 2. Média, 3. Baixa): ')),
                                ID=ID)
                # Abre um arquivo, resgatando a lista do arquivo(caso tenha, senão, executa um break), adiciona a nova
                # tarefa a lista, e adiciona novamente a lista ao arquivo
                arqbin = open(usuario + '.dat', 'ab')
                arqbin.close()
                arqbin = open(usuario + '.dat', 'rb')
                while True:
                    try:
                        tarefas = load(arqbin)
                    except EOFError:
                        break
                tarefas.append(tarefa)
                ordenar(tarefas)
                arqbin.close()
                arqbin = open(usuario + '.dat', 'wb')
                dump(tarefas, arqbin)
                arqbin.close()

            elif opcao2 == 2:  # Lê o ID a ser mostrado em cada tarefa, carrega a lista de tarefas do arquivo, e usa um
                # loop para ler cada tarefa mostrando seus atributos individualmente
                with open(usuario + '.txt', 'r') as arquivo:
                    ID = len(arquivo.read())
                arqbin2 = open(usuario + '.dat', 'rb')
                tarefas2 = load(arqbin2)
                for tarefa in tarefas2:
                    print('Título:', tarefa.titulo)
                    print('Descrição: ', tarefa.descricao)
                    if tarefa.prioridade == 1:
                        print('Prioridade: Alta')
                    elif tarefa.prioridade == 2:
                        print('Prioridade: Média')
                    else:
                        print('Prioridade: Baixa')
                    print('ID: ', tarefa.ID, '\n')
                arqbin2.close()

            elif opcao2 == 3:  # Retira a lista do arquivo, solicita ao usuário a ID da tarefa a ser alterada, busca a
                # tarefa na lista, retornando a mensagem de erro caso a ID não exista, e solicitando ao
                # usuário qual opção que ele deseja alterar. Em seguida altera a tarefa, retornando a
                # lista ao arquivo binário
                arqbin3 = open(usuario + '.dat', 'rb')
                tarefas3 = load(arqbin3)
                arqbin3.close()
                ID_tarefa_alterar = int(input('Digite a ID da tarefa a ser modificada: '))
                indice = buscar(tarefas3, ID_tarefa_alterar)
                while indice == -1:
                    ID_tarefa_alterar = int(input('ID não encontrada, por favor digite uma nova ID: '))
                    indice = buscar(tarefas3, ID_tarefa_alterar)
                print('1. Título\n2. Descrição\n3. Prioridade')
                atributo_a_ser_modificado = int(input('Digite o número correspondente a opção que deseja modificar: '))
                if atributo_a_ser_modificado == 1:
                    novo_titulo = input('Digite seu o novo título da sua tarefa: ')
                    tarefas3[indice].titulo = novo_titulo
                elif atributo_a_ser_modificado == 2:
                    nova_descricao = input('Digite a nova descrição da sua tarefa: ')
                    tarefas3[indice].descricao = nova_descricao
                else:
                    nova_prioridade = int(input('Digite a nova prioridade da sua tarefa '
                                                '(1. Alta, 2. Média, 3. Baixa): '))
                    tarefas3[indice].prioridade = nova_prioridade
                    ordenar(tarefas3)
                arqbin4 = open(usuario + '.dat', 'wb')
                dump(tarefas3, arqbin4)
                arqbin4.close()

            elif opcao2 == 4:  # Repede os procedimentos de busca e retorno ao arquivo da opção anterior, dessa vez
                # excluindo a tarefa selecionada pelo ID
                arqbin5 = open(usuario + '.dat', 'rb')
                tarefas4 = load(arqbin5)
                arqbin5.close()
                ID_tarefa_apagar = int(input('Digite o número da ID que deseja excluir: '))
                indice2 = buscar(tarefas4, ID_tarefa_apagar)
                while indice2 == -1:
                    ID_tarefa_apagar = int(input('ID não encontrada, por favor digite uma nova ID: '))
                    indice2 = buscar(tarefas4, ID_tarefa_apagar)
                tarefas4.pop(indice2)
                arqbin6 = open(usuario + '.dat', 'wb')
                dump(tarefas4, arqbin6)
                arqbin6.close()
            else:
                break
    else:
        break
