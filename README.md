
# Plataforma EAD Simples com Autenticação JWT e Dashboard em Streamlit

Projeto para prova de conceito (PoC) demonstrando uma aplicação web (simulando uma plataforma EAD) com funcionalidades básicas, utilizando autenticação JWT para incorporar um dashboard interativo em Streamlit com separação dos dados conforme os dados do usuário.

## Sumário

- [Introdução](#introdução)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
  - [Camada de Dados (Modelos)](#camada-de-dados-modelos)
    - [Esquema do Banco de Dados](#esquema-do-banco-de-dados)
    - [Descrição das Tabelas](#descrição-das-tabelas)
    - [Relacionamentos](#relacionamentos)
  - [Camada de Serviços](#camada-de-serviços)
    - [Aplicação Flask](#aplicação-flask)
    - [Dashboard Streamlit](#dashboard-streamlit)
- [Instruções de Configuração](#instruções-de-configuração)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
  - [Executando a Aplicação](#executando-a-aplicação)
- [Uso da Aplicação](#uso-da-aplicação)
  - [Registrando Usuários](#registrando-usuários)
  - [Fazendo Login](#fazendo-login)
  - [Acessando o Dashboard](#acessando-o-dashboard)
- [Considerações Adicionais](#considerações-adicionais)
  - [Segurança](#segurança)
  - [Possíveis Melhorias Futuras](#possíveis-melhorias-futuras)
- [Agradecimentos](#agradecimentos)
- [Contato](#contato)

## Introdução

Este projeto visa demonstrar a associação do controle de autenticação:

- **Modelagem de Dados**: Criação de um esquema de banco de dados relacional usando PostgreSQL, com tabelas inter-relacionadas para representar usuários, turmas, alunos, professores e aulas.
- **Autenticação JWT**: Implementação de login seguro com geração de tokens JWT que contêm informações encriptadas do usuário.
- **Integração de Aplicações**: Uso de um dashboard desenvolvido em Streamlit, integrado à aplicação web principal e controlado por tokens JWT.

## Arquitetura do Projeto

A aplicação é composta por duas principais camadas:

1. **Camada de Dados (Modelos)**: Responsável pelo armazenamento e gerenciamento dos dados usando PostgreSQL.
2. **Camada de Serviços**: Consiste na aplicação web desenvolvida com Flask.
3. **Dashboard Streamlit**: Dashboard interativo criado com Streamlit.

### Camada de Dados (Modelos)

#### Esquema do Banco de Dados

![er_ead_poc](https://github.com/user-attachments/assets/abd7889c-21f6-4c02-b33a-75a2eb37f9c4)

#### Descrição das Tabelas

1. **usuarios**

   | Campo    | Tipo         | Descrição                                 |
   | -------- | ------------ | ----------------------------------------- |
   | id       | SERIAL PK    | Identificador único do usuário            |
   | usuario  | VARCHAR(50)  | Nome de usuário (login)                   |
   | senha    | VARCHAR(255) | Senha hashificada                         |
   | role     | VARCHAR(50)  | Função do usuário (aluno, professor, etc) |

2. **alunos**

   | Campo      | Tipo         | Descrição                                  |
   | ---------- | ------------ | ------------------------------------------ |
   | id         | SERIAL PK    | Identificador único do aluno               |
   | nome       | VARCHAR(100) | Nome completo do aluno                     |
   | email      | VARCHAR(100) | Email do aluno                             |
   | usuario_id | INTEGER FK   | Referência ao usuário na tabela `usuarios` |

3. **professores**

   | Campo      | Tipo         | Descrição                                     |
   | ---------- | ------------ | --------------------------------------------- |
   | id         | SERIAL PK    | Identificador único do professor              |
   | nome       | VARCHAR(100) | Nome completo do professor                    |
   | email      | VARCHAR(100) | Email do professor                            |
   | usuario_id | INTEGER FK   | Referência ao usuário na tabela `usuarios`    |

4. **turmas**

   | Campo     | Tipo         | Descrição                    |
   | --------- | ------------ | ---------------------------- |
   | id        | SERIAL PK    | Identificador único da turma |
   | nome      | VARCHAR(100) | Nome da turma                |
   | descricao | TEXT         | Descrição da turma           |

5. **aulas**

   | Campo     | Tipo         | Descrição                                    |
   | --------- | ------------ | -------------------------------------------- |
   | id        | SERIAL PK    | Identificador único da aula                  |
   | titulo    | VARCHAR(100) | Título da aula                               |
   | conteudo  | TEXT         | Conteúdo da aula                             |
   | data_hora | TIMESTAMP    | Data e hora da aula                          |
   | turma_id  | INTEGER FK   | Referência à turma na tabela `turmas`        |

6. **alunos_turmas**

   | Campo    | Tipo       | Descrição                               |
   | -------- | ---------- | --------------------------------------- |
   | aluno_id | INTEGER FK | Referência ao aluno na tabela `alunos`  |
   | turma_id | INTEGER FK | Referência à turma na tabela `turmas`   |

   **Chave Primária Composta**: `(aluno_id, turma_id)`

7. **professores_turmas**

   | Campo        | Tipo       | Descrição                                     |
   | ------------ | ---------- | --------------------------------------------- |
   | professor_id | INTEGER FK | Referência ao professor na tabela `professores` |
   | turma_id     | INTEGER FK | Referência à turma na tabela `turmas`         |

   **Chave Primária Composta**: `(professor_id, turma_id)`

#### Relacionamentos

- **usuarios** ↔ **alunos**: Um para um (nem todos os usuários são alunos).
- **usuarios** ↔ **professores**: Um para um (nem todos os usuários são professores).
- **alunos** ↔ **turmas**: Muitos para muitos (tabela intermediária `alunos_turmas`).
- **professores** ↔ **turmas**: Muitos para muitos (tabela intermediária `professores_turmas`).
- **turmas** ↔ **aulas**: Um para muitos (uma turma possui várias aulas).

### Camada de Serviços

#### Aplicação Flask

A aplicação web desenvolvida com Flask é responsável por:

- **Autenticação de Usuários**: Registro e login com armazenamento seguro de senhas (usando `bcrypt` para hashing).
- **Geração de Tokens JWT**: Após o login, um token JWT é gerado contendo informações encriptadas do usuário.
- **Rotas Principais**:
  - `/register`: Rota para registro de novos usuários.
  - `/login`: Rota para autenticação de usuários existentes.
  - `/dashboard`: Rota que exibe a página com o dashboard embutido.

**Estrutura de Pastas**:

```plaintext
project/
├── app.py            # Aplicação Flask principal
├── templates/
│   ├── register.html # Template para registro
│   ├── login.html    # Template para login
│   └── dashboard.html# Template que embute o dashboard Streamlit
└── static/
    └── styles.css    # Arquivos de estilo (opcional)
```

### Dashboard Streamlit

O dashboard desenvolvido em Streamlit é responsável por:

- **Exibir Informações Personalizadas**: Mostra dados relevantes ao usuário logado, baseando-se em sua role (aluno, professor, etc).
- **Controle de Acesso**: Utiliza o token JWT passado como parâmetro para garantir que apenas usuários autenticados acessem o conteúdo.

**Principais Funcionalidades**:

- **Para Alunos**:
  - Visualização de turmas e aulas associadas.
  - Acesso ao conteúdo das aulas.
- **Para Professores**:
  - Visualização das turmas que leciona.
  - Gerenciamento de aulas (criação, edição, etc).
- **Para Outros Usuários**:
  - Conteúdo personalizado conforme a role (coordenador, diretor, etc).

## Instruções de Configuração

### Pré-requisitos

- Python 3.7+
- PostgreSQL
- Bibliotecas Python:
  - Flask
  - psycopg2-binary
  - PyJWT
  - bcrypt
  - Streamlit
  - Faker (para geração de dados fictícios)

### Instalação

Clone o Repositório:

```bash
git clone https://github.com/seu_usuario/ead_poc.git
cd ead_poc
```

Crie um Ambiente Virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scriptsctivate     # Windows
```

Instale as Dependências:

```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados

Crie o Banco de Dados:

```sql
CREATE DATABASE ead_db;
```

Crie as Tabelas executando o script `schema.sql` fornecido:

```bash
psql -U seu_usuario -d ead_db -f schema.sql
```

Popule o Banco de Dados com dados fictícios usando o script `populate_db.py`:

```bash
python populate_db.py
```

**Nota**: Certifique-se de configurar corretamente as credenciais de acesso ao banco de dados nos scripts.

### Executando a Aplicação

Inicie o Servidor Flask:

```bash
python app.py
```

O aplicativo estará disponível em [http://localhost:5000](http://localhost:5000).

Inicie o Dashboard Streamlit:

```bash
streamlit run dashboard.py
```

O dashboard estará disponível em [http://localhost:8501](http://localhost:8501).

## Uso da Aplicação

### Registrando Usuários

Acesse [http://localhost:5000/register](http://localhost:5000/register).

Preencha o formulário com as informações solicitadas:

- Nome
- Email
- Usuário
- Senha
- Role (aluno, professor, etc)

Submeta o formulário para criar a conta.

### Fazendo Login

Acesse [http://localhost:5000/login](http://localhost:5000/login).

Insira seu nome de usuário e senha.

Após o login bem-sucedido, você será redirecionado para o dashboard.

### Acessando o Dashboard

O dashboard está embutido na rota `/dashboard` da aplicação Flask.

O token JWT é passado automaticamente para o Streamlit via parâmetros de consulta.

O conteúdo exibido será personalizado com base na sua role.

## Considerações Adicionais

### Segurança

- **Armazenamento de Senhas**: As senhas são armazenadas usando hashing com bcrypt para garantir segurança.
- **Tokens JWT**: Contêm informações essenciais e expiram após um período definido para aumentar a segurança.
- **Validações**: Inputs do usuário são validados para prevenir ataques como SQL Injection.

### Possíveis Melhorias Futuras

- **Implementação de HTTPS**: Para criptografar o tráfego entre o cliente e o servidor.
- **Melhorias na UI/UX**: Desenvolver interfaces mais amigáveis e responsivas.
- **Funcionalidades Adicionais**: Como gerenciamento de materiais, fóruns de discussão, notificações, etc.
- **Testes Automatizados**: Implementar testes unitários e de integração para garantir a qualidade do código.

## Agradecimentos

Este projeto foi desenvolvido como parte de uma atividade acadêmica para demonstrar conceitos de engenharia de dados e desenvolvimento web. Agradeço a todos os colegas e professores que contribuíram com ideias e feedback durante o processo.

## Contato

Email: lauro.s.pereira@gmail.com
GitHub: github.com/lauroPereira
