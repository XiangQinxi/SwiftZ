# 📦 SwiftZ

**Temporary File Exchange Station** | [Visit Online](https://swiftz.streamlit.app/)

> The original project `Packages` has been discontinued. This project is its successor.

---

## About This Project

The first part of this project was developed by me, while the file retrieval functionality was developed with assistance from `ChatGPT 5.4` and `MiniMax 2.6`. The original content was somewhat limited, so I asked the AI to add more details.

## 🔥 Introduction

SwiftZ is a lightweight temporary file hosting tool built on **Streamlit**, running on the Streamlit Cloud platform.

Think of it as a "**simple temporary cloud drive**":
- Upload multiple files at once, packaged as ZIP
- Optional password protection (encrypted storage)
- Generate a unique "Query ID"
- Share the ID (and password) with others to download the original files

**Use Cases**:
- Temporarily share files with friends or colleagues
- Share resource collections (e.g., course notes, material packs)
- Quickly transfer large files (without WeChat/email limitations)
- Publicly share your resources (can be set to public)

> ⚠️ **Note**: This project is deployed on Streamlit Cloud, which has a sleep mechanism. If the site has no visitors for an extended period, data may be reset. **Please do not use SwiftZ as a long-term cloud storage or for sensitive data.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| Multi-file Upload | Upload multiple files at once, automatically packaged as ZIP |
| Optional Password | Choose whether to set an extraction password |
| Encrypted Storage | Use AES-256 encrypted ZIP when password is set |
| Public Sharing | Set file packages as public, displayed on the homepage |
| User System | Support registration and login, manage your uploaded files |
| Admin Panel | Administrators can manage users and all file packages |

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Data Storage**: YAML files + local ZIP packages
- **Encryption**: pyzipper (AES-256)
- **Deployment**: Streamlit Cloud

---

## 📦 Local Setup

```bash
# 1. Clone the project
git clone https://github.com/XiangQinxi/SwiftZ.git
cd SwiftZ

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run main.py
```

---

## 📄 License

MIT License · Open source and contributions welcome 🎉