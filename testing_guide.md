# NotScrum Testing Guide

This document provides a systematic approach to testing the NotScrum application to ensure all core functionalities work correctly.

## Prerequisites

Before beginning testing, ensure you have:

1. Docker and Docker Compose installed
2. The NotScrum repository cloned to your local machine
3. Navigated to the project root directory in your terminal

## Starting the Application

1. Build and start the application using Docker Compose:
   ```
   docker-compose up --build
   ```

2. Wait for both services to start up successfully. You should see log messages indicating:
   - The backend is running on http://localhost:5000
   - The frontend is running on http://localhost:3000

3. Open your browser and navigate to http://localhost:3000

## Test Cases

Execute the following test cases in order, as some depend on previous steps:

### 1. Board Management

#### 1.1 Board Creation
1. When first accessing the application, you should see a "No boards found" message
2. Click the "Create Board" button
3. Enter a name (e.g., "Test Board") and optional description
4. Click "Create Board"
5. **Expected Result**: The board is created with three default lanes (Todo, Doing, Done)

#### 1.2 Board Update
1. Click the board name in the header to edit (future enhancement)
2. **Expected Result**: This feature may not be implemented yet

#### 1.3 Board Selection
1. Create a second board by clicking the "New Board" button in the top right
2. Use the dropdown in the top right to switch between boards
3. **Expected Result**: The board view should change to display the selected board

### 2. Lane Management

#### 2.1 Lane Creation
1. Click the "Add Lane" button
2. Enter a name for the new lane (e.g., "Testing")
3. Click "Save"
4. **Expected Result**: A new empty lane should appear at the end of the board

#### 2.2 Lane Update
1. Click the "Edit" button on any lane
2. Change the name
3. Click "Save"
4. **Expected Result**: The lane name should be updated

#### 2.3 Lane Deletion
1. Click the "Delete" button on any lane
2. Confirm the deletion
3. **Expected Result**: The lane and all its cards should be removed

#### 2.4 Lane Reordering
1. Drag any lane by its header to a new position
2. Release the mouse button
3. **Expected Result**: The lane should remain in the new position, even after a page refresh

### 3. Card Management

#### 3.1 Card Creation
1. Click the "+ Add Card" button on any lane
2. Fill in the card details:
   - Title (required)
   - Description (optional)
   - Color (select from dropdown)
   - Due date (optional)
3. Click "Save"
4. **Expected Result**: The new card should appear in the lane

#### 3.2 Card Update
1. Click on any existing card
2. Modify the details
3. Click "Save"
4. **Expected Result**: The card should be updated with the new details

#### 3.3 Card Deletion
1. Click on any card to open it
2. Click the "Delete" button at the bottom
3. Confirm the deletion
4. **Expected Result**: The card should be removed from the lane

#### 3.4 Card Movement
1. Drag any card from one lane to another
2. Release the mouse button
3. **Expected Result**: The card should move to the new lane and remain there even after a page refresh

#### 3.5 Card Reordering
1. Drag a card to a different position within the same lane
2. Release the mouse button
3. **Expected Result**: The card should remain in the new position, even after a page refresh

### 4. Filtering Functionality

1. Create multiple cards with different titles and descriptions
2. Use the search bar above the board to enter a search term
3. **Expected Result**: Only cards containing the search term in their title or description should be visible

### 5. Color-Coding

1. Create a new card or edit an existing one
2. Select different colors from the color dropdown
3. Save the card
4. **Expected Result**: The card should be displayed with the selected background color

## Bug Reporting

If you encounter any issues during testing, please document them with the following information:

1. Test case number and name
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Browser and operating system information

## Conclusion

After completing all test cases, mark item #41 on the development checklist as complete. If any issues were identified, add them to a list for fixing in item #42.