import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import { Lane as LaneType, Card as CardType } from '../../types';
import Card from '../card/Card';

interface LaneProps {
  lane: LaneType;
  index: number;
  onAddCard: (laneId: number) => void;
  onEditCard: (card: CardType) => void;
  onDeleteCard: (cardId: number) => void;
  onEditLane: (lane: LaneType) => void;
  onDeleteLane: (laneId: number) => void;
}

const Lane: React.FC<LaneProps> = ({
  lane,
  index,
  onAddCard,
  onEditCard,
  onDeleteCard,
  onEditLane,
  onDeleteLane
}) => {
  return (
    <Draggable draggableId={`lane-${lane.id}`} index={index}>
      {(provided) => (
        <div 
          className="lane flex flex-col"
          ref={provided.innerRef}
          {...provided.draggableProps}
        >
          <div 
            className="lane-header flex justify-between items-center"
            {...provided.dragHandleProps}
          >
            <h3 className="text-lg font-bold">{lane.name}</h3>
            <div className="flex gap-2">
              <button 
                className="text-sm text-gray-500 hover:text-gray-700"
                onClick={() => onEditLane(lane)}
              >
                Edit
              </button>
              <button 
                className="text-sm text-gray-500 hover:text-danger"
                onClick={() => onDeleteLane(lane.id)}
              >
                Delete
              </button>
            </div>
          </div>
          
          <Droppable droppableId={`lane-${lane.id}`} type="CARD">
            {(provided) => (
              <div 
                className="flex-grow p-1 min-h-[100px]"
                ref={provided.innerRef} 
                {...provided.droppableProps}
              >
                {lane.cards.map((card, index) => (
                  <Card 
                    key={card.id} 
                    card={card} 
                    index={index} 
                    onEdit={onEditCard} 
                    onDelete={onDeleteCard} 
                  />
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
          
          <button 
            className="btn btn-secondary mt-2 w-full"
            onClick={() => onAddCard(lane.id)}
          >
            + Add Card
          </button>
        </div>
      )}
    </Draggable>
  );
};

export default Lane;