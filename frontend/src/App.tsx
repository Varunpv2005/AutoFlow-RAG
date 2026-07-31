import React, { useState } from "react";
import { ChakraProvider, Box } from '@chakra-ui/react';
import MainLayout from './components/Layout/MainLayout';
import LoginPage from './components/Auth/LoginPage';
import SignupPage from './components/Auth/SignupPage';
import theme from './styles/theme';
import { getToken, clearToken } from './api/authApi';
import { useFilesStore } from './state/filesStore';
import { useChatStore } from './state/chatStore';

type AuthView = 'login' | 'signup' | 'app';

function App() {
  const [view, setView] = useState<AuthView>(() =>
    getToken() ? 'app' : 'login'
  );

  const handleAuth = () => setView('app');
  const handleLogout = () => {
    clearToken();
    useFilesStore.getState().clearFiles();
    useChatStore.getState().clearChat();
    setView('login');
  };

  return (
    <ChakraProvider theme={theme}>
      <Box height="100%" bg="gray.50">
        {view === 'login' && (
          <LoginPage onAuth={handleAuth} onGoSignup={() => setView('signup')} />
        )}
        {view === 'signup' && (
          <SignupPage onAuth={handleAuth} onGoLogin={() => setView('login')} />
        )}
        {view === 'app' && (
          <MainLayout onLogout={handleLogout} />
        )}
      </Box>
    </ChakraProvider>
  );
}

export default App;
