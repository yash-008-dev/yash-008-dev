# NeuroLearn

[![Website](https://img.shields.io/badge/Website-NeuroLearn-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://YOUR-WEBSITE-URL)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=nextdotjs)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Prisma](https://img.shields.io/badge/Prisma-5.22.0-2D3748?style=for-the-badge&logo=prisma)](https://prisma.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql)](https://postgresql.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=for-the-badge&logo=google)](https://aistudio.google.com)

AI-powered learning platform that transforms PDF documents into summaries, notes, quizzes, knowledge maps, and interactive study materials.

---

## Features

- PDF Upload & Processing
- AI Generated Summaries
- Smart Notes
- Quiz Generation
- Knowledge Maps
- Context-Aware AI Chat
- Google OAuth Authentication
- Learning Analytics Dashboard

---

## Architecture

```mermaid
flowchart LR

User --> NextJS
NextJS --> Auth
Auth --> API
API --> Prisma
Prisma --> PostgreSQL

API --> FastAPI
FastAPI --> OCR

API --> Gemini
Gemini --> Summary
Gemini --> Quiz
Gemini --> Notes

Summary --> Dashboard
Quiz --> Dashboard
Notes --> Dashboard
```

---

## Document Processing Pipeline

```mermaid
flowchart LR

Upload --> Extract
Extract --> OCR
OCR --> Clean
Clean --> Gemini
Gemini --> Summary
Gemini --> Notes
Gemini --> Quiz
Summary --> Database
Notes --> Database
Quiz --> Database
Database --> Dashboard
```

---

## Tech Stack

### Frontend

- Next.js 16
- React 19
- Tailwind CSS
- Framer Motion
- D3.js
- Recharts

### Backend

- Next.js API Routes
- FastAPI

### Database

- PostgreSQL
- Prisma ORM
- Neon Database

### AI

- Google Gemini 2.0 Flash
- PyMuPDF
- pdfplumber
- Tesseract OCR

### Authentication

- NextAuth.js
- Google OAuth

---

## Project Structure

```text
src/
├── app/              # Next.js routes
├── components/       # UI components
├── lib/              # Shared utilities
├── types/            # Type definitions

prisma/
├── schema.prisma
├── migrations/

server/
├── main.py
├── requirements.txt
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/NeuroLearn.git
cd NeuroLearn
```

### Install Dependencies

```bash
npm install

cd server
pip install -r requirements.txt
cd ..
```

### Configure Environment

```bash
cp .env.example .env
```

Required variables:

```env
DATABASE_URL=
NEXTAUTH_URL=
NEXTAUTH_SECRET=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_API_KEY=

FASTAPI_URL=
NEXT_PUBLIC_AI_SERVICE_URL=
```

### Prisma Setup

```bash
npx prisma db push
npx prisma generate
```

### Start Development Servers

Terminal 1

```bash
npm run dev
```

Terminal 2

```bash
cd server
python main.py
```

Application:

```text
http://localhost:3000
```

---

## Security

- CSRF Protection
- Rate Limiting
- Input Validation using Zod
- Password Hashing with bcrypt
- Protected API Routes

---

## License

MIT License

---

## Author

**Adhyatma Singh Chauhan**

GitHub: https://github.com/asc006-git
