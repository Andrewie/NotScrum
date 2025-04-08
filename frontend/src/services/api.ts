import axios, { AxiosResponse, AxiosError } from 'axios';
import { Board, Lane, Card } from '../types';

// Get the API URL from environment variables, with a fallback
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
console.log('API URL being used:', API_URL); // Debug log to see what URL is being used

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add an interceptor to retry failed requests
const MAX_RETRIES = 5;
const RETRY_DELAY = 2000; // 2 seconds

async function retryRequest(error: any, retryCount = 0): Promise<AxiosResponse> {
  console.log('Retry request called with error:', error); // Debug log for retries
  const request = error.config;
  
  // If we've already tried the maximum number of times, throw the error
  if (retryCount >= MAX_RETRIES) {
    console.error(`Failed after ${MAX_RETRIES} retries:`, error);
    return Promise.reject(error);
  }
  
  // Wait before retrying
  await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
  console.log(`Retrying request (${retryCount + 1}/${MAX_RETRIES}): ${request.url}`);
  
  // Try again with incremented retry count
  try {
    const response = await axios(request);
    // If we get a successful response, return it and stop retrying
    if (response.status >= 200 && response.status < 300) {
      console.log(`Request successful after ${retryCount + 1} retries: ${request.url}`);
      return response;
    }
    return response;
  } catch (newError) {
    return retryRequest(newError, retryCount + 1);
  }
}

// Add response interceptor to handle retry
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    // Only retry if server is not available or internal server error
    if (!error.response || error.response.status >= 500) {
      console.log(`Backend not ready, retrying request: ${error.config?.url}`);
      return retryRequest(error);
    }
    return Promise.reject(error);
  }
);

// Board API calls
export const getBoards = async (): Promise<Board[]> => {
  const response = await api.get('/boards');
  return response.data;
};

export const getBoard = async (id: number): Promise<Board> => {
  const response = await api.get(`/boards/${id}`);
  return response.data;
};

export const createBoard = async (name: string, description: string = ''): Promise<Board> => {
  const response = await api.post('/boards', { name, description });
  return response.data;
};

export const updateBoard = async (id: number, data: Partial<Board>): Promise<Board> => {
  const response = await api.put(`/boards/${id}`, data);
  return response.data;
};

export const deleteBoard = async (id: number): Promise<void> => {
  await api.delete(`/boards/${id}`);
};

// Lane API calls
export const getLanes = async (boardId: number): Promise<Lane[]> => {
  const response = await api.get(`/boards/${boardId}/lanes`);
  return response.data;
};

export const createLane = async (boardId: number, name: string, position?: number): Promise<Lane> => {
  const response = await api.post(`/boards/${boardId}/lanes`, { name, position });
  return response.data;
};

export const updateLane = async (id: number, data: Partial<Lane>): Promise<Lane> => {
  const response = await api.put(`/lanes/${id}`, data);
  return response.data;
};

export const deleteLane = async (id: number): Promise<void> => {
  await api.delete(`/lanes/${id}`);
};

export const reorderLanes = async (boardId: number, laneOrder: number[]): Promise<Lane[]> => {
  const response = await api.put(`/boards/${boardId}/lanes/reorder`, { lane_order: laneOrder });
  return response.data;
};

// Card API calls
export const getCards = async (laneId: number): Promise<Card[]> => {
  const response = await api.get(`/lanes/${laneId}/cards`);
  return response.data;
};

export const createCard = async (
  laneId: number, 
  title: string, 
  description: string = '',
  color: string = 'white',
  position?: number,
  due_date?: string
): Promise<Card> => {
  const response = await api.post(`/lanes/${laneId}/cards`, { 
    title, 
    description,
    color,
    position,
    due_date
  });
  return response.data;
};

export const updateCard = async (id: number, data: Partial<Card>): Promise<Card> => {
  const response = await api.put(`/cards/${id}`, data);
  return response.data;
};

export const deleteCard = async (id: number): Promise<void> => {
  await api.delete(`/cards/${id}`);
};

export const moveCard = async (
  cardId: number, 
  targetLaneId: number, 
  position?: number,
  cardOrder?: number[]
): Promise<Card> => {
  const response = await api.put(`/cards/${cardId}/move`, { 
    lane_id: targetLaneId,
    position,
    card_order: cardOrder
  });
  return response.data;
};

export const reorderCards = async (laneId: number, cardOrder: number[]): Promise<Card[]> => {
  const response = await api.put(`/lanes/${laneId}/cards/reorder`, { card_order: cardOrder });
  return response.data;
};
