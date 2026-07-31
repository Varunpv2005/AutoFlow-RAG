import React, { useState, useEffect } from 'react';
import {
  Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton,
  ModalBody, ModalFooter, Button, SimpleGrid, Stat, StatLabel, StatNumber,
  StatHelpText, Box, Heading, Text, Badge, Spinner, Alert, AlertIcon, VStack,
  HStack, Divider, Progress, Icon, Card, CardBody
} from '@chakra-ui/react';
import { FaFileAlt, FaComments, FaUsers, FaDatabase, FaServer, FaBrain, FaClock, FaChartBar } from 'react-icons/fa';
import { fetchAnalytics } from '../../api/analyticsApi';

interface AnalyticsData {
  users: number;
  total_documents: number;
  user_documents: number;
  total_chats: number;
  user_chats: number;
  chunks: number;
  indexed_documents?: number;
  pending_documents?: number;
  total_queries?: number;
  average_retrieval_latency?: number;
  average_llm_response_time?: number;
  embedding_generation_time?: number;
  status: {
    database: string;
    gemini: string;
    faiss: string;
  };
}

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function AnalyticsModal({ isOpen, onClose }: Props) {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      setError(null);
      fetchAnalytics()
        .then((res) => {
          setData(res);
          setLoading(false);
        })
        .catch((err) => {
          setError(err?.toString() || 'Failed to fetch analytics');
          setLoading(false);
        });
    }
  }, [isOpen]);

  const docPercentage = data && data.total_documents > 0 ? (data.user_documents / data.total_documents) * 100 : 0;
  const chatPercentage = data && data.total_chats > 0 ? (data.user_chats / data.total_chats) * 100 : 0;

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="lg" isCentered>
      <ModalOverlay />
      <ModalContent borderRadius="2xl" boxShadow="2xl">
        <ModalHeader borderBottomWidth={1} borderColor="gray.100" color="blue.600" py={5}>
          Workspace Insights & Analytics
        </ModalHeader>
        <ModalCloseButton mt={2} />
        <ModalBody py={6}>
          {loading && (
            <Box display="flex" justifyContent="center" py={12}>
              <Spinner color="blue.500" size="xl" thickness="3px" />
            </Box>
          )}

          {error && (
            <Alert status="error" rounded="xl" mb={4}>
              <AlertIcon />
              {error}
            </Alert>
          )}

          {!loading && !error && data && (
            <VStack spacing={6} align="stretch">
              {/* User stats */}
              <Box>
                <Heading size="xs" textTransform="uppercase" color="gray.400" letterSpacing="wider" mb={4}>
                  Your Allocation
                </Heading>
                <SimpleGrid columns={2} spacing={4}>
                  <Card variant="outline" borderRadius="2xl" bg="blue.50" border="none">
                    <CardBody p={4}>
                      <HStack spacing={3} mb={2}>
                        <Icon as={FaFileAlt} color="blue.500" boxSize={5} />
                        <Text fontSize="xs" fontWeight="bold" color="blue.700" textTransform="uppercase">Documents</Text>
                      </HStack>
                      <Stat>
                        <StatNumber fontSize="2xl" color="blue.900">{data.user_documents}</StatNumber>
                        <StatHelpText color="gray.600" fontSize="xs">
                          {data.user_documents} of {data.total_documents} total files
                        </StatHelpText>
                      </Stat>
                      <Progress value={docPercentage} size="xs" colorScheme="blue" borderRadius="full" mt={2} bg="blue.100" />
                    </CardBody>
                  </Card>

                  <Card variant="outline" borderRadius="2xl" bg="purple.50" border="none">
                    <CardBody p={4}>
                      <HStack spacing={3} mb={2}>
                        <Icon as={FaComments} color="purple.500" boxSize={5} />
                        <Text fontSize="xs" fontWeight="bold" color="purple.700" textTransform="uppercase">Conversations</Text>
                      </HStack>
                      <Stat>
                        <StatNumber fontSize="2xl" color="purple.900">{data.user_chats}</StatNumber>
                        <StatHelpText color="gray.600" fontSize="xs">
                          {data.user_chats} of {data.total_chats} total chats
                        </StatHelpText>
                      </Stat>
                      <Progress value={chatPercentage} size="xs" colorScheme="purple" borderRadius="full" mt={2} bg="purple.100" />
                    </CardBody>
                  </Card>
                </SimpleGrid>
              </Box>

              <Divider />

              {/* System usage */}
              <Box>
                <Heading size="xs" textTransform="uppercase" color="gray.400" letterSpacing="wider" mb={4}>
                  Global Metrics
                </Heading>
                <SimpleGrid columns={3} spacing={3}>
                  <Box p={3} borderWidth={1} borderColor="gray.100" borderRadius="xl" textAlign="center" bg="gray.50">
                    <Icon as={FaUsers} color="gray.400" mb={1} />
                    <Stat>
                      <StatLabel fontSize="10px" color="gray.500">Active Users</StatLabel>
                      <StatNumber fontSize="lg" color="gray.700">{data.users}</StatNumber>
                    </Stat>
                  </Box>
                  <Box p={3} borderWidth={1} borderColor="gray.100" borderRadius="xl" textAlign="center" bg="gray.50">
                    <Icon as={FaDatabase} color="gray.400" mb={1} />
                    <Stat>
                      <StatLabel fontSize="10px" color="gray.500">Total Chunks</StatLabel>
                      <StatNumber fontSize="lg" color="gray.700">{data.chunks}</StatNumber>
                    </Stat>
                  </Box>
                  <Box p={3} borderWidth={1} borderColor="gray.100" borderRadius="xl" textAlign="center" bg="gray.50">
                    <Icon as={FaFileAlt} color="gray.400" mb={1} />
                    <Stat>
                      <StatLabel fontSize="10px" color="gray.500">Global Docs</StatLabel>
                      <StatNumber fontSize="lg" color="gray.700">{data.total_documents}</StatNumber>
                    </Stat>
                  </Box>
                </SimpleGrid>
                <SimpleGrid columns={2} spacing={3} mt={3}>
                  <Box p={3} borderWidth={1} borderColor="gray.100" borderRadius="xl" bg="green.50">
                    <HStack spacing={2} align="center" mb={2}>
                      <Icon as={FaFileAlt} color="green.500" />
                      <Text fontSize="10px" fontWeight="bold" color="green.700" textTransform="uppercase">Index Health</Text>
                    </HStack>
                    <Text fontSize="lg" fontWeight="bold" color="green.900">{data.indexed_documents ?? 0} indexed</Text>
                    <Text fontSize="xs" color="gray.600">{data.pending_documents ?? 0} pending</Text>
                  </Box>
                  <Box p={3} borderWidth={1} borderColor="gray.100" borderRadius="xl" bg="purple.50">
                    <HStack spacing={2} align="center" mb={2}>
                      <Icon as={FaChartBar} color="purple.500" />
                      <Text fontSize="10px" fontWeight="bold" color="purple.700" textTransform="uppercase">Retrieval Efficiency</Text>
                    </HStack>
                    <Text fontSize="lg" fontWeight="bold" color="purple.900">{data.total_queries ?? 0} queries</Text>
                    <Text fontSize="xs" color="gray.600">{(data.average_retrieval_latency ?? 0).toFixed(3)}s avg retrieval</Text>
                  </Box>
                </SimpleGrid>
              </Box>

              <Divider />

              {/* Service Health */}
              <Box>
                <Heading size="xs" textTransform="uppercase" color="gray.400" letterSpacing="wider" mb={4}>
                  Infrastructure Status
                </Heading>
                <VStack align="stretch" spacing={3}>
                  <HStack justify="space-between" p={3} borderWidth="1px" borderColor="gray.100" borderRadius="xl" bg="gray.50">
                    <HStack spacing={2.5}>
                      <Icon as={FaServer} color="blue.500" />
                      <Text fontSize="xs" fontWeight="semibold" color="gray.700">SQLite Database</Text>
                    </HStack>
                    <Badge colorScheme={data.status.database === 'OK' ? 'green' : 'red'} px={2.5} py={0.5} borderRadius="full" fontSize="10px">
                      {data.status.database === 'OK' ? 'Online' : 'Offline'}
                    </Badge>
                  </HStack>

                  <HStack justify="space-between" p={3} borderWidth="1px" borderColor="gray.100" borderRadius="xl" bg="gray.50">
                    <HStack spacing={2.5}>
                      <Icon as={FaBrain} color="purple.500" />
                      <Text fontSize="xs" fontWeight="semibold" color="gray.700">Google Gemini LLM</Text>
                    </HStack>
                    <Badge colorScheme={data.status.gemini.startsWith('OK') || data.status.gemini === 'Connected' ? 'green' : 'red'} px={2.5} py={0.5} borderRadius="full" fontSize="10px">
                      {data.status.gemini.startsWith('OK') || data.status.gemini === 'Connected' ? 'Connected' : 'Error'}
                    </Badge>
                  </HStack>

                  <HStack justify="space-between" p={3} borderWidth="1px" borderColor="gray.100" borderRadius="xl" bg="gray.50">
                    <HStack spacing={2.5}>
                      <Icon as={FaDatabase} color="green.500" />
                      <Text fontSize="xs" fontWeight="semibold" color="gray.700">FAISS Index</Text>
                    </HStack>
                    <Badge colorScheme={data.status.faiss === 'OK' ? 'green' : 'yellow'} px={2.5} py={0.5} borderRadius="full" fontSize="10px">
                      {data.status.faiss === 'OK' ? 'Active' : 'Uninitialized'}
                    </Badge>
                  </HStack>

                  <HStack justify="space-between" p={3} borderWidth="1px" borderColor="gray.100" borderRadius="xl" bg="gray.50">
                    <HStack spacing={2.5}>
                      <Icon as={FaClock} color="orange.500" />
                      <Text fontSize="xs" fontWeight="semibold" color="gray.700">LLM Response Time</Text>
                    </HStack>
                    <Text fontSize="xs" color="gray.700">{(data.average_llm_response_time ?? 0).toFixed(3)}s</Text>
                  </HStack>
                </VStack>
              </Box>
            </VStack>
          )}
        </ModalBody>
        <ModalFooter borderTopWidth={1} borderColor="gray.100" py={4}>
          <Button onClick={onClose} colorScheme="blue" borderRadius="xl" size="sm">Close</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
