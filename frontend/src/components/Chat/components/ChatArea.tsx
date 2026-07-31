import React, { useRef, useEffect } from 'react';
import {
  Box, VStack, Spinner, Flex, Alert, AlertIcon, Heading, Text, SimpleGrid, Icon, Card, CardBody, HStack
} from '@chakra-ui/react';
import { useChatStore } from 'state/chatStore';
import ChatBubble from './ChatBubble';
import ChatInput from './ChatInput';
import { useFilesStore } from 'state/filesStore';
import { FaBrain, FaFileAlt, FaQuestionCircle, FaMagic } from 'react-icons/fa';

const quickPrompts = [
  {
    label: 'Summarize this file',
    detail: 'Get a concise executive summary and key takeaways.',
    icon: FaFileAlt,
    prompt: 'Can you provide a high-level summary of the active document?',
    color: 'blue',
  },
  {
    label: 'Extract key concepts',
    detail: 'Surface important terminology and ideas quickly.',
    icon: FaMagic,
    prompt: 'Explain the main terminology and concepts discussed in the file.',
    color: 'purple',
  },
  {
    label: 'Find likely questions',
    detail: 'Generate the most useful questions this document answers.',
    icon: FaQuestionCircle,
    prompt: 'What are the top 3 questions this document answers?',
    color: 'green',
  },
];

const ChatArea = () => {
  const messages = useChatStore((state) => state.messages);
  const files = useFilesStore((state) => state.files);
  const noFiles = !files || files.length === 0;
  const loading = useChatStore((state) => state.loading);
  const error = useChatStore((state) => state.error);
  const loadHistory = useChatStore((state) => state.loadHistory);
  const streamChat = useChatStore((state) => state.streamChat);

  const chatScrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleQuickAction = (question: string) => {
    streamChat(question);
  };

  const renderWelcome = () => (
    <VStack spacing={3} align="center" justify="center" h="100%" py={4} px={2}>
      <Box p={1.5} bg="blue.50" borderRadius="2xl" color="blue.600">
        <Icon as={FaBrain} boxSize={8} />
      </Box>
      <VStack spacing={0} textAlign="center">
        <Heading size="md" color="gray.800">Your AI knowledge workspace</Heading>
        <Text color="gray.500" maxW="lg" fontSize="sm">
          Ask your documents questions naturally and get grounded answers with sources.
        </Text>
      </VStack>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={1.5} w="100%" maxW="680px">
        {quickPrompts.map((item) => (
          <Card
            key={item.label}
            variant="outline"
            borderRadius="xl"
            cursor="pointer"
            _hover={{ borderColor: `${item.color}.300`, bg: `${item.color}.50` }}
            onClick={() => handleQuickAction(item.prompt)}
          >
            <CardBody p={2}>
              <HStack spacing={2} align="flex-start">
                <Box p={1.5} bg={`${item.color}.50`} borderRadius="lg" color={`${item.color}.500`}>
                  <Icon as={item.icon} boxSize={4} />
                </Box>
                <Box>
                  <Text fontSize="sm" fontWeight="semibold" color="gray.700">{item.label}</Text>
                  <Text fontSize="xs" color="gray.500" mt={1}>{item.detail}</Text>
                </Box>
              </HStack>
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>
    </VStack>
  );

  return (
    <Flex direction="column" h="100%" minH={0} flex="1" px={{ base: 0, md: 0 }} pb={{ base: 3, md: 1 }}>
      <Box flex="1" minH={0} overflow="hidden">
        {noFiles ? (
          <Box h="100%" borderWidth="1px" borderColor="gray.100" borderRadius="2xl" bg="white" boxShadow="sm" px={{ base: 2, md: 3 }} py={2}>
            {renderWelcome()}
          </Box>
        ) : (
          <>
            {error && (
              <Alert status="error" borderRadius="lg" mb={3}>
                <AlertIcon />
                <Text fontSize="sm">{error}</Text>
              </Alert>
            )}
            <Box mb={3} p={2.5} bg="gray.50" borderWidth="1px" borderColor="gray.100" borderRadius="2xl">
              <HStack spacing={2} flexWrap="wrap">
                <HStack spacing={2} bg="white" p={1.5} borderRadius="xl" borderWidth="1px" borderColor="gray.100">
                  <Icon as={FaFileAlt} boxSize={4} color="blue.500" />
                  <Text fontSize="11px" color="gray.600">{files.length} document{files.length !== 1 ? 's' : ''} loaded</Text>
                </HStack>
                <HStack spacing={2} bg="white" p={1.5} borderRadius="xl" borderWidth="1px" borderColor="gray.100">
                  <Icon as={FaBrain} boxSize={4} color="purple.500" />
                  <Text fontSize="11px" color="gray.600">Source-backed answers</Text>
                </HStack>
              </HStack>
            </Box>
            <Box
              ref={chatScrollRef}
              h="100%"
              overflowY="auto"
              w="100%"
              px={{ base: 1, md: 1 }}
              py={1}
              tabIndex={0}
              aria-label="Chat messages"
              borderWidth="1px"
              borderColor="gray.100"
              bg="white"
              borderRadius="2xl"
              boxShadow="sm"
            >
              {messages.length === 0 ? (
                renderWelcome()
              ) : (
                <VStack spacing={6} align="stretch" w="100%">
                  {messages.map((msg, idx) => (
                    <ChatBubble key={`${msg.sender}-${idx}`} message={msg} />
                  ))}
                  {loading && (
                    <Box alignSelf="flex-start" p={2}>
                      <Spinner size="sm" color="blue.400" />
                    </Box>
                  )}
                </VStack>
              )}
            </Box>
          </>
        )}
      </Box>
      <Box mt={3} px={{ base: 0, md: 0.5 }}>
        <ChatInput />
      </Box>
    </Flex>
  );
};

export default ChatArea;
