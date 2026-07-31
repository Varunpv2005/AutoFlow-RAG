import React, { useEffect, useState } from 'react';
import { Box, Heading, Divider, useToast, Text, VStack, HStack, Spinner, Icon, Badge } from '@chakra-ui/react';
import { FaFolderOpen } from 'react-icons/fa';
import { useFilesStore } from 'state/filesStore';
import { useChatStore } from 'state/chatStore';
import { fetchFiles, deleteFile } from 'api/filesApi';
import { getUsername } from 'api/authApi';

import { FileUpload, FilesList, FileErrorAlert } from 'components/Files';
import { AdminPanel } from 'components/Admin';

interface FilesSidebarProps {
  collapsed?: boolean;
}

const FilesSidebar = ({ collapsed = false }: FilesSidebarProps) => {
  const files = useFilesStore((state) => state.files);
  const setFiles = useFilesStore((state) => state.setFiles);
  const loading = useFilesStore((state) => state.loading);
  const setLoading = useFilesStore((state) => state.setLoading);
  const error = useFilesStore((state) => state.error);
  const setError = useFilesStore((state) => state.setError);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const toast = useToast();
  const indexedCount = files.filter((file) => Boolean(file.is_indexed)).length;
  const pendingCount = files.length - indexedCount;

  useEffect(() => {
    const loadFiles = async () => {
      setLoading(true);
      try {
        const backendFiles = await fetchFiles();
        setFiles(backendFiles);
        setError(null);
      } catch (err: any) {
        setError(err?.toString() || 'Failed to fetch files');
      } finally {
        setLoading(false);
      }
    };
    loadFiles();
  }, [setFiles, setLoading, setError]);

  const handleDelete = async (id: number) => {
    setDeletingId(id);
    try {
      const resp = await deleteFile(id);
      const updatedFiles = files.filter((f) => f.id !== id);
      setFiles(updatedFiles);
      if (resp && resp.warnings && resp.warnings.length > 0) {
        setError(resp.warnings.join('\n'));
        toast({ title: 'File deleted with warnings', description: resp.warnings.join('\n'), status: 'warning', duration: 4000, isClosable: true });
      } else {
        setError(null);
        toast({ title: 'File deleted', status: 'success', duration: 2000, isClosable: true });
      }
      if (updatedFiles.length === 0) {
        useChatStore.getState().clearChat();
      }
    } catch (error: any) {
      const msg = error?.response?.data?.detail || error?.message || 'File deletion failed';
      setError(msg);
      toast({ title: 'File deletion failed', description: msg, status: 'error', duration: 4000, isClosable: true });
    } finally {
      setDeletingId(null);
    }
  };

  if (collapsed) {
    return (
      <Box display="flex" flexDirection="column" h="100%" w="100%" p={3} bg="white" alignItems="center" justifyContent="flex-start">
        <Box p={2.5} borderRadius="xl" bg="blue.50" color="blue.600" mb={4}>
          <Icon as={FaFolderOpen} boxSize={5} />
        </Box>
        <Text fontSize="10px" fontWeight="bold" letterSpacing="wider" color="gray.400" textTransform="uppercase" writingMode="vertical-rl" transform="rotate(180deg)">
          Documents
        </Text>
      </Box>
    );
  }

  return (
    <Box display="flex" flexDirection="column" h="100%" w="100%" p={0} bg="white">
      <Box p={{ base: 2, md: 3 }} pb={0}>
        <Heading size="md" mb={1} fontSize={{ base: 'lg', md: 'xl' }}>AutoFlow-RAG</Heading>
        <Text fontSize="11px" color="gray.500" mb={2}>Knowledge workspace</Text>
        <Box borderWidth="1px" borderColor="gray.100" borderRadius="xl" bg="gray.50" p={2} mb={3}>
          <HStack justify="space-between" align="center" mb={2} spacing={2}>
            <Text fontSize="9px" fontWeight="bold" color="gray.500" textTransform="uppercase" letterSpacing="wider">Workspace Health</Text>
            <Badge colorScheme="green" variant="subtle" fontSize="9px">{indexedCount} ready</Badge>
          </HStack>
          <HStack spacing={2} mt={2} align="center">
            <Text fontSize="9px" color="gray.500">Ready corpus: {indexedCount}/{files.length} files</Text>
            <Badge colorScheme={pendingCount > 0 ? 'yellow' : 'green'} fontSize="9px" px={2} py={0.5} borderRadius="full">
              {pendingCount} pending
            </Badge>
          </HStack>
          <HStack spacing={2} mt={3}>
            <Box flex="1" p={2} bg="white" borderRadius="lg" borderWidth="1px" borderColor="gray.100">
              <Text fontSize="9px" color="gray.500">Documents</Text>
              <Text fontSize="14px" fontWeight="bold" color="gray.800">{files.length}</Text>
            </Box>
            <Box flex="1" p={2} bg="white" borderRadius="lg" borderWidth="1px" borderColor="gray.100">
              <Text fontSize="9px" color="gray.500">Pending</Text>
              <Text fontSize="14px" fontWeight="bold" color="gray.800">{pendingCount}</Text>
            </Box>
          </HStack>
          <Text fontSize="9px" color="gray.500" mt={3}>A complete corpus improves answer relevance. Keep your knowledge base indexed before asking complex questions.</Text>
        </Box>
        <FileUpload />
        {loading && (
          <Box px={3} py={3} bg="blue.50" my={2} borderRadius="xl" borderWidth="1px" borderColor="blue.100">
            <VStack align="stretch" spacing={3}>
              <Text fontSize="10px" fontWeight="bold" color="blue.700" textTransform="uppercase" letterSpacing="wider">
                Processing Timeline
              </Text>
              <VStack align="stretch" spacing={2} pl={1}>
                <HStack spacing={2.5} align="center">
                  <Spinner size="xs" color="blue.500" />
                  <Text fontSize="11px" color="blue.900" fontWeight="medium">Uploading file to workspace...</Text>
                </HStack>
                <HStack spacing={2.5} align="center">
                  <Box w="6px" h="6px" borderRadius="full" bg="blue.400" />
                  <Text fontSize="11px" color="gray.600">Generating embeddings & chunk indexing</Text>
                </HStack>
                <HStack spacing={2.5} align="center">
                  <Box w="6px" h="6px" borderRadius="full" bg="blue.200" />
                  <Text fontSize="11px" color="gray.500">Extracting summary & suggested QA</Text>
                </HStack>
              </VStack>
            </VStack>
          </Box>
        )}
        <Divider my={3} />
        <FileErrorAlert error={error} />
      </Box>

      <Box flex={1} px={{ base: 1, md: 2 }} overflowY="auto" minH={0}>
        <FilesList files={files} loading={loading} deletingId={deletingId} onDelete={handleDelete} />
      </Box>
      {getUsername() === 'admin' && (
        <Box p={{ base: 2, md: 4 }} pt={0} mb={{ base: 2, md: 4 }} borderTopWidth={1} borderColor="gray.100" bg="white" boxShadow="sm" borderRadius="lg">
          <React.Suspense fallback={null}>
            {typeof window !== 'undefined' && <AdminPanel />}
          </React.Suspense>
        </Box>
      )}
    </Box>
  );
};

export default FilesSidebar;
