# PeerDrop

**PeerDrop** is a secure, encrypted file sharing web application built with Flask, SQLAlchemy, and IPFS.  
It allows users to upload, encrypt, share, and download files with strong privacy and integrity guarantees.

---

## Features

- **User Registration & Authentication** (JWT-based)
- **File Upload & Download** with end-to-end encryption (Fernet/AES)
- **IPFS Integration** for decentralized file storage
- **Integrity Checking** (SHA-256 hash verification)
- **File Sharing** with user-level permissions (read/write)
- **RESTful API** with OpenAPI/Swagger documentation

---

## Requirements

- Python 3.12+
- **IPFS Desktop** or a running IPFS node (default: `localhost:5001`)
- SQLite (default) or other SQLAlchemy-supported DB
- (Optional) Docker for containerized deployment

---

## Installation

1. **Clone the repository:**
```
git clone https://github.com/yourusername/peerdrop.git
cd peerdrop
```
2. **Create and activate a virtual environment:**
```
python3 -m venv .venv
source .venv/bin/activate
```
3. **Install dependencies:**
```
pip install -r requirements.txt
```
4. **Set up the database:**
```
flask db upgrade
```
5. **Run IPFS Desktop** (or ensure your IPFS node is running on `localhost:5001`).
6. **Start the app:**
```
python run.py
```
The app will be available at http://localhost:5000

---

## API Documentation

- Swagger/OpenAPI docs available at:  
    http://localhost:5000/swagger-ui

---

## Usage

- **Register** a new user via `/auth/register`
- **Login** to receive a JWT token via `/auth/login`
- **Upload** files via `/files/upload` (requires JWT)
- **Download** files via `/files/<file_id>` (requires JWT and permission)
- **Share** files with other users via `/files/share` (requires JWT and ownership)

---

## Configuration

Edit `config.py` to change:

- Database location
- JWT secret and expiry
- Upload folder
- API settings

---

## Security

- Files are encrypted before upload using Fernet symmetric encryption.
- Encryption keys are stored securely in the database.
- File integrity is verified on download using SHA-256 hashes.
- Only authorized users can access or share files.

---

## License

MIT License

---


**Feel free to contribute or open issues!**
