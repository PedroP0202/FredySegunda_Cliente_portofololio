"""
Script para criar superusers em produção via variáveis de ambiente.
Executado automaticamente no deploy do Railway.

Variáveis de ambiente necessárias no Railway:
  DJANGO_SUPERUSER_USERNAME  - username do superuser
  DJANGO_SUPERUSER_PASSWORD  - password do superuser
  DJANGO_SUPERUSER_EMAIL     - email do superuser (opcional)

Exemplo de uso:
  python scripts/create_superuser.py
"""

import os
import sys
import django

# Configurar o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

SUPERUSER_USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME")
SUPERUSER_PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
SUPERUSER_EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

if not SUPERUSER_USERNAME or not SUPERUSER_PASSWORD:
    print("⚠️  AVISO: DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD não definidas.")
    print("   Superuser não foi criado. Defina as variáveis de ambiente no Railway.")
    sys.exit(0)

if User.objects.filter(username=SUPERUSER_USERNAME).exists():
    print(f"✅ Superuser '{SUPERUSER_USERNAME}' já existe. Nenhuma ação necessária.")
else:
    User.objects.create_superuser(
        username=SUPERUSER_USERNAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )
    print(f"✅ Superuser '{SUPERUSER_USERNAME}' criado com sucesso!")
