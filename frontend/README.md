# Frontend Installation & Setup

This is the frontend for the Local RAG application, built with Vite, React, TypeScript, Zustand, and Chakra UI. It implements a Gemini-style UI for seamless document upload and chat functionality.

## Markdown Rendering for Chat Responses

- The chat UI now renders LLM answers as formatted markdown using the [react-markdown](https://github.com/remarkjs/react-markdown) package.
- **Install:** `npm install react-markdown`
- **Rationale:** Ensures all AI responses are easy to read, with proper headings, lists, and code formatting.

## Project Structure

```
/frontend
├── src/
│   ├── api/                # API utilities for backend requests
│   ├── components/
│   │   ├── Admin/          # AdminPanel and related components
│   │   ├── Chat/           # Chat UI components (ChatArea, ChatBubble, ChatInput)
│   │   ├── Files/          # File upload/list UI components
│   │   └── Layout/         # Layout and header components
│   ├── state/              # Zustand stores for chat and files
│   ├── styles/             # Theme and Chakra UI styling
│   ├── App.tsx             # Main React app entry
│   ├── main.tsx            # ReactDOM entrypoint
│   └── vite-env.d.ts       # Vite/TypeScript env types
├── index.html              # HTML entrypoint
├── package.json            # NPM dependencies and scripts
├── package-lock.json       # NPM lockfile
├── tsconfig.json           # TypeScript config
├── vite.config.ts          # Vite config
├── postcss.config.cjs      # PostCSS config
├── implementation_details.md # Frontend implementation notes
├── gotchas.md              # Frontend gotchas and pitfalls
├── quick_reference.md      # Frontend quick reference
├── .env                    # Environment variables
├── README.md               # This file
```

### Directory Descriptions
- **src/api/**: API utilities for backend requests (chat, files, health)
- **src/components/Admin/**: AdminPanel and admin controls
- **src/components/Chat/**: Chat UI (ChatArea, ChatBubble, ChatInput)
- **src/components/Files/**: File upload, list, and related components
- **src/components/Layout/**: Layout and header/navigation components
- **src/state/**: Zustand state management for chat and files
- **src/styles/**: Theme and Chakra UI styling

### Operational Notes
- All architectural decisions, pitfalls, and integration gotchas must be logged in `implementation_details.md` and `gotchas.md`.
- Changes to requirements or stack must be reflected in `quick_reference.md` and referenced in commit messages.
- All code and documentation updates must be kept in sync per operational directives.
├── postcss.config.cjs
├── implementation_details.md
├── gotchas.md
├── quick_reference.md
├── .env
├── README.md
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start development server:
   ```bash
   npm run dev
   ```

## Documentation
- See `/quick_reference.md` for API endpoints and configs.
- See `/implementation_details.md` for architecture and design decisions.
- See `/gotchas.md` for pitfalls and integration notes.
