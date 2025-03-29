import React, { useState, useEffect } from 'react';
import { DragDropContext, DropResult, Droppable } from 'react-beautiful-dnd';
import { Board as BoardType, Lane as LaneType, Card as CardType } from '../../types';
import Lane from '../lane/Lane';
import LaneModal from '../lane/LaneModal';
import CardModal from '../card/CardModal';
import SearchBar from '../search/SearchBar';
import * as api from '../../services/api';

interface BoardProps {
  boardId: number;
}

const Board: React.FC<BoardProps> = ({ boardId }) => {
  const [board, setBoard] = useState<BoardType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredBoard, setFilteredBoard] = useState<BoardType | null>(null);
  
  // Modal states
  const [showCardModal, setShowCardModal] = useState(false);
  const [showLaneModal, setShowLaneModal] = useState(false);
  const [currentCard, setCurrentCard] = useState<CardType | null>(null);
  const [currentLane, setCurrentLane] = useState<LaneType | null>(null);
  const [activeLaneId, setActiveLaneId] = useState<number | null>(null);
  
  // Fetch board data
  useEffect(() => {
    const fetchBoard = async () => {
      try {
        setLoading(true);
        const data = await api.getBoard(boardId);
        setBoard(data);
        setError(null);
      } catch (err) {
        setError('Failed to load board data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchBoard();
  }, [boardId]);
  
  // Update filtered board when board or search term changes
  useEffect(() => {
    if (!board) return;
    
    if (!searchTerm.trim()) {
      setFilteredBoard(board);
      return;
    }
    
    const lowerSearchTerm = searchTerm.toLowerCase();
    
    // Filter cards in each lane
    const filteredLanes = board.lanes.map(lane => {
      const filteredCards = lane.cards.filter(card => 
        card.title.toLowerCase().includes(lowerSearchTerm) || 
        (card.description && card.description.toLowerCase().includes(lowerSearchTerm))
      );
      
      return { ...lane, cards: filteredCards };
    });
    
    setFilteredBoard({ ...board, lanes: filteredLanes });
  }, [board, searchTerm]);
  
  // Handle drag end event
  const handleDragEnd = async (result: DropResult) => {
    const { source, destination, type, draggableId } = result;
    
    // Dropped outside of a droppable area
    if (!destination) return;
    
    // Dropped in the same position
    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    ) return;
    
    // If board is not loaded, return
    if (!board) return;
    
    // Handle card movement
    if (type === 'CARD') {
      const sourceId = parseInt(source.droppableId.replace('lane-', ''));
      const destinationId = parseInt(destination.droppableId.replace('lane-', ''));
      const cardId = parseInt(draggableId.replace('card-', ''));
      
      // Create a deep copy of board to update
      const newBoard = { ...board, lanes: [...board.lanes] };
      
      // Find source and destination lanes
      const sourceLane = newBoard.lanes.find(lane => lane.id === sourceId);
      const destLane = newBoard.lanes.find(lane => lane.id === destinationId);
      
      if (!sourceLane || !destLane) return;
      
      // Create copies of the lanes' cards
      const sourceCards = [...sourceLane.cards];
      const destCards = sourceId === destinationId ? sourceCards : [...destLane.cards];
      
      // Get the card that's being moved
      const [movedCard] = sourceCards.splice(source.index, 1);
      
      // Insert card at the destination
      destCards.splice(destination.index, 0, movedCard);
      
      // Update lanes with new card arrays
      if (sourceId === destinationId) {
        sourceLane.cards = sourceCards;
      } else {
        sourceLane.cards = sourceCards;
        destLane.cards = destCards;
        
        // Update card's lane_id
        movedCard.lane_id = destinationId;
      }
      
      // Update UI
      setBoard(newBoard);
      
      try {
        // Get card IDs for the destination lane after reordering
        const cardOrder = destCards.map(c => c.id);
        
        // Call API to move the card
        await api.moveCard(cardId, destinationId, destination.index, cardOrder);
      } catch (err) {
        console.error('Failed to update card position', err);
        // Revert to original board state in case of error
        const originalBoard = await api.getBoard(boardId);
        setBoard(originalBoard);
      }
    }
    
    // Handle lane movement
    if (type === 'LANE') {
      const newBoard = { ...board, lanes: [...board.lanes] };
      const [movedLane] = newBoard.lanes.splice(source.index, 1);
      newBoard.lanes.splice(destination.index, 0, movedLane);
      
      // Update positions
      newBoard.lanes.forEach((lane, index) => {
        lane.position = index;
      });
      
      // Update UI
      setBoard(newBoard);
      
      try {
        // Get lane IDs after reordering
        const laneOrder = newBoard.lanes.map(l => l.id);
        
        // Call API to reorder lanes
        await api.reorderLanes(boardId, laneOrder);
      } catch (err) {
        console.error('Failed to update lane positions', err);
        // Revert to original board state in case of error
        const originalBoard = await api.getBoard(boardId);
        setBoard(originalBoard);
      }
    }
  };
  
  // Handle adding a new lane
  const handleAddLane = () => {
    setCurrentLane(null);
    setShowLaneModal(true);
  };
  
  // Handle editing a lane
  const handleEditLane = (lane: LaneType) => {
    setCurrentLane(lane);
    setShowLaneModal(true);
  };
  
  // Handle saving a lane
  const handleSaveLane = async (laneData: Partial<LaneType>) => {
    try {
      let updatedLane: LaneType;
      
      if (laneData.id) {
        // Update existing lane
        updatedLane = await api.updateLane(laneData.id, laneData);
        
        // Update board with the updated lane
        if (board) {
          const updatedLanes = board.lanes.map(lane => 
            lane.id === updatedLane.id ? updatedLane : lane
          );
          setBoard({ ...board, lanes: updatedLanes });
        }
      } else {
        // Create new lane
        updatedLane = await api.createLane(boardId, laneData.name || 'New Lane');
        
        // Add the new lane to the board
        if (board) {
          setBoard({ ...board, lanes: [...board.lanes, updatedLane] });
        }
      }
    } catch (err) {
      setError('Failed to save lane');
      console.error(err);
    }
  };
  
  // Handle deleting a lane
  const handleDeleteLane = async (laneId: number) => {
    if (!board) return;
    
    if (window.confirm('Are you sure you want to delete this lane and all its cards?')) {
      try {
        await api.deleteLane(laneId);
        
        // Update UI
        const newBoard = {
          ...board,
          lanes: board.lanes.filter(lane => lane.id !== laneId)
        };
        setBoard(newBoard);
      } catch (err) {
        console.error('Failed to delete lane', err);
      }
    }
  };
  
  // Handle adding a new card
  const handleAddCard = (laneId: number) => {
    setCurrentCard(null);
    setActiveLaneId(laneId);
    setShowCardModal(true);
  };
  
  // Handle editing a card
  const handleEditCard = (card: CardType) => {
    setCurrentCard(card);
    setActiveLaneId(card.lane_id);
    setShowCardModal(true);
  };
  
  // Handle saving a card
  const handleSaveCard = async (cardData: Partial<CardType>) => {
    try {
      let updatedCard: CardType;
      
      if (cardData.id) {
        // Update existing card
        updatedCard = await api.updateCard(cardData.id, cardData);
        
        // Update board with the updated card
        if (board) {
          const updatedLanes = board.lanes.map(lane => {
            if (lane.id === updatedCard.lane_id) {
              const updatedCards = lane.cards.map(card => 
                card.id === updatedCard.id ? updatedCard : card
              );
              return { ...lane, cards: updatedCards };
            }
            return lane;
          });
          setBoard({ ...board, lanes: updatedLanes });
        }
      } else if (activeLaneId) {
        // Create new card
        updatedCard = await api.createCard(
          activeLaneId,
          cardData.title || 'New Card',
          cardData.description,
          cardData.color,
          undefined,
          cardData.due_date || undefined
        );
        
        // Add the new card to the appropriate lane
        if (board) {
          const updatedLanes = board.lanes.map(lane => {
            if (lane.id === activeLaneId) {
              return { ...lane, cards: [...lane.cards, updatedCard] };
            }
            return lane;
          });
          setBoard({ ...board, lanes: updatedLanes });
        }
      }
    } catch (err) {
      setError('Failed to save card');
      console.error(err);
    }
  };
  
  // Handle deleting a card
  const handleDeleteCard = async (cardId: number) => {
    if (!board) return;
    
    if (window.confirm('Are you sure you want to delete this card?')) {
      try {
        await api.deleteCard(cardId);
        
        // Update UI
        const newBoard = {
          ...board,
          lanes: board.lanes.map(lane => ({
            ...lane,
            cards: lane.cards.filter(card => card.id !== cardId)
          }))
        };
        setBoard(newBoard);
      } catch (err) {
        console.error('Failed to delete card', err);
      }
    }
  };
  
  // Handle search
  const handleSearch = (term: string) => {
    setSearchTerm(term);
  };
  
  if (loading) return <div className="p-4">Loading board...</div>;
  if (error) return <div className="p-4 text-danger">{error}</div>;
  if (!board) return <div className="p-4">Board not found.</div>;
  
  return (
    <div className="board">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">{board.name}</h1>
        <button 
          className="btn btn-primary"
          onClick={handleAddLane}
        >
          Add Lane
        </button>
      </div>
      
      {board.description && (
        <div className="mb-4 text-gray-600">{board.description}</div>
      )}
      
      <div className="mb-4">
        <SearchBar onSearch={handleSearch} placeholder="Search cards by title or description..." />
      </div>
      
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="lanes" direction="horizontal" type="LANE">
          {(provided) => (
            <div 
              className="flex gap-4 overflow-x-auto pb-4" 
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {(filteredBoard?.lanes || []).map((lane, index) => (
                <Lane
                  key={lane.id}
                  lane={lane}
                  index={index}
                  onAddCard={handleAddCard}
                  onEditCard={handleEditCard}
                  onDeleteCard={handleDeleteCard}
                  onEditLane={handleEditLane}
                  onDeleteLane={handleDeleteLane}
                />
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
      
      {/* Lane Modal */}
      {showLaneModal && (
        <LaneModal
          isOpen={showLaneModal}
          onClose={() => setShowLaneModal(false)}
          onSave={handleSaveLane}
          lane={currentLane}
          boardId={boardId}
        />
      )}
      
      {/* Card Modal */}
      {showCardModal && activeLaneId && (
        <CardModal
          isOpen={showCardModal}
          onClose={() => setShowCardModal(false)}
          onSave={handleSaveCard}
          card={currentCard}
          laneId={activeLaneId}
        />
      )}
    </div>
  );
};

export default Board;