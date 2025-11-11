import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import uuid

def test_api():
    base_url = "http://localhost:8001"
    
    print("Тестирование API...")
    
    # Тест 1: Получение списка пользователей
    print("\n1. Получение списка пользователей:")
    try:
        req = urllib.request.Request(f"{base_url}/users/", method="GET")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"   Статус: {response.status}")
            print(f"   Ответ: {len(data)} пользователей")
            if len(data) > 0:
                print(f"   Пример: {data[0]['username']} - {data[0]['email']}")
    except HTTPError as e:
        print(f"   Статус: {e.code}")
        print(f"   Ответ: {e.read().decode()}")
    
    # Тест 2: Создание нового пользователя
    print("\n2. Создание нового пользователя:")
    new_user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    
    try:
        json_data = json.dumps(new_user_data).encode('utf-8')
        req = urllib.request.Request(f"{base_url}/users/", data=json_data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            created_user = json.loads(response.read().decode())
            print(f"   Статус: {response.status}")
            print(f"   Ответ: Пользователь создан - {created_user['username']}")
            
            if 'id' in created_user:
                user_id = created_user.get('id')
                
                # Тест 3: Получение созданного пользователя по ID
                print(f"\n3. Получение пользователя по ID {user_id}:")
                try:
                    req = urllib.request.Request(f"{base_url}/users/{user_id}", method="GET")
                    req.add_header('Content-Type', 'application/json')
                    
                    with urllib.request.urlopen(req) as response:
                        user = json.loads(response.read().decode())
                        print(f"   Статус: {response.status}")
                        print(f"   Ответ: {user['username']} - {user['email']}")
                except HTTPError as e:
                    print(f"   Статус: {e.code}")
                    print(f"   Ответ: {e.read().decode()}")
                
                # Тест 4: Обновление пользователя
                print(f"\n4. Обновление пользователя {user_id}:")
                update_data = {
                    "username": "updateduser",
                    "email": "updated@example.com"
                }
                
                try:
                    json_data = json.dumps(update_data).encode('utf-8')
                    req = urllib.request.Request(f"{base_url}/users/{user_id}", data=json_data, method="PUT")
                    req.add_header('Content-Type', 'application/json')
                    
                    with urllib.request.urlopen(req) as response:
                        updated_user = json.loads(response.read().decode())
                        print(f"   Статус: {response.status}")
                        print(f"   Ответ: {updated_user['username']} - {updated_user['email']}")
                except HTTPError as e:
                    print(f"   Статус: {e.code}")
                    print(f"   Ответ: {e.read().decode()}")
                
                # Тест 5: Удаление пользователя
                print(f"\n5. Удаление пользователя {user_id}:")
                try:
                    req = urllib.request.Request(f"{base_url}/users/{user_id}", method="DELETE")
                    
                    with urllib.request.urlopen(req) as response:
                        print(f"   Статус: {response.status}")
                        print(f"   Ответ: Удаление выполнено")
                except HTTPError as e:
                    print(f"   Статус: {e.code}")
                    print(f"   Ответ: {e.read().decode()}")
    except HTTPError as e:
        print(f"   Статус: {e.code}")
        print(f"   Ответ: {e.read().decode()}")
    
    print("\nТестирование завершено.")

if __name__ == "__main__":
    test_api()