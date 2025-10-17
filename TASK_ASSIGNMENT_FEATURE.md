# 📋 Task Assignment Feature

## Overview
Supervisors can now assign tasks to workers from the web dashboard, and workers will see these tasks in real-time on their mobile app.

## How It Works

### For Supervisors (Web Dashboard)

1. **Navigate to Tasks Page**
   - Open the web dashboard at http://localhost:3000
   - Click on "Tasks" in the left sidebar

2. **Assign a New Task**
   - Click the "Assign New Task" button
   - Select a worker from the dropdown
   - Enter task title (required)
   - Add description (optional)
   - Set priority: Low, Medium, or High
   - Set due date (optional)
   - Click "Assign Task"

3. **View All Tasks**
   - See all assigned tasks with their status
   - Tasks show: title, description, worker, priority, status, and dates
   - Status indicators: Pending, In Progress, Completed

### For Workers (Mobile App)

1. **View Tasks**
   - Open the mobile app
   - Navigate to the "Tasks" tab (first tab)
   - See all your assigned tasks organized by status

2. **Update Task Status**
   - Tap on any task card
   - Choose an action:
     - **Pending tasks**: "Start Task" → Changes to In Progress
     - **In Progress tasks**: "Mark as Completed" → Changes to Completed

3. **Auto-Refresh**
   - Tasks automatically refresh every 30 seconds
   - Pull down to manually refresh
   - New tasks from supervisor appear immediately

## Features

### Task Properties
- **Title**: Short description of the task
- **Description**: Detailed instructions
- **Priority**: Low (Blue), Medium (Orange), High (Red)
- **Status**: Pending → In Progress → Completed
- **Due Date**: Optional deadline
- **Assigned By**: Shows who assigned the task
- **Timestamps**: Created, Updated, and Completed dates

### Real-Time Updates
- Workers see new tasks within 30 seconds (or immediately on manual refresh)
- Status changes are reflected instantly
- Supervisors can track task progress in real-time

## API Endpoints

### Create Task
```
POST /task/create
Body: {
  "worker_id": 1,
  "title": "Complete assembly line inspection",
  "description": "Check all stations for safety compliance",
  "priority": "high",
  "due_date": "2024-10-20T10:00:00",
  "assigned_by": "Supervisor"
}
```

### Get Worker Tasks
```
GET /task/worker/{worker_id}
Optional query param: ?status=pending
```

### Update Task Status
```
PUT /task/{task_id}
Body: {
  "status": "in_progress"
}
```

### Get All Tasks
```
GET /task/all
```

## Testing the Feature

1. **Start all servers** (if not already running):
   ```bash
   # Backend
   cd backend
   python -m uvicorn main:app --reload

   # Web Frontend
   cd web
   npm run dev

   # Mobile App
   cd mobile
   npx expo start
   ```

2. **Assign a task from web dashboard**:
   - Go to http://localhost:3000/tasks
   - Click "Assign New Task"
   - Select "Worker 1"
   - Title: "Test Task"
   - Priority: "High"
   - Click "Assign Task"

3. **Check mobile app**:
   - Open mobile app (web browser or device)
   - Go to "Tasks" tab
   - You should see the newly assigned task
   - Tap on it and select "Start Task"

4. **Verify on web dashboard**:
   - Refresh the Tasks page
   - Task status should now show "In Progress"

## Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    worker_id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    priority VARCHAR DEFAULT 'medium',
    status VARCHAR DEFAULT 'pending',
    assigned_by VARCHAR DEFAULT 'Supervisor',
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

## Benefits

1. **Real-Time Communication**: Supervisors can instantly assign tasks to workers
2. **Status Tracking**: Monitor task progress in real-time
3. **Priority Management**: Highlight urgent tasks with color coding
4. **Mobile Accessibility**: Workers can manage tasks from anywhere
5. **Historical Record**: Track completion times and performance

## Future Enhancements

- Push notifications for new task assignments
- Task comments and feedback
- Attach files/images to tasks
- Task templates for common assignments
- Analytics dashboard for task completion rates
- Worker workload balancing

---

**Note**: The mobile app currently defaults to Worker ID 1 for demonstration. In production, implement proper authentication to show tasks for the logged-in worker.
