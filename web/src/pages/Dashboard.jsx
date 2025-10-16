import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Chip,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import { roleAPI, predictionAPI, assignmentAPI, analyticsAPI } from '../api';

export default function Dashboard() {
  const [roles, setRoles] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedRole, setSelectedRole] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [loadingRecs, setLoadingRecs] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [rolesRes, analyticsRes] = await Promise.all([
        roleAPI.getAll(),
        analyticsAPI.getOverview(),
      ]);
      setRoles(rolesRes.data);
      setAnalytics(analyticsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = async (role) => {
    setSelectedRole(role);
    setDialogOpen(true);
    setLoadingRecs(true);
    setRecommendations([]); // Clear previous recommendations

    try {
      console.log('Fetching recommendations for role:', role.id);
      const response = await predictionAPI.predictFit(role.id, 5);
      console.log('Recommendations received:', response.data);
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      alert('Failed to get recommendations: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoadingRecs(false);
    }
  };

  const getFatigueColor = (hoursPerWeek) => {
    if (hoursPerWeek >= 50) return 'error';
    if (hoursPerWeek >= 45) return 'warning';
    return 'success';
  };

  const handleAssign = async (workerId, roleId, fitScore) => {
    try {
      await assignmentAPI.create({
        worker_id: workerId,
        role_id: roleId,
        fit_score: fitScore,
      });
      alert('Worker assigned successfully!');
      setDialogOpen(false);
      loadData();
    } catch (error) {
      console.error('Error assigning worker:', error);
      alert('Failed to assign worker');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Supervisor Dashboard
      </Typography>

      {/* Analytics Cards */}
      {analytics && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Total Workers
                </Typography>
                <Typography variant="h3">{analytics.total_workers}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Total Roles
                </Typography>
                <Typography variant="h3">{analytics.total_roles}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Assignments
                </Typography>
                <Typography variant="h3">{analytics.total_assignments}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Success Rate
                </Typography>
                <Typography variant="h3">
                  {(analytics.success_rate * 100).toFixed(0)}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Roles List */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Available Roles
      </Typography>
      <Grid container spacing={3}>
        {roles.map((role) => (
          <Grid item xs={12} md={6} key={role.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {role.name}
                </Typography>
                {role.description && (
                  <Typography variant="body2" color="textSecondary" gutterBottom sx={{ mb: 2 }}>
                    {role.description}
                  </Typography>
                )}
                <Typography color="textSecondary" gutterBottom>
                  Difficulty: {(role.difficulty_level * 10).toFixed(1)}/10
                </Typography>
                {role.typical_tasks && role.typical_tasks.length > 0 && (
                  <Box sx={{ mt: 1, mb: 2 }}>
                    <Typography variant="caption" color="textSecondary">
                      Key Tasks:
                    </Typography>
                    <ul style={{ margin: '4px 0', paddingLeft: '20px' }}>
                      {role.typical_tasks.slice(0, 3).map((task, idx) => (
                        <li key={idx}>
                          <Typography variant="caption">{task}</Typography>
                        </li>
                      ))}
                    </ul>
                  </Box>
                )}
                <Box sx={{ mt: 2, mb: 2 }}>
                  <Typography variant="caption" color="textSecondary">
                    Required Skills:
                  </Typography>
                  <Box sx={{ mt: 0.5 }}>
                    {role.required_skills.map((skill, idx) => (
                      <Chip key={idx} label={skill} size="small" sx={{ mr: 1, mb: 1 }} />
                    ))}
                  </Box>
                </Box>
                {role.current_assignee_id && (
                  <Chip label="Currently Assigned" color="success" size="small" sx={{ mb: 2 }} />
                )}
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => handleGetRecommendations(role)}
                >
                  Find Best Workers
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recommendations Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Recommendations for {selectedRole?.name}
        </DialogTitle>
        <DialogContent>
          {loadingRecs ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
              <Typography sx={{ ml: 2 }}>Loading recommendations...</Typography>
            </Box>
          ) : recommendations.length === 0 ? (
            <Alert severity="info" sx={{ mt: 2 }}>
              No recommendations available. Please ensure workers exist in the system.
            </Alert>
          ) : (
            <List>
              {recommendations.map((rec, idx) => (
                <Card key={rec.worker_id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Typography variant="h6">
                        #{idx + 1} {rec.worker_name}
                      </Typography>
                      <Chip
                        label={`${(rec.fit_score * 100).toFixed(0)}% Fit`}
                        color={rec.fit_score > 0.7 ? 'success' : 'warning'}
                      />
                    </Box>
                    <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                      Performance: {(rec.performance_score * 100).toFixed(0)}% | 
                      Skill Match: {rec.skill_match_percentage.toFixed(0)}%
                    </Typography>
                    <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                      <Chip 
                        label={`${rec.hours_per_day}h/day`} 
                        size="small" 
                        color={rec.hours_per_day > 8 ? 'warning' : 'success'}
                      />
                      <Chip 
                        label={`${rec.hours_per_week}h/week`} 
                        size="small" 
                        color={getFatigueColor(rec.hours_per_week)}
                      />
                    </Box>
                    <Box sx={{ mt: 1 }}>
                      {rec.skills.slice(0, 5).map((skill, i) => (
                        <Chip key={i} label={skill} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                      ))}
                    </Box>
                    <Button
                      variant="contained"
                      size="small"
                      sx={{ mt: 2 }}
                      onClick={() => handleAssign(rec.worker_id, selectedRole.id, rec.fit_score)}
                    >
                      Assign to Role
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
