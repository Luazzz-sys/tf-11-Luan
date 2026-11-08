TF-11: Loja refatorada
1. Normalização

Normalizar é guardar cada informação em um lugar só, em vez de copiar a mesma coisa várias vezes. Na loja feia, os dados da Ana (nome, cpf, email, rua, cidade, cep e tipo) estavam repetidos dentro de cada pedido dela. Se ela mudasse de endereço, eu teria que lembrar de trocar em todos os pedidos, e era fácil esquecer um. Agora a Ana é um único objeto Cliente, criado uma vez só no roteiro, e os pedidos 1 e 3 apontam para esse mesmo objeto.

2. Obsessão por tipos primitivos

O Cpf virou uma classe porque uma string comum não sabe se é válida: antes, a validação ficava numa função separada (valida) que alguém precisava lembrar de chamar. Agora a validação está dentro do construtor, então é impossível existir um Cpf inválido no programa. O ganho foi que o erro aparece na hora em que o dado é criado, e a função cheia de if aninhados deixou de existir. O Dinheiro guarda centavos inteiros e não float porque o float erra conta (0.1 + 0.2 dá 0.30000000000000004), e com inteiros as somas, subtrações e descontos ficam exatos.

3. Diga, não pergunte

Antes, quem queria pagar um pedido perguntava o status com get_status, decidia lá fora se podia e depois mandava mudar com set_status. Agora eu só chamo pedido.pagar() e o próprio Pedido decide e responde True ou False. A regra ficou melhor dentro do Pedido porque só ele conhece o seu status e os seus itens, então a regra fica junto dos dados que usa e não se espalha pelo programa.

4. Fail first

O hadouken da loja feia estava na função valida, com if dentro de if dentro de if e vários else. Agora cada validação é um if simples no construtor que levanta o erro e sai, e o resto do código segue reto. O mesmo vale para pagar e cancelar do Pedido, que devolvem False logo no começo. O else foi trocado por retorno antecipado porque assim o caminho feliz não fica escondido dentro de aninhamentos. E foi trocado por polimorfismo no desconto: cada tipo de cliente (TipoNormal, TipoVip e TipoFuncionario) sabe calcular o seu próprio desconto, então um tipo novo é só uma classe nova, sem mexer num if/elif gigante.

5. Modularização 

Cpf: representa um CPF e só existe se tiver 11 caracteres.
Email: representa um email e só existe se não for vazio e tiver "@".
Cep: representa um CEP e só existe se tiver 8 caracteres.
Dinheiro: guarda um valor em centavos inteiros e faz as contas com ele.
Status: guarda a situação do pedido (aberto, pago ou cancelado) e sabe se descrever.
Pessoa: reúne os dados de identificação de quem compra (nome, cpf e email).
Endereco: guarda onde o cliente mora (rua, cidade e cep).
TipoNormal: representa o cliente comum, que não ganha desconto.
TipoVip: representa o cliente vip, que ganha 10% de desconto.
TipoFuncionario: representa o funcionário da loja, que ganha 20% de desconto.
Cliente: junta a pessoa, o endereço e o tipo que define o desconto.
Produto: representa o que a loja vende, com nome e preço guardados uma única vez.
ItemDoPedido: representa uma linha do pedido, com um produto e a quantidade dele.
ItensDoPedido: guarda os itens de um pedido e sabe somar e imprimir eles.
Pedido: representa uma compra de um cliente, com seus itens e o seu status, e sabe pagar, cancelar e calcular valores.
Pedidos: guarda todos os pedidos da loja pelo número e responde sobre o conjunto deles.

6. Dívida técnica

Ficou uma coisa que não resolvi por completo: o Dinheiro lê o _centavos de outro Dinheiro (nos métodos somar e subtrair), o que é acessar o atributo privado de outra instância. Também tenho métodos descrever() em Pessoa e Endereco que devolvem um texto de dentro do objeto, o que se parece muito com um getter disfarçado. Deixei assim porque era o jeito mais simples de montar o relatório sem quebrar a Lei de Demeter. O custo é que, se a forma de guardar o dinheiro mudar, essas classes precisam mudar juntas. Eu pagaria essa dívida se o programa crescesse, por exemplo fazendo cada objeto imprimir a sua parte em vez de devolver texto.