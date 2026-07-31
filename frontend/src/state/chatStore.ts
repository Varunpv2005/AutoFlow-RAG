import { create } from 'zustand';
import { sendChat as sendChatApi, fetchChatHistory, streamChat as streamChatApi, submitFeedback as submitFeedbackApi } from '../api/chatApi';

export interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
  sources?: any[];
  chat_id?: number | null;
  response_time?: number | null;
  chunk_count?: number | null;
  retrieval_latency_ms?: number | null;
  confidence_score?: number | null;
  retrieved_chunks?: Array<{ chunk_id?: number | string | null; document_name?: string; page_number?: number | null; similarity_score?: number | null; content_preview?: string }>; 
  feedback?: 'up' | 'down' | null;
  streaming?: boolean;   // true while tokens are still arriving
}

interface ChatState {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
  sendMessage: (msg: ChatMessage) => void;
  receiveMessage: (msg: ChatMessage) => void;
  clearChat: () => void;
  loadHistory: () => Promise<void>;
  sendChat: (
    question: string,
    options?: {
      fileId?: string | null;
      keywords?: string[];
      metadataFilter?: Record<string, any>;
      k?: number;
    }
  ) => Promise<void>;
  streamChat: (
    question: string,
    options?: { fileId?: string | null }
  ) => void;
  submitFeedback: (chatId: number, feedback: 'up' | 'down') => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  loading: false,
  error: null,

  sendMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  receiveMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  clearChat: () => set({ messages: [] }),

  loadHistory: async () => {
    set({ loading: true, error: null });
    try {
      const history = await fetchChatHistory();
      set({ messages: history, loading: false, error: null });
    } catch (err: any) {
      set({ loading: false, error: typeof err === 'string' ? err : 'Failed to load history' });
    }
  },

  sendChat: async (question, options) => {
    set({ loading: true, error: null });
    try {
      set((state) => ({ messages: [...state.messages, { sender: 'user', text: question }] }));
      const response = await sendChatApi({ question, ...options });
      set((state) => ({
        messages: [...state.messages, {
          sender: 'ai',
          text: response.answer,
          sources: response.sources,
          chat_id: response.chat_id,
          response_time: response.response_time,
          chunk_count: response.chunk_count,
          retrieval_latency_ms: response.retrieval_latency_ms,
          confidence_score: response.confidence_score,
          retrieved_chunks: response.retrieved_chunks,
        }],
        loading: false,
        error: null,
      }));
    } catch (err: any) {
      set({ loading: false, error: typeof err === 'string' ? err : 'Chat failed' });
    }
  },

  streamChat: (question, options) => {
    set({ loading: true, error: null });
    // Add user message
    set((state) => ({ messages: [...state.messages, { sender: 'user', text: question }] }));
    // Add placeholder AI message that we'll update in-place
    set((state) => ({
      messages: [...state.messages, { sender: 'ai', text: '', streaming: true }]
    }));

    const conversationHistory = get().messages
      .slice(-8)
      .filter((message) => message.sender === 'user' || message.sender === 'ai')
      .map((message) => ({
        role: message.sender === 'user' ? 'user' : 'assistant',
        content: message.text,
      }));

    streamChatApi(
      question,
      options?.fileId ?? null,
      conversationHistory,
      (token) => {
        // Append token to the last AI message
        set((state) => {
          const msgs = [...state.messages];
          const last = msgs[msgs.length - 1];
          if (last?.sender === 'ai') {
            msgs[msgs.length - 1] = { ...last, text: last.text + token };
          }
          return { messages: msgs };
        });
      },
      (meta) => {
        // Streaming complete — attach metadata
        set((state) => {
          const msgs = [...state.messages];
          const last = msgs[msgs.length - 1];
          if (last?.sender === 'ai') {
            msgs[msgs.length - 1] = {
              ...last,
              streaming: false,
              sources: meta.sources,
              chat_id: meta.chat_id,
              response_time: meta.response_time,
              chunk_count: meta.chunk_count,
              retrieval_latency_ms: meta.retrieval_latency_ms,
              confidence_score: meta.confidence_score,
              retrieved_chunks: meta.retrieved_chunks,
            };
          }
          return { messages: msgs, loading: false };
        });
      },
      (errMsg) => {
        set((state) => {
          const msgs = [...state.messages];
          const last = msgs[msgs.length - 1];
          if (last?.sender === 'ai') {
            msgs[msgs.length - 1] = { ...last, text: errMsg || 'Error', streaming: false };
          }
          return { messages: msgs, loading: false, error: null };
        });
      }
    );
  },

  submitFeedback: async (chatId, feedback) => {
    await submitFeedbackApi(chatId, feedback);
    set((state) => ({
      messages: state.messages.map((m) =>
        m.chat_id === chatId ? { ...m, feedback } : m
      ),
    }));
  },
}));
