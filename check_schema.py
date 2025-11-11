import json
import urllib.request
from urllib.error import HTTPError

def check_schema():
    base_url = "http://localhost:8001"
    
    print("Проверка схемы API...")
    
    # Получаем OpenAPI схему в JSON
    print("\n1. Получение OpenAPI схемы в JSON:")
    try:
        req = urllib.request.Request(f"{base_url}/schema/openapi.json", method="GET")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"   Статус: {response.status}")
            print(f"   Схема получена, версия: {data.get('openapi', 'unknown')}")
            
            # Проверяем пути
            paths = data.get('paths', {})
            if '/users' in paths:
                user_paths = paths['/users']
                print(f"   Методы для /users: {list(user_paths.keys())}")
                
                if 'post' in user_paths:
                    post_operation = user_paths['post']
                    print(f"   POST операция: {post_operation}")
                    
    except HTTPError as e:
        print(f"   Статус: {e.code}")
        print(f"   Ответ: {e.read().decode()}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Пробуем получить YAML схему
    print("\n2. Получение OpenAPI схемы в YAML:")
    try:
        req = urllib.request.Request(f"{base_url}/schema/openapi.yaml", method="GET")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode()
            print(f"   Статус: {response.status}")
            print(f"   Схема YAML получена")
            
    except HTTPError as e:
        print(f"   Статус: {e.code}")
        try:
            error_content = e.read().decode()
            print(f"   Ответ: {error_content}")
        except:
            print("   Не удалось получить содержимое ошибки")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Пробуем получить Swagger UI
    print("\n3. Проверка наличия документации:")
    try:
        req = urllib.request.Request(f"{base_url}/schema/swagger", method="GET")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode()
            print(f"   Статус: {response.status}")
            print(f"   Документация доступна")
            
    except HTTPError as e:
        print(f"   Статус: {e.code}")
        try:
            error_content = e.read().decode()
            print(f"   Ответ: {error_content[:200]}...")  # Показываем только начало
        except:
            print("   Не удалось получить содержимое ошибки")
    except Exception as e:
        print(f"   Ошибка: {e}")

if __name__ == "__main__":
    check_schema()