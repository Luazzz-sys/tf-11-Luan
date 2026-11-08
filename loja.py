# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                      # todos os pedidos da loja: lista solta, global


# Cpf: guarda um CPF e se recusa a existir se nao tiver 11 caracteres.
class Cpf:
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor


# Email: guarda um email e se recusa a existir se estiver vazio ou sem "@".
class Email:
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self._valor = valor


# Cep: guarda um CEP e se recusa a existir se nao tiver 8 caracteres.
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

    def calcular_percentual(self, percentual):
        return Dinheiro(self._centavos * percentual // 100)

    def __str__(self):
        return "R$ %d.%02d" % (self._centavos // 100, self._centavos % 100)


# Status: guarda o codigo da situacao do pedido (A, P ou C) e sabe se descrever.
class Status:
    def __init__(self, codigo):
        self._codigo = codigo

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"

    def descrever(self):
        if self._codigo == "A":
            return "aberto"
        elif self._codigo == "P":
            return "pago"
        else:
            return "cancelado"


# Cliente: junta todos os dados de uma pessoa que compra na loja. Existe UM por cliente.
class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo          # tipo do cliente: "N" normal, "V" vip, "F" funcionario


# Produto: o que a loja vende, com o nome e o preco guardados uma unica vez.
class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


# ItemDoPedido: uma linha do pedido, ou seja, um produto e quantas unidades dele.
class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


# Pedido: uma compra de um cliente, com seus itens e a situacao em que ela esta.
class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero            # numero do pedido
        self.cliente = cliente
        self.itens = []       # lista de ItemDoPedido
        self.status = Status("A")

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status


def novo_pedido(numero, cliente):
    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    total = Dinheiro(0)
    for item in pedido.itens:
        total = total.somar(item.produto.preco.multiplicar(item.quantidade))
    return total


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total.calcular_percentual(10)
    elif tipo == "F":
        desconto = total.calcular_percentual(20)
    else:
        desconto = Dinheiro(0)
    return desconto


def calcular_valor_a_pagar(pedido):
    total = calcular_total(pedido)
    return total.subtrair(calcular_desconto(pedido.cliente.tipo, total))


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if len(pedido.itens) > 0:
            pedido.set_status(Status("P"))
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status().esta_aberto():
        pedido.set_status(Status("C"))
        return True
    else:
        return False


def imprimir_relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", pedido.get_status().descrever())
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.produto.preco.multiplicar(item.quantidade))
        if len(pedido.itens) > 0:
            total = calcular_total(pedido)
            print("  total:", total, "| desconto:", calcular_desconto(pedido.cliente.tipo, total), "| a pagar:", calcular_valor_a_pagar(pedido))


def calcular_total_arrecadado():
    total = Dinheiro(0)
    for pedido in pedidos:
        if pedido.get_status().esta_pago():
            total = total.somar(calcular_valor_a_pagar(pedido))
    return total


def contar_pedidos_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.get_status().esta_aberto():
            quantidade = quantidade + 1
    return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
def criar_cliente_ou_recusar(numero_do_pedido, nome, cpf, email, rua, cidade, cep, tipo):
    try:
        email_validado = Email(email)
        cpf_validado = Cpf(cpf)
        cep_validado = Cep(cep)
        return Cliente(nome, cpf_validado, email_validado, rua, cidade, cep_validado, tipo)
    except ValueError as erro:
        print("pedido", numero_do_pedido, "recusado:", erro)
        return None


caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

cliente_ana = criar_cliente_ou_recusar(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
primeiro_pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(primeiro_pedido_da_ana, caderno, 2)
adicionar_item(primeiro_pedido_da_ana, caneta, 5)

# Pedidos 2, 4 e 7: o cliente e recusado, entao nao vira pedido.
criar_cliente_ou_recusar(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

segundo_pedido_da_ana = novo_pedido(3, cliente_ana)
adicionar_item(segundo_pedido_da_ana, livro, 1)

criar_cliente_ou_recusar(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

cliente_diego = criar_cliente_ou_recusar(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
pedido_do_diego = novo_pedido(5, cliente_diego)

cliente_eva = criar_cliente_ou_recusar(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
pedido_da_eva = novo_pedido(6, cliente_eva)
adicionar_item(pedido_da_eva, fone, 1)

criar_cliente_ou_recusar(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

cliente_gil = criar_cliente_ou_recusar(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
pedido_do_gil = novo_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(primeiro_pedido_da_ana))
print("pagar 3:", pagar(segundo_pedido_da_ana))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(primeiro_pedido_da_ana))

imprimir_relatorio()
print("arrecadado:", calcular_total_arrecadado())
print("abertos:", contar_pedidos_abertos())