# GadNEXUS 🧠📱  
A full-stack gadget blog platform built with Flask, MongoDB, and Jinja — where tech enthusiasts can read and share posts about the latest phones, laptops, accessories, and more.

---

## ✨ Features

- 🔐 User Authentication (Register / Login / Reset Password)
- 📝 Create posts with Title, Description, and optional Image URL
- ✏️ Edit and update your own posts
- 🗑️ Delete posts with confirmation popup
- 📱 Mobile-friendly responsive design
- ☁️ MongoDB Atlas cloud database
- 🚀 Deployed on Vercel with GitHub auto-deployment

---

## 🛠 Tech Stack

- 🧠 Backend: Python + Flask
- 💾 Database: MongoDB Atlas
- 🎨 Frontend: HTML5, CSS3, Jinja2 templates
- ⚙️ Deployment: Vercel
- 🧩 Styling: Custom CSS + Bootstrap components

---

## 📁 Folder Structure

├── app.py # Main Flask app <br>
├── templates/<br>
│ ├── layout.html # Base layout<br>
│ ├── index.html # Public blog home page<br>
│ ├── dashboard.html # Logged-in user dashboard<br>
│ ├── login.html # Login page<br>
│ ├── register.html # Register page<br>
│ ├── add.html # Create post form<br>
│ ├── edit.html # Edit post form<br>
├── vercel.json # Vercel deployment config<br>
└── README.md

---

## ⚙️ How It Works

1. Users can register/login securely.
2. Logged-in users can:
   - 📝 Create new gadget blog posts
   - ✏️ Edit existing posts
   - 🗑️ Delete posts they created
3. All posts are saved in MongoDB Atlas.
4. The public homepage displays all user-contributed posts.
5. Auto-deployed to Vercel on every GitHub push.

---

## 🔧 Local Setup Instructions

1. Clone the repo:
  git clone https://github.com/yourusername/gadnexus.git
  cd gadnexus

2.Install Python dependencies:
  pip install flask pymongo dnspython

3. Set up environment variables (or hardcode in app.py):
  MONGO_URI → your MongoDB Atlas connection string
  SECRET_KEY → any secret string for session management

4. Run the flask app
  python app.py
  Then visit: http://localhost:5000

☁️ Deployment (Vercel)
Linked to GitHub repository

Automatically deploys on every commit

Add a vercel.json file to tell Vercel how to run Flask

No sleep time, fast, free-tier friendly

✅ Completed Functionality
 Register/Login system with sessions

 Create/Read/Update/Delete posts

 Cloud database using MongoDB Atlas

 Responsive blog-style UI

 Deploy to Vercel with vercel.json

 GitHub integration for auto-deploy
