# TrainTrack API

API REST para gerenciamento de treinos e usuários, desenvolvida com Django e Django REST Framework.

## 📋 Características

- Autenticação JWT com `djangorestframework_simplejwt`
- Gerenciamento de usuários com sistema de roles (admin, trainer, trainee)
- Gerenciamento de workouts (treinos)
- Documentação automática com Swagger/OpenAPI
- Persistência de dados com PostgreSQL
- Containerização com Docker e Docker Compose
- Filtros e paginação nas listagens

## 🚀 Início Rápido

### Pré-requisitos

- Docker
- Docker Compose

### Instalação e Execução com Docker

1. **Clone o repositório** (se aplicável):
```bash
git clone <seu-repositorio>
cd traintrack-api
```

2. **Configure as variáveis de ambiente**:
```bash
cp .env.example .env
```

3. **Inicie os containers**:
```bash
docker-compose up --build
```

A aplicação estará disponível em `http://127.0.0.1:8000`

A documentação Swagger estará em `http://127.0.0.1:8000/api/swagger`

### Parar os containers

```bash
docker-compose down
```

### Remover dados e volume do banco

```bash
docker-compose down -v
```

## 🔧 Configuração Local (Sem Docker)

### Pré-requisitos

- Python 3.10+
- PostgreSQL 15+
- pip

### Passos

1. **Crie um ambiente virtual**:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure o arquivo `.env`**:
```bash
cp .env.example .env
```

4. **Execute as migrações**:
```bash
python manage.py migrate
```

5. **Crie um superusuário**:
```bash
python manage.py createsuperuser
```

6. **Inicie o servidor**:
```bash
python manage.py runserver
```

## 📚 Endpoints Principais

### Autenticação

- `POST /api/token/` - Obter token JWT
  - Body: `{ "username": "...", "password": "..." }`
  
- `POST /api/token/refresh/` - Renovar token
  - Body: `{ "refresh": "..." }`

### Usuários

- `GET /api/users/` - Listar usuários (requer autenticação)
- `POST /api/users/create-trainee/` - Criar trainee
- `POST /api/users/create-trainer/` - Criar trainer

### Workouts

- `GET /api/workout/` - Listar workouts
- `POST /api/workout/` - Criar workout
- `GET /api/workout/<id>/` - Detalhes do workout
- `PUT /api/workout/<id>/` - Atualizar workout
- `DELETE /api/workout/<id>/` - Deletar workout

### Documentação Interativa

- `GET /api/swagger` - Swagger UI (documentação interativa)
- `GET /api/swagger.json` - Schema OpenAPI em JSON

## 🔐 Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação.

### Como usar:

1. **Obter token**:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"seu_usuario","password":"sua_senha"}'
```

2. **Usar token em requisições**:
```bash
curl http://127.0.0.1:8000/api/users/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📁 Estrutura do Projeto

```
traintrack-api/
├── traintrack_setup/      # Configurações do Django
│   ├── settings.py        # Configurações gerais
│   ├── urls.py            # Rotas principais
│   ├── asgi.py
│   └── wsgi.py
├── users/                 # App de usuários
│   ├── models.py          # Modelos de usuário
│   ├── serializer.py      # Serializadores
│   ├── views.py           # Views/endpoints
│   ├── roles.py           # Definição de roles
│   ├── managers.py        # Custom managers
│   └── migrations/
├── workouts/              # App de treinos
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   └── migrations/
├── Dockerfile             # Configuração Docker
├── docker-compose.yml     # Orquestração Docker
├── requirements.txt       # Dependências Python
├── manage.py
└── db.sqlite3            # Banco local (não usado em Docker)
```

## 🛠 Variáveis de Ambiente

As seguintes variáveis podem ser configuradas em `.env`:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,web,traintrack_api

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=traintrack_db
DATABASE_USER=traintrack_user
DATABASE_PASSWORD=traintrack_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

## 🗄️ Banco de Dados

### Com Docker Compose

O PostgreSQL é iniciado automaticamente como serviço no Docker Compose. Para acessá-lo:

```bash
docker-compose exec db psql -U traintrack_user -d traintrack_db
```

### Migrações

```bash
# Em Docker
docker-compose exec web python manage.py migrate

# Local
python manage.py migrate
```

### Criar migrações

```bash
# Em Docker
docker-compose exec web python manage.py makemigrations

# Local
python manage.py makemigrations
```

## 🧪 Testes

```bash
# Em Docker
docker-compose exec web python manage.py test

# Local
python manage.py test
```

## 📦 Dependências Principais

- **Django** 5.2.12 - Framework web
- **djangorestframework** 3.16.1 - Framework REST
- **djangorestframework_simplejwt** 5.5.1 - Autenticação JWT
- **drf-yasg** 1.21.15 - Documentação Swagger/OpenAPI
- **psycopg2-binary** 2.9.10 - Driver PostgreSQL
- **django-filter** 25.2 - Filtros nos endpoints
- **django-role-permissions** 3.2.0 - Gerenciamento de roles

## 🚨 Troubleshooting

### Erro: "database does not exist"

Remova os volumes e reinicie:
```bash
docker-compose down -v
docker-compose up --build
```

### Erro: "permission denied"

Certifique-se que as variáveis de ambiente estão corretas em `.env`

### Erro: "connection refused"

Aguarde alguns segundos para o banco de dados inicializar completamente.

## 📝 Roles e Permissões

- **admin** - Acesso total à plataforma
- **trainer** - Pode criar e gerenciar trainees e workouts
- **trainee** - Pode visualizar workouts atribuídos

## 🔄 Fluxo de Desenvolvimento

1. Faça alterações no código
2. Com Docker: os arquivos são sincronizados em tempo real
3. Reinicie o container se necessário: `docker-compose restart web`
4. Acesse `http://127.0.0.1:8000/api/swagger` para testar

## 👤 Autor

Antonio Gabriel da Silva - 2026

## 📞 Suporte

Para problemas ou dúvidas, consulte a documentação Swagger em `/api/swagger`
