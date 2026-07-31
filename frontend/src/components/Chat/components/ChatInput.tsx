import React, { useRef, useState } from 'react';
import { Box, HStack, Textarea, IconButton, Spinner, Tooltip, ButtonGroup, useToast, Text } from '@chakra-ui/react';
import { FaPaperPlane, FaFilePdf, FaFileCode } from 'react-icons/fa';
import { useChatStore } from 'state/chatStore';
import { useFilesStore } from 'state/filesStore';

const ChatInput = () => {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const streamChat = useChatStore((state) => state.streamChat);
  const loading = useChatStore((state) => state.loading);
  const error = useChatStore((state) => state.error);
  const messages = useChatStore((state) => state.messages);
  const toast = useToast();
  const files = useFilesStore((state) => state.files);
  const chatDisabled = !files || files.length === 0;

  const handleSend = () => {
    if (!value.trim() || loading || chatDisabled) return;
    streamChat(value);
    setValue('');
    requestAnimationFrame(() => textareaRef.current?.focus());
  };

  const handleExportMarkdown = () => {
    if (messages.length === 0) return;
    const md = messages
      .map((m) => `**${m.sender === 'user' ? 'You' : 'AutoFlow-RAG'}:** ${m.text}`)
      .join('\n\n---\n\n');
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-export-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
    toast({ title: 'Exported as Markdown', status: 'success', duration: 2000, isClosable: true, position: 'bottom-right' });
  };

  const handleExportPDF = () => {
    if (messages.length === 0) return;
    const win = window.open('', '_blank');
    if (!win) return;
    const html = `<!DOCTYPE html><html><head><title>AutoFlow-RAG Chat Export</title>
      <style>body{font-family:sans-serif;max-width:800px;margin:40px auto;line-height:1.6}
      .user{background:#ebf8ff;padding:12px 16px;border-radius:12px;margin:8px 0}
      .ai{background:#f7fafc;padding:12px 16px;border-radius:12px;margin:8px 0;border-left:3px solid #3182ce}
      .label{font-size:11px;font-weight:bold;text-transform:uppercase;color:#718096;margin-bottom:4px}
      </style></head><body>
      <h2>AutoFlow-RAG — Chat Export</h2>
      <p style="color:#718096;font-size:12px">${new Date().toLocaleString()}</p>
      ${messages.map((m) => `
        <div class="${m.sender === 'user' ? 'user' : 'ai'}">
          <div class="label">${m.sender === 'user' ? 'You' : 'AutoFlow-RAG'}</div>
          <div>${m.text.replace(/\n/g, '<br/>')}</div>
        </div>`).join('')}
      </body></html>`;
    win.document.write(html);
    win.document.close();
    win.focus();
    setTimeout(() => { win.print(); win.close(); }, 500);
  };

  React.useEffect(() => {
    if (error) {
      toast({ title: 'Chat Error', description: error, status: 'error', duration: 4000, isClosable: true, position: 'top' });
    }
  }, [error, toast]);

  return (
    <Box borderWidth="1px" borderColor="gray.100" borderRadius="2xl" bg="white" boxShadow="sm" p={3}>
      <HStack spacing={3} align="flex-end">
        <Textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={chatDisabled ? 'Please upload a file to start chatting' : 'Ask anything about your documents…'}
          isDisabled={chatDisabled || loading}
          minH="38px"
          maxH="120px"
          resize="none"
          rows={1}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <IconButton
          aria-label="Send"
          icon={loading ? <Spinner size="sm" /> : <FaPaperPlane />}
          onClick={handleSend}
          isDisabled={chatDisabled || loading || !value.trim()}
          colorScheme="blue"
        />
      </HStack>
      <HStack justify="space-between" pt={1.5}>
        <Text fontSize="10px" color="gray.400">Enter to send • Shift+Enter new line</Text>
        <ButtonGroup size="xs" variant="ghost" isAttached>
          <Tooltip label="Export as Markdown" fontSize="xs">
            <IconButton
              aria-label="Export Markdown"
              icon={<FaFileCode />}
              color="gray.400"
              _hover={{ color: 'green.500' }}
              isDisabled={messages.length === 0}
              onClick={handleExportMarkdown}
            />
          </Tooltip>
          <Tooltip label="Export as PDF" fontSize="xs">
            <IconButton
              aria-label="Export PDF"
              icon={<FaFilePdf />}
              color="gray.400"
              _hover={{ color: 'red.500' }}
              isDisabled={messages.length === 0}
              onClick={handleExportPDF}
            />
          </Tooltip>
        </ButtonGroup>
      </HStack>
    </Box>
  );
};

export default ChatInput;
