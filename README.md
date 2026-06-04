# 🧠 NeuroLearn AI

> Cinematic AI-Powered Document Comprehension & Active Recall Learning System

[![Next.js](https://img.shields.io/badge/Next.js-16.2.6-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2.5-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Prisma](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=for-the-badge&logo=prisma&logoColor=white)](https://www.prisma.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

NeuroLearn AI is a production-grade, highly immersive educational assistant designed to ingest unstructured PDF documents (textbooks, research papers, project reports) and synthesize them into structured study aids. Utilizing a hybrid processing model, the system leverages Google Gemini AI models for generation, backed by a FastAPI document extraction microservice, and features a cinematic, dark-themed dashboard built on Next.js 16, React 19, and Tailwind CSS 4.0.

---

---

## 🛠️ Tech Stack & Architecture

- **Frontend Core**: Next.js 16 (using App Router and Turbopack compiler) & React 19
- **Design System**: Vanilla CSS with Tailwind CSS 4.0 (leveraging the `@theme` directive, custom `@layer base` Saturn-inspired variables, and Framer Motion 12.0 for cinematic spring transitions)
- **Data Visualizations**: Recharts & D3.js (used to construct the interactive 2D spatial knowledge coordinate system)
- **Primary Database**: PostgreSQL hosted on Neon DB, managed via Prisma ORM
- **Authentication**: NextAuth.js (configured with Credentials + Google OAuth providers)
- **AI Core**: Google Gemini API (`gemini-2.0-flash` endpoint) + Python FastAPI microservice (housing PyMuPDF, pdfplumber, and Tesseract OCR)
- **Security Protocols**: Timing-safe CSRF cookie validations, in-memory sliding window rate-limiters, and Zod input sanitization

---

## 📊 System Diagrams

### 1. System Architecture Flowchart
This diagram outlines the request lifecycle from the client dashboard, passing through the secure NextAuth gateway, down to the database layers, AI processors, and D3 analytics engine.

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
    Prisma -->|Read / Write Data| DB[(Neon PostgreSQL Database)]
    AI_Engine -->|Generate Summary & Quiz JSON| Gemini[Google Gemini API: gemini-2.0-flash]
    Gemini -->|Return Semantic JSON Schema| AI_Engine
    AI_Engine -->|Generate D3 Coordinates| Map_Gen[Knowledge Map Generator]
    Map_Gen -->|Calculate Spatial Node Coordinates| D3[D3.js Node Engine]
    D3 -->|Stream Visual Telemetry| FE
```

### 2. Document Processing & Ingestion Pipeline
This diagram traces the lifecycle of a document from file upload validation down to real-time status emissions via SSE streams, database writes, and visual analytics.

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

## 📁 Project Folder Structure

```text
├── .env                          # Local configuration and secret keys
├── .env.example                  # Template listing required environment variables
├── Dockerfile                    # Multi-stage production container build for the Next.js app
├── docker-compose.yml            # Services orchestration (Next.js, FastAPI, PostgreSQL)
├── package.json                  # Next.js configurations, tasks, and NPM dependencies
├── tsconfig.json                 # TypeScript compiler configuration
├── next.config.js                # Next.js configuration containing Webpack modifications
├── prisma/
│   ├── migrations/               # Database SQL schema updates history
│   └── schema.prisma             # PostgreSQL schema models (User, Document, Summary, Note, Quiz, etc.)
├── server/                       # FastAPI microservice for raw document extraction & OCR
│   ├── main.py                   # FastAPI service endpoints (PyMuPDF, pdfplumber, pytesseract)
│   ├── requirements.txt          # Python packages (fastapi, PyMuPDF, pdfplumber, pytesseract, uvicorn)
│   └── Dockerfile                # Docker build configuration for Python service
├── public/                       # Static public assets served directly
├── src/                          # Next.js application source root
│   ├── app/                      # Next.js 16 app Router folder
│   │   ├── (dashboard)/          # Grouped authenticated views
│   │   │   ├── analytics/        # Cognitive telemetry and study statistics page
│   │   │   ├── dashboard/        # Main hub showing upload areas and recently studied material
│   │   │   ├── documents/        # Detailed document review, editing, and reprocessing layout
│   │   │   ├── quiz-lab/         # Interactive testing studio for active recall quizing
│   │   │   ├── smart-notes/      # Dynamic concept cards, definition indexes, and revision sheets
│   │   │   ├── summaries/        # Detailed executive briefs, methodologies, and findings view
│   │   │   └── settings/         # Custom app settings (accent colors, light/dark mode, notifications)
│   │   ├── api/                  # Backend REST API routes
│   │   │   ├── auth/             # Session, signup, password-reset, and email verification endpoints
│   │   │   ├── upload/           # Core ingestion endpoint streaming real-time pipeline status via SSE
│   │   │   ├── chat/             # Context-aware chat endpoint using uploaded PDFs as dynamic grounding
│   │   │   └── [notes/quizzes...] # CRUD API endpoints for notes, quizzes, and telemetry
│   │   ├── auth/                 # Frontend signin, register, and reset screens
│   │   ├── layout.tsx            # Global application root layout
│   │   └── providers.tsx         # NextAuth SessionProvider wrappers
│   ├── components/               # Custom modular visual elements
│   │   ├── Assistant/            # Floating interactive AI orb supporting drag/drop and chat
│   │   ├── Background/           # Immersive canvas-drawn neural connection background
│   │   ├── Layout/               # Page wrapper layouts
│   │   ├── Navigation/           # Glassmorphic QuantumDock and TopNavbar command bars
│   │   └── Workspace/            # Ingestion drop-zones and progress loading indicators
│   ├── lib/                      # Common library logic
│   │   ├── ai-engine.ts          # AI manager. Directs Gemini Flash API or coordinates local NLP fallbacks
│   │   ├── db.ts                 # Prisma Client initializer
│   │   ├── auth.ts               # NextAuth setup supporting credentials and OAuth callbacks
│   │   ├── csrf.ts               # Timing-safe CSRF validation wrapper
│   │   ├── rate-limit.ts         # Sliding-window rate limiter utilizing in-memory Maps
│   │   └── knowledge-map-generator.ts # D3 node positioning generator for knowledge visualization
│   └── index.css                 # Custom font injections and layout utility wrappers (neural-glass)
```

---

## 💾 Database Schema Overview

The database models are designed to store hierarchical learning states linked to an authenticated user:

| Model | Primary Fields | Relations / Purpose |
| :--- | :--- | :--- |
| **User** | `id`, `name`, `email`, `hashedPassword`, `image`, `authProvider` | Central account profile. Links user data. |
| **Account** | `id`, `userId`, `type`, `provider`, `providerAccountId`, `refresh_token` | Links third-party login providers (e.g. Google OAuth). |
| **Session** | `id`, `sessionToken`, `userId`, `expires` | Handles user authentication sessions. |
| **Document** | `id`, `userId`, `title`, `fileUrl`, `fileData`, `processingStatus` | Uploaded PDFs (raw binary fileData stored for standalone reprocessing). |
| **Extraction**| `id`, `documentId`, `text` | Cleaned full text extracted from the document. |
| **Summary** | `id`, `documentId`, `executiveBrief`, `concepts`, `formulas`, `techStack`| Comprehensive AI-generated analysis of the document. |
| **Quiz** | `id`, `summaryId`, `questions` (JSON), `difficulty`, `score` | Active recall assessment cards linked to a summary. |
| **Note** | `id`, `userId`, `summaryId`, `title`, `content`, `type`, `pinned` | Concept, definition, or revision notes. |
| **KnowledgeMap**| `id`, `userId`, `topic`, `category`, `points`, `connections`, `x`, `y`| Nodes in the 2D coordinate network. |
| **Analytics** | `id`, `userId`, `studyMinutes`, `cognitiveScore`, `quizzesTaken`, `date`| Focus telemetry metrics over time. |
| **UserPreferences**| `id`, `userId`, `intensity`, `adaptive`, `dark`, `accentColor` | Configures client-side dashboard styling. |
| **LearningSession**| `id`, `userId`, `title`, `type`, `duration`, `score` | Historical log tracking study activities. |

---

## 🔌 API Endpoints Table

All API endpoints are protected using NextAuth session checks. Mutating endpoints validate CSRF tokens.

### Authentication & Profile
| Method | Endpoint | Description | Request/Response Payload |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/signup` | Registers a new credentials user. | `{ email, password, name }` → `{ success: true }` |
| `POST` | `/api/auth/forgot-password`| Sends a password reset token via email. | `{ email }` → `{ success: true }` |
| `POST` | `/api/auth/reset-password` | Resets user password using reset token. | `{ token, password }` → `{ success: true }` |
| `GET` | `/api/profile` | Fetches active user profile metrics. | Returns User data, sessions, preferences. |
| `PATCH`| `/api/profile` | Updates profile name or image URL. | `{ name, image }` → Updated user object. |
| `DELETE`| `/api/profile` | Deletes user account and cascade-deletes data. | Returns status check confirmation. |
| `GET` | `/api/profile/export` | Generates a JSON download of all user data. | Returns User, Documents, Notes, Quizzes. |

### Document Ingestion & Chat
| Method | Endpoint | Description | Request/Response Payload |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/upload` | Core upload pipeline streaming status via SSE. | `multipart/form-data` with `file: PDF` → Streams SSE. |
| `GET` | `/api/uploads/[filename]`| Serves raw document file for user rendering. | Returns PDF file bytes. |
| `GET` | `/api/documents` | Lists all documents belonging to user. | Returns Document array with status flags. |
| `DELETE`| `/api/documents` | Deletes specified document. | Query: `?id=uuid` → `{ success: true }` |
| `GET` | `/api/documents/[id]`| Fetches a specific document, summary, and quiz. | Returns document with relational models. |
| `POST` | `/api/documents/[id]`| Triggers manual reprocessing of parsed text. | Reprocesses extraction through the AI Engine. |
| `PATCH`| `/api/documents/[id]`| Updates document metadata (e.g. title). | `{ title }` → Updated Document object. |
| `POST` | `/api/chat` | Context-aware chat using PDF contents as grounding. | `{ message, history }` → `{ reply: string }` |

### Learning Objects (Notes, Quizzes, Maps)
| Method | Endpoint | Description | Request/Response Payload |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/notes` | Lists smart study notes. Filterable by type/doc.| Query: `?documentId=uuid` → Note array. |
| `POST` | `/api/notes` | Manually creates a new study note. | `{ title, content, type, summaryId }` → Note object.|
| `PUT` | `/api/notes` | Updates note content, title, or pins it. | `{ id, title, content, pinned }` → Note object. |
| `DELETE`| `/api/notes` | Deletes specified note. | Query: `?id=uuid` → `{ success: true }` |
| `GET` | `/api/summaries` | Lists summaries. | Returns Summary array. |
| `GET` | `/api/quizzes` | Lists quizzes. | Returns Quiz array. |
| `POST` | `/api/quizzes` | Submits score from completed quiz. | `{ id, score }` → Updated Quiz object. |
| `GET` | `/api/knowledge-map`| Fetches knowledge map coordinates for rendering. | Returns array of map nodes with connections. |
| `GET` | `/api/analytics` | Fetches focus telemetry and diagnostics. | Returns metrics, activityData, mastery, diagnosis. |
| `GET` | `/api/preferences` | Fetches user settings (accent colors, dark mode).| Returns UserPreferences object. |
| `PUT` | `/api/preferences` | Updates user settings. | `{ dark, accentColor, intensity, adaptive }` |
| `GET` | `/api/search` | Search index across summaries, notes, and docs. | Query: `?q=searchterm` → `{ results: [] }` |
| `GET` | `/api/csrf` | Fetches fresh CSRF token. | Returns `{ csrfToken }` |
| `GET` | `/api/health` | Next.js API router health check. | `{ status: "ok" }` |

---

## 🔒 Security Features

1. **CSRF Protection**: All state-modifying requests (`POST`, `PUT`, `PATCH`, `DELETE`) are wrapped in custom middleware that validates timing-safe CSRF tokens generated via cryptographic hashes.
2. **Sliding Window Rate Limiting**: In-memory rate limits restrict excessive requests on sensitive endpoints:
   - File uploads: `10 requests per minute` per IP address.
   - Interactive AI chat: `30 requests per minute` per IP address.
3. **Strict Input Sanitization**: Chat messages, note inputs, and profile edits are sanitized using Zod schemas and regex scripts to prevent cross-site scripting (XSS) and code injections.
4. **Credential Hashing**: User passwords are encrypted with `bcryptjs` before insertion into Neon DB.
5. **Secure Middleware Guards**: Dynamic route groups (like the `(dashboard)`) and API endpoints require active session checks via custom authentication validators, returning 401/403 responses immediately upon token expiration.

---

## ⚡ Performance Considerations

- **Dynamic Component Loading**: Heavy interface elements (like `NeuralBackground` canvas particle physics, the circular `QuantumDock`, and the floating `FloatingAIAssistant`) are imported dynamically with SSR disabled to optimize initial load times.
- **Standalone Build Optimization**: Build script compiles Next.js into a standalone runner bundle (`.next/standalone`), reducing docker image sizes and minimizing dependency overhead.
- **Incremental Data Streaming**: File upload pipelines utilize Server-Sent Events (SSE) to report progress to clients incrementally, avoiding network timeouts during deep AI processing.
- **Database Selection Constraints**: Database queries restrict returned payloads using Prisma's `select` and `take` operators, preventing memory spikes when retrieving summaries and notes.

---

## 📦 Installation & Setup

Ensure you have **Node.js 20+**, **Python 3.10+**, and **Docker** installed.

### 1. Repository Setup & Dependencies
```bash
# Clone the repository
git clone https://github.com/your-username/NeuroLearn-AI.git
cd NeuroLearn-AI

# Install Next.js dependencies
npm install

# Install FastAPI dependencies
cd server
pip install -r requirements.txt
cd ..
```

### 2. Database Migration
Make sure your PostgreSQL database is running, copy the environment template, and run migrations:
```bash
# Copy env variables template
cp .env.example .env

# Configure your database connection in .env (DATABASE_URL)
# Run Prisma schema migration
npx prisma db push
npx prisma generate
```

### 3. Running Locally
Run the servers separately or coordinate them via Docker Compose:

#### Local Development Run:
```bash
# Terminal 1: Run Next.js
npm run dev

# Terminal 2: Run Python FastAPI
cd server
python main.py
```

#### Run with Docker Compose:
```bash
# Build and run containers
docker-compose up --build
```
The application will launch on `http://localhost:3000`, database on port `5432`, and FastAPI backend on `http://localhost:8000`.

---

## 🛠️ Environment Configuration Matrix

The application reads configurations from `.env` in the root:

| Environment Variable | Description | Default Value / Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL DB URL connection string | `postgresql://neurolearn:password@postgres:5432/neurolearn` |
| `NEXTAUTH_URL` | Application root URL for NextAuth session callbacks | `http://localhost:3000` |
| `NEXTAUTH_SECRET` | 32-character key for encrypting JWT tokens | `openssl rand -base64 64` |
| `GOOGLE_CLIENT_ID` | Client identifier for Google OAuth login | `google-oauth-client-id` |
| `GOOGLE_CLIENT_SECRET`| Client secret for Google OAuth authentication | `google-oauth-client-secret` |
| `GOOGLE_API_KEY` | Google Gemini API Studio key (Fast Flash calls) | `AIzaSy...` |
| `NEXT_PUBLIC_AI_SERVICE_URL`| Browser endpoint redirecting to FastAPI | `http://127.0.0.1:8000` |
| `FASTAPI_URL` | Server-to-server endpoint for Next.js to FastAPI | `http://127.0.0.1:8000` |
| `SMTP_HOST` | Outgoing SMTP mail server host for password resets | `smtp.ethereal.email` |
| `SMTP_PORT` | Outgoing SMTP mail port | `587` |
| `SMTP_SECURE` | Set to true if utilizing SSL for mail connections | `false` |
| `SMTP_USER` | SMTP server username | `smtp-user-email` |
| `SMTP_PASS` | SMTP server password | `smtp-user-password` |
| `SMTP_FROM` | Default sender display email | `noreply@neurolearn.ai` |

---

## 🚀 Deployment Guide (Production)

### 1. Neon Database Setup
1. Sign up on [Neon Database](https://neon.tech) and create a new PostgreSQL project.
2. Retrieve the pooled connection string (`DATABASE_URL`).
3. Set the `DATABASE_URL` in your `.env` configuration file.

### 2. Google OAuth Configuration
1. Access the [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project and configure the OAuth consent screen.
3. Access Credentials, create an OAuth 2.0 Client ID, and set application type to Web.
4. Set Authorized Redirect URIs to:
   `https://your-domain.com/api/auth/callback/google`
5. Save the generated `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.

### 3. Vercel Deployment
1. Log in to Vercel and create a new project.
2. Select your repository, configure environment variables matching the table, and configure Vercel settings:
   - **Build Command**: `prisma generate && next build`
   - **Output Directory**: `.next`
3. Add the Vercel project domain URL to your `NEXTAUTH_URL` environment variable.

### 4. Deploying the FastAPI Parser (Render / Fly.io)
1. Deploy the FastAPI service using the provided Dockerfile in `/server`.
2. Configure your FastAPI service environment variables (e.g. `TESSERACT_CMD` setup).
3. Set your production FastAPI deployment URL as the `NEXT_PUBLIC_AI_SERVICE_URL` and `FASTAPI_URL` on your Vercel Next.js dashboard variables.

---

## 🗺️ Future Roadmap

- [ ] **Voice-Activated Recall**: Introduce interactive vocal study sessions utilizing web speech synthesizers.
- [ ] **Web Clipper Browser Extension**: Instantly send selected article pages and PDFs from Chrome directly to your dashboard workspace.
- [ ] **Pinecone Vector Integration**: Adapt the text chunks database to support vector similarity searches (RAG) across multiple uploaded documents.
- [ ] **Collaborative Classrooms**: Allow users to share generated summaries, quizzes, and live study maps with friends.

---

## 📄 License & Attribution

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<p align="center">
  <span class="text-gradient-neural" style="font-weight: 700;">Designed with Cinematic Neural Aesthetics.</span><br/>
  <span>© 2026 NeuroLearn AI. Syncing Cognitive Telemetry and Enhancing Active Recall.</span>
</p>
