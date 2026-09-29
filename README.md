# Aplicação ao BD

Implementação do exemplo clássico da Biblioteca salvando os dados em um banco de dados sqlite.

As tabelas do projeto são:

usuarios(id, nome)
autores(id, nome)
editoras(id, nome)
livros(id, titulo, autor_id, editora_id, ano_publicacao, edicao, disponivel)
emprestimos(id, usuario_id, data)
emprestimos_livros(emprestimo_id, livro_id, data_devolucao)
