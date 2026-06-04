# NeuroLearn AI

NeuroLearn AI is an open-source, full-stack learning platform designed to ingest unstructured PDF documents (textbooks, research papers, study notes) and automatically synthesize them into structured study guides. The system features real-time progress updates, visual concept relationship mapping, active recall assessments, and a context-aware chat assistant grounded in your documents.

[![Website](https://img.shields.io/badge/Website-NeuroLearn-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://neurolearn-ai.vercel.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/asc006-git/NeuroLearn)
[![Next.js](https://img.shields.io/badge/Next.js-16.2.6-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2.5-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Prisma](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=for-the-badge&logo=prisma&logoColor=white)](https://www.prisma.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Enabled-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

---

## Project Overview

NeuroLearn AI transforms educational PDFs into study materials. The platform processes documents via a dual-layered Next.js and FastAPI ingestion pipeline, leverages Google Gemini API for semantic synthesis and quiz generation, and builds an interactive 2D visualization graph of the extracted concepts.

---

## Features

- **PDF Upload & Processing**: Supports file sizes up to 20MB. Automatically attempts fast local parsing, falling back to Python-based extraction and Tesseract OCR for scanned documents.
- **AI Summaries**: Synthesizes structured summaries highlighting objectives, key findings, and methodologies.
- **Smart Notes**: Generates concept cards, revision guides, and terminology definitions based on document content.
- **Quiz Generation**: Creates multiple-choice, fill-in-the-blank, true/false, match, and scenario-based active recall questions.
- **Knowledge Maps**: Connects topics and key entities into a coordinate-mapped visual relationship graph.
- **AI Chat**: Floating chat assistant grounded in the summaries and smart notes of your uploaded documents.
- **Authentication**: Secure registration and sessions powered by NextAuth credentials and optional Google OAuth.

---

## Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Knowledge Map
![Knowledge Map](docs/screenshots/knowledge-map.png)

### Quiz Generator
![Quiz Generator](docs/screenshots/quiz-generator.png)

---

## System Diagrams

### 1. System Architecture
```mermaid
flowchart LR
    Client[User Client] -->|React 19 / UI| App[Next.js App Server]
    App -->|NextAuth| Auth{Auth Check}
    Auth -->|REST API| Endpoints[API Endpoints]
    Endpoints -->|Local Parse| PDFParse[pdf-parse]
    Endpoints -->|OCR / Parser| FastAPI[FastAPI Server]
    Endpoints -->|Gemini API| Gemini[Gemini-2.0-Flash]
    Endpoints -->|Prisma Client| PostgreSQL[(PostgreSQL DB)]
    Endpoints -->|D3 coordinates| KMap[Knowledge Map Generator]
```

### 2. Document Processing Ingestion Pipeline
```mermaid
flowchart LR
    Upload[PDF Ingest] --> InApp{In-App Parse?}
    InApp -->|Success| Clean[Text Cleaning]
    InApp -->|Failed| FastAPI[FastAPI OCR/Parse]
    FastAPI --> Clean
    Clean --> AI[Gemini Flash Synthesis]
    AI --> Summary[Generate Summary]
    AI --> Notes[Generate Smart Notes]
    AI --> Quiz[Generate Active Recall Quiz]
    AI --> KMap[Generate Knowledge Map]
    KMap --> DB[(Save to DB)]
    DB --> SSE[Stream SSE Done]
```

---

## Project Structure

- **`prisma/`**: PostgreSQL schema definitions and database migrations.
- **`server/`**: Python FastAPI document parsing and Tesseract OCR service.
- **`src/app/`**: Next.js App Router layouts, page views, and API endpoint routes.
- **`src/components/`**: Reusable UI modules (AI Assistant orb, canvas neural background, QuantumDock navigation).
- **`src/lib/`**: Core logic utilities (Gemini integration, CSRF middleware, rate limiting, knowledge map coordinate generator).

---

## Tech Stack

- **Frontend**: Next.js 16.2.6 (App Router), React 19.2.5, Tailwind CSS 4.3.0, Framer Motion 12.38.0
- **Visualizations**: D3.js 7.9.0, Recharts 3.8.1
- **Database & ORM**: PostgreSQL, Prisma ORM 5.22.0
- **Authentication**: NextAuth.js 4.24.14
- **AI Core**: Google Gemini API (`gemini-2.0-flash` endpoint)
- **Document Processing**: FastAPI, PyMuPDF, pdfplumber, pytesseract, pdf-parse

---

## Local Development Setup

### Prerequisites
- **Node.js 20+**
- **Python 3.10+** (if running the document service locally)
- **Tesseract OCR** (installed and added to your system path if utilizing local OCR)
- **PostgreSQL** database instance

### 1. Clone the Repository
```bash
git clone https://github.com/asc006-git/NeuroLearn.git
cd NeuroLearn
```

### 2. Install Dependencies
```bash
# Install frontend dependencies
npm install

# Install FastAPI dependencies
cd server
pip install -r requirements.txt
cd ..
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/neurolearn"
NEXTAUTH_SECRET="your-32-character-session-secret"
GOOGLE_API_KEY="your-gemini-api-key"
NEXT_PUBLIC_AI_SERVICE_URL="http://127.0.0.1:8000"
FASTAPI_URL="http://127.0.0.1:8000"
```

### 4. Database Setup
Run migrations to set up your PostgreSQL tables:
```bash
npx prisma db push
npx prisma generate
```

### 5. Running the Application

#### Terminal 1: Run Next.js Server
```bash
npm run dev
```
Accessible at `http://localhost:3000`.

#### Terminal 2: Run FastAPI Server
```bash
cd server
python main.py
```
Accessible at `http://localhost:8000`.

---

## Docker Compose Setup (Optional)

Alternatively, run the entire stack (Next.js, FastAPI, and PostgreSQL database) using Docker Compose:

```bash
docker-compose up --build
```
Containers started:
- **`neurolearn-db`**: PostgreSQL 16 database running on port `5432`
- **`neurolearn-app`**: Next.js application running on port `3000`
- **`neurolearn-fastapi`**: Python document extractor running on port `8000`

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---
Developed by **Adhyatma Singh Chauhan**

GitHub: [asc006-git](https://github.com/asc006-git)
