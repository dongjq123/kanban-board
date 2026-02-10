"""
Integration test for BoardList component
Tests the backend API endpoints that the BoardList component uses
"""
import os
os.environ['FLASK_ENV'] = 'testing'

from app import app, db
from models.board import Board

def test_board_api_integration():
    """Test the board API endpoints"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create test client
        client = app.test_client()
        
        print("Testing Board API endpoints for BoardList component...")
        print("=" * 60)
        
        # Test 1: GET /api/boards (empty list)
        print("\n1. Testing GET /api/boards (empty list)")
        response = client.get('/api/boards')
        assert response.status_code == 200
        data = response.get_json()
        assert 'boards' in data
        assert isinstance(data['boards'], list)
        assert len(data['boards']) == 0
        print("✓ GET /api/boards returns empty list")
        
        # Test 2: POST /api/boards (create board)
        print("\n2. Testing POST /api/boards (create board)")
        response = client.post('/api/boards', json={'name': '测试看板1'})
        assert response.status_code == 201
        board1 = response.get_json()
        assert board1['name'] == '测试看板1'
        assert 'id' in board1
        assert 'created_at' in board1
        print(f"✓ Created board: {board1['name']} (ID: {board1['id']})")
        
        # Test 3: POST /api/boards (create another board)
        print("\n3. Testing POST /api/boards (create another board)")
        response = client.post('/api/boards', json={'name': '项目开发看板'})
        assert response.status_code == 201
        board2 = response.get_json()
        assert board2['name'] == '项目开发看板'
        print(f"✓ Created board: {board2['name']} (ID: {board2['id']})")
        
        # Test 4: GET /api/boards (list with boards)
        print("\n4. Testing GET /api/boards (list with boards)")
        response = client.get('/api/boards')
        assert response.status_code == 200
        data = response.get_json()
        boards = data['boards']
        assert len(boards) == 2
        # Boards might be in any order, so check both exist
        board_names = [b['name'] for b in boards]
        assert '测试看板1' in board_names
        assert '项目开发看板' in board_names
        print(f"✓ GET /api/boards returns {len(boards)} boards")
        
        # Test 5: GET /api/boards/:id (get specific board)
        print("\n5. Testing GET /api/boards/:id (get specific board)")
        response = client.get(f'/api/boards/{board1["id"]}')
        assert response.status_code == 200
        board = response.get_json()
        assert board['id'] == board1['id']
        assert board['name'] == '测试看板1'
        print(f"✓ GET /api/boards/{board1['id']} returns correct board")
        
        # Test 6: POST /api/boards with empty name (validation error)
        print("\n6. Testing POST /api/boards with empty name (validation error)")
        response = client.post('/api/boards', json={'name': ''})
        assert response.status_code == 400
        error = response.get_json()
        assert 'error' in error
        print(f"✓ Empty name rejected with error: {error['error']['message']}")
        
        # Test 7: DELETE /api/boards/:id (delete board)
        print("\n7. Testing DELETE /api/boards/:id (delete board)")
        response = client.delete(f'/api/boards/{board1["id"]}')
        assert response.status_code == 204
        print(f"✓ Deleted board ID: {board1['id']}")
        
        # Test 8: GET /api/boards (verify deletion)
        print("\n8. Testing GET /api/boards (verify deletion)")
        response = client.get('/api/boards')
        assert response.status_code == 200
        data = response.get_json()
        boards = data['boards']
        assert len(boards) == 1
        assert boards[0]['id'] == board2['id']
        print(f"✓ Only {len(boards)} board remains after deletion")
        
        # Test 9: GET /api/boards/:id (non-existent board)
        print("\n9. Testing GET /api/boards/:id (non-existent board)")
        response = client.get('/api/boards/99999')
        assert response.status_code == 404
        error = response.get_json()
        assert 'error' in error
        print(f"✓ Non-existent board returns 404: {error['error']['message']}")
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("\nBoardList component can successfully:")
        print("  - Display all boards (GET /api/boards)")
        print("  - Create new boards (POST /api/boards)")
        print("  - Select boards (GET /api/boards/:id)")
        print("  - Delete boards (DELETE /api/boards/:id)")
        print("  - Handle validation errors (empty names)")
        print("  - Handle not found errors (non-existent boards)")
        
        # Clean up
        db.drop_all()

if __name__ == '__main__':
    test_board_api_integration()
