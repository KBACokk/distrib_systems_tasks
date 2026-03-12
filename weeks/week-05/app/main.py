import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn

tasks_db = []  # Изменено с items_db

@strawberry.type
class Task:  # Изменено с Item
    id: str
    name: str
    price: float

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> list[Task]:  # Изменено с items
        return [Task(**item) for item in tasks_db]

    @strawberry.field
    def task(self, id: str) -> Task | None:  # Изменено с item
        for item in tasks_db:
            if item["id"] == id:
                return Task(**item)
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(self, name: str, price: float) -> Task:  # Изменено с create_item
        new_id = str(len(tasks_db) + 1)
        new_task = {"id": new_id, "name": name, "price": price}
        tasks_db.append(new_task)
        return Task(**new_task)

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")

@app.get("/")
async def main():
    return {"link": "http://localhost:8122/graphql"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8122)