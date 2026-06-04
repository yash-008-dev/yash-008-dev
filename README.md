# 🧠 NeuroLearn AI

NeuroLearn AI is an open-source, full-stack learning platform designed to ingest unstructured PDF documents (textbooks, research papers, study notes) and automatically synthesize them into dynamic, interactive study guides. The system features real-time progress updates, visual concept relationship mapping, active recall assessments, and a context-aware chat assistant grounded in your documents.

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_NeuroLearn-success?style=for-the-badge)](https://neurolearn-ai.vercel.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/your-username/NeuroLearn-AI)

[![Next.js Version](https://img.shields.io/badge/Next.js-16.2.6-000000?style=flat&logo=nextdotjs)](https://nextjs.org/)
[![React Version](https://img.shields.io/badge/React-19.2.5-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3.0-06B6D4?style=flat&logo=tailwindcss)](https://tailwindcss.com/)
[![Prisma ORM](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=flat&logo=prisma)](https://www.prisma.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Enabled-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Gemini API](https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?style=flat&logo=googlegemini)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)

---

## 📖 Project Overview

NeuroLearn AI transforms unstructured educational PDFs into highly structured study materials. The platform processes documents via a dual-layered Next.js and FastAPI ingestion pipeline, leverages Google Gemini API for semantic synthesis and quiz generation, and builds an interactive 2D visualization graph of the extracted concepts.

---

## ✨ Key Features

- **Document Ingestion Pipeline**: Processes PDF uploads (up to 20MB) with local extraction fallbacks. Streams progress real-time from the backend to the UI via Server-Sent Events (SSE).
- **Multi-Strategy Text Extraction**: Employs standard in-app text parsing (`pdf-parse`) and routes scanned or image-heavy documents to a Python FastAPI service using `PyMuPDF`, `pdfplumber`, and `Tesseract OCR`.
- **AI-Powered Synthesizer**: Uses `gemini-2.0-flash` to generate detailed summaries, TLDRs, project objectives, key findings, chapter-by-chapter breakdowns, advantages, limitations, and future scope.
- **Dynamic 2D Knowledge Maps**: Generates coordinates to map out relationships between concepts, technologies, system architectures, workflows, and future scopes.
- **Smart Study Notes**: Automatically populates note databases containing concept cards, definition indexes, system architecture descriptions, and exam-oriented revision notes.
- **Active Recall Quizzes**: Creates test questions spanning 8 formats (MCQs with explanations for wrong answers, Fill-in-the-Blank, True/False, Match, Short Answer, Scenarios, and Applications).
- **Grounded Chat Assistant**: Context-aware floating assistant allowing you to chat directly with your document libraries. It feeds summaries and user-generated notes into the context window.
- **Study Analytics & Progress Telemetry**: Tracks active focus hours, mastered concepts, quizzes taken, and logs study history sessions.

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Knowledge Map
![Knowledge Map](docs/screenshots/knowledge-map.png)

### Quiz Generator
![Quiz Generator](docs/screenshots/quiz-generator.png)

---

## 📊 System Architecture & Workflow

### System Architecture Diagram
The flowchart below outlines the request lifecycle from the client interface, passing through authentication, the API routing layer, down to the database, AI model service, and visualization engine.

```mermaid
flowchart TD
    User([User Client]) -->|Interacts with UI| FE[Frontend: Next.js 16 + React 19]
    FE -->|Requests / Submissions| Auth{Authentication Gateway\nNextAuth.js / Google OAuth}
    Auth -->|Authorized Session| API[API Routing Layer: Next.js API Routes]
    Auth -->|Session Denied| Login[Auth Login Interface]
    API -->|Rate Limits & CSRF Validated| CSRF{RateLimiter & CSRF check}
    CSRF -->|Failed| Blocked[403 / 429 Error Response]
    CSRF -->|Passed| AI_Engine[NeuroLearn AI Ingestion Engine]
    AI_Engine -->|Extract Document Text| PY_Service[FastAPI OCR / PyMuPDF Server]
    AI_Engine -->|Prisma Queries| Prisma[Prisma Client]
    Prisma -->|Read / Write Data| DB[(PostgreSQL Database)]
    AI_Engine -->|Generate Summary & Quiz JSON| Gemini[Google Gemini API: gemini-2.0-flash]
    Gemini -->|Return Semantic JSON Schema| AI_Engine
    AI_Engine -->|Generate D3 Coordinates| Map_Gen[Knowledge Map Generator]
    Map_Gen -->|Calculate Spatial Node Coordinates| D3[D3.js Coordinate Node Engine]
    D3 -->|Stream Visual Telemetry| FE
```

### Document Processing Ingestion Pipeline
This flowchart details how uploaded documents are processed and saved, including the fallbacks and SSE message logs.

```mermaid
flowchart TD
    Upload[PDF Document Upload\nValidation <= 20MB] --> Status_Log[Write Status: 'Uploading']
    Status_Log --> PDF_Parse[Attempt Fast In-App Text Parse\npdf-parse library]
    PDF_Parse --> Check_Text{Was sufficient\ntext extracted?}
    Check_Text -->|Yes| Clean[Clean Text & Remove Control Chars]
    Check_Text -->|No| Python_Parser[Call FastAPI Python Service]
    Python_Parser --> PyMuPDF[PyMuPDF fast parsing]
    PyMuPDF --> Check_PyMuPDF{Text length >= 50?}
    Check_PyMuPDF -->|Yes| Clean
    Check_PyMuPDF -->|No| PDFPlumber[pdfplumber fallback]
    PDFPlumber --> Check_Plumber{Text length >= 50?}
    Check_Plumber -->|Yes| Clean
    Check_Plumber -->|No| OCR[Tesseract OCR scanned-page fallback]
    OCR --> Clean
    Clean --> Chunk[Chunk Text Semantically]
    Chunk --> Status_Processing[Write Status: 'Processing']
    Status_Processing --> AI_Scribe[Gemini AI Synthesis\ngemini-2.0-flash]
    AI_Scribe --> Summary_Gen[Summary Table populated\nExecutive Brief, TLDR, Chapters]
    Summary_Gen --> Note_Pop[Notes Table populated\nConcepts, Definitions, Tech Stack]
    Note_Pop --> Quiz_Gen[Quiz Table populated\n8 Question Types MCQ, TF, Scenario]
    Quiz_Gen --> KMap_Gen[KnowledgeMap Table populated\nCalculated X/Y Node Coordinates]
    KMap_Gen --> Complete[Write Status: 'Completed']
    Complete --> SSE[Stream final event payload to User via SSE]
```

---

## 📁 Project Structure

```text
├── prisma/
│   ├── migrations/               # Database SQL schema migration history
│   └── schema.prisma             # PostgreSQL schema models definitions
├── server/                       # FastAPI document microservice
│   ├── main.py                   # FastAPI service endpoints (PyMuPDF, pdfplumber, pytesseract)
│   ├── requirements.txt          # Python package requirements
│   └── Dockerfile                # Docker build configuration for Python service
├── src/                          # Next.js application source
│   ├── app/                      # App Router layouts, views, and REST API endpoints
│   ├── components/               # UI components (Floating Assistant orb, Background canvas, Navigation docks)
│   │   ├── Assistant/            # Floating interactive AI assistant
│   │   ├── Background/           # Immersive canvas-drawn neural connection background
│   │   ├── Layout/               # Page wrapper layouts
│   │   ├── Navigation/           # Glassmorphic QuantumDock and TopNavbar navigation
│   │   └── Workspace/            # Ingestion upload areas and progress indicators
│   └── lib/                      # Business logic utilities
│       ├── ai-engine.ts          # Core AI coordinator (Gemini API & local NLP fallback)
│       ├── db.ts                 # Prisma client instance
│       ├── auth.ts               # NextAuth setup supporting Credentials & Google OAuth callbacks
│       ├── csrf.ts               # Timing-safe CSRF validation middleware
│       ├── rate-limit.ts         # Sliding-window rate limiter
│       └── knowledge-map-generator.ts # D3 node positioning coordinator
```

---

## 🔌 API Summary

| Endpoint | Method | Authentication | Description |
| :--- | :--- | :--- | :--- |
| `/api/auth/[signup/forgot-password...]`| `POST` | Public | Handles signup, password-reset, and email validations. |
| `/api/upload` | `POST` | User | Ingests PDF document and streams status events via SSE. |
| `/api/chat` | `POST` | User | Context-aware chat grounded in your uploaded documents and notes. |
| `/api/documents` | `GET`/`DELETE` | User | Lists and deletes document records. |
| `/api/documents/[id]` | `GET`/`POST`/`PATCH` | User | Fetches details, reprocesses parser texts, or edits metadata. |
| `/api/notes` | `GET`/`POST`/`PUT`/`DELETE`| User | CRUD actions for study notes. |
| `/api/quizzes` | `GET`/`POST` | User | Lists quizzes and updates telemetry scores. |
| `/api/knowledge-map` | `GET` | User | Fetches calculated X/Y node coordinate arrays. |
| `/api/analytics` | `GET` | User | Aggregates focus duration, efficiency, and diagnosis. |
| `/api/preferences` | `GET`/`PUT` | User | Configures client-side dashboard styling parameters. |

---

## 🛠️ Local Development & Setup

### Prerequisites
- **Node.js 20+**
- **Python 3.10+** (if running document service locally)
- **Tesseract OCR** (installed and added to path if utilizing local OCR)
- **PostgreSQL** database (or docker running postgres)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/NeuroLearn-AI.git
cd NeuroLearn-AI
```

### 2. Install Dependencies
```bash
# Install Next.js frontend dependencies
npm install

# Install FastAPI document service dependencies
cd server
pip install -r requirements.txt
cd ..
```

### 3. Configure the Environment
Copy the example environment template and configure your values:
```bash
cp .env.example .env
```
Ensure you update the `DATABASE_URL` and `GOOGLE_API_KEY` (Gemini API key).

### 4. Database Setup & Migrations
Sync your PostgreSQL database schema with Prisma:
```bash
npx prisma db push
npx prisma generate
```

### 5. Running the Application Locally

#### Terminal 1: Run Next.js App
```bash
npm run dev
```
The Next.js app will be accessible at `http://localhost:3000`.

#### Terminal 2: Run FastAPI Document Service
```bash
cd server
python main.py
```
The document extraction service will run at `http://localhost:8000`.

---

## 🐳 Running with Docker Compose

NeuroLearn AI can be orchestrated with a single command using Docker Compose:

```bash
docker-compose up --build
```
This command starts three containers:
- **`neurolearn-db`**: PostgreSQL 16 database mapping port `5432`
- **`neurolearn-app`**: Next.js Node app mapping port `3000`
- **`neurolearn-fastapi`**: Python document extractor mapping port `8000`

---

## 🛠️ Environment Configuration Matrix

| Environment Variable | Description | Default / Example Value |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL database connection string | `postgresql://neurolearn:password@postgres:5432/neurolearn` |
| `NEXTAUTH_URL` | Application root URL for NextAuth session callbacks | `http://localhost:3000` |
| `NEXTAUTH_SECRET` | Secret key for encrypting JWT tokens | `generate-using-openssl-rand` |
| `GOOGLE_CLIENT_ID` | Client identifier for Google OAuth login | `google-oauth-client-id` |
| `GOOGLE_CLIENT_SECRET`| Client secret for Google OAuth authentication | `google-oauth-client-secret` |
| `GOOGLE_API_KEY` | Google Gemini API Studio key (Flash calls) | `AIzaSy...` |
| `NEXT_PUBLIC_AI_SERVICE_URL`| Browser endpoint redirecting to FastAPI | `http://127.0.0.1:8000` |
| `FASTAPI_URL` | Server-to-server endpoint for Next.js to FastAPI | `http://127.0.0.1:8000` |
| `SMTP_HOST` | Outgoing SMTP mail server host for password resets | `smtp.ethereal.email` |
| `SMTP_PORT` | Outgoing SMTP mail port | `587` |
| `SMTP_SECURE` | Set to true if utilizing SSL for mail connections | `false` |
| `SMTP_USER` | SMTP server username | `smtp-user-email` |
| `SMTP_PASS` | SMTP server password | `smtp-user-password` |
| `SMTP_FROM` | Default sender display email | `noreply@neurolearn.ai` |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<p align="center">
  <span>© 2026 NeuroLearn AI. Syncing telemetry and enhancing active recall.</span>
</p>
