import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Alert,
} from '@mui/material';
import { Add, Assignment } from '@mui/icons-material';
import axios from 'axios';
import { API_BASE_URL } from '../config';

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [formData, setFormData] = useState({
    worker_id: '',
    role_id: '',
    title: '',
    description: '',
    priority: 'medium',
    due_date: '',
  });

  useEffect(() => {
    loadTasks();
    loadWorkers();
    loadRoles();
    
    // Auto-refresh tasks every 3 seconds to see worker updates
    const interval = setInterval(() => {
      loadTasks();
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const loadTasks = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/task/all`);
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const loadWorkers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/worker/all`);
      setWorkers(response.data);
    } catch (error) {
      console.error('Error loading workers:', error);
    }
  };

  const loadRoles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/role/all`);
      setRoles(response.data);
    } catch (error) {
      console.error('Error loading roles:', error);
    }
  };

  const handleAdd = () => {
    console.log('[SUPERVISOR] "Assign New Task" button clicked');
    console.log('[SUPERVISOR] Opening task assignment dialog...');
    setFormData({
      worker_id: '',
      role_id: '',
      title: '',
      description: '',
      priority: 'medium',
      due_date: '',
    });
    setDialogOpen(true);
    console.log('[SUPERVISOR] Dialog opened. Available workers:', workers.length);
  };

  const handleSave = async () => {
    console.log('[SUPERVISOR] ========================================');
    console.log('[SUPERVISOR] ASSIGN TASK BUTTON CLICKED!');
    console.log('[SUPERVISOR] ========================================');
    
    try {
      console.log('[SUPERVISOR] Current form data:', formData);
      
      // Validate required fields
      if (!formData.worker_id || !formData.title) {
        console.error('[SUPERVISOR] ❌ VALIDATION FAILED');
        console.error('[SUPERVISOR] Worker ID:', formData.worker_id);
        console.error('[SUPERVISOR] Title:', formData.title);
        alert('❌ Please select a worker and enter a task title');
        return;
      }

      console.log('[SUPERVISOR] ✅ Validation passed');

      const taskData = {
        worker_id: parseInt(formData.worker_id),
        role_id: formData.role_id ? parseInt(formData.role_id) : null,
        title: formData.title,
        description: formData.description || '',
        priority: formData.priority || 'medium',
        due_date: formData.due_date || null,
        assigned_by: 'Supervisor Dashboard',
      };

      console.log('[SUPERVISOR] 📤 Sending task to backend...');
      console.log('[SUPERVISOR] Task data:', JSON.stringify(taskData, null, 2));
      console.log('[SUPERVISOR] Backend URL:', `${API_BASE_URL}/task/create`);

      const response = await axios.post(`${API_BASE_URL}/task/create`, taskData);
      
      console.log('[SUPERVISOR] 🎉🎉🎉 SUCCESS! 🎉🎉🎉');
      console.log('[SUPERVISOR] Response status:', response.status);
      console.log('[SUPERVISOR] Task created:', response.data);
      console.log('[SUPERVISOR] Task ID:', response.data.id);
      console.log('[SUPERVISOR] Worker ID:', response.data.worker_id);
      console.log('[SUPERVISOR] Title:', response.data.title);
      
      // Get worker name
      const workerName = workers.find(w => w.id === parseInt(formData.worker_id))?.name || 'Unknown Worker';
      console.log('[SUPERVISOR] Assigned to:', workerName);
      
      // Close dialog
      setDialogOpen(false);
      
      // Reset form
      setFormData({
        worker_id: '',
        role_id: '',
        title: '',
        description: '',
        priority: 'medium',
        due_date: '',
      });
      
      // Reload tasks
      console.log('[SUPERVISOR] Reloading task list...');
      await loadTasks();
      
      // Show success message
      const successMsg = `✅ TASK ASSIGNED!\n\nTask: ${response.data.title}\nWorker: ${workerName} (ID: ${response.data.worker_id})\nTask ID: ${response.data.id}\n\n✨ The mobile app will show this within 2 seconds!`;
      
      setSuccessMessage(`✅ Task "${response.data.title}" assigned to ${workerName}! Mobile app will update within 2 seconds.`);
      setTimeout(() => setSuccessMessage(''), 8000);
      
      console.log('[SUPERVISOR] Showing success alert...');
      alert(successMsg);
      
      console.log('[SUPERVISOR] ========================================');
      console.log('[SUPERVISOR] TASK ASSIGNMENT COMPLETE!');
      console.log('[SUPERVISOR] Now check the mobile app!');
      console.log('[SUPERVISOR] ========================================');
      
    } catch (error) {
      console.error('[SUPERVISOR] ========================================');
      console.error('[SUPERVISOR] ❌❌❌ ERROR ❌❌❌');
      console.error('[SUPERVISOR] ========================================');
      console.error('[SUPERVISOR] Error object:', error);
      console.error('[SUPERVISOR] Error message:', error.message);
      console.error('[SUPERVISOR] Error response:', error.response);
      console.error('[SUPERVISOR] Response data:', error.response?.data);
      console.error('[SUPERVISOR] Response status:', error.response?.status);
      
      const errorMsg = error.response?.data?.detail || error.message || 'Unknown error';
      
      alert(`❌ FAILED TO ASSIGN TASK!\n\nError: ${errorMsg}\n\nBackend URL: ${API_BASE_URL}\n\nCheck console (F12) for details.`);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'in_progress':
        return 'primary';
      case 'pending':
        return 'default';
      default:
        return 'default';
    }
  };

  const getWorkerName = (workerId) => {
    const worker = workers.find((w) => w.id === workerId);
    return worker ? worker.name : `Worker ${workerId}`;
  };

  const getRoleName = (roleId) => {
    if (!roleId) return 'No specific role';
    const role = roles.find((r) => r.id === roleId);
    return role ? role.name : `Role ${roleId}`;
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Task Management</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={handleAdd}>
          Assign New Task
        </Button>
      </Box>

      {successMessage && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccessMessage('')}>
          {successMessage}
        </Alert>
      )}

      <Grid container spacing={3}>
        {tasks.map((task) => (
          <Grid item xs={12} md={6} lg={4} key={task.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                  <Typography variant="h6" sx={{ flex: 1 }}>
                    {task.title}
                  </Typography>
                  <Chip
                    label={task.priority}
                    color={getPriorityColor(task.priority)}
                    size="small"
                    sx={{ textTransform: 'capitalize' }}
                  />
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {task.description || 'No description'}
                </Typography>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      Worker:
                    </Typography>
                    <Typography variant="body2">{getWorkerName(task.worker_id)}</Typography>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      Role:
                    </Typography>
                    <Typography variant="body2" color="primary">
                      {getRoleName(task.role_id)}
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      Status:
                    </Typography>
                    <Chip
                      label={task.status.replace('_', ' ')}
                      color={getStatusColor(task.status)}
                      size="small"
                      sx={{ textTransform: 'capitalize' }}
                    />
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      Assigned:
                    </Typography>
                    <Typography variant="body2">
                      {new Date(task.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>

                  {task.due_date && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        Due:
                      </Typography>
                      <Typography variant="body2">
                        {new Date(task.due_date).toLocaleDateString()}
                      </Typography>
                    </Box>
                  )}

                  {task.completed_at && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        Completed:
                      </Typography>
                      <Typography variant="body2">
                        {new Date(task.completed_at).toLocaleDateString()}
                      </Typography>
                    </Box>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Add/Edit Task Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Assignment />
            Assign New Task
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <FormControl fullWidth required>
              <InputLabel>Select Worker</InputLabel>
              <Select
                value={formData.worker_id}
                onChange={(e) => setFormData({ ...formData, worker_id: e.target.value })}
                label="Select Worker"
              >
                {workers.map((worker) => (
                  <MenuItem key={worker.id} value={worker.id}>
                    {worker.name} - {worker.current_role || 'No current role'}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Select Role (Optional)</InputLabel>
              <Select
                value={formData.role_id}
                onChange={(e) => setFormData({ ...formData, role_id: e.target.value })}
                label="Select Role (Optional)"
              >
                <MenuItem value="">
                  <em>No specific role</em>
                </MenuItem>
                {roles.map((role) => (
                  <MenuItem key={role.id} value={role.id}>
                    {role.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Task Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
              fullWidth
            />

            <TextField
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              multiline
              rows={3}
              fullWidth
            />

            <FormControl fullWidth>
              <InputLabel>Priority</InputLabel>
              <Select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                label="Priority"
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Due Date"
              type="datetime-local"
              value={formData.due_date}
              onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={!formData.worker_id || !formData.title}
          >
            Assign Task
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
