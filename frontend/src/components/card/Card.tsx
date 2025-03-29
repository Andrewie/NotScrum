import React from 'react';
import { Draggable } from 'react-beautiful-dnd';
import { Card as CardType } from '../../types';

interface CardProps {
  card: CardType;
  index: number;
  onEdit: (card: CardType) => void;
  onDelete: (cardId: number) => void;
}

const Card: React.FC<CardProps> = ({ card, index, onEdit, onDelete }) => {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <Draggable draggableId={`card-${card.id}`} index={index}>
      {(provided) => (
        <div
          className={`card ${card.color !== 'white' ? `bg-${card.color}-100` : ''}`}
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          onClick={() => onEdit(card)}
        >
          <div className="card-title">{card.title}</div>
          {card.description && (
            <div className="card-description">{card.description}</div>
          )}
          {card.due_date && (
            <div className="card-deadline">
              Due: {formatDate(card.due_date)}
            </div>
          )}
          <div className="flex justify-end mt-2">
            <button
              className="text-xs text-gray-500 hover:text-danger"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(card.id);
              }}
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </Draggable>
  );
};

export default Card;