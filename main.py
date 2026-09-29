
import sqlite3

banco = sqlite3.connect("biblioteca.db")
cursor = banco.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS editoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor_id INTEGER,
    editora_id INTEGER,
    ano_publicacao INTEGER,
    edicao INTEGER,
    disponivel INTEGER,
    FOREIGN KEY (autor_id) REFERENCES autores(id),
    FOREIGN KEY (editora_id) REFERENCES editoras(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    data TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos_livros (
    emprestimo_id INTEGER,
    livro_id INTEGER,
    data_devolucao TEXT,
    PRIMARY KEY (emprestimo_id, livro_id),
    FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
)
""")

banco.commit()


while True:

    print("\n===== SISTEMA DE BIBLIOTECA =====")
    print("1 - Cadastrar usuário")
    print("2 - Listar usuários")
    print("3 - Cadastrar autor")
    print("4 - Listar autores")
    print("5 - Cadastrar editora")
    print("6 - Listar editoras")
    print("7 - Cadastrar livro")
    print("8 - Listar livros")
    print("9 - Cadastrar empréstimo")
    print("10 - Listar empréstimos")
    print("11 - Cadastrar livro em empréstimo")
    print("12 - Listar livros emprestados")
    print("13 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        nome = input("Nome do usuário: ")

        cursor.execute(
            "INSERT INTO usuarios (nome) VALUES (?)",
            (nome,)
        )

        banco.commit()

        print("Usuário cadastrado com sucesso!")

    elif opcao == "2":

        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        if len(usuarios) == 0:
            print("Nenhum usuário cadastrado.")
        else:
            print("\n=== Lista de Usuários ===")

            for usuario in usuarios:
                print(f"\nID: {usuario[0]}")
                print(f"Nome: {usuario[1]}")

    elif opcao == "3":

        nome = input("Nome do autor: ")

        cursor.execute(
            "INSERT INTO autores (nome) VALUES (?)",
            (nome,)
        )

        banco.commit()

        print("Autor cadastrado com sucesso!")

    elif opcao == "4":

        cursor.execute("SELECT * FROM autores")
        autores = cursor.fetchall()

        if len(autores) == 0:
            print("Nenhum autor cadastrado.")
        else:
            print("\n=== Lista de Autores ===")

            for autor in autores:
                print(f"\nID: {autor[0]}")
                print(f"Nome: {autor[1]}")

    elif opcao == "5":

        nome = input("Nome da editora: ")

        cursor.execute(
            "INSERT INTO editoras (nome) VALUES (?)",
            (nome,)
        )

        banco.commit()

        print("Editora cadastrada com sucesso!")

    elif opcao == "6":

        cursor.execute("SELECT * FROM editoras")
        editoras = cursor.fetchall()

        if len(editoras) == 0:
            print("Nenhuma editora cadastrada.")
        else:
            print("\n=== Lista de Editoras ===")

            for editora in editoras:
                print(f"\nID: {editora[0]}")
                print(f"Nome: {editora[1]}")

    elif opcao == "7":

        titulo = input("Título: ")
        autor_id = input("ID do autor: ")
        editora_id = input("ID da editora: ")
        ano = input("Ano de publicação: ")
        edicao = input("Edição: ")

        cursor.execute("""
            INSERT INTO livros
            (titulo, autor_id, editora_id, ano_publicacao, edicao, disponivel)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            titulo,
            autor_id,
            editora_id,
            ano,
            edicao,
            1
        ))

        banco.commit()

        print("Livro cadastrado com sucesso!")

    elif opcao == "8":

        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()

        if len(livros) == 0:
            print("Nenhum livro cadastrado.")
        else:
            print("\n=== Lista de Livros ===")

            for livro in livros:
                print(f"\nID: {livro[0]}")
                print(f"Título: {livro[1]}")
                print(f"ID do autor: {livro[2]}")
                print(f"ID da editora: {livro[3]}")
                print(f"Ano de publicação: {livro[4]}")
                print(f"Edição: {livro[5]}")

                if livro[6] == 1:
                    print("Disponível: Sim")
                else:
                    print("Disponível: Não")
   
    elif opcao == "9":

        usuario_id = input("ID do usuário: ")
        data = input("Data do empréstimo: ")

        cursor.execute("""
            INSERT INTO emprestimos (usuario_id, data)
            VALUES (?, ?)
        """, (
            usuario_id,
            data
        ))

        banco.commit()

        print("Empréstimo cadastrado com sucesso!")

    elif opcao == "10":

        cursor.execute("""
            SELECT
                emprestimos.id,
                usuarios.nome,
                emprestimos.data
            FROM emprestimos
            LEFT JOIN usuarios
            ON emprestimos.usuario_id = usuarios.id
        """)

        emprestimos = cursor.fetchall()

        if len(emprestimos) == 0:
            print("Nenhum empréstimo cadastrado.")
        else:
            print("\n=== Lista de Empréstimos ===")

            for emprestimo in emprestimos:
                print(f"\nID: {emprestimo[0]}")
                print(f"Usuário: {emprestimo[1]}")
                print(f"Data: {emprestimo[2]}")

    elif opcao == "11":

        emprestimo_id = input("ID do empréstimo: ")
        livro_id = input("ID do livro: ")
        data_devolucao = input("Data de devolução: ")

        cursor.execute("""
            INSERT INTO emprestimos_livros
            (emprestimo_id, livro_id, data_devolucao)
            VALUES (?, ?, ?)
        """, (
            emprestimo_id,
            livro_id,
            data_devolucao
        ))

        cursor.execute("""
            UPDATE livros
            SET disponivel = 0
            WHERE id = ?
        """, (livro_id,))

        banco.commit()

        print("Livro adicionado ao empréstimo com sucesso!")

    elif opcao == "12":

        cursor.execute("""
            SELECT
                emprestimos_livros.emprestimo_id,
                livros.titulo,
                usuarios.nome,
                emprestimos.data,
                emprestimos_livros.data_devolucao
            FROM emprestimos_livros

            LEFT JOIN livros
            ON emprestimos_livros.livro_id = livros.id

            LEFT JOIN emprestimos
            ON emprestimos_livros.emprestimo_id = emprestimos.id

            LEFT JOIN usuarios
            ON emprestimos.usuario_id = usuarios.id
        """)

        livros_emprestados = cursor.fetchall()

        if len(livros_emprestados) == 0:
            print("Nenhum livro emprestado.")
        else:
            print("\n=== Livros Emprestados ===")

            for item in livros_emprestados:
                print(f"\nID do empréstimo: {item[0]}")
                print(f"Livro: {item[1]}")
                print(f"Usuário: {item[2]}")
                print(f"Data do empréstimo: {item[3]}")
                print(f"Data de devolução: {item[4]}")

    elif opcao == "13":

        print("Encerrando o sistema...")
        banco.close()
        break

    else:

        print("Opção inválida! Tente novamente.")

