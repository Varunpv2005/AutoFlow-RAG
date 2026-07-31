// theme.ts - Chakra UI theme override for Gemini-style minimal UI
import { extendTheme, ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  fonts: {
    heading: "system-ui, sans-serif",
    body: "system-ui, sans-serif",
  },
  styles: {
    global: {
      body: {
        bg: "#f9f9fb",
        color: "#222",
      },
    },
  },
  components: {
    Button: {
      baseStyle: {
        borderRadius: "md",
        fontWeight: "medium",
      },
    },
    Input: {
      baseStyle: {
        borderRadius: "md",
      },
    },
  },
});

export default theme;
