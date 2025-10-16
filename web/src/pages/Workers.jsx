import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { Edit, Delete, Add } from '@mui/icons-material';
import { workerAPI } from '../api';

export default function Workers() {
  const [workers, setWorkers] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingWorker, setEditingWorker] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    experience: '',
    skills: '',
    hours_per_day: '8.0',
    hours_per_week: '40.0',
    fatigue_level: '0.2',
    performance_score: '0.75',
  });

  useEffect(() => {
    loadWorkers();
  }, []);

  const loadWorkers = async () => {
    try {
      const response = await workerAPI.getAll();
      setWorkers(response.data);
    } catch (error) {
      console.error('Error loading workers:', error);
    }
  };

  const handleAdd = () => {
    setEditingWorker(null);
    setFormData({
      name: '',
      age: '',
      experience: '',
      skills: '',
      hours_per_day: '8.0',
      hours_per_week: '40.0',
      fatigue_level: '0.2',
      performance_score: '0.75',
    });
    setDialogOpen(true);
  };

  const handleEdit = (worker) => {
    setEditingWorker(worker);
    setFormData({
      name: worker.name,
      age: worker.age.toString(),
      experience: worker.experience.toString(),
      skills: worker.skills.join(', '),
      hours_per_day: worker.hours_per_day?.toString() || '8.0',
      hours_per_week: worker.hours_per_week?.toString() || '40.0',
      fatigue_level: worker.fatigue_level.toString(),
      performance_score: worker.performance_score.toString(),
    });
    setDialogOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this worker?')) {
      try {
        await workerAPI.delete(id);
        loadWorkers();
      } catch (error) {
        console.error('Error deleting worker:', error);
      }
    }
  };

  const handleSave = async () => {
    // Calculate fatigue from hours worked
    const hoursPerWeek = parseFloat(formData.hours_per_week);
    const hoursPerDay = parseFloat(formData.hours_per_day);
    const calculatedFatigue = Math.min(
      (hoursPerWeek / 52) * 0.7 + (hoursPerDay / 8.5) * 0.3,
      1.0
    );

    const data = {
      name: formData.name,
      age: parseInt(formData.age),
      experience: parseFloat(formData.experience),
      skills: formData.skills.split(',').map(s => s.trim()).filter(s => s),
      hours_per_day: parseFloat(formData.hours_per_day),
      hours_per_week: parseFloat(formData.hours_per_week),
      fatigue_level: calculatedFatigue,
      performance_score: parseFloat(formData.performance_score),
    };

    try {
      if (editingWorker) {
        await workerAPI.update(editingWorker.id, data);
      } else {
        await workerAPI.add(data);
      }
      setDialogOpen(false);
      loadWorkers();
    } catch (error) {
      console.error('Error saving worker:', error);
      alert('Failed to save worker');
    }
  };

  return (
    <div>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Workers Management</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={handleAdd}>
          Add Worker
        </Button>
      </Box>

      <Grid container spacing={3}>
        {workers.map((worker) => (
          <Grid item xs={12} md={6} key={worker.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="start">
                  <div>
                    <Typography variant="h6">{worker.name}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      Age: {worker.age} | Experience: {worker.experience} years
                    </Typography>
                  </div>
                  <Box>
                    <IconButton size="small" onClick={() => handleEdit(worker)}>
                      <Edit />
                    </IconButton>
                    <IconButton size="small" onClick={() => handleDelete(worker.id)}>
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>

                <Box mt={2}>
                  <Chip
                    label={`Performance: ${(worker.performance_score * 100).toFixed(0)}%`}
                    color="primary"
                    size="small"
                    sx={{ mr: 1, mb: 1 }}
                  />
                  <Chip
                    label={`${worker.hours_per_day || 8}h/day`}
                    color={worker.hours_per_day > 8 ? 'warning' : 'success'}
                    size="small"
                    sx={{ mr: 1, mb: 1 }}
                  />
                  <Chip
                    label={`${worker.hours_per_week || 40}h/week`}
                    color={worker.hours_per_week >= 50 ? 'error' : worker.hours_per_week >= 45 ? 'warning' : 'success'}
                    size="small"
                    sx={{ mb: 1 }}
                  />
                </Box>

                {worker.current_role && (
                  <Chip label={`Current: ${worker.current_role}`} sx={{ mt: 1 }} />
                )}

                <Box mt={2}>
                  {worker.skills.map((skill, idx) => (
                    <Chip key={idx} label={skill} size="small" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingWorker ? 'Edit Worker' : 'Add Worker'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Age"
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Experience (years)"
            type="number"
            value={formData.experience}
            onChange={(e) => setFormData({ ...formData, experience: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Skills (comma separated)"
            value={formData.skills}
            onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
            margin="normal"
            multiline
            rows={2}
          />
          <TextField
            fullWidth
            label="Hours Per Day"
            type="number"
            value={formData.hours_per_day}
            onChange={(e) => setFormData({ ...formData, hours_per_day: e.target.value })}
            margin="normal"
            inputProps={{ step: 0.5, min: 0, max: 8.5 }}
            helperText="Maximum 8.5 hours per day"
          />
          <TextField
            fullWidth
            label="Hours Per Week"
            type="number"
            value={formData.hours_per_week}
            onChange={(e) => setFormData({ ...formData, hours_per_week: e.target.value })}
            margin="normal"
            inputProps={{ step: 1, min: 0, max: 52 }}
            helperText="Maximum 52 hours per week (fatigue calculated automatically)"
          />
          <TextField
            fullWidth
            label="Performance Score (0-1)"
            type="number"
            value={formData.performance_score}
            onChange={(e) => setFormData({ ...formData, performance_score: e.target.value })}
            margin="normal"
            inputProps={{ step: 0.1, min: 0, max: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">
            {editingWorker ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
