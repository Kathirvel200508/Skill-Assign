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
  LinearProgress,
} from '@mui/material';
import { Edit, Delete, Add } from '@mui/icons-material';
import { roleAPI } from '../api';

export default function Roles() {
  const [roles, setRoles] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingRole, setEditingRole] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    required_skills: '',
    difficulty_level: '0.5',
  });

  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    try {
      const response = await roleAPI.getAll();
      setRoles(response.data);
    } catch (error) {
      console.error('Error loading roles:', error);
    }
  };

  const handleAdd = () => {
    setEditingRole(null);
    setFormData({
      name: '',
      required_skills: '',
      difficulty_level: '0.5',
    });
    setDialogOpen(true);
  };

  const handleEdit = (role) => {
    setEditingRole(role);
    setFormData({
      name: role.name,
      required_skills: role.required_skills.join(', '),
      difficulty_level: role.difficulty_level.toString(),
    });
    setDialogOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this role?')) {
      try {
        await roleAPI.delete(id);
        loadRoles();
      } catch (error) {
        console.error('Error deleting role:', error);
      }
    }
  };

  const handleSave = async () => {
    const data = {
      name: formData.name,
      required_skills: formData.required_skills.split(',').map(s => s.trim()).filter(s => s),
      difficulty_level: parseFloat(formData.difficulty_level),
    };

    try {
      if (editingRole) {
        await roleAPI.update(editingRole.id, data);
      } else {
        await roleAPI.add(data);
      }
      setDialogOpen(false);
      loadRoles();
    } catch (error) {
      console.error('Error saving role:', error);
      alert('Failed to save role');
    }
  };

  return (
    <div>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Roles Management</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={handleAdd}>
          Add Role
        </Button>
      </Box>

      <Grid container spacing={3}>
        {roles.map((role) => (
          <Grid item xs={12} md={6} key={role.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="start">
                  <div>
                    <Typography variant="h6">{role.name}</Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                      Difficulty Level
                    </Typography>
                    <Box display="flex" alignItems="center" mt={1}>
                      <LinearProgress
                        variant="determinate"
                        value={role.difficulty_level * 100}
                        sx={{ flexGrow: 1, mr: 2, height: 8, borderRadius: 4 }}
                        color={role.difficulty_level < 0.5 ? 'success' : role.difficulty_level < 0.8 ? 'warning' : 'error'}
                      />
                      <Typography variant="body2">
                        {(role.difficulty_level * 10).toFixed(1)}/10
                      </Typography>
                    </Box>
                  </div>
                  <Box>
                    <IconButton size="small" onClick={() => handleEdit(role)}>
                      <Edit />
                    </IconButton>
                    <IconButton size="small" onClick={() => handleDelete(role.id)}>
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>

                {role.current_assignee_id && (
                  <Chip label="Currently Assigned" color="success" size="small" sx={{ mt: 2 }} />
                )}

                <Typography variant="body2" sx={{ mt: 2, mb: 1 }}>
                  Required Skills:
                </Typography>
                <Box>
                  {role.required_skills.map((skill, idx) => (
                    <Chip key={idx} label={skill} size="small" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingRole ? 'Edit Role' : 'Add Role'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Role Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Required Skills (comma separated)"
            value={formData.required_skills}
            onChange={(e) => setFormData({ ...formData, required_skills: e.target.value })}
            margin="normal"
            multiline
            rows={2}
          />
          <TextField
            fullWidth
            label="Difficulty Level (0-1)"
            type="number"
            value={formData.difficulty_level}
            onChange={(e) => setFormData({ ...formData, difficulty_level: e.target.value })}
            margin="normal"
            inputProps={{ step: 0.1, min: 0, max: 1 }}
            helperText="0 = Easy, 0.5 = Medium, 1 = Very Difficult"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">
            {editingRole ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
