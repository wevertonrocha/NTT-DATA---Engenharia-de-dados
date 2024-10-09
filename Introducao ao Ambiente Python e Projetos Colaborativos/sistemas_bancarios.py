import textwrap


class Usuario:
    """Representa um usuário do banco."""

    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}"


class Conta:
    """Representa uma conta bancária."""

    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = ""
        self.limite = 500.0
        self.numero_saques = 0
        self.limite_saques = 3

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        """Realiza um saque da conta."""
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\nOperação falhou! O valor informado é inválido.")

    def exibir_extrato(self):
        """Exibe o extrato da conta."""
        print("\n================ EXTRATO ================")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

    def __str__(self):
        return (
            f"Agência:\t{self.agencia}\n"
            f"C/C:\t\t{self.numero_conta}\n"
            f"Titular:\t{self.usuario.nome}"
        )


class Banco:
    """Representa o banco, gerenciando usuários e contas."""

    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.agencia = "0001"

    def menu(self):
        """Exibe o menu de opções e retorna a opção escolhida."""
        menu_texto = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu_texto))

    def filtrar_usuario(self, cpf):
        """Filtra e retorna um usuário pelo CPF."""
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def criar_usuario(self):
        """Cria um novo usuário no banco."""
        cpf = input("Informe o CPF (somente número): ")
        if self.filtrar_usuario(cpf):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print("=== Usuário criado com sucesso! ===")

    def criar_conta(self):
        """Cria uma nova conta para um usuário existente."""
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            numero_conta = len(self.contas) + 1
            conta = Conta(self.agencia, numero_conta, usuario)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")

    def listar_contas(self):
        """Lista todas as contas existentes no banco."""
        print("\n================ LISTA DE CONTAS ================")
        if not self.contas:
            print("Não há contas cadastradas.")
            return

        for conta in self.contas:
            print("=" * 100)
            print(conta)
        print("=" * 100)

    def executar_operacao(self, opcao):
        """Executa a operação escolhida pelo usuário."""
        if opcao == "d":
            self.depositar()
        elif opcao == "s":
            self.sacar()
        elif opcao == "e":
            self.extrato()
        elif opcao == "nu":
            self.criar_usuario()
        elif opcao == "nc":
            self.criar_conta()
        elif opcao == "lc":
            self.listar_contas()
        elif opcao == "q":
            print("Obrigado por usar o sistema bancário. Até logo!")
            exit()
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

    def selecionar_conta(self):
        """Seleciona uma conta com base no CPF do usuário."""
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)
        if usuario:
            for conta in self.contas:
                if conta.usuario.cpf == cpf:
                    return conta
            print("\n@@@ Conta não encontrada para o usuário informado! @@@")
        else:
            print("\n@@@ Usuário não encontrado! @@@")
        return None

    def depositar(self):
        """Realiza um depósito em uma conta selecionada."""
        conta = self.selecionar_conta()
        if conta:
            try:
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            except ValueError:
                print("\n@@@ Operação falhou! Valor inválido. @@@")

    def sacar(self):
        """Realiza um saque de uma conta selecionada."""
        conta = self.selecionar_conta()
        if conta:
            try:
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            except ValueError:
                print("\n@@@ Operação falhou! Valor inválido. @@@")

    def extrato(self):
        """Exibe o extrato de uma conta selecionada."""
        conta = self.selecionar_conta()
        if conta:
            conta.exibir_extrato()

    def iniciar(self):
        """Inicia a aplicação do banco."""
        while True:
            opcao = self.menu()
            self.executar_operacao(opcao)


def main():
    banco = Banco()
    banco.iniciar()


if __name__ == "__main__":
    main()
