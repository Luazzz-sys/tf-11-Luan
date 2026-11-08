# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja.py


# Cpf: guarda um CPF e se recusa a existir se nao tiver 11 caracteres.
class Cpf:
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor


# Email: representa um email e so existe se nao for vazio e tiver "@".
class Email:
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self._valor = valor


# Cep: representa um CEP e so existe se tiver 8 caracteres.
class Cep:
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self._valor = valor


# Dinheiro: guarda um valor em CENTAVOS (int) e sabe fazer as contas com ele.
class Dinheiro:
    def __init__(self, centavos):
        self._centavos = centavos

    def somar(self, outro):
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro):
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self._centavos * quantidade)

    def percentual(self, porcento):
        return Dinheiro(self._centavos * porcento // 100)

    def __str__(self):
        return "R$ %d.%02d" % (self._centavos // 100, self._centavos % 100)


# Status: guarda o codigo da situacao do pedido (A, P ou C) e sabe se descrever.
class Status:
    _DESCRICOES = {"A": "aberto", "P": "pago", "C": "cancelado"}

    def __init__(self, codigo):
        self._codigo = codigo

    def descricao(self):
        return self._DESCRICOES[self._codigo]

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"


# Pessoa: reune os dados de identificacao de quem compra na loja.
class Pessoa:
    def __init__(self, nome, cpf, email):
        self._nome = nome
        self._cpf = cpf
        self._email = email

    def descrever(self):
        return self._nome


# Endereco: guarda onde o cliente mora.
class Endereco:
    def __init__(self, rua, cidade, cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = cep

    def descrever(self):
        return self._cidade


# Cliente: junta a pessoa, o endereco e o tipo que define o desconto dela.
class Cliente:
    def __init__(self, pessoa, endereco, tipo):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo      # "N" normal, "V" vip, "F" funcionario

    def descrever(self):
        return self._pessoa.descrever() + " - " + self._endereco.descrever()

    def calcular_desconto(self, total):
        if self._tipo == "V":
            desconto = total.percentual(10)
        elif self._tipo == "F":
            desconto = total.percentual(20)
        else:
            desconto = Dinheiro(0)
        return desconto


# Produto: o que a loja vende, com o nome e o preco guardados uma unica vez.
class Produto:
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    def calcular_subtotal(self, quantidade):
        return self._preco.multiplicar(quantidade)

    def imprimir_linha(self, quantidade):
        print("  ", quantidade, "x", self._nome, "=", self.calcular_subtotal(quantidade))


# ItemDoPedido: uma linha do pedido, ou seja, um produto e quantas unidades dele.
class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade

    def calcular_subtotal(self):
        return self._produto.calcular_subtotal(self._quantidade)

    def imprimir(self):
        self._produto.imprimir_linha(self._quantidade)


# ItensDoPedido: guarda a lista de itens de um pedido e sabe somar e imprimir eles.
class ItensDoPedido:
    def __init__(self):
        self._itens = []

    def adicionar(self, item):
        self._itens.append(item)

    def esta_vazia(self):
        return len(self._itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self._itens:
            total = total.somar(item.calcular_subtotal())
        return total

    def imprimir(self):
        for item in self._itens:
            item.imprimir()


# Pedido: uma compra de um cliente, com seus itens e a situacao em que ela esta.
class Pedido:
    def __init__(self, cliente):
        self._cliente = cliente
        self._itens = ItensDoPedido()
        self._status = Status("A")

    def adicionar_item(self, produto, quantidade):
        self._itens.adicionar(ItemDoPedido(produto, quantidade))

    def pagar(self):
        if self._status.esta_aberto():
            if not self._itens.esta_vazia():
                self._status = Status("P")
                return True
            else:
                return False
        else:
            return False

    def cancelar(self):
        if self._status.esta_aberto():
            self._status = Status("C")
            return True
        else:
            return False

    def esta_aberto(self):
        return self._status.esta_aberto()

    def calcular_total(self):
        return self._itens.calcular_total()

    def calcular_desconto(self):
        return self._cliente.calcular_desconto(self.calcular_total())

    def calcular_valor_a_pagar(self):
        return self.calcular_total().subtrair(self.calcular_desconto())

    def calcular_valor_arrecadado(self):
        if self._status.esta_pago():
            return self.calcular_valor_a_pagar()
        else:
            return Dinheiro(0)

    def imprimir(self, numero):
        print("Pedido", numero, "-", self._cliente.descrever())
        print("  status:", self._status.descricao())
        self._itens.imprimir()
        if not self._itens.esta_vazia():
            print("  total:", self.calcular_total(), "| desconto:", self.calcular_desconto(),
                  "| a pagar:", self.calcular_valor_a_pagar())


# Pedidos: guarda todos os pedidos da loja pelo numero e responde sobre o conjunto deles.
class Pedidos:
    def __init__(self):
        self._pedidos = {}

    def criar_pedido(self, numero, cliente):
        pedido = Pedido(cliente)
        self._pedidos[numero] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero, pedido in self._pedidos.items():
            pedido.imprimir(numero)

    def calcular_total_arrecadado(self):
        total = Dinheiro(0)
        for pedido in self._pedidos.values():
            total = total.somar(pedido.calcular_valor_arrecadado())
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        for pedido in self._pedidos.values():
            if pedido.esta_aberto():
                quantidade = quantidade + 1
        return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
def criar_cliente_ou_recusar(numero_do_pedido, nome, cpf, email, rua, cidade, cep, tipo):
    try:
        pessoa = Pessoa(nome, Cpf(cpf), Email(email))
        endereco = Endereco(rua, cidade, Cep(cep))
        return Cliente(pessoa, endereco, tipo)
    except ValueError as erro:
        print("pedido", numero_do_pedido, "recusado:", erro)
        return None


pedidos = Pedidos()

caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

cliente_ana = criar_cliente_ou_recusar(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
primeiro_pedido_da_ana = pedidos.criar_pedido(1, cliente_ana)
primeiro_pedido_da_ana.adicionar_item(caderno, 2)
primeiro_pedido_da_ana.adicionar_item(caneta, 5)

# Pedidos 2, 4 e 7: o cliente e recusado, entao nao vira pedido.
criar_cliente_ou_recusar(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

segundo_pedido_da_ana = pedidos.criar_pedido(3, cliente_ana)
segundo_pedido_da_ana.adicionar_item(livro, 1)

criar_cliente_ou_recusar(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

cliente_diego = criar_cliente_ou_recusar(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
pedido_do_diego = pedidos.criar_pedido(5, cliente_diego)

cliente_eva = criar_cliente_ou_recusar(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
pedido_da_eva = pedidos.criar_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(fone, 1)

criar_cliente_ou_recusar(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

cliente_gil = criar_cliente_ou_recusar(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
pedido_do_gil = pedidos.criar_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(fone, 2)

print("pagar 1:", primeiro_pedido_da_ana.pagar())
print("pagar 3:", segundo_pedido_da_ana.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", primeiro_pedido_da_ana.cancelar())

pedidos.imprimir_relatorio()
print("arrecadado:", pedidos.calcular_total_arrecadado())
print("abertos:", pedidos.contar_pedidos_abertos())