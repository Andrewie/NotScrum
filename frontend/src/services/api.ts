import axios from 'axios';
import { Board, Lane, Card } from '../types';

// Use window.location.origin to determine if we're in browser or production
// In development, the React app is served at localhost:3000 and needs to connect to localhost:5000
// In Docker container communication, we use the service name
const API_BASE = process.env.NODE_ENV === 'production' 
  ? process.env.REACT_APP_API_URL 
  : 'http://localhost:5000/api';

// If we're accessing through a browser, use the browser's origin
const isBrowser = typeof window !== 'undefined';
const API_URL = isBrowser && window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api'
  : API_BASE;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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