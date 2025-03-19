# Collab Backend Service

Collab's backend service is a **FastAPI-powered** system that streamlines **influencer-brand collaborations**, handling authentication, user management, campaign structuring, payments, and performance tracking.

## **Tech Stack**
- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Package Management**: Poetry
- **Authentication**: Google OAuth (Brands), Instagram OAuth (Influencers)
- **Deployment**: Docker (for PostgreSQL), DBeaver (for database management)

## **Setup & Installation**

### **1. Clone the Repository**
```bash
 git clone https://github.com/ameerasherin98/collab-be-svc.git
 cd collab-be-svc
```

### **2. Install Poetry**
If you haven't installed Poetry, install it with:
```bash
 curl -sSL https://install.python-poetry.org | python3 -
```

### **3. Install Dependencies**
```bash
 poetry install
```

### **4. Set Up Environment Variables**
Create a `.env` file and add:
```env
 GOOGLE_CLIENT_ID=your_google_client_id
 GOOGLE_CLIENT_SECRET=your_google_client_secret
 GOOGLE_REDIRECT_URI=your_redirect_uri
 DATABASE_URL=postgresql://user:password@localhost:5432/collab_db
```

### **5. Start the Server**
```bash
 poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
