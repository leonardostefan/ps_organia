# Processo seletivo Organia

Projeto desenvolvido para ser entregue como parte do processo seletivo da empresa organia


## Índice

<!-- TOC -->
- [Processo seletivo Organia](#processo-seletivo-organia)
  - [Índice](#índice)
  - [Sobre arquivos do projeto](#sobre-arquivos-do-projeto)
  - [Intruções de execução](#intruções-de-execução)
    - [Build local do projeto](#build-local-do-projeto)
    - [Testes de desenvolvimento](#testes-de-desenvolvimento)
  - [Descrição do projeto](#descrição-do-projeto)
    - [Teste de conhecimento Back-End Python](#teste-de-conhecimento-back-end-python)
      - [Requisitos Técnicos:](#requisitos-técnicos)
      - [Critérios de Avaliação:](#critérios-de-avaliação)
  - [Decisões de projeto](#decisões-de-projeto)
<!-- /TOC -->


## Sobre arquivos do projeto

**./ps_organia/**
├── **.devcontainer/** : *Arquivos para configuração do ambiente de desenvolvimento no VSCode*
├──
├── **app/**
│&emsp;├── **database/**: Arquivos da API referente a conexão com o BD
│&emsp;├── **domains/**: Arquivos referente aos "dominios" do projeto, é onde são processados os dados e validado regras de negócio*
│&emsp;├── **init-db/** : *Arquivos referentes a inicialização do banco de dados*
│&emsp;└── **tests/**: *Scripts de testes unitarios*
├── **requirements.txt** : *Dependencias Python do projeto*
├── **README.md**: *Este documento*
├── **anexo_avaliacoes.csv**: *Exemplos de dados para utilização no projeto (retirado da documentação original)*
└── **Teste_BackEnd_Python.pdf**: Arquivo original enviado pela empresa para o proceso seletivo

\* O modulo foi simplificado mas o ideal é ser mais separado em projetos grandes
## Intruções de execução
### Build local do projeto
 - Requisitos:
    - Docker, com compose instalado
    - 15Gb de armazenamento livre:
      Durante o build, o projeto pode ocupar até 15GB devido à instalação dos modelos de análise de sentimentos. Após o build, o uso estabiliza em cerca de 12GB.
;

  ```shell
  # Executar na raiz do projeto
  docker compose build; # O Build pode levar bastante tempo devido o modelo de Análise de Sentimentos
  docker compose up; # Inicialização do sistema
  ```

### Testes de desenvolvimento
Para testar o desenvolvimento recomendo a utilização do DevContainer dentro do VSCode (arquivo de configuração versionado em ".devcontainer")
Antes de abrir o Projeto no Devcontainer é necessário fazer os builds e subir apenas a base de dados:

```shell
docker compose build;
docker compose up organia_db;
```

Para realizar os testes unitários utilizasse o seguinte comando:
```
coverage run --source=app -m pytest &&
coverage report

```

Para inserir os dados de exemplo  do *anexo_avaliacoes.csv* na base de dados basta executar o seguinte comando:

```shell
python app/init-db/populate_db.py
```

## Descrição do projeto
Descrição do projeto conforme foi passado pelos avaliadores.
### Teste de conhecimento Back-End Python
Desenvolver uma API REST em Python para classificar automaticamente as avaliações de clientes sobre o serviço/produto/suporte (exemplo em anexo_avaliacoes.csv) de uma empresa em Positiva, Negativa ou Neutra. A API receberá textos de avaliações e retornará a classificação com base em uma análise de sentimento.
#### Requisitos Técnicos:
1. API:
    - Utilize FastAPI criar a API.
    - A API deve ter pelo menos três endpoints:
        - POST /reviews: classifica as avaliações dos clientes
        - GET /reviews: retorna uma lista de avaliações analisadas, juntamente com suas respectivas classificações. Permite filtrar os resultados por intervalo de datas, conforme a necessidade do usuário. Parâmetros de entrada: start_date: Data inicial no formato YYYY-MM-DD (opcional). end_date: Data final no formato YYYY-MM-DD (opcional).
        - GET /reviews/{id}: busca a análise de um comentário específico
        - GET /reviews/report: retorna um relatório das avaliações realizadas em um determinado período, incluindo a contagem das avaliações classificadas como positiva, negativa ou neutra. Parâmetros de entrada: start_date: Data inicial no formato YYYY-MM-DD. end_date: Data final no formato YYYY-MM-DD. GET reviews/report?start_date=2024-09-01&end_date=2024-09-17
2. Banco de Dados:
    - Utilize um banco de dados PostgreSQL para armazenar as conversas e suas análises.
3. Análise de Sentimento:
    - Para realizar a análise de sentimento dos comentários, você tem total liberdade para escolher a abordagem e as bibliotecas que preferir. Você pode optar por soluções simples que forneçam resultados rápidos ou explorar técnicas mais avançadas de processamento de linguagem natural, dependendo da sua experiência e preferência (exemplos: TextBlob, VADER, Flair, Hugging Face Transformers, LLMs).
4. Boas Práticas:
    - Utilize PEP8 para manter o código organizado e limpo (Use ferramentas de análise, como Flake8 ou Black, para validar automaticamente a conformidade com a PEP8).
    - Implemente uma estrutura de pastas modular e adequada para o projeto.
5. Testes Unitários:
    - Implemente testes unitários para os principais componentes da aplicação.
6. Documentação:
    - A API deve ser documentada com Swagger.
    - Faça uso de docstrings para documentação das funções e classes, no padrão Google.
    - Descreva o processo de instalação e execução do projeto no arquivo README.md.
7. Disponibilização
    - O candidato deve hospedar o código em um repositório público (por exemplo, GitHub).

#### Critérios de Avaliação:
- Organização do código e boas práticas.
- Implementação de testes unitários.
- Funcionamento correto da API (usabilidade, consistência e robustez).
- Documentação clara e detalhada.
- Boas práticas de commits Entrega:
- Ao finalizar o teste, envie o link do repositório para gente@weon.com.br com o assunto “Teste Prático Desenvolvedor Back-End Python - {seu nome}”

## Decisões de projeto
Aqui estão listado as decisões de projeto que foram realizadas ao longo do desenvolvimento.

**Padrões de projeto:**
  - Banco de dados:
    - Para simplificar o projeto, optei por não usar um gerenciador de migrations (como Alembic) para simplificação. O schema é criado automaticamente via script ao subir o container;
    - Para simplificar, ***foi mantido o nome do usuário na mesma tabela da avaliação *(review)**, porém em um sistema complexo o ideal seria normalizar estes dados deixando em tabelas distintas;
  - Análise de Sentimentos:
    - Como não havia uma amostragem significativa de dados para realizar algum treinamento, **foi utilizado o modelo ja pronto da biblioteca `pysentimiento`, mas o ideal é realizar um retreino** com uma amostra significativa de entradas;
    - Foi criado a rota `/reviews/eval_model/` a **fim de validar a analise de sentimentos** que esta sendo realizada . No momento ela faz apenas a contagem e listagem de divergencias, mas seria possivel adicionar outras métricas como acuracia, precisão, ou métricas personalizadas.
  - Code Patter:
    - Em um projeto maior **o ideal seria separar melhor as atribuições de cada modulo**, mas para um MVP mantive uma arquitetura mais enxuta, separando apenas na camada da API (main.py), Dominio de execução (/Domains/) e conexão a base de dados (/database/);
    - Como ainda não estou habituado as melhores praticas frameworks e afins para lidar com o FastAPI (sou acostumado com Django e Flask), preferi manter a simplicidade do projeto não criando muitas abstrações de modulos;
**Ferramentas:**
  - Para facilidade do testes em qualquer maquina, foi decidido utilizar docker compose para realizar o build do banco de dados e da aplicação;
**Intepretações dos requisitos**
  - A definição do método Http `POST /reviews/` no projeto esta muito rasa e ambigua: pela descrição poderia ser um "trigger" para processar todas avaliações pendentes ja registradas no BD, ou insersão via arquivo de avaliações, ou a inserção unica de uma avaliação. Por questão de logica de API foi decidido que seria a inserão de uma unica avaliação. Porém o ideal era resolver com o time/pessoa responsável pela definição do projeto;

**Implementações**
  - Como demandaria muito tempo implementar os testes de todas funcionalidades, foi implementado apenas na camada de dominio, onde possui mais processamento e se vê mais necessidade de implementação, porém em um projeto normal eu manteria um validador no repositorio (github/azure/gitlab...) que ao menos **garantisse coverage de 85**% de cada arquivo. Também implementaria **testes mutantes com 60%** de cobertura;
  - Foi realizado a implementação extra da rota `/reviews/eval_model/` como ja dito anteriormente;
