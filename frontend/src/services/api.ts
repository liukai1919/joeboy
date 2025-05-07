import axios from 'axios';

const API_URL = `${window.location.protocol}//${window.location.hostname}:8000/api/v1`;

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  messages: Message[];
  max_tokens?: number;
}

export interface ChatResponse {
  response: string;
}

export const chatApi = {
  sendMessage: async (messages: Message[]): Promise<ChatResponse> => {
    const response = await axios.post(`${API_URL}/chat/chat`, { 
      messages,
      max_tokens: 512
    });
    return response.data;
  },
}; 