import { useCallback, useRef } from 'react';
import { useFilesStore } from 'state/filesStore';
import { uploadFile, fetchFiles } from 'api/filesApi';
import { useToast } from '@chakra-ui/react';

const SUPPORTED_EXTENSIONS = ['pdf', 'docx', 'txt', 'csv', 'xlsx'];
const MAX_SIZE_MB = 20;

export function useFileUpload() {
  const setFiles = useFilesStore((state) => state.setFiles);
  const setLoading = useFilesStore((state) => state.setLoading);
  const setError = useFilesStore((state) => state.setError);
  const loading = useFilesStore((state) => state.loading);
  const toast = useToast();
  const uploading = useRef(false);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      if (!file.name) {
        setError('File name is missing.');
        continue;
      }
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (!ext || !SUPPORTED_EXTENSIONS.includes(ext)) {
        toast({ title: 'Unsupported file type', status: 'error', duration: 4000 });
        continue;
      }
      if (file.size > MAX_SIZE_MB * 1024 * 1024) {
        toast({ title: 'File too large', status: 'error', duration: 4000 });
        continue;
      }
      setLoading(true);
      uploading.current = true;
      try {
        await uploadFile(file);
        const backendFiles = await fetchFiles();
        setFiles(backendFiles);
        toast({ title: 'File uploaded', status: 'success', duration: 2000 });
      } catch (error: any) {
        setError(error?.toString() || 'Upload failed');
        toast({ title: 'Upload failed', description: error?.toString(), status: 'error', duration: 4000 });
      } finally {
        setLoading(false);
        uploading.current = false;
      }
    }
  }, [setFiles, setLoading, setError, toast]);

  return { onDrop, loading, uploading };
}
