import React, { useState, useEffect } from 'react';
import { Card } from '../../types';

interface CardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (card: Partial<Card>) => void;
  card: Card | null;
  laneId: number;
}

const CardModal: React.FC<CardModalProps> = ({
  isOpen,
  onClose,
  onSave,
  card,
  laneId
}) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [color, setColor] = useState('white');
  const [dueDate, setDueDate] = useState<string>('');
  
  // Reset form when card changes
  useEffect(() => {
    if (card) {
      setTitle(card.title);
      setDescription(card.description || '');
      setColor(card.color || 'white');
      setDueDate(card.due_date ? card.due_date.slice(0, 10) : '');
    } else {
      setTitle('');
      setDescription('');
      setColor('white');
      setDueDate('');
    }
  }, [card]);
  
  if (!isOpen) return null;
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const updatedCard: Partial<Card> = {
      title,
      description,
      color,
      due_date: dueDate || null,
      lane_id: laneId
    };
    
    if (card) {
      updatedCard.id = card.id;
    }
    
    onSave(updatedCard);
    onClose();
  };
  
  const colorOptions = [
    { value: 'white', label: 'White' },
    { value: 'blue-100', label: 'Blue' },
    { value: 'green-100', label: 'Green' },
    { value: 'yellow-100', label: 'Yellow' },
    { value: 'red-100', label: 'Red' }
  ];
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-md p-6">
        <h2 className="text-xl font-semibold mb-4">
          {card ? 'Edit Card' : 'Create New Card'}
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Color
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={color}
              onChange={(e) => setColor(e.target.value)}
            >
              {colorOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Due Date
            </label>
            <input
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </div>
          
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CardModal;