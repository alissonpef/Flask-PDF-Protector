# AquaMark 💧

A robust Flask web application to add custom watermarks (text or image) to your PDF files, protecting your documents simply and efficiently.

## ✨ Key Features

- **Dual Watermark Types:** Choose between applying a custom text or an image (like a logo) as a watermark.
- **Full Style Control:** Customize the opacity, color, and font size (for text) to create the perfect protection.
- **Secure In-Memory Processing:** Uploads and handles files without temporarily saving them to the server's disk.
- **Interactive UI:** The form dynamically adapts to your choice of watermark type (text or image).
- **Direct Download:** Download the new, protected PDF file directly from the application after processing.

## 🛠️ Tech Stack

#### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

#### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

#### Code Quality

![Flake8](https://img.shields.io/badge/Flake8-4B8BBE?style=for-the-badge&logo=python&logoColor=white)

## ⚙️ How It Works (Technical Flow)

1.  **User Interface:** The user accesses the main page, which displays a dynamic form built with **Flask-WTF** for data validation and CSRF protection. JavaScript adapts the UI based on the chosen watermark type.
2.  **Data Submission:** The PDF file and its settings are sent via a `POST` request to the Flask server.
3.  **In-Memory Processing:** The `add_watermark` function uses **ReportLab** to generate a watermark PDF and **PyPDF2** to merge it with the original PDF. The entire process occurs in memory using `io.BytesIO`, ensuring performance and security by not writing files to disk.
4.  **Response & Download:** The application returns the modified PDF file directly in the HTTP response with a `Content-Disposition` header, triggering the download in the user's browser without saving the final file on the server.

## 🚀 Getting Started

### Local Setup (Recommended for Development)

**Prerequisites:**

- Python 3.8+

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/alissonpef/AquaMark.git](https://github.com/alissonpef/AquaMark.git)
    cd AquaMark
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    ```

    - On Windows (using Git Bash): `source env/Scripts/activate`
    - On macOS or Linux: `source env/bin/activate`

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    - Make a copy of the `.env.example` file and rename it to `.env`.
    - Open the `.env` file and add a long, random `SECRET_KEY`.
      ```
      SECRET_KEY='your-super-secret-and-long-key'
      ```
    - The `.flaskenv` file is already configured for the development environment.

5.  **Run the application:**

    ```bash
    flask run
    ```

6.  Access the application at **http://127.0.0.1:5000** in your browser.

## 📁 Project Structure

```
/
├── .env.example        # Environment variables template
├── .flaskenv           # Variables for the Flask CLI
├── .flake8             # Flake8 linter configuration
├── .gitignore          # Files ignored by Git
├── requirements.txt    # Python dependencies
├── api/                # Application source code
│   ├── __init__.py     # Makes the directory a Python package
│   ├── index.py        # Main logic and Flask routes
│   ├── forms.py        # Flask-WTF forms definitions
│   └── pdf_utils.py    # PDF manipulation logic
├── static/             # Static files (CSS, JS)
└── templates/          # HTML templates (Jinja2)
```

## lint Code Quality

This project uses **Flake8** to ensure a clean, readable, and consistent codebase, following Python community best practices. The configuration can be found in the `.flake8` file.

To check the code, run:

```bash
flake8 api
```

---

## 📫 Let's Connect!

I'd love to chat about backend development, Python, Flask, or other technologies. Feel free to reach out or connect with me on social media.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alisson-pereira-ferreira-45022623b/)
[![Gmail](https://img.shields.io/badge/Gmail-%23EA4335.svg?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alissonpef@gmail.com)

---

Made with ❤️ by **Alisson Pereira**.
