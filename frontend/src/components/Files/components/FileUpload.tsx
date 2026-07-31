
import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Text, Spinner } from '@chakra-ui/react';
import { useFileUpload } from '../hooks/useFileUpload';

const FileUpload = () => {
  const { onDrop, loading, uploading } = useFileUpload();
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, multiple: true });

  return (
    <Box
      {...getRootProps()}
      border="2px dashed"
      borderColor={isDragActive ? 'blue.400' : 'gray.200'}
      borderRadius="md"
      p={4}
      textAlign="center"
      bg={isDragActive ? 'blue.50' : 'gray.50'}
      cursor="pointer"
      mb={2}
      position="relative"
    >
      <input {...getInputProps()} />
      {loading && uploading.current ? <Spinner size="sm" position="absolute" right={2} top={2} /> : null}
      <Text color="gray.500">
        {isDragActive ? 'Drop the files here...' : 'Drag & drop or click to upload'}
      </Text>
    </Box>
  );
};

export default FileUpload;
