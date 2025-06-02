🚀 Projeto de E-commerce Básico com React e Vite

Este é um projeto frontend de um e-commerce básico, desenvolvido com React e Vite, focado em demonstrar o fluxo de autenticação, listagem de produtos, carrinho de compras e histórico de pedidos.

✨ Funcionalidades Incluídas

Esta aplicação oferece uma experiência de compra simplificada com as seguintes funcionalidades principais:

- Autenticação de Usuário: Sistema de login que gerencia a sessão do usuário através de cookies.
- Listagem de Produtos: Exibe uma vitrine de produtos obtidos de um backend, com cards informativos e responsivos.

Carrinho de Compras:

- Adição de produtos ao carrinho com persistência dos itens em cookies do navegador.
- Contador de itens no carrinho visível no cabeçalho.
- Página dedicada ao carrinho para visualizar, ajustar quantidades e remover produtos.
- Finalização de Compra: Envio do pedido para um endpoint de backend, utilizando os itens e quantidades do carrinho.

Histórico de Pedidos: 

- Página para consultar os pedidos anteriores do usuário, exibindo detalhes como ID, data, status e itens comprados.

🛠️ Tecnologias Utilizadas

- React: Biblioteca JavaScript para construção de interfaces de usuário.
- Vite: Ferramenta de build moderna e rápida para projetos front-end.
- TypeScript: Superset do JavaScript que adiciona tipagem estática.
- Tailwind CSS: Framework CSS utilitário para estilização rápida e responsiva.
- React Router DOM: Para gerenciamento de rotas e navegação na aplicação.
- js-cookie: Para manipulação simplificada de cookies.
- React Icons: Biblioteca de ícones populares para React.

⚙️ Como Rodar o Projeto (Front-end)

Para colocar o projeto em funcionamento na sua máquina, siga os passos abaixo:

Pré-requisitos:

- Certifique-se de ter o Node.js e o npm (ou Yarn) instalados na sua máquina.
- Node.js (versão 20 ou superior recomendada)
- npm (geralmente vem com o Node.js)

1. Clonar o Repositório

Primeiro, clone este repositório para o seu ambiente local:


```
git clone https://github.com/1cleiton/ilia`
cd ilia
````

2. Instalar as Dependências

Dentro da pasta do projeto, instale todas as dependências necessárias:

```
npm install
```

3. Configurar o Backend

Este projeto frontend depende de um backend para autenticação, listagem de produtos e gerenciamento de pedidos. Certifique-se de que seu backend esteja rodando e acessível na URL http://localhost:8001.

Os endpoints esperados são:

```
POST http://localhost:8001/api/v1/auth/login
GET http://localhost:8001/api/v1/products
POST http://localhost:8001/api/v1/orders
GET http://localhost:8001/api/v1/orders
```

4. Iniciar o Servidor de Desenvolvimento

Após instalar as dependências e garantir que o backend esteja ativo, você pode iniciar o servidor de desenvolvimento do Vite:

```
npm run dev
```

5. Acessar a Aplicação

A aplicação estará disponível em http://localhost:5173 (ou outra porta, se 5173 estiver em uso).

Você será redirecionado para a página de login e, após autenticar, poderá navegar entre os produtos, adicionar itens ao carrinho, finalizar compras e visualizar seus pedidos.

