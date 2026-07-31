import React, { useState } from 'react';
import {
  Box, HStack, Icon, Text, IconButton, useDisclosure, Modal, ModalOverlay,
  ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter, Button,
  VStack, Badge, List, ListItem, Heading, Tooltip, Wrap, WrapItem, Spinner, useToast
} from '@chakra-ui/react';
import { FaFilePdf, FaFileWord, FaFileExcel, FaFileAlt, FaTrash, FaBrain, FaRegQuestionCircle, FaEye } from 'react-icons/fa';
import { FileMeta } from 'state/filesStore';
import { useChatStore } from 'state/chatStore';
import { previewFile } from 'api/filesApi';

const getFileIcon = (filename?: string) => {
  if (!filename) return { icon: FaFileAlt, color: 'gray.400' };
  const ext = filename.split('.').pop()?.toLowerCase();
  switch (ext) {
    case 'pdf':
      return { icon: FaFilePdf, color: 'red.500' };
    case 'docx':
    case 'doc':
      return { icon: FaFileWord, color: 'blue.500' };
    case 'xlsx':
    case 'xls':
    case 'csv':
      return { icon: FaFileExcel, color: 'green.500' };
    default:
      return { icon: FaFileAlt, color: 'gray.500' };
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch {
    return dateStr;
  }
};

const formatFileSize = (size?: number | null) => {
  if (size == null || size < 0) return 'Unknown size';
  if (size < 1024) return `${size} B`;
  const kb = size / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  const mb = kb / 1024;
  return `${mb.toFixed(1)} MB`;
};

type FilePillProps = {
  file: FileMeta;
  onDelete?: (id: number) => void;
  deleting?: boolean;
};

interface IntelData {
  summary?: string;
  keywords?: string[];
  suggested_questions?: string[];
}

const FilePill = ({ file, onDelete, deleting }: FilePillProps) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const previewDisclosure = useDisclosure();
  const sendChat = useChatStore((state) => state.sendChat);
  const { icon, color } = getFileIcon(file.filename);
  const toast = useToast();
  const [preview, setPreview] = useState<{ type: string; content?: string; path?: string } | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);

  let intel: IntelData | null = null;
  if (file.file_metadata) {
    try {
      intel = JSON.parse(file.file_metadata);
    } catch {
      // Ignored
    }
  }

  const handleQuestionClick = (question: string) => {
    sendChat(question, { fileId: String(file.id) });
    onClose();
  };

  const normalizedFileType = (file.file_type || file.filename.split('.').pop()?.toUpperCase() || 'FILE').replace(/^\./, '');
  const indexed = Boolean(file.is_indexed);
  const chunkCount = file.chunk_count ?? 0;
  const processingStatus = (file.processing_status || (indexed ? 'indexed' : 'pending')).toLowerCase();
  const processingLabel = processingStatus === 'indexed' ? 'Indexed' : processingStatus === 'processing' ? 'Processing' : processingStatus === 'failed' ? 'Failed' : 'Pending';
  const processingColor = processingStatus === 'indexed' ? 'green' : processingStatus === 'processing' ? 'blue' : processingStatus === 'failed' ? 'red' : 'gray';

  const openPreview = async () => {
    if (previewDisclosure.isOpen) {
      previewDisclosure.onClose();
      return;
    }
    setPreviewLoading(true);
    try {
      const result = await previewFile(file.id);
      setPreview(result);
      previewDisclosure.onOpen();
    } catch {
      toast({ title: 'Preview unavailable', description: 'This file could not be previewed right now.', status: 'error', duration: 3000, isClosable: true });
    } finally {
      setPreviewLoading(false);
    }
  };

  return (
    <>
      <Box
        p={2.5}
        borderWidth="1px"
        borderColor="gray.200"
        borderRadius="xl"
        bg="white"
        boxShadow="sm"
        transition="all 0.2s"
        _hover={{ shadow: 'md', borderColor: 'blue.300', transform: 'translateY(-1px)' }}
        w="100%"
      >
        <HStack spacing={3} align="flex-start" justify="space-between">
          <HStack spacing={2} minW={0} flex={1} align="flex-start">
            <Icon as={icon} color={color} boxSize={5} mt={1} />
            <VStack align="stretch" spacing={1} minW={0} flex={1}>
              <Text fontSize="sm" fontWeight="semibold" color="gray.800" isTruncated>
                {file.filename}
              </Text>
              <HStack spacing={2} flexWrap="wrap">
                <Text fontSize="10px" color="gray.400">
                  {formatDate(file.upload_time)}
                </Text>
                <Badge colorScheme="blue" fontSize="9px" px={1.5} py={0.2} borderRadius="full">
                  {normalizedFileType}
                </Badge>
              </HStack>
              <Wrap spacing={1} pt={1}>
                <WrapItem>
                  <Badge colorScheme="gray" variant="subtle" fontSize="9px" px={2} py={0.4} borderRadius="md">
                    {formatFileSize(file.file_size_bytes)}
                  </Badge>
                </WrapItem>
                <WrapItem>
                  <Badge colorScheme={processingColor} variant="subtle" fontSize="9px" px={2} py={0.4} borderRadius="md">
                    {processingLabel}
                  </Badge>
                </WrapItem>
                <WrapItem>
                  <Badge colorScheme="purple" variant="subtle" fontSize="9px" px={2} py={0.4} borderRadius="md">
                    {chunkCount} chunks
                  </Badge>
                </WrapItem>
                {file.is_indexed && (
                  <WrapItem>
                    <Badge colorScheme="green" variant="subtle" fontSize="9px" px={2} py={0.4} borderRadius="md">
                      Indexed
                    </Badge>
                  </WrapItem>
                )}
              </Wrap>
              {intel?.summary && (
                <Text fontSize="11px" color="gray.500" mt={2} noOfLines={2}>
                  {intel.summary}
                </Text>
              )}
            </VStack>
          </HStack>
          <HStack spacing={1}>
            <Tooltip label="Preview document" placement="top">
              <IconButton
                aria-label="Preview file"
                icon={<FaEye />}
                size="xs"
                colorScheme="blue"
                variant="ghost"
                onClick={openPreview}
                isLoading={previewLoading}
              />
            </Tooltip>
            {intel && (intel.summary || intel.keywords || intel.suggested_questions) ? (
              <Tooltip label="View AI Insights" placement="top">
                <IconButton
                  aria-label="Document Intelligence"
                  icon={<FaBrain />}
                  size="xs"
                  colorScheme="purple"
                  variant="ghost"
                  onClick={onOpen}
                />
              </Tooltip>
            ) : (
              <Tooltip label="AI Processing..." placement="top">
                <IconButton
                  aria-label="Document Intelligence"
                  icon={<FaBrain />}
                  size="xs"
                  colorScheme="gray"
                  variant="ghost"
                  isDisabled
                />
              </Tooltip>
            )}
            {onDelete && (
              <Tooltip label="Delete Document" placement="top">
                <IconButton
                  aria-label="Delete file"
                  icon={<FaTrash />}
                  size="xs"
                  colorScheme="red"
                  variant="ghost"
                  isLoading={deleting}
                  onClick={() => onDelete(file.id)}
                />
              </Tooltip>
            )}
          </HStack>
        </HStack>
      </Box>

      <Modal isOpen={previewDisclosure.isOpen} onClose={previewDisclosure.onClose} size="lg" isCentered>
        <ModalOverlay />
        <ModalContent borderRadius="xl">
          <ModalHeader borderBottomWidth={1} borderColor="gray.100" color="blue.600" fontSize="md" isTruncated>
            Preview: {file.filename}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody py={5} maxH="70vh" overflowY="auto">
            {previewLoading ? (
              <HStack spacing={3} justify="center" py={8}>
                <Spinner size="sm" />
                <Text color="gray.500">Loading preview…</Text>
              </HStack>
            ) : preview?.type === 'text' ? (
              <Box bg="gray.50" borderRadius="md" p={4} whiteSpace="pre-wrap" fontSize="sm" color="gray.700">
                {preview.content || 'No content available.'}
              </Box>
            ) : preview?.type === 'pdf' ? (
              <Box borderWidth="1px" borderColor="gray.200" borderRadius="md" overflow="hidden">
                <iframe src={`/api/files/${file.id}/preview?download=1`} title={file.filename} style={{ width: '100%', height: '60vh', border: 'none' }} />
              </Box>
            ) : (
              <Text color="gray.500">Preview is not available for this file type.</Text>
            )}
          </ModalBody>
          <ModalFooter borderTopWidth={1} borderColor="gray.100">
            <Button onClick={previewDisclosure.onClose} size="sm">Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Modal isOpen={isOpen} onClose={onClose} size="md" isCentered>
        <ModalOverlay />
        <ModalContent borderRadius="xl">
          <ModalHeader borderBottomWidth={1} borderColor="gray.100" color="purple.600" fontSize="md" isTruncated>
            🧠 AI Insights: {file.filename}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody py={5}>
            {intel && (
              <VStack spacing={4} align="stretch">
                {intel.summary && (
                  <Box>
                    <Heading size="xs" color="gray.500" textTransform="uppercase" mb={2}>Summary</Heading>
                    <Text fontSize="sm" color="gray.700" lineHeight="tall" bg="gray.50" p={3} borderRadius="md">
                      {intel.summary}
                    </Text>
                  </Box>
                )}

                {intel.keywords && intel.keywords.length > 0 && (
                  <Box>
                    <Heading size="xs" color="gray.500" textTransform="uppercase" mb={2}>Keywords</Heading>
                    <HStack spacing={2} flexWrap="wrap">
                      {intel.keywords.map((kw, idx) => (
                        <Badge key={idx} colorScheme="purple" variant="subtle" px={2} py={0.5} borderRadius="md" fontSize="xs">
                          {kw}
                        </Badge>
                      ))}
                    </HStack>
                  </Box>
                )}

                {intel.suggested_questions && intel.suggested_questions.length > 0 && (
                  <Box>
                    <Heading size="xs" color="gray.500" textTransform="uppercase" mb={2}>Suggested Questions</Heading>
                    <List spacing={2}>
                      {intel.suggested_questions.map((q, idx) => (
                        <ListItem
                          key={idx}
                          fontSize="xs"
                          p={2}
                          borderWidth={1}
                          borderColor="gray.200"
                          borderRadius="md"
                          cursor="pointer"
                          _hover={{ bg: 'purple.50', borderColor: 'purple.200' }}
                          onClick={() => handleQuestionClick(q)}
                          display="flex"
                          alignItems="center"
                        >
                          <Icon as={FaRegQuestionCircle} mr={2} color="purple.500" />
                          <Text fontWeight="medium" color="gray.700">{q}</Text>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
              </VStack>
            )}
          </ModalBody>
          <ModalFooter borderTopWidth={1} borderColor="gray.100">
            <Button onClick={onClose} size="sm">Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default FilePill;
