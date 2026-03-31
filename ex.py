import sqlite3 as bd

conexao = bd.connect('ex.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL UNIQUE DEFAULT 0)''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS pedidos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )''')
def add_users():
    while True:
        nome = input("Digite um nome(deixe vazio para encerrar o cadastro): ")
        if not nome:
            break
        else:
            idade = int(input("Digite a idade: "))
            email = input("Digite um email: ")
            try:
                cursor.execute('INSERT INTO usuarios (nome,idade,email) VALUES (?,?,?)',(nome,idade,email))
                print('Usuário cadastrado com sucesso!')
            except:
                print('Email já está no sistema!')
    conexao.commit()
def exibir_users():
    cursor.execute("SELECT * FROM usuarios ORDER BY nome ASC")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("\nNão há usuários no banco de dados!")
        return
    print(f"\n*Exibindo usuários em ordem alfabética*")
    for user in usuarios:
        id,nome,idade,email,telefone = user
        print(f'''Id: {id}
Nome: {nome}
Idade: {idade}
Email: {email}
Telefone: {telefone}
{'='*50}''')
    conexao.commit()
def exibir_users_menores():
    cursor.execute("SELECT * FROM usuarios WHERE idade < 18 ORDER BY nome ASC")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("\nNão há usuários no banco de dados!")
        return
    print(f"\n*Exibindo usuários menores de idade em ordem alfabética*")
    for user in usuarios:
        id,nome,idade,email,telefone= user
        print(f'''Id: {id}
Nome: {nome}
Idade: {idade}
Email: {email}
Telefone: {telefone}
{'='*50}''')
    conexao.commit()
def exibir_users_maiores():
    cursor.execute("SELECT * FROM usuarios WHERE idade > 17 ORDER BY nome ASC")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("\nNão há usuários no banco de dados!")
        return
    print(f"\n*Exibindo usuários maiores de idade em ordem alfabética*")
    for user in usuarios:
        id,nome,idade,email,telefone = user
        print(f'''Id: {id}
Nome: {nome}
Idade: {idade}
Email: {email}
Telefone: {telefone}
{'='*50}''')
    conexao.commit()
def editar_users():
    cursor.execute("SELECT * FROM usuarios ORDER BY nome ASC")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("\nNão há usuários no banco de dados!")
        return
    ID = int(input("Digite o id do usuário para editá-lo: "))
    cursor.execute('SELECT * FROM usuarios WHERE id = ?',[ID])
    for item in cursor.fetchall():
        id,nome,idade,email,telefone = item
        print(f'''
{'-'*20}Informações do Usuário{'-'*20}
Id: {id}
Nome = {nome}
Idade = {idade}
Email: {email}
Telefone: {telefone}\n''')
    edit_op = input('O que você deseja editar: ').lower()
    novo_valor = input("Qual o valor para inserir: ")
    try:
        cursor.execute(f'UPDATE usuarios SET {edit_op} = ? WHERE id = ?',(novo_valor,ID))
    except:
        print('Informação não encontrada!')
        return
    print(f"Editado com sucesso!\n")
    conexao.commit()
def remove_users():
    cursor.execute("SELECT * FROM usuarios ORDER BY nome ASC")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("\nNão há usuários no banco de dados!")
        return
    ID = int(input("Digite o id do usuário para excluí-lo: "))
    cursor.execute('SELECT * FROM usuarios WHERE id = ?',[ID])
    resultado = cursor.fetchall()
    if not resultado:
        print('Id não encontrado!')
        return
    for item in resultado:
        id,nome,idade,email,telefone = item
        print(f'''
{'-'*20}Informações do Usuário{'-'*20}
Id: {id}
Nome = {nome}
Idade = {idade}
Email: {email}
Telefone: {telefone}\n''')
    confirm = input('Digite Sim para deletar(ao digitar qualquer outra palavra a exclusão será cancelada): ').capitalize()
    if confirm == 'Sim':
        cursor.execute("DELETE FROM usuarios WHERE id = ?",[ID])
        print('Deletado com sucesso!\n')
    else:
        print('Operação cancelada com sucesso!\n')
        return
    conexao.commit()
while True:
    print(f'''
{'-'*50}SISTEMA DE USUÁRIOS{'-'*50}

🧩 Menu:
🟢 1 — Adicionar usuários
🔵 2 — Exibir usuários (A-Z)
    2.1 — Mostrar menores de idade
    2.2 — Mostrar maiores de idade
🟡 3 — Editar usuário
🔴 4 — Remover usuário
❌ 5 — Sair\n''')
    try:
        opcao = float(input("Digite uma das opções anteriores: "))
        match opcao:
            case 1:
                add_users()
            case 2:
                exibir_users()
            case 2.1:
                exibir_users_menores()
            case 2.2:
                exibir_users_maiores()
            case 3:
                editar_users()
            case 4:
                remove_users()
            case 5:
                print('Saindo do programa...\n')
                break
            case _:
                print("Opção não encotrada!")
    except ValueError:
        print("Digite apenas números!")