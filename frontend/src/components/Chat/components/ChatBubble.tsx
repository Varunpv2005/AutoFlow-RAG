import {
  Box, Text, HStack, Icon, Badge, Collapse, Button, VStack, Divider,
  useToast, IconButton, Tooltip, Flex, Code, Spinner
} from '@chakra-ui/react';
import {
  FaRobot, FaUser, FaFileAlt, FaChevronDown, FaChevronUp,
  FaCopy, FaThumbsUp, FaThumbsDown
} from 'react-icons/fa';
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useChatStore, ChatMessage } from 'state/chatStore';

const HIDDEN_FIELDS = new Set([
  'source', 'source_file', 'file_path', 'filepath', 'path',
  'page_content', 'file_id', 'file_name'
]);

interface SourceMeta {
  filename?: string;
  document_name?: string;
  page?: number;
  page_number?: number;
  chunk_index?: number;
  metadata?: Record<string, any>;
  [key: string]: any;
}

const markdownComponents = {
  p: ({ children }: any) => <Text fontSize="sm" lineHeight="1.7" mb={2}>{children}</Text>,
  ul: ({ children }: any) => <Box as="ul" pl={4} mb={2}>{children}</Box>,
  ol: ({ children }: any) => <Box as="ol" pl={4} mb={2}>{children}</Box>,
  li: ({ children }: any) => <Text as="li" fontSize="sm" lineHeight="1.7">{children}</Text>,
  code: ({ inline, children, className }: any) => {
    if (inline) {
      return <Code px={1.5} py={0.5} borderRadius="md" colorScheme="gray" fontSize="xs">{children}</Code>;
    }
    if (className) {
      return (
        <Box as="pre" bg="gray.900" color="white" p={3} borderRadius="lg" overflowX="auto" my={2}>
          <Code color="white" bg="transparent" fontSize="xs">{children}</Code>
        </Box>
      );
    }
    return <Text as="span" fontFamily="mono" fontSize="sm" whiteSpace="pre-wrap">{children}</Text>;
  },
  a: ({ href, children }: any) => (
    <Text as="a" href={href} color="blue.500" textDecoration="underline" target="_blank" rel="noreferrer">
      {children}
    </Text>
  ),
};

function SourceCard({ src, index }: { src: string | SourceMeta; index: number }) {
  const [detailsOpen, setDetailsOpen] = useState(false);

  if (typeof src === 'string') {
    const basename = src.split(/[\\/]/).pop() || src;
    return (
      <Box bg="white" borderWidth="1px" borderColor="gray.200" borderRadius="2xl" p={4}>
        <HStack spacing={3} align="flex-start" flexWrap="wrap">
          <Box bg="blue.50" borderRadius="xl" p={2} color="blue.600" flexShrink={0}>
            <Icon as={FaFileAlt} boxSize={4} />
          </Box>
          <Box flex="1" minW={0}>
            <Text fontSize="sm" fontWeight="semibold" color="gray.800" isTruncated>{basename}</Text>
            <Text fontSize="11px" color="gray.500" mt={1}>Referenced source</Text>
            <HStack spacing={2} mt={3} flexWrap="wrap">
              <Badge colorScheme="gray" variant="subtle" fontSize="9px" px={2}>Reference only</Badge>
              <Badge colorScheme="blue" variant="subtle" fontSize="9px" px={2}>Source {index + 1}</Badge>
            </HStack>
          </Box>
        </HStack>
      </Box>
    );
  }

  const filename = src.filename || src.document_name || src.metadata?.filename || src.metadata?.source_file || src.metadata?.file_name || 'Unknown source';
  const page = src.page ?? src.page_number ?? src.metadata?.page ?? src.metadata?.page_number;
  const chunkIndex = src.chunk_index ?? src.metadata?.chunk_index ?? index;
  const similarityScore = src.similarity_score ?? src.metadata?.similarity_score ?? src.score ?? null;
  const contentPreview = src.content_preview || src.metadata?.content_preview || null;
  const safeExtra = src.metadata
    ? Object.entries(src.metadata).filter(
        ([k]) => !HIDDEN_FIELDS.has(k) && k !== 'page' && k !== 'page_number' && k !== 'chunk_index'
      )
    : [];
  const hasDetails = safeExtra.length > 0 || Boolean(contentPreview);

  return (
    <Box bg="white" borderWidth="1px" borderColor="gray.200" borderRadius="2xl" p={4}>
      <HStack spacing={3} align="flex-start" flexWrap="wrap">
        <Box bg="blue.50" borderRadius="xl" p={2} color="blue.600" flexShrink={0}>
          <Icon as={FaFileAlt} boxSize={4} />
        </Box>
        <Box flex="1" minW={0}>
          <HStack spacing={2} align="flex-start" flexWrap="wrap" justify="space-between">
            <Box minW={0} flex="1">
              <Text fontSize="sm" fontWeight="semibold" color="gray.800" isTruncated>{filename}</Text>
              <Text fontSize="11px" color="gray.500" mt={1}>Source {index + 1}</Text>
            </Box>
            <ConfidenceBadge score={similarityScore} />
          </HStack>
          <HStack spacing={2} mt={3} flexWrap="wrap">
            <Badge colorScheme="gray" variant="subtle" fontSize="9px" px={2}>Chunk {chunkIndex + 1}</Badge>
            {page != null && <Badge colorScheme="purple" variant="subtle" fontSize="9px" px={2}>Page {page}</Badge>}
            {similarityScore != null && <Badge colorScheme="gray" variant="subtle" fontSize="9px" px={2}>Score {Number(similarityScore).toFixed(2)}</Badge>}
          </HStack>
        </Box>
      </HStack>

      {contentPreview && (
        <Text fontSize="12px" color="gray.600" mt={3} noOfLines={3}>{contentPreview}</Text>
      )}

      {hasDetails && (
        <Button
          size="xs"
          variant="ghost"
          colorScheme="blue"
          mt={3}
          onClick={() => setDetailsOpen((prev) => !prev)}
          rightIcon={<Icon as={detailsOpen ? FaChevronUp : FaChevronDown} boxSize={2} />}
        >
          {detailsOpen ? 'Hide details' : 'Show details'}
        </Button>
      )}

      {hasDetails && (
        <Collapse in={detailsOpen} animateOpacity>
          <Box mt={3} p={3} bg="gray.50" borderRadius="lg" borderWidth="1px" borderColor="gray.200">
            {contentPreview && (
              <Box mb={3}>
                <Text fontSize="10px" color="gray.500" fontWeight="semibold" textTransform="uppercase" letterSpacing="wider" mb={2}>
                  Retrieved fragment
                </Text>
                <Text fontSize="12px" color="gray.700" whiteSpace="pre-wrap" lineHeight="1.6">
                  {contentPreview}
                </Text>
              </Box>
            )}
            {safeExtra.map(([key, value]) => (
              <HStack key={key} align="flex-start" spacing={2} mt={1}>
                <Text fontSize="10px" color="gray.500" minW="74px" fontWeight="semibold" textTransform="capitalize">
                  {key}
                </Text>
                <Text fontSize="10px" color="gray.600" whiteSpace="pre-wrap">
                  {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </Text>
              </HStack>
            ))}
          </Box>
        </Collapse>
      )}
    </Box>
  );
}

function getConfidenceLabel(score?: number | null) {
  if (score == null) return 'Low';
  if (score >= 0.85) return 'Very High';
  if (score >= 0.7) return 'High';
  if (score >= 0.5) return 'Medium';
  return 'Low';
}

function ConfidenceBadge({ score }: { score?: number | null }) {
  const label = getConfidenceLabel(score);
  const colorScheme = label === 'Very High' || label === 'High'
    ? 'green'
    : label === 'Medium'
      ? 'yellow'
      : 'orange';

  return (
    <Badge colorScheme={colorScheme} variant="subtle" fontSize="9px" px={2} py={0.5}>
      {label}
    </Badge>
  );
}

const ChatBubble = ({ message }: { message: ChatMessage }) => {
  const isUser = message.sender === 'user';
  const hasSources = !isUser && message.sources && message.sources.length > 0;
  const toast = useToast();
  const submitFeedback = useChatStore((s) => s.submitFeedback);
  const [feedbackSent, setFeedbackSent] = useState<'up' | 'down' | null>(message.feedback ?? null);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    toast({ title: 'Copied', status: 'success', duration: 1500, isClosable: true, position: 'bottom-right' });
  };

  const handleFeedback = async (fb: 'up' | 'down') => {
    if (!message.chat_id || feedbackSent) return;
    setFeedbackSent(fb);
    await submitFeedback(message.chat_id, fb);
  };

  const uniqueSources: (string | SourceMeta)[] = [];
  if (hasSources) {
    const seen = new Set<string>();
    for (const src of message.sources!) {
      const key = typeof src === 'string'
        ? (src.split(/[\\/]/).pop() || src)
        : (src.filename || src.document_name || src.metadata?.filename || src.metadata?.source_file || src.metadata?.file_name || JSON.stringify(src));
      if (!seen.has(key)) { seen.add(key); uniqueSources.push(src); }
    }
  }

  return (
    <Flex justify={isUser ? 'flex-end' : 'flex-start'} w="100%" py={3}>
      <HStack spacing={2} maxW={{ base: '100%', md: '100%' }} align="flex-start" justify={isUser ? 'flex-end' : 'flex-start'}>
        {!isUser && (
          <Box borderRadius="full" p={2} bg="blue.500" color="white" shadow="md" flexShrink={0}>
            <Icon as={FaRobot} boxSize={4} />
          </Box>
        )}
        <VStack align={isUser ? 'flex-end' : 'flex-start'} spacing={1.5} maxW="100%">
          <Box
            bg={isUser ? 'linear-gradient(135deg, #2563eb 0%, #3b82f6 100%)' : 'white'}
            color={isUser ? 'white' : 'gray.800'}
            borderWidth={isUser ? '0px' : '1px'}
            borderColor={isUser ? 'transparent' : 'gray.200'}
            borderRadius="xl"
            borderBottomRightRadius={isUser ? 'none' : 'xl'}
            borderBottomLeftRadius={isUser ? 'xl' : 'none'}
            px={4}
            py={3}
            boxShadow="sm"
            fontSize="sm"
            lineHeight="1.55"
            maxW={{ base: '100%', md: isUser ? 'min(60%, 420px)' : '78%' }}
          >
            {message.streaming && message.text === '' ? (
              <HStack spacing={2}><Spinner size="xs" color="blue.400" /><Text fontSize="sm" color="gray.400">Thinking…</Text></HStack>
            ) : (
              <ReactMarkdown components={markdownComponents}>{message.text}</ReactMarkdown>
            )}
            {message.streaming && message.text !== '' && (
              <Spinner size="xs" color="blue.400" ml={1} />
            )}
          </Box>

          {!isUser && !message.streaming && (
            <HStack spacing={3} pt={2} align="center" flexWrap="wrap" w="100%">
              <Tooltip label="Copy response" fontSize="xs">
                <IconButton aria-label="Copy" icon={<FaCopy />} size="xs" variant="ghost"
                  color="gray.400" _hover={{ color: 'blue.500' }} onClick={handleCopy} />
              </Tooltip>
              {message.chat_id && (
                <>
                  <Tooltip label="Good response" fontSize="xs">
                    <IconButton
                      aria-label="Thumbs up"
                      icon={<FaThumbsUp />}
                      size="xs" variant="ghost"
                      color={feedbackSent === 'up' ? 'green.500' : 'gray.400'}
                      _hover={{ color: 'green.500' }}
                      isDisabled={!!feedbackSent}
                      onClick={() => handleFeedback('up')}
                    />
                  </Tooltip>
                  <Tooltip label="Poor response" fontSize="xs">
                    <IconButton
                      aria-label="Thumbs down"
                      icon={<FaThumbsDown />}
                      size="xs" variant="ghost"
                      color={feedbackSent === 'down' ? 'red.500' : 'gray.400'}
                      _hover={{ color: 'red.500' }}
                      isDisabled={!!feedbackSent}
                      onClick={() => handleFeedback('down')}
                    />
                  </Tooltip>
                </>
              )}
            </HStack>
          )}

          {!isUser && !message.streaming && uniqueSources.length > 0 && (
            <VStack spacing={3} align="stretch" mt={5}>
              <Divider borderColor="gray.200" />
              <HStack spacing={2} mb={2} justify="space-between" flexWrap="wrap">
                <Text fontSize="10px" fontWeight="bold" color="gray.400" textTransform="uppercase" letterSpacing="wider">
                  Grounded sources
                </Text>
                <HStack spacing={2} wrap="wrap">
                  <Badge colorScheme="blue" variant="subtle" fontSize="9px" px={2} py={0.5}>
                    {uniqueSources.length} source{uniqueSources.length !== 1 ? 's' : ''}
                  </Badge>
                  <ConfidenceBadge score={uniqueSources.reduce<number | null>((bestScore, src) => {
                    if (typeof src === 'string') return bestScore;
                    const score = src.similarity_score ?? src.metadata?.similarity_score ?? src.score ?? null;
                    if (score == null) return bestScore;
                    if (bestScore == null || score > bestScore) return score;
                    return bestScore;
                  }, null)} />
                </HStack>
              </HStack>
              <VStack spacing={3} align="stretch">
                {uniqueSources.map((src, i) => <SourceCard key={i} src={src} index={i} />)}
              </VStack>
            </VStack>
          )}
        </VStack>

        {isUser && (
          <Box borderRadius="full" p={2} bg="gray.200" color="gray.600" shadow="md" flexShrink={0}>
            <Icon as={FaUser} boxSize={4} />
          </Box>
        )}
      </HStack>
    </Flex>
  );
};

export default ChatBubble;
