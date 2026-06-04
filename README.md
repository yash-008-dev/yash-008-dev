# NeuroLearn AI

NeuroLearn AI is an open-source web application designed to help users ingest PDF documents and automatically synthesize them into structured study aids, active recall assessments, and visual relationship maps.

[![Website](https://img.shields.io/badge/Website-NeuroLearn-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://neurolearn-ai.vercel.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/asc006-git/NeuroLearn)
[![Next.js](https://img.shields.io/badge/Next.js-16.2.6-000000?style=flat&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2.5-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3.0-06B6D4?style=flat&logo=tailwindcss)](https://tailwindcss.com/)
[![Prisma](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=flat&logo=prisma)](https://www.prisma.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Enabled-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

---

## Project Overview

NeuroLearn AI parses uploaded educational files, extracts and cleans text content, and uses the Google Gemini API to structure information. It generates summaries, smart revision notes, and quiz questions, visualizing the conceptual structure with a dynamic D3 coordinate map.

---

## Features

- **PDF Upload & Processing**: Support for PDFs up to 20MB, utilizing local text extraction with OCR fallback for scanned materials.
- **AI Generated Summaries**: In-depth analysis of document concepts, key takeaways, chapter-by-chapter breakdowns, advantages, and limitations.
- **Smart Notes**: Auto-generates categorised note cards for definitions, technical stacks, methodologies, and concepts.
- **Quiz Generation**: Produces active recall testing across multiple question formats (MCQ, Fill-in-the-Blank, Scenario, Application, True/False).
- **Knowledge Maps**: Visually structures related entities and topics onto an interactive 2D node map.
- **AI Chat**: Floating document-grounded chatbot referencing uploaded files and user notes.
- **Authentication**: User profiles and authentication sessions managed securely via NextAuth.
- **Analytics Dashboard**: Tracks study sessions, mastered concepts, active focus time, and logs historical activity.

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

### System Architecture
```mermaid
flowchart LR
    Client[User Client] --> App[Next.js App Server]
    App --> Auth{NextAuth / OAuth}
    Auth --> API[API Endpoints]
    API --> Parsers[Local Parser & FastAPI OCR]
    API --> Gemini[Gemini API]
    API --> DB[(PostgreSQL Database)]
    API --> Visual[D3 Knowledge Map]
```

### Document Ingestion Pipeline
```mermaid
flowchart LR
    Upload[Upload PDF] --> Parse{Extract Text}
    Parse -->|pdf-parse| Clean[Clean & Chunk]
    Parse -->|FastAPI OCR| Clean
    Clean --> Gemini[Gemini Flash API]
    Gemini --> Save[Populate Tables]
    Save --> DB[(PostgreSQL)]
    Save --> SSE[Stream Progress via SSE]
```

---

## Tech Stack

- **Frontend**: Next.js 16.2.6, React 19.2.5, Tailwind CSS 4.3.0, Framer Motion 12.38.0
- **Backend & Document Parser**: FastAPI, pdf-parse, PyMuPDF, pdfplumber, Tesseract OCR
- **Database & ORM**: PostgreSQL, Prisma ORM 5.22.0
- **AI Integration**: Google Gemini API (`gemini-2.0-flash`)
- **Authentication**: NextAuth.js 4.24.14
- **Infrastructure**: Docker, Docker Compose

---

## Project Structure

- **`prisma/`**: Database schema declarations and migrations.
- **`server/`**: Python FastAPI OCR and document parsing server.
- **`src/app/`**: Next.js App Router (pages and API endpoints).
- **`src/components/`**: Reusable frontend components (Assistant, Background, QuantumDock).
- **`src/lib/`**: Core helpers, NextAuth configuration, CSRF middleware, and rate limiters.

---

## Local Development Setup

### Prerequisites
- Node.js 20+
- Python 3.10+
- Tesseract OCR (if using local OCR fallback)
- PostgreSQL database instance

### 1. Clone the Repository
```bash
git clone https://github.com/asc006-git/NeuroLearn.git
cd NeuroLearn
```

### 2. Install Dependencies
```bash
# Install Next.js frontend dependencies
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
```bash
npx prisma db push
npx prisma generate
```

### 5. Running the Servers Locally

#### Terminal 1: Next.js Frontend
```bash
npm run dev
```
Accessible at `http://localhost:3000`.

#### Terminal 2: FastAPI Document Service
```bash
cd server
python main.py
```
Accessible at `http://localhost:8000`.

---

## Docker Compose Setup (Optional)

Run the entire application stack including Next.js, FastAPI, and PostgreSQL database:

```bash
docker-compose up --build
```
Containers configured:
- **`neurolearn-db`**: PostgreSQL 16 database mapping port `5432`
- **`neurolearn-app`**: Next.js application mapping port `3000`
- **`neurolearn-fastapi`**: Python document extractor mapping port `8000`

---

## Security Features

- **CSRF Token Validation**: Timing-safe CSRF cookie validations protect all mutating request endpoints.
- **API Rate Limiting**: In-memory rate limiting applies request caps to document uploads and AI chat exchanges.
- **Input Sanitization**: Client requests are parsed and sanitized via Zod schemas to block XSS injections.
- **Bcrypt Password Hashing**: Hashing algorithm encrypts password strings before saving them to the database.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Author

**Adhyatma Singh Chauhan**

GitHub: [asc006-git](https://github.com/asc006-git)
