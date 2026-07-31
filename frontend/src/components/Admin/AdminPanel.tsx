import React, { useState } from 'react';
import { Box, Button, Alert, AlertIcon, useToast, Heading, Text } from '@chakra-ui/react';
import axios from 'axios';

const ADMIN_TOKEN = import.meta.env.VITE_ADMIN_TOKEN || 'supersecret';

const AdminPanel = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();

  const handleClearAll = async () => {
    if (!window.confirm('Are you sure you want to delete ALL files and chat history? This cannot be undone.')) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const resp = await axios.post('/api/admin/clear_all', {}, {
        headers: { 'admin-token': ADMIN_TOKEN }
      });
      setResult(`Deleted ${resp.data.files_deleted} files and ${resp.data.chats_deleted} chat messages.`);
      toast({ title: 'App reset', description: 'All files and chat history deleted.', status: 'success', duration: 4000, isClosable: true });
      window.location.reload();
    } catch (err: any) {
      let detail = err?.response?.data?.detail;
      if (typeof detail === 'object' && detail?.msg) detail = detail.msg;
      setError(typeof detail === 'string' ? detail : JSON.stringify(detail || err.message || 'Reset failed'));
      toast({ title: 'Reset failed', description: typeof detail === 'string' ? detail : JSON.stringify(detail || err.message), status: 'error', duration: 4000, isClosable: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4} borderWidth={1} borderRadius="lg" boxShadow="md" my={4}>
      <Heading size="sm" mb={2}>Admin Controls</Heading>
      <Text fontSize="sm" color="gray.500" mb={2}>Danger zone: This will delete <b>all</b> files and chat history from the app.</Text>
      <Button colorScheme="red" onClick={handleClearAll} isLoading={loading}>
        Reset App (Clear All)
      </Button>
      {result && <Alert status="success" mt={3}><AlertIcon />{result}</Alert>}
      {error && <Alert status="error" mt={3}><AlertIcon />{error}</Alert>}
    </Box>
  );
};

export default AdminPanel;
