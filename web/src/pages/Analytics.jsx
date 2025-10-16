import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from '@mui/material';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { analyticsAPI, predictionAPI } from '../api';
import api from '../api';

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [skillGap, setSkillGap] = useState(null);
  const [training, setTraining] = useState(false);
  const [trainResult, setTrainResult] = useState(null);

  useEffect(() => {
    loadAnalytics();
    loadSkillGap();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await analyticsAPI.getOverview();
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    }
  };

  const loadSkillGap = async () => {
    try {
      const response = await api.get('/analytics/skill-gap');
      setSkillGap(response.data);
    } catch (error) {
      console.error('Error loading skill gap:', error);
    }
  };

  const handleTrainModel = async () => {
    setTraining(true);
    setTrainResult(null);
    try {
      const response = await predictionAPI.trainModel();
      setTrainResult(response.data);
      alert('Model trained successfully!');
    } catch (error) {
      console.error('Error training model:', error);
      alert('Failed to train model: ' + (error.response?.data?.detail || error.message));
    } finally {
      setTraining(false);
    }
  };

  if (!analytics) {
    return <Typography>Loading...</Typography>;
  }

  // Prepare chart data
  const skillsChartData = Object.entries(analytics.skills_distribution || {}).map(([skill, count]) => ({
    skill,
    workers: count
  }));

  const hoursChartData = Object.entries(analytics.average_hours_per_week || {}).map(([id, data]) => ({
    name: data.name,
    hours: data.hours
  }));

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High': return 'error';
      case 'Medium': return 'warning';
      case 'Low': return 'info';
      default: return 'default';
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Analytics & Insights
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Overall Statistics */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Overall Statistics
              </Typography>
              <Typography variant="body1">
                Total Workers: {analytics.total_workers}
              </Typography>
              <Typography variant="body1">
                Total Roles: {analytics.total_roles}
              </Typography>
              <Typography variant="body1">
                Total Assignments: {analytics.total_assignments}
              </Typography>
              <Typography variant="body1">
                Average Fit Score: {(analytics.average_fit_score * 100).toFixed(1)}%
              </Typography>
              <Typography variant="body1">
                Success Rate: {(analytics.success_rate * 100).toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Performers
              </Typography>
              {analytics.top_performers.map((worker, idx) => (
                <Typography key={worker.id} variant="body1">
                  {idx + 1}. {worker.name} - Performance: {(worker.performance_score * 100).toFixed(0)}%
                </Typography>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Skills Distribution Bar Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Workers Available per Skill
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={skillsChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="skill" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="workers" fill="#1976d2" name="Number of Workers" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Hours Per Week Line Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Hours Worked Per Week
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={hoursChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis domain={[0, 52]} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="hours" stroke="#dc004e" strokeWidth={2} name="Hours/Week" />
                  <Line type="monotone" dataKey={() => 48} stroke="#ff9800" strokeDasharray="5 5" name="Warning (48h)" />
                  <Line type="monotone" dataKey={() => 52} stroke="#f44336" strokeDasharray="5 5" name="Max (52h)" />
                </LineChart>
              </ResponsiveContainer>
              <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                * Workers approaching 48-52 hours/week are at high fatigue risk
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Skill Gap Analysis */}
        {skillGap && skillGap.workers_needing_training.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Workers Needing Skill Development
                </Typography>
                <TableContainer component={Paper} variant="outlined" sx={{ mt: 2 }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell><strong>Worker</strong></TableCell>
                        <TableCell><strong>Current Skills</strong></TableCell>
                        <TableCell><strong>Recommended Skills</strong></TableCell>
                        <TableCell><strong>Reason</strong></TableCell>
                        <TableCell><strong>Priority</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {skillGap.workers_needing_training.map((rec) => (
                        <TableRow key={rec.worker_id}>
                          <TableCell>{rec.worker_name}</TableCell>
                          <TableCell>
                            {rec.current_skills.slice(0, 3).map((skill, idx) => (
                              <Chip key={idx} label={skill} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                            ))}
                            {rec.current_skills.length > 3 && (
                              <Chip label={`+${rec.current_skills.length - 3}`} size="small" />
                            )}
                          </TableCell>
                          <TableCell>
                            {rec.recommended_skills.map((skill, idx) => (
                              <Chip key={idx} label={skill} size="small" color="primary" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                            ))}
                          </TableCell>
                          <TableCell>{rec.reason}</TableCell>
                          <TableCell>
                            <Chip label={rec.priority} color={getPriorityColor(rec.priority)} size="small" />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Most Demanded Skills */}
        {skillGap && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Most In-Demand Skills
                </Typography>
                {skillGap.most_demanded_skills.slice(0, 5).map((item, idx) => (
                  <Box key={idx} display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body1">{item.skill}</Typography>
                    <Chip label={`${item.demand} roles`} size="small" color="primary" />
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* ML Model Training */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Machine Learning Model
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                Train the ML model with current assignment data to improve predictions.
                Requires at least 10 assignments with feedback.
              </Typography>
              <Button
                variant="contained"
                onClick={handleTrainModel}
                disabled={training}
                fullWidth
              >
                {training ? 'Training...' : 'Train Model'}
              </Button>
              {trainResult && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    Model trained successfully!
                  </Typography>
                  <Typography variant="body2">
                    MSE: {trainResult.metrics.mse.toFixed(4)} | 
                    R²: {trainResult.metrics.r2.toFixed(4)} | 
                    Samples: {trainResult.training_samples}
                  </Typography>
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}
