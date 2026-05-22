# Personal Chico Security API

API Django REST com autenticação JWT, gerenciamento de usuários, diário privado e sistema de permissões baseado em grupos.

## 🚀 Configuração Inicial

### 1. Clonar o repositório
```bash
git clone <seu_repositorio>
cd personal-chico-security-api
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Aplicar migrações
```bash
python manage.py migrate
```

### 5. Criar superusuário
```bash
python manage.py createsuperuser
```

### 6. Criar grupo Editor (opcional)
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group
Group.objects.get_or_create(name='Editor')
```

### 7. Executar servidor
```bash
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/`

---

## 📋 Endpoints

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/register/` | Registrar novo usuário |
| POST | `/api/auth/login/` | Obter tokens JWT |
| POST | `/api/auth/refresh/` | Renovar access token |
| POST | `/api/auth/logout/` | Logout e invalidar refresh token |
| GET | `/api/auth/me/` | Obter dados do usuário logado |

### Diário (Journal)

| Método | Endpoint | Autenticação | Descrição |
|--------|----------|-------------|-----------|
| GET | `/api/journal/` | Requerida | Listar entradas |
| POST | `/api/journal/` | Requerida | Criar entrada |
| GET | `/api/journal/{id}/` | Requerida | Detalhe de entrada |
| PUT | `/api/journal/{id}/` | Requerida | Editar entrada (owner) |
| DELETE | `/api/journal/{id}/` | Requerida | Deletar entrada (owner) |
| GET | `/api/journal/public/` | Nenhuma | Listar entradas públicas |

---

## 🔑 Autenticação JWT

### 1. Registrar novo usuário
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -d '{"username":"seu_usuario","email":"email@example.com","password":"senha123"}' \
  -H "Content-Type: application/json"
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -d '{"username":"seu_usuario","password":"senha123"}' \
  -H "Content-Type: application/json"
```

Resposta:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Usar o access token
```bash
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  http://localhost:8000/api/auth/me/
```

### 4. Renovar access token
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -d '{"refresh":"SEU_REFRESH_TOKEN"}' \
  -H "Content-Type: application/json"
```

### 5. Logout
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -d '{"refresh":"SEU_REFRESH_TOKEN"}' \
  -H "Content-Type: application/json"
```

---

## 📝 Operações com Diário

### Criar entrada
```bash
curl -X POST http://localhost:8000/api/journal/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -d '{
    "title":"Meu dia",
    "content":"Conteúdo da entrada",
    "mood":"happy",
    "is_public":false
  }' \
  -H "Content-Type: application/json"
```

### Listar minhas entradas
```bash
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  http://localhost:8000/api/journal/
```

### Ver entrada específica
```bash
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  http://localhost:8000/api/journal/1/
```

### Editar entrada (apenas owner)
```bash
curl -X PUT http://localhost:8000/api/journal/1/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -d '{"title":"Novo título","content":"Novo conteúdo","mood":"sad","is_public":true}' \
  -H "Content-Type: application/json"
```

### Deletar entrada (apenas owner)
```bash
curl -X DELETE http://localhost:8000/api/journal/1/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### Listar entradas públicas (sem autenticação)
```bash
curl http://localhost:8000/api/journal/public/
```

---

## 👥 Sistema de Grupos - Editor

### Adicionar usuário ao grupo Editor
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='seu_usuario')
editor_group = Group.objects.get(name='Editor')
user.groups.add(editor_group)
```

### Permissões do grupo Editor
- ✅ Ver todas as entradas de qualquer usuário (somente leitura)
- ❌ Não pode editar entradas de outros usuários
- ❌ Não pode deletar entradas de outros usuários
- ✅ Pode criar, editar e deletar suas próprias entradas

---

## 🔒 Campos do Diário

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | ID da entrada |
| author | String | Username do autor (somente leitura) |
| title | String | Título da entrada |
| content | String | Conteúdo da entrada |
| mood | Choice | happy, neutral, sad |
| is_public | Boolean | Se a entrada é pública |
| created_at | DateTime | Data de criação (somente leitura) |

---

## 🛠️ Stack Tecnológico

- Django 6.0
- Django REST Framework
- djangorestframework-simplejwt
- djangorestframework-simplejwt[blacklist]
- SQLite3 (desenvolvimento)

---

## 📄 Estrutura do Projeto

```
personal-chico-security-api/
├── accounts/              # App de autenticação
│   ├── migrations/
│   ├── views.py          # RegisterView, CurrentUserView, LogoutView
│   ├── serializers.py    # RegisterSerializer, UserSerializer
│   ├── urls.py
│   └── models.py
├── journal/               # App de diário
│   ├── migrations/
│   ├── views.py          # JournalEntryViewSet, PublicJournalViewSet
│   ├── serializers.py    # JournalEntrySerializer
│   ├── permissions.py    # IsOwner, IsEditorOrReadOnly
│   ├── urls.py
│   ├── models.py         # JournalEntry
│   └── admin.py
├── core/                  # Configurações do projeto
│   ├── settings.py       # Configurações Django
│   ├── urls.py           # URLs principais
│   └── wsgi.py
├── manage.py
└── db.sqlite3            # Banco de dados (não commitado)
```

---

## ⚙️ Configurações Importantes

### JWT Token Lifetime
- Access Token: 60 minutos
- Refresh Token: 7 dias

### Blacklist de Tokens
Tokens inválidos após logout são armazenados em `OutstandingToken` e `BlacklistedToken`.

### Permissões
- `IsAuthenticated`: Usuário deve estar autenticado
- `IsOwner`: Usuário deve ser o proprietário da entrada
- `IsEditorOrReadOnly`: Editor pode ver tudo (read-only), owner pode fazer qualquer coisa
- `AllowAny`: Sem autenticação requerida

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'django'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "TypeError: 'module' object is not iterable"
Verifique se `urlpatterns` é uma lista em todos os `urls.py`.

### Token inválido após logout
Tokens blacklistados não podem ser usados novamente. Obtenha um novo token com login.

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação:
- [Django REST Framework](https://www.django-rest-framework.org/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
