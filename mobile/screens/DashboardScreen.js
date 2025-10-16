import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  RefreshControl,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  ActivityIndicator,
  Chip,
  Divider,
  Text,
  Portal,
  Modal,
  List,
} from 'react-native-paper';
import { roleAPI, predictionAPI, assignmentAPI, analyticsAPI } from '../api/client';

export default function DashboardScreen() {
  const [roles, setRoles] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [loadingPredictions, setLoadingPredictions] = useState(false);

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
      Alert.alert('Error', 'Failed to load data. Make sure the backend is running.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleGetRecommendations = async (role) => {
    setSelectedRole(role);
    setLoadingPredictions(true);
    setShowModal(true);

    try {
      const response = await predictionAPI.predictFit(role.id, 5);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      Alert.alert('Error', 'Failed to get recommendations');
      setShowModal(false);
    } finally {
      setLoadingPredictions(false);
    }
  };

  const handleAssignWorker = async (workerId, roleId, fitScore) => {
    try {
      await assignmentAPI.create({
        worker_id: workerId,
        role_id: roleId,
        fit_score: fitScore,
      });
      Alert.alert('Success', 'Worker assigned successfully!');
      setShowModal(false);
      loadData();
    } catch (error) {
      console.error('Error assigning worker:', error);
      Alert.alert('Error', 'Failed to assign worker');
    }
  };

  const getFatigueColor = (level) => {
    if (level < 0.3) return '#4caf50';
    if (level < 0.7) return '#ff9800';
    return '#f44336';
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#6200ee" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      {/* Analytics Overview */}
      {analytics && (
        <Card style={styles.card}>
          <Card.Content>
            <Title>Analytics Overview</Title>
            <View style={styles.statsContainer}>
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{analytics.total_workers}</Text>
                <Text style={styles.statLabel}>Workers</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{analytics.total_roles}</Text>
                <Text style={styles.statLabel}>Roles</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{analytics.total_assignments}</Text>
                <Text style={styles.statLabel}>Assignments</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statValue}>
                  {(analytics.success_rate * 100).toFixed(0)}%
                </Text>
                <Text style={styles.statLabel}>Success Rate</Text>
              </View>
            </View>
            
            <Divider style={styles.divider} />
            
            <Paragraph style={styles.sectionTitle}>Fatigue Distribution</Paragraph>
            <View style={styles.fatigueContainer}>
              <Chip icon="check-circle" style={[styles.chip, { backgroundColor: '#e8f5e9' }]}>
                Low: {analytics.workers_by_fatigue.low}
              </Chip>
              <Chip icon="alert-circle" style={[styles.chip, { backgroundColor: '#fff3e0' }]}>
                Medium: {analytics.workers_by_fatigue.medium}
              </Chip>
              <Chip icon="close-circle" style={[styles.chip, { backgroundColor: '#ffebee' }]}>
                High: {analytics.workers_by_fatigue.high}
              </Chip>
            </View>
          </Card.Content>
        </Card>
      )}

      {/* Roles List */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Available Roles</Title>
          <Paragraph style={styles.subtitle}>
            Select a role to get AI-powered worker recommendations
          </Paragraph>
        </Card.Content>
      </Card>

      {roles.map((role) => (
        <Card key={role.id} style={styles.roleCard}>
          <Card.Content>
            <Title>{role.name}</Title>
            <Paragraph style={styles.difficulty}>
              Difficulty: {(role.difficulty_level * 10).toFixed(1)}/10
            </Paragraph>
            
            <View style={styles.skillsContainer}>
              {role.required_skills.map((skill, index) => (
                <Chip key={index} style={styles.skillChip} mode="outlined">
                  {skill}
                </Chip>
              ))}
            </View>

            {role.current_assignee_id && (
              <Chip icon="account-check" style={styles.assignedChip}>
                Currently Assigned
              </Chip>
            )}
          </Card.Content>
          <Card.Actions>
            <Button
              mode="contained"
              onPress={() => handleGetRecommendations(role)}
              icon="account-search"
            >
              Find Best Workers
            </Button>
          </Card.Actions>
        </Card>
      ))}

      {/* Recommendations Modal */}
      <Portal>
        <Modal
          visible={showModal}
          onDismiss={() => setShowModal(false)}
          contentContainerStyle={styles.modalContainer}
        >
          <Title style={styles.modalTitle}>
            Recommendations for {selectedRole?.name}
          </Title>

          {loadingPredictions ? (
            <ActivityIndicator size="large" color="#6200ee" style={styles.modalLoader} />
          ) : (
            <ScrollView style={styles.recommendationsList}>
              {recommendations.map((rec, index) => (
                <Card key={rec.worker_id} style={styles.recommendationCard}>
                  <Card.Content>
                    <View style={styles.recommendationHeader}>
                      <Title>#{index + 1} {rec.worker_name}</Title>
                      <Chip
                        style={[
                          styles.scoreChip,
                          { backgroundColor: rec.fit_score > 0.7 ? '#4caf50' : '#ff9800' },
                        ]}
                      >
                        {(rec.fit_score * 100).toFixed(0)}% Fit
                      </Chip>
                    </View>

                    <View style={styles.metricsRow}>
                      <Text style={styles.metricLabel}>Performance:</Text>
                      <Text style={styles.metricValue}>
                        {(rec.performance_score * 100).toFixed(0)}%
                      </Text>
                    </View>

                    <View style={styles.metricsRow}>
                      <Text style={styles.metricLabel}>Skill Match:</Text>
                      <Text style={styles.metricValue}>
                        {rec.skill_match_percentage.toFixed(0)}%
                      </Text>
                    </View>

                    <View style={styles.metricsRow}>
                      <Text style={styles.metricLabel}>Fatigue:</Text>
                      <Chip
                        style={[
                          styles.fatigueChip,
                          { backgroundColor: getFatigueColor(rec.fatigue_level) },
                        ]}
                      >
                        {(rec.fatigue_level * 100).toFixed(0)}%
                      </Chip>
                    </View>

                    <View style={styles.skillsContainer}>
                      {rec.skills.slice(0, 4).map((skill, idx) => (
                        <Chip key={idx} style={styles.smallChip} compact>
                          {skill}
                        </Chip>
                      ))}
                    </View>
                  </Card.Content>
                  <Card.Actions>
                    <Button
                      mode="contained"
                      onPress={() =>
                        handleAssignWorker(rec.worker_id, selectedRole.id, rec.fit_score)
                      }
                    >
                      Assign Role
                    </Button>
                  </Card.Actions>
                </Card>
              ))}
            </ScrollView>
          )}

          <Button mode="outlined" onPress={() => setShowModal(false)} style={styles.closeButton}>
            Close
          </Button>
        </Modal>
      </Portal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    margin: 16,
    marginBottom: 8,
  },
  roleCard: {
    margin: 16,
    marginTop: 8,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#6200ee',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  divider: {
    marginVertical: 16,
  },
  sectionTitle: {
    fontWeight: 'bold',
    marginBottom: 8,
  },
  fatigueContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chip: {
    marginRight: 8,
    marginBottom: 8,
  },
  subtitle: {
    color: '#666',
    fontSize: 14,
  },
  difficulty: {
    color: '#666',
    marginBottom: 8,
  },
  skillsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 8,
  },
  skillChip: {
    marginRight: 8,
    marginBottom: 8,
  },
  smallChip: {
    marginRight: 4,
    marginBottom: 4,
  },
  assignedChip: {
    marginTop: 8,
    backgroundColor: '#e8f5e9',
  },
  modalContainer: {
    backgroundColor: 'white',
    margin: 20,
    borderRadius: 8,
    maxHeight: '80%',
  },
  modalTitle: {
    padding: 16,
    paddingBottom: 8,
  },
  modalLoader: {
    padding: 32,
  },
  recommendationsList: {
    maxHeight: 400,
  },
  recommendationCard: {
    margin: 16,
    marginTop: 8,
  },
  recommendationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  scoreChip: {
    color: 'white',
  },
  metricsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  metricLabel: {
    color: '#666',
  },
  metricValue: {
    fontWeight: 'bold',
  },
  fatigueChip: {
    color: 'white',
  },
  closeButton: {
    margin: 16,
  },
});
