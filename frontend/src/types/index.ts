export interface Board {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
  lanes: Lane[];
}

export interface Lane {
  id: number;
  name: string;
  position: number;
  board_id: number;
  created_at: string;
  updated_at: string;
  cards: Card[];
}

export interface Card {
  id: number;
  title: string;
  description: string;
  color: string;
  position: number;
  due_date: string | null;
  lane_id: number;
  created_at: string;
  updated_at: string;
}