# 🌉 The Skill Bridge
> **Bridging the gap between the Township Economy and the 4th Industrial Revolution.**

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Platform](https://img.shields.io/badge/platform-Render-purple) ![Status](https://img.shields.io/badge/status-Open%20For%20Business-orange)

## 🌍 About The Project

**The Skill Bridge** is not just an EdTech platform; it is a digital infrastructure intervention designed for the South African context. We provide high-impact, short-form micro-courses aimed at digitizing the informal economy.

Our mission is to move youth from being **passive consumers** of technology to **active producers** of digital assets.

### 🚀 Key Features

*   **🤖 GenB (Generative Business Assistant):** An integrated AI tutor that translates complex tech concepts into localized, relatable South African context. GenB speaks the language of the user.
*   **🔐 Immutable Verification System:** A robust certificate validation engine. Every qualification issued generates a unique `TSB-XXXX` code that can be instantly verified by employers on our platform.
*   **📱 Mobile-First Architecture:** Designed for low-bandwidth environments and mobile devices.
*   **🛠 API-Ready:** Built as a scalable backend service ready for integration with third-party apps and bots.

---

## 📚 Course Modules (Beta)

1.  **Township Cyber Security:** Protecting digital assets and mobile money in the informal sector.
2.  **Urban Data Farming:** Monetizing local data and environment insights.

---

## 🛠 Tech Stack

*   **Backend:** Python (Django/Flask)
*   **Database:** PostgreSQL
*   **AI Engine:** OpenAI API (Customized System Prompting)
*   **Hosting:** Render (Cloud Native)
*   **Frontend:** HTML5 / CSS3 / JavaScript

---

## ⚙️ Installation & Setup (Local Development)

To run The Skill Bridge locally on your machine:

1.  **Clone the repo**
    ```bash
    git clone https://github.com/44Mage/skillbridge-backend.git
    cd skillbridge-backend
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a `.env` file and add your keys:
    ```env
    SECRET_KEY=your_secret_key
    OPENAI_API_KEY=your_openai_key
    DATABASE_URL=your_db_url
    ```

5.  **Run the server**
    ```bash
    python app.py
    # or
    python manage.py runserver
    ```

---

## 🔍 Verification Protocol

The Skill Bridge takes accreditation seriously. To test the verification logic:
1.  Navigate to the Chat/Verify interface.
2.  Enter a valid code (e.g., `TSB-DEMO-123`).
3.  The system queries the database and returns the Student Profile and Course Details.

---

## 🤝 Contributing

We welcome contributions from the community!
1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Rossman Walker Of Code**
*   *Architect of The Skill Bridge*
*   *Caretaker of GenB*

> "We are not just coding; we are future-proofing the hustle." 🇿🇦
