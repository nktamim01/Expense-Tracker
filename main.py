import json
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

app = FastAPI()

class Expense(BaseModel):
    id: Annotated[str, Field(..., description='ID of the expense', example='E001')]
    name: Annotated[str, Field(..., description='Name of the expense', example='Groceries')]
    amount: Annotated[float, Field(..., description='Amount of the expense', example=100.0)]
    category: Annotated[str, Field(..., description='Category of the expense', example='Food')]
    date: Annotated[str, Field(..., description='Date of the expense', example='2023-01-01')]
    description: Annotated[str, Field(..., description='Description of the expense', example='Weekly grocery shopping')]


class ExpenseUpdate(BaseModel):

    name: Annotated[str | None, Field(default=None)]
    amount: Annotated[int | None, Field(default=None)]
    category: Annotated[str | None, Field(default=None)]
    date: Annotated[str | None, Field(default=None)]
    description: Annotated[str | None, Field(default=None)]


def load_data():
    with open('expenses.json','r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('expenses.json','w') as f:
        json.dump(data, f, indent=4)

@app.get("/hello")
def hello():
    return "Hi"
 

@app.get("/about")
def about():
    return "This is our about page."

@app.get("/view")
def view_expenses():
    data = load_data()
    return data

@app.get("/view/{expense_id}")
def view_specific_expense(expense_id: str = Path(..., description='ID of the expenses', example='E001')):
    data = load_data()
    if expense_id in data:
        return data[expense_id]
    else:
        raise HTTPException(status_code=404, detail="Expense not found")


@app.get("/sort")
def view_sorted_expenses(sorted_by: str , order : str):
    data = load_data()

    sorted_data = list(data.values())
    def get_values(expenses):
        return expenses[sorted_by]
    if order == 'asc':
        sorted_data.sort(key=get_values)
    else:
        sorted_data.sort(key=get_values, reverse=True)
    #sorted_data.sort(key=lambda x: x[sorted_by])
    return sorted_data


@app.post("/create")
def create_expense(expense: Expense):
    data = load_data()
    if expense.id in data:
        raise HTTPException(status_code=400, detail="Expense ID already exists.")
    data[expense.id] = expense.model_dump(exclude=['id'])
    save_data(data)
    return {"message": "Expense information saved successfully."}



@app.put("/edit/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseUpdate):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found.")
    data[expense_id].update(expense.model_dump(exclude_unset=True))
    save_data(data)
    return {"message": "Expense information saved successfully."}


@app.delete("/edit/{expense_id}")
def delete_expense(expense_id: str):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found.")
    del data[expense_id]
    save_data(data)
    return {"message": "Expense deleted successfully."}