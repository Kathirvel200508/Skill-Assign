import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControlLabel,
  Switch,
  Alert,
  Badge,
} from '@mui/material';
import { CheckCircle } from '@mui/icons-material';
import { assignmentAPI } from '../api';
import axios from 'axios';
import { API_BASE_URL } from '../config';

export default function Assignments() {
  const [assignments, setAssignments] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [feedback, setFeedback] = useState({ success: true, feedback: '' });
  const [completedTasks, setCompletedTasks] = useState([]);
  const [newCompletions, setNewCompletions] = useState([]);
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);

  useEffect(() => {
    loadAssignments();
    loadCompletedTasks();
    
    // Auto-refresh every 3 seconds to see worker task completions
    const interval = setInterval(() => {
      loadAssignments(); // Refresh assignments to update status
      loadCompletedTasks();
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const loadAssignments = async () => {
    try {
      const [assignmentsRes, tasksRes] = await Promise.all([
        assignmentAPI.getAll(),
        axios.get(`${API_BASE_URL}/task/all`)
      ]);
      
      const assignmentsData = assignmentsRes.data;
      const tasksData = tasksRes.data;
      
      // Enhance assignments with task status
      const enhancedAssignments = assignmentsData.map(assignment => {
        const linkedTask = tasksData.find(t => t.id === assignment.task_id);
        
        if (linkedTask) {
          // Auto-update assignment based on task status
          if (linkedTask.status === 'completed' && assignment.success === null) {
            assignment.success = true;
            assignment.completed_at = linkedTask.completed_at;
            assignment.taskStatus = 'completed';
          } else {
            assignment.taskStatus = linkedTask.status;
          }
        }
        
        return assignment;
      });
      
      setAssignments(enhancedAssignments);
    } catch (error) {
      console.error('Error loading assignments:', error);
    }
  };

  const loadCompletedTasks = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/task/all`);
      const tasks = response.data;
      
      // Filter only completed tasks
      const completed = tasks.filter(t => t.status === 'completed');
      
      // Check for newly completed tasks
      const previousCompletedIds = completedTasks.map(t => t.id);
      const newlyCompleted = completed.filter(t => !previousCompletedIds.includes(t.id));
      
      if (newlyCompleted.length > 0) {
        setNewCompletions(newlyCompleted);
        setShowSuccessAlert(true);
        
        // Hide alert after 5 seconds
        setTimeout(() => {
          setShowSuccessAlert(false);
        }, 5000);
      }
      
      setCompletedTasks(completed);
    } catch (error) {
      console.error('Error loading completed tasks:', error);
    }
  };

  const handleAddFeedback = (assignment) => {
    setSelectedAssignment(assignment);
    setFeedback({ success: true, feedback: '' });
    setDialogOpen(true);
  };

  const handleSaveFeedback = async () => {
    try {
      await assignmentAPI.addFeedback(selectedAssignment.id, feedback);
      alert('Feedback saved successfully!');
      setDialogOpen(false);
      loadAssignments();
    } catch (error) {
      console.error('Error saving feedback:', error);
      alert('Failed to save feedback');
    }
  };

  return (
    <div>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">
          Assignment History
        </Typography>
        <Badge badgeContent={completedTasks.length} color="success">
          <Chip 
            icon={<CheckCircle />}
            label="Completed Tasks"
            color="success"
            variant="outlined"
          />
        </Badge>
      </Box>
      
      {showSuccessAlert && newCompletions.length > 0 && (
        <Alert 
          severity="success" 
          sx={{ mb: 2 }}
          onClose={() => setShowSuccessAlert(false)}
        >
          🎉 <strong>{newCompletions.length} new task(s) completed!</strong>
          {newCompletions.map((task, idx) => (
            <div key={task.id}>
              • {task.title} (Worker ID: {task.worker_id})
            </div>
          ))}
        </Alert>
      )}
      
      {/* Show Recently Completed Tasks Section */}
      {completedTasks.length > 0 && (
        <Card sx={{ mb: 3, bgcolor: '#e8f5e9', borderLeft: '4px solid #4caf50' }}>
          <CardContent>
            <Typography variant="h6" color="success.main" gutterBottom>
              ✅ Recently Completed by Workers
            </Typography>
            {completedTasks.slice(0, 5).map((task) => (
              <Box 
                key={task.id} 
                sx={{ 
                  mb: 1, 
                  p: 1, 
                  bgcolor: 'white', 
                  borderRadius: 1,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <Typography variant="body1">
                    <strong>{task.title}</strong>
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Worker ID: {task.worker_id} • Priority: {task.priority}
                  </Typography>
                </div>
                <Chip 
                  icon={<CheckCircle />}
                  label="Completed" 
                  color="success" 
                  size="small"
                />
              </Box>
            ))}
          </CardContent>
        </Card>
      )}

      <Box mt={3}>
        {assignments.map((assignment) => (
          <Card key={assignment.id} sx={{ mb: 2 }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="start">
                <div>
                  <Typography variant="h6">
                    Assignment #{assignment.id}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Worker ID: {assignment.worker_id} → Role ID: {assignment.role_id}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Fit Score: {(assignment.fit_score * 100).toFixed(0)}%
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Assigned: {new Date(assignment.assigned_at).toLocaleString()}
                  </Typography>
                  {assignment.completed_at && (
                    <Typography variant="body2" color="textSecondary">
                      Completed: {new Date(assignment.completed_at).toLocaleString()}
                    </Typography>
                  )}
                </div>
                <Box>
                  {assignment.taskStatus === 'completed' || assignment.success === true ? (
                    <Chip
                      icon={<CheckCircle />}
                      label="Success"
                      color="success"
                    />
                  ) : assignment.taskStatus === 'in_progress' ? (
                    <Chip
                      label="In Progress"
                      color="info"
                    />
                  ) : assignment.taskStatus === 'pending' ? (
                    <Chip
                      label="Pending"
                      color="warning"
                    />
                  ) : assignment.success === false ? (
                    <Chip
                      label="Failed"
                      color="error"
                    />
                  ) : (
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleAddFeedback(assignment)}
                    >
                      Add Feedback
                    </Button>
                  )}
                </Box>
              </Box>
              {assignment.feedback && (
                <Typography variant="body2" sx={{ mt: 2, fontStyle: 'italic' }}>
                  Feedback: {assignment.feedback}
                </Typography>
              )}
            </CardContent>
          </Card>
        ))}
      </Box>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Assignment Feedback</DialogTitle>
        <DialogContent>
          <FormControlLabel
            control={
              <Switch
                checked={feedback.success}
                onChange={(e) => setFeedback({ ...feedback, success: e.target.checked })}
              />
            }
            label={feedback.success ? 'Successful Assignment' : 'Failed Assignment'}
            sx={{ mt: 2 }}
          />
          <TextField
            fullWidth
            label="Feedback Comments"
            value={feedback.feedback}
            onChange={(e) => setFeedback({ ...feedback, feedback: e.target.value })}
            margin="normal"
            multiline
            rows={4}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveFeedback} variant="contained">
            Save Feedback
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
