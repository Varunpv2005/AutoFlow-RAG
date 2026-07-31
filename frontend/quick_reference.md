# Quick Reference: Frontend

## Main Libraries
- **React** (Vite, TypeScript)
- **Chakra UI** (component library, theming, accessibility)
- **Zustand** (state management)
- **react-markdown** (LLM markdown rendering)

## Component Structure
- `/components/Files/FilesSidebar.tsx` — Main sidebar, now modular and responsive
- `/components/Files/FilesList.tsx` — File list, empty state, loading spinner
- `/components/Files/FileErrorAlert.tsx` — Error display
- `/components/Files/FileUpload.tsx` — File uploader (drag/drop)
- `/components/Files/FilePill.tsx` — File pill (single file display)

## Responsive Design
- Chakra UI responsive props used throughout
- Sidebar is scrollable and adapts to mobile/tablet/desktop

## State Management
- All file and chat state via Zustand stores
- UI updates only after backend confirmation (upload, delete)

## Common Scripts
- `npm run dev` — Start dev server
- `npm run build` — Build for production

## Removed
- Tailwind CSS (no longer used)

For API endpoints, see backend quick reference.
