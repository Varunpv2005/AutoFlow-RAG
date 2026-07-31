import React, { useState } from "react";
import { Flex, Box, IconButton, Icon } from '@chakra-ui/react';
import { FaBars, FaTimes } from 'react-icons/fa';
import { FilesSidebar } from '../Files';
import { ChatArea } from '../Chat';
import Header from './Header';

interface Props {
  onLogout: () => void;
}

const MainLayout = ({ onLogout }: Props) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <Flex height="100vh" direction="row" overflow="hidden" bg="gray.50">
      <Box
        width={{ base: sidebarCollapsed ? '72px' : '260px', md: sidebarCollapsed ? '80px' : '280px' }}
        minW={{ base: sidebarCollapsed ? '72px' : '260px', md: sidebarCollapsed ? '80px' : '280px' }}
        bg="white"
        borderRightWidth="1px"
        borderColor="gray.100"
        zIndex={5}
        position="relative"
        boxShadow="sm"
      >
        <IconButton
          aria-label={sidebarCollapsed ? 'Expand documents' : 'Collapse documents'}
          icon={<Icon as={sidebarCollapsed ? FaBars : FaTimes} />}
          size="sm"
          variant="ghost"
          position="absolute"
          top={3}
          right={3}
          zIndex={6}
          onClick={() => setSidebarCollapsed((value) => !value)}
        />
        <FilesSidebar collapsed={sidebarCollapsed} />
      </Box>
      <Box
        flex="1"
        display="flex"
        flexDirection="column"
        minWidth={0}
        height="100vh"
        overflow="hidden"
        bgGradient="linear(to-b, #f8fbff 0%, #f6f8fc 100%)"
      >
        <Header onLogout={onLogout} />
        <Box
          flex="1"
          minH={0}
          overflow="hidden"
          px={{ base: 0.5, sm: 1.5, md: 2 }}
          py={{ base: 1, md: 1.5 }}
        >
          <ChatArea />
        </Box>
      </Box>
    </Flex>
  );
};

export default MainLayout;
