from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Load or initialize blog data
BLOG_FILE = "blog.json"

if not os.path.exists(BLOG_FILE):
    with open(BLOG_FILE, "w") as f:
        json.dump([], f)


def read_blog_data():
    with open(BLOG_FILE, "r") as f:
        return json.load(f)


def write_blog_data(data):
    with open(BLOG_FILE, "w") as f:
        json.dump(data, f)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    blogs = read_blog_data()
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})


@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int):
    blogs = read_blog_data()
    post = blogs[post_id] if 0 <= post_id < len(blogs) else None
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@app.get("/create_post", response_class=HTMLResponse)
async def create_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.post("/create_post")
async def create_post(title: str = Form(...), content: str = Form(...)):
    blogs = read_blog_data()
    blogs.append({"title": title, "content": content})
    write_blog_data(blogs)
    return RedirectResponse("/", status_code=303)


@app.post("/delete_post/{post_id}")
async def delete_post(post_id: int):
    blogs = read_blog_data()
    if 0 <= post_id < len(blogs):
        blogs.pop(post_id)
        write_blog_data(blogs)
    return RedirectResponse("/", status_code=303)
