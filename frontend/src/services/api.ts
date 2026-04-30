import axios from 'axios';
import type { GmailStatus, WhatsAppStatus, HealthCheck, WhatsAppSendRequest, WhatsAppQueryRequest, WhatsAppSendResponse, WhatsAppQueryResponse, ChannelMetrics, ActivityData } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health Check
  getHealth: async (): Promise<HealthCheck> => {
    const response = await api.get<HealthCheck>('/health');
    return response.data;
  },

  // Gmail APIs
  getGmailStatus: async (): Promise<GmailStatus> => {
    const response = await api.get<GmailStatus>('/gmail/status');
    return response.data;
  },

  checkEmails: async (): Promise<{ status: string }> => {
    const response = await api.get('/gmail/check-emails');
    return response.data;
  },

  submitQuery: async (data: { user_email: string; user_name?: string; query: string }): Promise<{ status: string; message: string; response_preview: string }> => {
    const response = await api.post('/gmail/submit-query', data);
    return response.data;
  },

  // WhatsApp APIs
  getWhatsAppStatus: async (): Promise<WhatsAppStatus> => {
    const response = await api.get<WhatsAppStatus>('/whatsapp/status');
    return response.data;
  },

  sendWhatsApp: async (data: WhatsAppSendRequest): Promise<WhatsAppSendResponse> => {
    const response = await api.post<WhatsAppSendResponse>('/whatsapp/send', data);
    return response.data;
  },

  submitWhatsAppQuery: async (data: WhatsAppQueryRequest): Promise<WhatsAppQueryResponse> => {
    const response = await api.post<WhatsAppQueryResponse>('/whatsapp/submit-query', data);
    return response.data;
  },

  // Metrics APIs
  getChannelMetrics: async (): Promise<ChannelMetrics> => {
    const response = await api.get<ChannelMetrics>('/metrics/channels');
    return response.data;
  },

  getActivityMetrics: async (hours: number = 7): Promise<ActivityData> => {
    const response = await api.get<ActivityData>(`/metrics/activity?hours=${hours}`);
    return response.data;
  },
};

export default api;
