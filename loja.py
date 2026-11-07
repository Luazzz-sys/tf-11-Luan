# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                      # todos os pedidos da loja: lista solta, global


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
        self.status = "A"         # A = aberto, P = pago, C = cancelado

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status


def validar_dados_do_cliente(email, cpf, cep):
    if len(email) > 0:
        if "@" in email:
            if len(cpf) == 11:
                if len(cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, cliente):
    resultado = validar_dados_do_cliente(cliente.email, cliente.cpf, cliente.cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)
        return None
    else:
        pedido = Pedido(numero, cliente)
        pedidos.append(pedido)
        return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    total = 0
    for item in pedido.itens:
        total = total + item.quantidade * item.produto.preco
    return total


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total * 0.10
    elif tipo == "F":
        desconto = total * 0.20
    else:
        desconto = 0
    return desconto


def calcular_valor_a_pagar(pedido):
    return calcular_total(pedido) - calcular_desconto(pedido.cliente.tipo, calcular_total(pedido))


def pagar(pedido):
    if pedido.get_status() == "A":
        if len(pedido.itens) > 0:
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status() == "A":
        pedido.set_status("C")
        return True
    else:
        return False


def descrever_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def imprimir_relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", descrever_status(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "= R$ %.2f" % (item.quantidade * item.produto.preco))
        if len(pedido.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (calcular_total(pedido), calcular_desconto(pedido.cliente.tipo, calcular_total(pedido)), calcular_valor_a_pagar(pedido)))


def calcular_total_arrecadado():
    total = 0
    for pedido in pedidos:
        if pedido.get_status() == "P":
            total = total + calcular_valor_a_pagar(pedido)
    return total


def contar_pedidos_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.get_status() == "A":
            quantidade = quantidade + 1
    return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
caderno = Produto("Caderno", 15.5)
caneta = Produto("Caneta", 2.5)
livro = Produto("Livro", 89.5)
fone = Produto("Fone", 60.0)

cliente_ana = Cliente("Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
cliente_bruno = Cliente("Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")
cliente_carla = Cliente("Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")
cliente_diego = Cliente("Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
cliente_eva = Cliente("Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
cliente_fabio = Cliente("Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")
cliente_gil = Cliente("Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")

primeiro_pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(primeiro_pedido_da_ana, caderno, 2)
adicionar_item(primeiro_pedido_da_ana, caneta, 5)

novo_pedido(2, cliente_bruno)

segundo_pedido_da_ana = novo_pedido(3, cliente_ana)
adicionar_item(segundo_pedido_da_ana, livro, 1)

novo_pedido(4, cliente_carla)

pedido_do_diego = novo_pedido(5, cliente_diego)

pedido_da_eva = novo_pedido(6, cliente_eva)
adicionar_item(pedido_da_eva, fone, 1)

novo_pedido(7, cliente_fabio)

pedido_do_gil = novo_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(primeiro_pedido_da_ana))
print("pagar 3:", pagar(segundo_pedido_da_ana))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(primeiro_pedido_da_ana))

imprimir_relatorio()
print("arrecadado: R$ %.2f" % calcular_total_arrecadado())
print("abertos:", contar_pedidos_abertos())
