```markdown
# 🚀 Portfolio Management System

A comprehensive RESTful API for managing user portfolios with JWT authentication, project management, skills tracking, category organization, search, and dashboard statistics. Built with Flask, SQLAlchemy, and Flask-JWT-Extended.

---

## ✨ Features

- ✅ **User Registration & Login** – Secure JWT token-based authentication
- 📁 **Full CRUD for Projects** – Create, Read, Update, Delete projects
- 👤 **Portfolio Information** – Personal info, about, contact, social media links
- 🛠️ **Skills Management** – Add, update, delete skills with proficiency levels
- 🏷️ **Project Categories** – Categorize projects (Web, Mobile, Design, Data, custom)
- 🔍 **Search Functionality** – Search projects by name, technology, or category
- 📊 **Dashboard Statistics** – Total projects, skills, category breakdowns
- 📖 **Swagger Documentation** – Interactive API docs at `/api/docs`
- 🔒 **User Isolation** – Each user sees only their own data
- 🔐 **Password Hashing** – Secured with bcrypt
- 🗄️ **SQLite Database** – Ready to switch to PostgreSQL for production

---

## 🛠️ Tech Stack

- 🐍 **Python 3.8+**
- 🌐 **Flask** – Web framework
- 🗃️ **Flask-SQLAlchemy** – Database ORM
- 🔑 **Flask-JWT-Extended** – JWT authentication
- 🔒 **Flask-Bcrypt** – Password hashing
- 📘 **Flask-Swagger-UI** – Interactive API documentation
- 💾 **SQLite** – Development database

---

## 📁 Project Structure

```
portfolio_manager/
├── app.py              # App factory & entry point
├── config.py           # Configuration settings
├── models.py           # User, Portfolio, Project, Skill, Category models
├── auth.py             # Register & login routes
├── routes.py           # All CRUD routes (portfolio, skills, categories, projects, search, dashboard)
├── swagger.py          # Swagger UI blueprint setup
├── requirements.txt    # Python dependencies
├── test.http           # Example requests (VS Code REST Client)
├── .gitignore
└── static/
    └── swagger.json    # OpenAPI specification
```

---

## ⚙️ Installation & Run

### 1️⃣ Clone or create the project

```bash
git clone 
cd portfolio_manager
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the server

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`.

---

## 📡 API Endpoints

### 🔐 Authentication

| Method | Endpoint    | Body                               | Response                     |
| ------ | ----------- | ---------------------------------- | ---------------------------- |
| POST   | `/register` | `{"username":"x", "password":"y"}` | `{"message":"User created"}` |
| POST   | `/login`    | `{"username":"x", "password":"y"}` | `{"access_token":"..."}`     |

### 👤 Portfolio (requires `Authorization: Bearer `)

| Method | Endpoint      | Body (see below)                           | Response                        |
| ------ | ------------- | ----------------------------------------- | ------------------------------- |
| GET    | `/portfolio`  | —                                         | Portfolio data                  |
| PUT    | `/portfolio`  | See portfolio fields below                | `{"message":"Portfolio updated"}` |

**Portfolio fields:** `full_name`, `email`, `phone`, `location`, `title`, `about`, `experience_years`, `contact_email`, `contact_phone`, `github`, `linkedin`, `twitter`, `website`

### 🛠️ Skills (requires `Authorization: Bearer `)

| Method | Endpoint        | Body                                        | Response                          |
| ------ | --------------- | ------------------------------------------- | --------------------------------- |
| GET    | `/skills`       | —                                           | Array of user's skills            |
| POST   | `/skills`       | `{"name":"...", "proficiency":90, "category":"..."}` | `{"message":"Skill added"}` |
| PUT    | `/skills/`  | Any subset of fields above                  | `{"message":"Skill updated"}`     |
| DELETE | `/skills/`  | —                                           | `{"message":"Skill deleted"}`     |

### 🏷️ Categories (requires `Authorization: Bearer `)

| Method | Endpoint           | Body                                        | Response                              |
| ------ | ------------------ | ------------------------------------------- | ------------------------------------- |
| GET    | `/categories`      | —                                           | Array of all categories               |
| POST   | `/categories`      | `{"name":"...", "description":"..."}`       | `{"message":"Category created"}`      |
| PUT    | `/categories/` | Any subset of fields above                  | `{"message":"Category updated"}`      |
| DELETE | `/categories/` | —                                           | `{"message":"Category deleted"}`      |

### 📂 Projects (requires `Authorization: Bearer `)

| Method | Endpoint          | Body                                                        | Response                          |
| ------ | ----------------- | ----------------------------------------------------------- | --------------------------------- |
| GET    | `/projects`       | —                                                           | Array of user's projects          |
| POST   | `/projects`       | `{"name":"...", "description":"...", "technologies":"...", "category":"...", "start_date":"2024-01-01", "end_date":"2024-03-15"}` | `{"message":"Project created"}` |
| PUT    | `/projects/`  | Any subset of the fields above                              | `{"message":"Project updated"}`   |
| DELETE | `/projects/`  | —                                                           | `{"message":"Project deleted"}`  |

### 🔍 Search Projects (requires `Authorization: Bearer `)

| Method | Endpoint                    | Query Parameters                          | Response                  |
| ------ | --------------------------- | ----------------------------------------- | ------------------------- |
| GET    | `/projects/search?q=...&tech=...&category=...` | `q` (name/desc), `tech` (technology), `category` | Filtered projects array |

### 📊 Dashboard Statistics (requires `Authorization: Bearer `)

| Method | Endpoint             | Response                                      |
| ------ | -------------------- | --------------------------------------------- |
| GET    | `/dashboard/stats`   | `{"total_projects": N, "total_skills": N, "category_counts": {...}, "skills_by_category": {...}}` |

### 📖 Swagger Documentation (public)

| Method | Endpoint      | Description                        |
| ------ | ------------- | ---------------------------------- |
| GET    | `/api/docs`   | Interactive Swagger UI             |

---

## 🧪 Testing with VS Code REST Client

1. 📦 Install the **REST Client** extension in VS Code
2. 📄 Open the `test.http` file
3. ▶️ Start the server (`python app.py`)
4. 🖱️ Click **"Send Request"** above each block in this order:
   - `### Register` (first time only)
   - `### Login` – copy the returned token
   - 🔄 Replace `YOUR_TOKEN` in the Authorization headers with your token
   - `### Update Portfolio`
   - `### Get Portfolio`
   - `### Add Skill`
   - `### Get All Skills`
   - `### Get Categories`
   - `### Add Project`
   - `### Get All Projects`
   - `### Search Projects by Name`
   - `### Get Dashboard Stats`

---

## 🌐 Testing with curl (examples)

```bash
# Register
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'

# Login (save the token)
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}' | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Update portfolio
curl -X PUT http://127.0.0.1:5000/portfolio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"full_name":"John Doe","title":"Full Stack Developer","about":"5 years experience"}'

# Add skill
curl -X POST http://127.0.0.1:5000/skills \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Python","proficiency":90,"category":"Backend"}'

# Add project
curl -X POST http://127.0.0.1:5000/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"E-commerce Platform","description":"Full-stack app","technologies":"Python,Flask,React","category":"Web Development"}'

# Get dashboard stats
curl http://127.0.0.1:5000/dashboard/stats \
  -H "Authorization: Bearer $TOKEN"

# Search projects
curl "http://127.0.0.1:5000/projects/search?q=ecommerce&tech=React" \
  -H "Authorization: Bearer $TOKEN"
```

---

## ✅ Evaluation Criteria Met

| Criteria            | Status |
| ------------------- | ------ |
| 🏗️ **API Design**   | ✅ RESTful endpoints with proper HTTP methods and status codes |
| 🗃️ **Database Structure** | ✅ SQLAlchemy models with relationships and constraints |
| 📖 **Documentation** | ✅ Swagger UI + Postman-ready `test.http` + this README |
| 🔑 **Authentication** | ✅ JWT with bcrypt password hashing, all protected endpoints |
| 💻 **Code Quality**  | ✅ Modular Blueprints, clean separation, error handling, readable |

### Week 2 Enhancements

- ✅ **Portfolio Information API** – Personal info, about, contact, social
- ✅ **Skills Management API** – Full CRUD with proficiency and category
- ✅ **Project Categories** – 4 default + custom categories
- ✅ **Search Functionality** – By name, technology, category
- ✅ **Dashboard Statistics API** – Project/skill counts, category breakdown
- ✅ **Swagger Documentation** – Interactive API docs

---

## 📚 What I Learned

- 🌐 **Flask Framework** – Building RESTful APIs with Blueprints for modular code
- 🔑 **JWT Authentication** – Implementing secure token-based user login/registration
- 🔒 **Password Hashing** – Using bcrypt to securely store user passwords
- 🗃️ **SQLAlchemy ORM** – Creating database models with relationships (one-to-many, many-to-one)
- 🏗️ **API Design** – Structuring endpoints with proper HTTP methods and status codes
- ⚠️ **Error Handling** – Managing exceptions and returning meaningful responses
- 🧪 **Testing APIs** – Using VS Code REST Client and curl to test endpoints
- 📂 **Project Structure** – Organizing code into separate files for maintainability
- 📖 **API Documentation** – Setting up Swagger UI with OpenAPI specification
- 💼 **Real-World Workflow** – Following task requirements and meeting evaluation criteria

---

## 👨‍💻 Author

**Muhammad Ishaq**  
📧 Email: [ishaqriaz12345@gmail.com](mailto:ishaqriaz12345@gmail.com)  
🔗 GitHub: [IshaqRiaz](https://github.com/IshaqRiaz)

---

## ⭐ Support

If you like this project:

- ⭐ **Star** the repository
- 🍴 **Fork** it
- 🧠 **Share** it with others

---

## 🚀 Future Enhancements (Optional)

- 📄 Add pagination to `GET /projects` and `GET /skills`
- 🖼️ Image upload for project screenshots
- 🐘 Switch to PostgreSQL for production deployment
- 🧪 Write unit tests with pytest
- 🌐 Add CORS for frontend integration
- ☁️ Deploy to Heroku, AWS, or DigitalOcean
- 🎨 Build a React/Angular frontend
- ⏱️ Add rate limiting for security
- 🔄 Implement refresh tokens
- 🌍 Multi-language support

---

**Built with ❤️ as Internship Task for Codiora Technologies**

```
