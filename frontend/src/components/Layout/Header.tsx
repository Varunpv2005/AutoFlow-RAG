import React from "react";
import { Flex, Text, Button, useDisclosure, HStack, VStack, Box, Badge, Icon } from '@chakra-ui/react';
import { FaBrain, FaChartLine } from 'react-icons/fa';
import LLMStatus from './LLMStatus';
import AnalyticsModal from '../Analytics/AnalyticsModal';

interface Props {
  onLogout: () => void;
}

const Header = ({ onLogout }: Props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Flex
      as="header"
      align="center"
      px={{ base: 3, md: 4 }}
      py={2}
      borderBottomWidth="1px"
      borderColor="gray.100"
      bg="whiteAlpha.90"
      backdropFilter="blur(12px)"
      zIndex={10}
      justify="space-between"
    >
      <HStack spacing={2}>
        <Box p={2} bg="blue.50" borderRadius="xl" color="blue.600">
          <Icon as={FaBrain} boxSize={4} />
        </Box>
        <VStack align="start" spacing={0}>
          <Text fontWeight="bold" fontSize="lg" color="gray.800">AutoFlow-RAG</Text>
          <HStack spacing={2}>
            <Text fontSize="11px" color="gray.500">Conversation-first RAG workspace</Text>
            <Badge colorScheme="green" variant="subtle" fontSize="9px">Online</Badge>
          </HStack>
        </VStack>
      </HStack>

      <HStack spacing={2}>
        <Button leftIcon={<Icon as={FaChartLine} />} size="xs" colorScheme="blue" variant="ghost" onClick={onOpen}>
          Analytics
        </Button>
        <LLMStatus />
        <Button size="xs" variant="outline" colorScheme="red" onClick={onLogout}>
          Logout
        </Button>
      </HStack>

      <AnalyticsModal isOpen={isOpen} onClose={onClose} />
    </Flex>
  );
};

export default Header;
