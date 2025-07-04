import os
import sys
import django

# Ensure project root is on Python path so Django modules can be found
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
backend_dir = os.path.join(base_dir, 'backend')
sys.path.append(backend_dir)
# Also add direct app folders so Django finds the 'api' and 'products' modules
sys.path.append(os.path.join(backend_dir, 'api'))
sys.path.append(os.path.join(backend_dir, 'products'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.cfehome.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_user(username, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        print(f"User '{username}' created successfully with ID {user.id}")
    else:
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists with ID {user.id}")
    
    token, created = Token.objects.get_or_create(user=user)
    if created:
        print(f"New token generate: {token.key}")
    else:
        print(f"Existing token: {token.key}")

    with open('.env', 'a') as env_file:
        env_file.write(f'\n{username.upper()}_TOKEN={token.key}')
    print(f"Token saved in .env as {username.upper()}_TOKEN")

    return user

if __name__ == '__main__':
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
        create_user(username, password)
    else:
        print("Usage: python create_user.py <username> <password>")