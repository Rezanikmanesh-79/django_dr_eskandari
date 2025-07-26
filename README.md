# 🐳 Django Dr Eskandari - Dockerized Classroom Project

This is a Django-based classroom project, fully containerized using Docker and Docker Compose for easy setup and deployment.

---

## 🚀 Features

- Basic Django web application for class exercises  
- Containerized environment for consistent development  
- Uses Docker Compose to orchestrate services (web, db, etc.)  
- Easy to build, run, and maintain  

---

## 🧰 Technology Stack

- Python 3.x  
- Django 5.x  
- PostgreSQL (or SQLite, depending on setup)  
- Docker & Docker Compose  

---

## ⚙️ Running with Docker Compose

Make sure you have Docker and Docker Compose installed.

1. Clone the repository:

```bash
git clone https://github.com/Rezanikmanesh-79/django_dr_eskandari.git
cd django_dr_eskandari
````

2. Build and start containers:

```bash
docker-compose up --build
```

3. Access the app at:

```
http://localhost:8000/
```

4. To create superuser (inside the container):

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 📂 Project Structure

```
django_dr_eskandari/
├── blog/              # Main app
├── core/              # Django project settings
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## 👨‍💻 Author

**Reza Nikmanesh**
GitHub: [@Rezanikmanesh-79](https://github.com/Rezanikmanesh-79)

---

## 📝 License

MIT License — free for personal and educational use.


