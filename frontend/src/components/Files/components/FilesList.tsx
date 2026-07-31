import React from 'react';
import { VStack, Text, Spinner } from '@chakra-ui/react';
import FilePill from './FilePill';
import { FileMeta } from 'state/filesStore';

interface FilesListProps {
  files: FileMeta[];
  loading: boolean;
  deletingId: number | null;
  onDelete: (id: number) => void;
}

const FilesList: React.FC<FilesListProps> = ({ files, loading, deletingId, onDelete }) => {
  if (loading) {
    return <Spinner size="md" mx="auto" my={6} />;
  }
  if (!Array.isArray(files) || files.length === 0) {
    return <Text color="gray.400">No files uploaded yet.</Text>;
  }
  return (
    <VStack align="stretch" spacing={3}>
      {files.map((file) => (
        <FilePill
          key={file.id}
          file={file}
          onDelete={onDelete}
          deleting={deletingId === file.id}
        />
      ))}
    </VStack>

  );
};

export default FilesList;
