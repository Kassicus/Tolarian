import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import Cookies from 'js-cookie';

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  errors?: Record<string, any>;
  pagination?: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
    has_prev: boolean;
    has_next: boolean;
  };
}

// User types
export interface User {
  id: number | string;
  email: string;
  role: 'viewer' | 'editor' | 'admin';
  created_at: string;
  full_name: string;
  username?: string;
  avatar_url?: string;
}

// Content types
export interface Content {
  id: string;
  title: string;
  slug: string;
  body?: string;
  content_type: 'document' | 'template' | 'guide' | 'link';
  category?: string;
  tags?: string[];
  author_id: string;
  status: 'draft' | 'published' | 'archived';
  is_featured?: boolean;
  view_count?: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

// Category type
export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
}

// API Client class
class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
      withCredentials: true, // Send cookies with requests
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for authentication
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = Cookies.get('auth_token');
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError<ApiResponse>) => {
        if (error.response?.status === 401) {
          // Handle unauthorized - redirect to login
          Cookies.remove('auth_token');
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication endpoints
  async login(email: string, password: string, remember: boolean = false): Promise<ApiResponse<{ user: User }>> {
    const response = await this.client.post<ApiResponse>('/api/v1/auth/login', {
      email,
      password,
      remember,
    });

    // Store session if successful
    if (response.data.success && response.data.data?.session_id) {
      Cookies.set('session_id', response.data.data.session_id, { expires: remember ? 30 : undefined });
    }

    return response.data;
  }

  async logout(): Promise<ApiResponse> {
    const response = await this.client.post<ApiResponse>('/api/v1/auth/logout');
    Cookies.remove('auth_token');
    Cookies.remove('session_id');
    return response.data;
  }

  async register(email: string, password: string, password_confirm: string): Promise<ApiResponse<{ user: User }>> {
    const response = await this.client.post<ApiResponse>('/api/v1/auth/register', {
      email,
      password,
      password_confirm,
    });
    return response.data;
  }

  async checkAuth(): Promise<ApiResponse<{ authenticated: boolean; user?: User }>> {
    const response = await this.client.get<ApiResponse>('/api/v1/auth/check');
    return response.data;
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    const response = await this.client.get<ApiResponse>('/api/v1/auth/profile');
    return response.data;
  }

  async getProfile(): Promise<ApiResponse<User>> {
    const response = await this.client.get<ApiResponse>('/api/v1/auth/profile');
    return response.data;
  }

  async updateProfile(data: Partial<User>): Promise<ApiResponse<User>> {
    const response = await this.client.put<ApiResponse>('/api/v1/auth/profile', data);
    return response.data;
  }

  // Content endpoints
  async getContent(params?: {
    page?: number;
    per_page?: number;
    category?: string;
    search?: string;
    sort?: string;
    order?: 'asc' | 'desc';
  }): Promise<ApiResponse<Content[]>> {
    const response = await this.client.get<ApiResponse>('/api/v1/content', { params });
    return response.data;
  }

  async getContentById(id: string): Promise<ApiResponse<Content>> {
    const response = await this.client.get<ApiResponse>(`/api/v1/content/${id}`);
    return response.data;
  }

  async createContent(data: {
    title: string;
    category: string;
    content: string;
    tags?: string[];
  }): Promise<ApiResponse<Content>> {
    const response = await this.client.post<ApiResponse>('/api/v1/content', data);
    return response.data;
  }

  async updateContent(id: string, data: Partial<Content>): Promise<ApiResponse<Content>> {
    const response = await this.client.put<ApiResponse>(`/api/v1/content/${id}`, data);
    return response.data;
  }

  async deleteContent(id: string): Promise<ApiResponse> {
    const response = await this.client.delete<ApiResponse>(`/api/v1/content/${id}`);
    return response.data;
  }

  async getCategories(): Promise<ApiResponse<Category[]>> {
    const response = await this.client.get<ApiResponse>('/api/v1/content/categories');
    return response.data;
  }

  // Search endpoints
  async search(query: string, category?: string, limit?: number): Promise<ApiResponse<Content[]>> {
    const response = await this.client.get<ApiResponse>('/api/v1/search', {
      params: { q: query, category, limit },
    });
    return response.data;
  }

  async searchSuggestions(query: string, limit: number = 10): Promise<ApiResponse<Array<{ id: string; title: string; category: string }>>> {
    const response = await this.client.get<ApiResponse>('/api/v1/search/suggestions', {
      params: { q: query, limit },
    });
    return response.data;
  }

  // User endpoints
  async getUsers(page: number = 1, per_page: number = 20): Promise<ApiResponse<User[]>> {
    const response = await this.client.get<ApiResponse>('/api/v1/users', {
      params: { page, per_page },
    });
    return response.data;
  }

  async getUserById(id: string): Promise<ApiResponse<User>> {
    const response = await this.client.get<ApiResponse>(`/api/v1/users/${id}`);
    return response.data;
  }

  async getUserContent(userId: string, page: number = 1, per_page: number = 20): Promise<ApiResponse<Content[]>> {
    const response = await this.client.get<ApiResponse>(`/api/v1/users/${userId}/content`, {
      params: { page, per_page },
    });
    return response.data;
  }

  async getUserStats(): Promise<ApiResponse<{
    total_users: number;
    admin_count: number;
    user_count: number;
    top_contributors: Array<{ id: string; email: string; content_count: number }>;
  }>> {
    const response = await this.client.get<ApiResponse>('/api/v1/users/stats');
    return response.data;
  }
}

// Export singleton instance
const apiClient = new ApiClient();
export default apiClient;