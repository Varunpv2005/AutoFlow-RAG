# Implementation Details: Frontend Refactor (2025-04-30)

## [2025-05-02] Breaking Change: sendChat API Refactor
- `sendChat` in `chatStore.ts` now takes an `options` object for all parameters except `question`.
- Removed `useMMR` parameter (was unused in API call).
- Updated `ChatState` interface accordingly.
- **Breaking:** All callers of `sendChat` must use the new signature:
  ```ts
  sendChat(question, { fileId, keywords, metadataFilter, k })
  ```
- Motivation: Prevent parameter order/type errors, improve extensibility and type safety.

## Motivation
- Improve maintainability, testability, and responsiveness
- Reduce component size and responsibility

## Changes
- **FilesSidebar** refactored to use:
  - `FilesList` (file rendering, empty/loading states)
  - `FileErrorAlert` (error display)
- Chakra UI responsive props (`minW`, `maxW`, `overflowY`, etc.) ensure mobile/tablet/desktop support
- File list now scrollable on small screens
- All business logic preserved; only presentation changed

## Best Practices Adopted
- Components < 100 lines where possible
- Single-responsibility principle
- Responsive design with Chakra UI
- Zustand selectors for state
- No direct state mutation
- Error boundaries recommended for future
- All async actions provide user feedback (toast/alerts)

## Next Steps
- Apply same refactor to other large components (e.g., FileUpload, ChatArea)
- Add Storybook for UI documentation
- Add error boundaries for resilience
- Expand test coverage (Jest/React Testing Library)
