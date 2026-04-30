export interface ApiResponse<T = any> {
  status: string;
  data?: T;
  message?: string;
  error?: string;
}

export interface GmailStatus {
  status: 'connected' | 'error' | 'offline';
  service: string;
}

export interface WhatsAppStatus {
  status: 'configured' | 'not_configured' | 'error';
  service: string;
  number?: string;
}

export interface HealthCheck {
  status: string;
  timestamp: string;
  version: string;
  channels: {
    email: boolean;
    whatsapp: boolean;
    web_form: boolean;
  };
}

export interface WhatsAppSendRequest {
  to: string;
  message: string;
}

export interface WhatsAppQueryRequest {
  phone_number: string;
  query: string;
}

export interface WhatsAppSendResponse {
  status: string;
  to: string;
  message_sid: string;
}

export interface WhatsAppQueryResponse {
  status: string;
  message: string;
  question_sid: string;
  answer_sid: string;
  response_preview: string;
}

export interface ChannelMetrics {
  email: {
    total_conversations: number;
    resolved_count: number;
    failed_count: number;
    success_rate: number;
  };
  whatsapp: {
    total_conversations: number;
    resolved_count: number;
    failed_count: number;
    success_rate: number;
  };
}

export interface ActivityData {
  email: Array<{ time: string; emails: number }>;
  whatsapp: Array<{ time: string; messages: number }>;
}
