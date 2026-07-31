# Gotchas & Integration Quirks (Frontend Refactor 2025-04-30)

- Large components (FilesSidebar, FileUpload) should be split if >200 lines or handling multiple concerns
- Always use Chakra UI responsive props for layouts (e.g., `minW`, `overflowY`, `fontSize`)
- State must be updated only after backend confirmation to avoid UI drift
- File list area must be scrollable on mobile/tablet
- Error feedback must be visible and accessible (alerts/toasts)
- If adding new UI, follow modular/component-first approach

## Recent Change Log
- [2025-04-30] FilesSidebar refactored, new FilesList and FileErrorAlert components, responsive improvements
- [2025-04-30] Tailwind fully removed
