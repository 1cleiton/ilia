🐍 Backend de E-commerce com Django, DRF e Celery

Este é o projeto de backend para um e-commerce básico, construído com Python, Django e Django REST Framework. Ele fornece as APIs necessárias para autenticação, gerenciamento de pedidos e integração com um serviço externo de produtos.

✨ Funcionalidades Principais

O backend é dividido em módulos (apps) que oferecem as seguintes funcionalidades:

Autenticação:

- Registro de Usuário: Permite que novos usuários se cadastrem na plataforma.
- Login: Autenticação de usuários com geração de tokens JWT (JSON Web Tokens) para acesso seguro às APIs protegidas.

Pedidos:

- Criação de Pedidos: API para registrar novos pedidos com base nos itens do carrinho.
- Listagem de Pedidos: API para listar os pedidos realizados por um usuário autenticado.

Integração com API Externa de Produtos: Os detalhes dos produtos (nome, preço, etc.) são obtidos de uma API externa, garantindo flexibilidade e desacoplamento.

🛠️ Tecnologias Utilizadas

- Python 3.11: Linguagem de programação principal.
- Django 5: Framework web de alto nível para desenvolvimento rápido e seguro.
- Django REST Framework 3: Toolkit poderoso para construir APIs RESTful.
- Celery: Sistema de fila de tarefas distribuída para processamento assíncrono (ex: processar pedidos complexos em segundo plano).
- Redis: Utilizado como broker para o Celery, gerenciando a fila de tarefas.
- Docker: Para conteinerização do ambiente de desenvolvimento e produção, garantindo portabilidade e fácil configuração.

🚀 Como Rodar o Projeto

Este projeto utiliza Docker para gerenciar seu ambiente e dependências, e um Makefile para simplificar os comandos de execução.

Pré-requisitos

Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

1. Clonar o Repositório

Primeiro, clone o repositório do backend para o seu ambiente local:

```
git clone https://github.com/1cleiton/ilia
cd ilia/backend
```

2. Configuração do Ambiente

Não é necessário criar um arquivo .env para rodar o projeto em desenvolvimento com make rundev, pois as configurações padrão já estão pré-definidas no Makefile.

3. Rodar o Projeto em Modo de Desenvolvimento

Use o comando make rundev para construir as imagens Docker, iniciar os containers (Django, Celery, Redis) e aplicar as migrações do banco de dados automaticamente. O backend estará acessível na porta 8001.

```
make rundev
```

- Contruirá (ou reconstruirá) as imagens Docker.
- Subirá os serviços definidos no docker-compose.yml.
- Aplicará as migrações do Django.
- Iniciará o servidor de desenvolvimento do Django na porta 8001.
- Iniciará o worker do Celery e o Redis broker.

4. Acessar a API Externa de Produtos

Este projeto integra-se com a seguinte API externa para obter a lista de produtos:

URL Base: https://683792e52c55e01d184a3a91.mockapi.io/api/v1/products

Certifique-se de que sua conexão com a internet permite o acesso a esta URL.

🐛 Debugging no VS Code

Para depurar o projeto Python dentro dos containers Docker usando o VS Code, siga estas instruções:

1. Instalar a Extensão Python

Certifique-se de ter a extensão oficial do Python instalada no seu VS Code.

2. Criar o Arquivo launch.json

No diretório raiz do seu projeto (onde está o manage.py), crie uma pasta .vscode e dentro dela um arquivo chamado launch.json com o seguinte conteúdo:

```
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [        
        {
            "name": "Python: Attach to Docker",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}", // Pasta no seu PC
                    "remoteRoot": "/app" // Pasta dentro do container
                }
            ]
        }
    ]
}
```

3. Iniciar o Debug

Com o projeto Docker rodando via make rundev, você pode ativar o debug:

- Abra a aba "Run and Debug" (ícone de um triângulo com um bug) no VS Code.
- Selecione a configuração "Python: Attach to Docker" no menu suspenso.
- Pressione F5 (ou clique no botão de "play" verde).
- Agora você pode definir breakpoints em seu código Python e o depurador do VS Code irá pausar a execução nesses pontos quando as requisições API forem feitas.

🧪 Testando as APIs com requests.http

Para auxiliar na utilização e testes das APIs do projeto, há um arquivo requests.http incluído na raiz do projeto. Ele contém exemplos de requisições HTTP para os principais endpoints.

Pré-requisito

Para usar o arquivo requests.http, você precisa ter a extensão REST Client instalada no VS Code.

Extensão [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

Após instalar a extensão, basta abrir o arquivo requests.http no VS Code e clicar no botão "Send Request" acima de cada requisição para executá-la.