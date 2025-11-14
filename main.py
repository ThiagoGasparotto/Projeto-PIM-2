import json, os

arquivo = "turmas_json"

#Salvar dados.
def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

def carregar_dados(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as file:
            dados = json.load(file)
            return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, IOError):
        return []


#garante que cada aluno tenha 'nome','matricula','notas'
def normalizar_turmas(turmas):
    for turma in turmas:
        turma.setdefault("nome", "Turma sem nome")
        turma.setdefault("curso", "")
        turma.setdefault("alunos", [])
        turma.setdefault("aulas", [])
        for aluno in turma["alunos"]:
            aluno.setdefault("nome", "Aluno sem nome")
            aluno.setdefault("matricula", "")
            aluno.setdefault("notas", [])
    return turmas

#cadastra a turma.
def cadastrar_turma():
    turmas = carregar_dados(arquivo)
    turmas = normalizar_turmas(turmas)

    nome = input("Nome da turma: ").strip()
    curso = input("Curso: ").strip()
    turma = {"nome": nome or "Turma sem nome", "curso": curso, "alunos": [], "aulas": []}
    turmas.append(turma)
    salvar_dados(arquivo, turmas)
    print("Turma cadastrada com sucesso!\n")

#mostrar turmas (nome,curso)
def listar_turmas(turmas):
    for i, turma in enumerate(turmas):
        print(f"{i} - {turma.get('nome','(sem nome)')} ({turma.get('curso','')})")

#cadastrar turma
def cadastrar_aluno():
    turmas = carregar_dados(arquivo)
    turmas = normalizar_turmas(turmas)

    if not turmas:
        return print ("Nenhuma turma cadastrada!")

    nome = input("Nome do aluno: ").strip()
    matricula = input("Matrícula: ").strip()
    aluno = {"nome": nome or "Aluno sem nome", "matricula": matricula, "notas": []}

    print("\nEscolha a turma para adicionar o aluno:")
    listar_turmas(turmas)
    NMR = int(input("Número da turma: "))
    if 0 <= NMR < len (turmas):
        turmas[NMR]["alunos"].append(aluno)
        salvar_dados(arquivo, turmas)
        print("Aluno cadastrado com sucesso!\n")
    else:
        print("Essa turma nao existe!")

#cadastrar notas
def registrar_nota():
    turmas = carregar_dados(arquivo)
    turmas = normalizar_turmas(turmas)

    if not turmas:
        return print("Nenhuma turma cadastrada!")

    print("\nEscolha a turma:")
    listar_turmas(turmas)
    t_nmr = int(input("Número da turma: "))
    if t_nmr is None:
        return

    if not turmas[t_nmr]["alunos"]:
        print("Nenhum aluno nessa turma!")
        return
    
    print("\nEscolha o aluno:")
    for i, aluno in enumerate(turmas[t_nmr]["alunos"]):
        print(f"{i} - {aluno.get('nome','(sem nome)')} (Matrícula: {aluno.get('matricula','')})")
    a_nmr = int(input("Número do aluno: "))
    if a_nmr is None:
        return

    nota = float(input("Digite a nota do aluno (0 a 10): "))
    if nota < 0 or nota > 10:
        print("Nota precisa ser de 0 a 10.")
        return

    turmas[t_nmr]["alunos"][a_nmr].setdefault("notas", []).append(nota)
    salvar_dados(arquivo, turmas)
    print(f"Nota {nota} registrada para {turmas[t_nmr]['alunos'][a_nmr]['nome']}!\n")

#cadastrar aulas
def registrar_aula():
    turmas = carregar_dados(arquivo)
    turmas = normalizar_turmas(turmas)

    if not turmas:
        return print("Nenhuma turma cadastrada!")

    print("\nEscolha a turma para registrar a aula:")
    listar_turmas(turmas)
    t_nmr = int(input("Número da turma: "))
    if t_nmr is None:
        return

    data = input("Data da aula (ex: 03/11/2025): ").strip()
    conteudo = input("Conteúdo da aula: ").strip()

    aula = {"data": data, "conteudo": conteudo}
    turmas[t_nmr].setdefault("aulas", []).append(aula)
    salvar_dados(arquivo, turmas)
    print("Aula registrada com sucesso!\n")

#mostrar aulas
def consultar_aulas():
    turmas = carregar_dados(arquivo)
    turmas = normalizar_turmas(turmas)

    if not turmas:
        print("Nenhuma turma cadastrada!")
        return

    print("\nEscolha a turma para ver as aulas:")
    listar_turmas(turmas)
    t_nmr = int(input("Número da turma: "))
    if t_nmr is None:
        return

    aulas = turmas[t_nmr].get("aulas", [])
    if not aulas:
        print("Nenhuma aula registrada nessa turma.")
        return

    print(f"\nAulas da turma {turmas[t_nmr]['nome']}:")
    for i, aula in enumerate(aulas):
        print(f"{i} - {aula.get('data','')} | {aula.get('conteudo','')} | {aula.get('observacoes','')}")

#tela do programa
def menu():
    while True:
        print("\n===== SISTEMA ESCOLAR =====")
        print("1 - Cadastrar Turma")
        print("2 - Cadastrar Aluno")
        print("3 - Registrar Nota")
        print("4 - Registrar Aula")
        print("5 - Consultar Aulas")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_turma()
        elif opcao == "2":
            cadastrar_aluno()
        elif opcao == "3":
            registrar_nota()
        elif opcao == "4":
            registrar_aula()
        elif opcao == "5":
            consultar_aulas()
        elif opcao == "6":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

#inicar programa
if __name__ == "__main__":
    menu()