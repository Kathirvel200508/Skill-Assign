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
} from '@mui/material';
import { assignmentAPI } from '../api';

export default function Assignments() {
  const [assignments, setAssignments] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [feedback, setFeedback] = useState({ success: true, feedback: '' });

  useEffect(() => {
    loadAssignments();
  }, []);

  const loadAssignments = async () => {
    try {
      const response = await assignmentAPI.getAll();
      setAssignments(response.data);
    } catch (error) {
      console.error('Error loading assignments:', error);
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
      <Typography variant="h4" gutterBottom>
        Assignment History
      </Typography>

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
                  {assignment.success !== null ? (
                    <Chip
                      label={assignment.success ? 'Success' : 'Failed'}
                      color={assignment.success ? 'success' : 'error'}
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
