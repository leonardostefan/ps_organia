# Processo seletivo Organia 

Projeto desenvolvido para ser entregue como parte do processo seletivo da empresa organia 


## Indice


## Intruções de execução 

- TODO : Realizar a documentação

## Descrição do projeto conforme foi passado 
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
  - XYZ

**Ferramentas:**
  - XYZ

**Intepretações dos requisitos**
  - XYZ
