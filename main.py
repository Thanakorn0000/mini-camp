from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# สินค้าในโกดัง: id, name, quantity
products: List[dict] = []
product_id = 1

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.post("/add-product")
def add_product(name: str = Form(...), quantity: int = Form(...)):
    global product_id
    products.append({"id": product_id, "name": name, "quantity": quantity})
    product_id += 1
    return RedirectResponse("/", status_code=303)

@app.post("/delete-product")
async def delete_product(id: int = Form(...)):
    global products
    products = [p for p in products if p["id"] != id]
    return JSONResponse({"success": True})

@app.post("/update-product")
async def update_product(id: int = Form(...), name: str = Form(...), quantity: int = Form(...)):
    for p in products:
        if p["id"] == id:
            p["name"] = name
            p["quantity"] = quantity
            return JSONResponse({"success": True})
    return JSONResponse({"success": False}, status_code=404)

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/contact", response_class=HTMLResponse)
def submit_contact(request: Request, name: str = Form(...), message: str = Form(...)):
    print(f"Message from {name}: {message}")
    return templates.TemplateResponse("contact.html", {"request": request, "success": True})