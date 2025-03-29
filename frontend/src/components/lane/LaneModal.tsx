import React, { useState, useEffect } from 'react';
import { Lane } from '../../types';

interface LaneModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (lane: Partial<Lane>) => void;
  lane: Lane | null;
  boardId: number;
}

const LaneModal: React.FC<LaneModalProps> = ({
  isOpen,
  onClose,
  onSave,
  lane,
  boardId
}) => {
  const [name, setName] = useState('');
  
  // Reset form when lane changes
  useEffect(() => {
    if (lane) {
      setName(lane.name);
    } else {
      setName('');
    }
  }, [lane]);
  
  if (!isOpen) return null;
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const updatedLane: Partial<Lane> = {
      name,
      board_id: boardId
    };
    
    if (lane) {
      updatedLane.id = lane.id;
      updatedLane.position = lane.position;
    }
    
    onSave(updatedLane);
    onClose();
  };
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-md p-6">
        <h2 className="text-xl font-semibold mb-4">
          {lane ? 'Edit Lane' : 'Create New Lane'}
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Name
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
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

export default LaneModal;