import React, { useState } from 'react';
import {
  Box, Button, FormControl, FormLabel, Heading, Input,
  Text, VStack, Alert, AlertIcon, Link
} from '@chakra-ui/react';
import { signup } from '../../api/authApi';

interface Props {
  onAuth: () => void;
  onGoLogin: () => void;
}

export default function SignupPage({ onAuth, onGoLogin }: Props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await signup(username, password);
      onAuth();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box minH="100vh" display="flex" alignItems="center" justifyContent="center" bg="gray.50">
      <Box bg="white" p={8} rounded="xl" boxShadow="lg" w="100%" maxW="400px">
        <VStack spacing={6} as="form" onSubmit={handleSubmit}>
          <Heading size="lg" color="blue.600">AutoFlow-RAG</Heading>
          <Text color="gray.500" fontSize="sm">Create an account</Text>
          {error && <Alert status="error" rounded="md"><AlertIcon />{error}</Alert>}
          <FormControl isRequired>
            <FormLabel>Username</FormLabel>
            <Input value={username} onChange={e => setUsername(e.target.value)} autoFocus />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input type="password" value={password} onChange={e => setPassword(e.target.value)} />
          </FormControl>
          <Button type="submit" colorScheme="blue" w="full" isLoading={loading}>
            Sign Up
          </Button>
          <Text fontSize="sm">
            Already have an account?{' '}
            <Link color="blue.500" onClick={onGoLogin} cursor="pointer">Sign in</Link>
          </Text>
        </VStack>
      </Box>
    </Box>
  );
}
