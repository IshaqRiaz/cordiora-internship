# 🚀 Portfolio Management System

A RESTful API for managing user portfolios with JWT authentication. Built with Flask, SQLAlchemy, and Flask-JWT-Extended.

## ✨ Features

- ✅ **User Registration & Login** – Secure JWT token-based authentication
- 📁 **Full CRUD for Projects** – Create, Read, Update, Delete projects
- 🔒 **User Isolation** – Each user sees only their own projects
- 🔐 **Password Hashing** – Secured with bcrypt
- 🗄️ **SQLite Database** – Ready to switch to PostgreSQL for production

## 🛠️ Tech Stack

- 🐍 **Python 3.8+**
- 🌐 **Flask** – Web framework
- 🗃️ **Flask-SQLAlchemy** – Database ORM
- 🔑 **Flask-JWT-Extended** – JWT authentication
- 🔒 **Flask-Bcrypt** – Password hashing
- 💾 **SQLite** – Development database

## 📁 Project Structure

```
portfolio_manager/
├── app.py          # App factory & entry point
├── models.py       # User & Project models
├── auth.py         # Register & login routes
├── routes.py       # CRUD routes for projects
├── config.py       # Configuration
├── requirements.txt
├── .gitignore
└── test.http       # Example requests (VS Code REST Client)
```

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

## 📡 API Endpoints

### 🔐 Authentication

| Method | Endpoint    | Body                               | Response                     |
| ------ | ----------- | ---------------------------------- | ---------------------------- |
| POST   | `/register` | `{"username":"x", "password":"y"}` | `{"message":"User created"}` |
| POST   | `/login`    | `{"username":"x", "password":"y"}` | `{"access_token":"..."}`     |

### 📂 Projects (all require `Authorization: Bearer ` header)

| Method | Endpoint     | Body                                                        | Response                        |
| ------ | ------------ | ----------------------------------------------------------- | ------------------------------- |
| GET    | `/projects`  | —                                                           | Array of user's projects        |
| POST   | `/projects`  | `{"name":"...", "description":"...", "technologies":"..."}` | `{"message":"Project created"}` |
| PUT    | `/projects/` | Any subset of the fields above                              | `{"message":"Project updated"}` |
| DELETE | `/projects/` | —                                                           | `{"message":"Project deleted"}` |

## 🧪 Testing the API with VS Code

1. 📦 Install the **REST Client** extension in VS Code
2. 📄 Open the `test.http` file
3. ▶️ Start the server (`python app.py`)
4. 🖱️ Click **"Send Request"** above each block in this order:
   - `### Register` (first time only)
   - `### Login` – copy the returned token
   - 🔄 Replace `REPLACE_ME` in the Authorization headers with your token
   - `### Add Project`
   - `### Get All Projects`
   - `### Update Project`
   - `### Delete Project`

## 🌐 Testing with curl (alternative)

```bash
# Register
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'

# Login (save the token)
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'

# Add project
curl -X POST http://127.0.0.1:5000/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name":"My Project","description":"Test","technologies":"Python,Flask"}'

# Get projects
curl http://127.0.0.1:5000/projects \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Update project
curl -X PUT http://127.0.0.1:5000/projects/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name":"Updated Name"}'

# Delete project
curl -X DELETE http://127.0.0.1:5000/projects/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## ✅ Evaluation Criteria Met

- ✅ **API Structure** – Clean separation of concerns using Flask Blueprints
- ✅ **Database Integration** – SQLAlchemy with SQLite
- ✅ **Authentication Implementation** – JWT-based with bcrypt password hashing
- ✅ **Code Quality** – Modular, readable, error handling
- ✅ **Proper CRUD** – All four operations implemented

## 📚 What I Learned

- 🌐 **Flask Framework** – Building RESTful APIs with Blueprints for modular code
- 🔑 **JWT Authentication** – Implementing secure token-based user login/registration
- 🔒 **Password Hashing** – Using bcrypt to securely store user passwords
- 🗃️ **SQLAlchemy ORM** – Creating database models and performing CRUD operations
- 🏗️ **API Design** – Structuring endpoints with proper HTTP methods and status codes
- ⚠️ **Error Handling** – Managing exceptions and returning meaningful responses
- 🧪 **Testing APIs** – Using VS Code REST Client to test endpoints locally
- 📂 **Project Structure** – Organizing code into separate files for maintainability
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

## 🚀 Future Work (Optional Enhancements)

- 📄 Add pagination to `GET /projects`
- 🔍 Add project search by name or technology
- 🐘 Switch to PostgreSQL for production
- 👤 Add user profile management
- 🌐 Add CORS for frontend integration
- 🧪 Write unit tests with pytest
- 🏷️ Add project categories/tags
- ☁️ Deploy to production (Heroku, AWS, or DigitalOcean)
- 🎨 Add frontend (React/Angular) for visual interface
- 📖 Add API documentation with Swagger/OpenAPI
- ⏱️ Add rate limiting for security
- 🔄 Implement refresh tokens for better authentication
- 🖼️ Add image upload for project screenshots

---

**Built with ❤️ as Task 1 for Codiora Technologies Internship**
