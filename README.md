# 📚 Sutra-Atlas - Digital Learning Resource Management System (DL-RMS)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## 🚀 Live Demo

**Try Sutra-Atlas now:** [https://sutraatlas-production.up.railway.app](https://sutraatlas-production.up.railway.app)

*Experience the full functionality of our Digital Learning Resource Management System online!*

## 🌟 Overview

**Sutra-Atlas** is a comprehensive Digital Learning Resource Management System designed to help users organize, manage, and track their educational resources effectively. Built with Flask and modern web technologies, it provides an intuitive platform for managing learning materials with advanced search capabilities and progress tracking.

### ✨ Key Features

- 📁 **Collection Management** - Organize resources by subject, project, or category
- 📖 **Resource Tracking** - Store and manage books, articles, videos, and online materials
- 🏷️ **Status System** - Track progress with 4 status levels (Not Started, In Progress, Paused, Completed)
- 🔍 **Advanced Search** - Search and filter across collections and resources
- 👤 **User Authentication** - Secure login system with profile management
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🛡️ **Security Features** - Input validation, ownership protection, and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/d-sakshiway/sutraAtlas.git
   cd sutraAtlas
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   ```
   Navigate to: http://localhost:5000
   ```

## 📋 Usage Guide

### Getting Started

1. **Create an Account**
   - Click "Register" and create your account
   - Password requirements: 8+ characters, uppercase, lowercase, and numbers

2. **Create Your First Collection**
   - Navigate to Collections → "Create New Collection"
   - Add a descriptive name and optional description

3. **Add Resources**
   - Open a collection → "Add Resource"
   - Fill in title (required), authors, URL, and set status

4. **Track Progress**
   - Update resource status as you progress
   - Use search and filters to organize your learning

### Status System

| Status | Description | Use Case |
|--------|-------------|----------|
| 🔘 **Not Started** | Haven't begun this resource | Resources in your queue |
| 🔵 **In Progress** | Currently studying/reading | Active learning materials |
| 🟡 **Paused** | Temporarily stopped | Resources to resume later |
| 🟢 **Completed** | Finished studying | Completed learning materials |

## 🏗️ Technical Architecture

### Backend Stack

- **Framework**: Flask 2.0+
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: Flask-Login with secure password hashing
- **Validation**: Custom validation utilities with input sanitization
- **Security**: CSRF protection ready, input validation, ownership checks

### Frontend Stack

- **UI Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JS with modern features
- **Styling**: Custom CSS with dark mode support
- **Responsiveness**: Mobile-first responsive design

### Database Schema

```
User (1) ←→ (N) Collection (1) ←→ (N) Resource
```

- **Users**: Authentication, profiles, and preferences
- **Collections**: Organizational containers for resources
- **Resources**: Learning materials with metadata and progress tracking

## 🛡️ Security Features

- ✅ **Input Validation** - Server-side and client-side validation
- ✅ **Authentication Protection** - Login required for all user data
- ✅ **Ownership Validation** - Users can only access their own data
- ✅ **URL Manipulation Protection** - Prevents unauthorized access via URL
- ✅ **Error Handling** - Graceful error pages and user feedback
- ✅ **Password Security** - Hashed passwords with strength requirements

## 📁 Project Structure

```
sutraAtlas/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models
│   ├── utils.py                 # Validation utilities
│   ├── auth/                    # Authentication routes
│   ├── collections/             # Collection management
│   ├── resources/               # Resource management
│   ├── pages/                   # Page routes
│   ├── suggestions/             # Resource suggestions (API)
│   ├── static/                  # CSS, JS, images
│   └── templates/               # HTML templates
├── config.py                    # Application configuration
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                   # Project documentation
```

## 🎨 Features Showcase

### Collections Dashboard
- Create and organize collections by topic or project
- Search across all collections
- Sort by name or creation date

### Resource Management
- Add detailed metadata (title, authors, URLs)
- Track reading/learning progress
- Filter by status and search content

### User Experience
- **Responsive Design** - Works on all devices
- **Dark Mode** - Eye-friendly theme switching
- **Intuitive Navigation** - Clear breadcrumbs and navigation
- **Search & Filter** - Find resources quickly
- **Error Handling** - User-friendly error messages

## 🔮 Future Enhancements

The following features are planned for future releases:

- 📊 **Statistics Dashboard** - Progress analytics and learning insights (probable)
- 🔄 **Bulk Operations** - Mass edit and organize resources
- 📥 **Import/Export** - Data portability features
- 🔗 **Resource Suggestions** - Integrated book/article recommendations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Sakshi Verma** - [d-sakshiway](https://github.com/d-sakshiway)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap team for the responsive framework
- Font Awesome for beautiful icons
- Open Library API for resource suggestions

---

<div align="center">

**⭐ If you find Sutra-Atlas helpful, please consider giving it a star! ⭐**

Made with ❤️ by [Sakshi Verma](https://github.com/d-sakshiway)

</div>