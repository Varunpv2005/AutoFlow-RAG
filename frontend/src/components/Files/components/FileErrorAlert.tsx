import React from 'react';
import { Alert, AlertIcon } from '@chakra-ui/react';

interface FileErrorAlertProps {
  error: string | null;
}

const FileErrorAlert: React.FC<FileErrorAlertProps> = ({ error }) => {
  if (!error) return null;
  return (
    <Alert status="error" mb={2} borderRadius="md">
      <AlertIcon />
      {error}
    </Alert>
  );
};

export default FileErrorAlert;
