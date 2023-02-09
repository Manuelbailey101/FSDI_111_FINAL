from flask import (
Flask, 
request,   
render_template 
)
 
import requests


app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5000/"


@app.get("/")
def index():
    response = requests.get(BACKEND_URL)
    message = "API not detected."
    if response.status_code == 200:
        message = "API is up and running"
    return render_template("index.html", message=message)

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/task")    
def task_list():
    url = "%s%s" % (BACKEND_URL, "tasks")
    response = requests.get(url)
    if response.status_code == 200:
        tasks = response.json().get("task")
        return render_template("error.html"), response.status_code


@app.get("/task/<int:pk>")    
def task_detail(pk):
    url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)  
    response = request.get(url)
    if response.status_code == 200:
        task = response.json().get("task")
        return render_template("detail.html", task=task)
    return render_template("error.html"), response.status_code

@app.get("/task/new")
def task_create_form():
    return render_template("new.html")

@app.post("/task/new")           
def create_new_task():
    raw_data = request.form
    task_dict = {
        "summary": raw_data.get("summary"),
        "description": raw_data.get("description")
    }
    url = "%s%s" % (BACKEND_URL, "task")
    response = request.get(url, json=task_dict)
    if response.status_code == 204:
        return render_template("success.html")
    return render_template("error.html"), response.status_code

@app.get("/tasks/<int:pk>/edit")
def task_edit_form(pk):
    url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
    response = requests.get(url)
    if response.status_code == 200:
        task = response.json().get("task")
        return render_template("edit.html", task=task)
    return render_template("error.html"), response.status_code

@app.post("/task/edit")
def edit_task(pk):
    raw_data = request.form
    task_dict = {
        "summary": raw_data.get("summary"),
        "description": raw_data.get("description")
    }
    url = "%s%s/%s" % ( BACKEND_URL,"tasks", pk)
    response = request.get(url, json=task_dict)
    if response.status_code == 204:
        return render_template("success.html")
    return render_template("error.html"), response.status_code

@app.get("/tasks/<int:pk>/delete")        
def delete_task_form(pk):
    url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
    response = request.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("delete_form.html", task=task_data)
    return render_template("error.html"), response.status_code

@app.get("/task/<int:pk>/delete")       
def delete_task(pk):
    url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
    response = request.delete(url)
    if response.status_code == 204:
       return render_template("success.html")
    return render_template("error.html"), response.status_code   