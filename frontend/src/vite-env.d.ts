/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_ADMIN_TOKEN?: string;
  // add other env vars here if needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
