import axios from 'axios';
import { getToken } from './authApi';

const authHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export interface ChatOptions {
  question: string;
  fileId?: string | null;
  keywords?: string[]
  metadataFilter?: Record<string, any>;
  k?: number;
  conversationHistory?: Array<{ role: 'user' | 'assistant'; content: string }>;
}

export const sendChat = async (
  optsOrFileId: ChatOptions | string | null,
  question?: string
) => {
  if (
    optsOrFileId &&
    typeof optsOrFileId === 'object' &&
    ('question' in optsOrFileId || 'fileId' in optsOrFileId)
  ) {
    const response = await axios.post(
      '/api/chat',
      {
        question: optsOrFileId.question,
        file_id: optsOrFileId.fileId,
        keywords: optsOrFileId.keywords,
        metadata_filter: optsOrFileId.metadataFilter,
        k: optsOrFileId.k,
        conversation_history: optsOrFileId.conversationHistory,
      },
      { headers: authHeaders() }
    );
    return response.data;
  }
  try {
    const response = await axios.post(
      '/api/chat',
      { question, file_id: optsOrFileId },
      { headers: authHeaders() }
    );
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'Chat request failed';
  }
};

export const fetchChatHistory = async () => {
  try {
    const response = await axios.get('/api/chat/history', {
      headers: authHeaders()
    });
    return response.data;
  } catch (error: any) {
    throw error?.response?.data?.detail || 'Fetching chat history failed';
  }
};

/** Submit 👍 / 👎 feedback for an AI response */
export const submitFeedback = async (chatId: number, feedback: 'up' | 'down') => {
  try {
    await axios.post(
      '/api/chat/feedback',
      { chat_id: chatId, feedback },
      { headers: authHeaders() }
    );
  } catch {
    // Feedback is best-effort; silently ignore errors
  }
};

/** Fetch recent activity */
export const fetchActivity = async () => {
  const response = await axios.get('/api/activity', { headers: authHeaders() });
  return response.data;
};

/**
 * Open a streaming SSE connection to /api/chat/stream.
 * Calls onToken for each word chunk, onDone when finished.
 */
export const streamChat = (
  question: string,
  fileId: string | null | undefined,
  conversationHistory: Array<{ role: 'user' | 'assistant'; content: string }> | undefined,
  onToken: (text: string) => void,
  onDone: (meta: { sources: any[]; chat_id: number | null; response_time: number | null; chunk_count: number; retrieval_latency_ms?: number | null; confidence_score?: number | null; retrieved_chunks?: any[] }) => void,
  onError?: (msg: string) => void
): (() => void) => {
  const token = getToken();
  const params = new URLSearchParams({ question });
  if (fileId) params.append('file_id', fileId);
  if (conversationHistory && conversationHistory.length > 0) {
    params.append('conversation_history', JSON.stringify(conversationHistory));
  }

  const url = `/api/chat/stream?${params.toString()}`;
  const es = new EventSource(
    url + (token ? `&_auth=${encodeURIComponent(token)}` : '')
  );

  // EventSource doesn't support custom headers; we pass token as query param
  // The backend reads it via a middleware or the standard Depends(get_current_user).
  // Since FastAPI's OAuth2PasswordBearer reads the Authorization header only,
  // we fall back to a standard fetch-based SSE with the header.
  es.close(); // close the native EventSource immediately

  // Use fetch + ReadableStream instead so we can send Authorization header
  let cancelled = false;
  const controller = new AbortController();

  fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
    signal: controller.signal,
  }).then(async (res) => {
    if (!res.ok || !res.body) {
      onError?.('Stream connection failed');
      return;
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (!cancelled) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() ?? '';
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const evt = JSON.parse(line.slice(6));
          if (evt.type === 'token') onToken(evt.text);
          else if (evt.type === 'done') onDone(evt);
          else if (evt.type === 'error') onError?.(evt.text);
        } catch (parseError) {
          // Ignore malformed SSE events and continue streaming.
          console.warn('Failed to parse stream event', parseError);
        }
      }
    }
  }).catch((err) => {
    if (!cancelled) onError?.(String(err));
  });

  return () => {
    cancelled = true;
    controller.abort();
  };
};
