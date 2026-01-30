from pathlib import Path
import json

def get_stored_username(path):
    """저장된 사용자 이름이 있으면 가져옵니다."""
    if path.exists():
        contents = path.read_text()
        username = json.loads(contents)
        return username
    else:
        return None 

def greet_user():
    """사용자를 이름으로 환영합니다."""
    path = Path('username.json')
    username = get_stored_username(path)
    if username:
        print(f"Welcome back, {username}!")
    else:
        username = input("What is your name? ")
        contents = json.dumps(username)
        path.write_text(contents)
        print(f"We'll remember you when you come back, {username}!")

greet_user()
