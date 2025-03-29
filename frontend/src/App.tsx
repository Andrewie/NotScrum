import React, { useState, useEffect } from 'react';
import Board from './components/board/Board';
import { getBoards, createBoard } from './services/api';
import { Board as BoardType } from './types';

const App: React.FC = () => {
  const [boards, setBoards] = useState<BoardType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedBoardId, setSelectedBoardId] = useState<number | null>(null);
  const [showNewBoardForm, setShowNewBoardForm] = useState(false);
  const [newBoardName, setNewBoardName] = useState('');
  const [newBoardDescription, setNewBoardDescription] = useState('');

  useEffect(() => {
    const fetchBoards = async () => {
      try {
        setLoading(true);
        const data = await getBoards();
        setBoards(data);
        
        // Select the first board by default if none is selected
        if (data.length > 0 && !selectedBoardId) {
          setSelectedBoardId(data[0].id);
        }
        
        setError(null);
      } catch (err) {
        setError('Failed to fetch boards. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchBoards();
  }, [selectedBoardId]);

  const handleBoardSelect = (boardId: number) => {
    setSelectedBoardId(boardId);
  };

  const handleCreateBoard = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newBoardName.trim()) return;
    
    try {
      const newBoard = await createBoard(newBoardName, newBoardDescription);
      setBoards([...boards, newBoard]);
      setSelectedBoardId(newBoard.id);
      setShowNewBoardForm(false);
      setNewBoardName('');
      setNewBoardDescription('');
    } catch (err) {
      setError('Failed to create new board');
      console.error(err);
    }
  };

  if (loading && boards.length === 0) {
    return <div className="p-4">Loading boards...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-900">Simple Project Board</h1>
          
          <div className="flex items-center gap-4">
            {boards.length > 0 && (
              <select 
                className="border border-gray-300 rounded-md px-3 py-1"
                value={selectedBoardId || ''}
                onChange={(e) => handleBoardSelect(Number(e.target.value))}
              >
                {boards.map(board => (
                  <option key={board.id} value={board.id}>{board.name}</option>
                ))}
              </select>
            )}
            
            <button
              className="btn btn-primary"
              onClick={() => setShowNewBoardForm(true)}
            >
              New Board
            </button>
          </div>
        </div>
      </header>
      
      <main className="mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        {showNewBoardForm && (
          <div className="bg-white shadow rounded-md p-4 mb-6">
            <h2 className="text-lg font-semibold mb-4">Create New Board</h2>
            <form onSubmit={handleCreateBoard}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Board Name</label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={newBoardName}
                  onChange={(e) => setNewBoardName(e.target.value)}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
                <textarea
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={newBoardDescription}
                  onChange={(e) => setNewBoardDescription(e.target.value)}
                  rows={3}
                />
              </div>
              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowNewBoardForm(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                >
                  Create Board
                </button>
              </div>
            </form>
          </div>
        )}
        
        {selectedBoardId && <Board boardId={selectedBoardId} />}
        
        {boards.length === 0 && !showNewBoardForm && (
          <div className="text-center py-10">
            <h2 className="text-xl font-semibold mb-2">No boards found</h2>
            <p className="text-gray-600 mb-4">Create your first board to get started</p>
            <button 
              className="btn btn-primary"
              onClick={() => setShowNewBoardForm(true)}
            >
              Create Board
            </button>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;