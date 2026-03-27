import requests
import json

project_code = "tasks-s11"

def build_payload(query: str, variables: dict) -> dict:
    return {"query": query, "variables": variables}


def execute_query(url: str, query: str, variables: dict = None):
    payload = build_payload(query, variables or {})
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if "errors" in result:
            print("GraphQL Errors:")
            for error in result["errors"]:
                print(f"  - {error.get('message', 'Unknown error')}")
            return result
        else:
            print("Data received successfully:")
            print(json.dumps(result.get("data"), indent=2, ensure_ascii=False))
            return result.get("data")
            
    except Exception as error:
        print(f"Error: {error}")
        return None


def main():
    url = "http://localhost:8272/graphql"
    print(f"Project code: {project_code}")
    
    query_get_data = """
    query GetData {
        tasks {
            id
            title
            description
            status
        }
    }
    """
    
    mutation_create_data = """
    mutation CreateTask($title: String!, $description: String!) {
        createTask(
            title: $title,
            description: $description,
            status: "pending"
        ) {
            id
            title
            description
            status
        }
    }
    """
    
    items_data = [
        {"title": "Задача 1", "description": "Описание задачи 1"},
        {"title": "Задача 2", "description": "Описание задачи 2"},
        {"title": "Задача 3", "description": "Описание задачи 3"},
    ]
    
    print("=" * 50)
    print(f"Создание новых {project_code}:")
    print("=" * 50)
    for item in items_data:
        print(f"\nСоздание {project_code} с заголовком '{item['title']}':")
        execute_query(url, mutation_create_data, item)
        print("-" * 30)
    
    print("\n" + "=" * 50)
    print(f"Получение списка всех {project_code}:")
    print("=" * 50)
    execute_query(url, query_get_data)


if __name__ == "__main__":
    main()