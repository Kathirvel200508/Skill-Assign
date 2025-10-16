import React, { useState, useEffect } from 'react';
import { View, ScrollView, StyleSheet, RefreshControl } from 'react-native';
import { Card, Title, Paragraph, Chip, ActivityIndicator, Text, Badge, Divider } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import apiClient from '../api/client';

export default function NotificationsScreen() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // For demo purposes, using worker ID 1. In production, this would come from authentication
  const workerId = 1;

  const loadAssignments = async () => {
    try {
      const response = await apiClient.get('/assignment/all');
      // Filter assignments for this worker
      const workerAssignments = response.data.filter(
        assignment => assignment.worker_id === workerId
      );
      // Sort by date (newest first)
      workerAssignments.sort((a, b) => new Date(b.assignment_date) - new Date(a.assignment_date));
      setAssignments(workerAssignments);
    } catch (error) {
      console.error('Error loading assignments:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadAssignments();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadAssignments();
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'completed':
        return '#4caf50';
      case 'in_progress':
        return '#2196f3';
      case 'pending':
        return '#ff9800';
      default:
        return '#757575';
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'completed':
        return 'check-circle';
      case 'in_progress':
        return 'progress-clock';
      case 'pending':
        return 'clock-outline';
      default:
        return 'information';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
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
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Title style={styles.headerTitle}>Task Notifications</Title>
        <Paragraph style={styles.headerSubtitle}>
          {assignments.length} {assignments.length === 1 ? 'assignment' : 'assignments'}
        </Paragraph>
      </View>

      {assignments.length === 0 ? (
        <Card style={styles.emptyCard}>
          <Card.Content style={styles.emptyContent}>
            <MaterialCommunityIcons name="bell-off-outline" size={64} color="#ccc" />
            <Title style={styles.emptyTitle}>No Notifications</Title>
            <Paragraph style={styles.emptyText}>
              You don't have any task assignments yet.
            </Paragraph>
          </Card.Content>
        </Card>
      ) : (
        assignments.map((assignment, index) => (
          <Card key={assignment.id || index} style={styles.notificationCard}>
            <Card.Content>
              <View style={styles.cardHeader}>
                <View style={styles.iconContainer}>
                  <MaterialCommunityIcons 
                    name={getStatusIcon(assignment.status)} 
                    size={24} 
                    color={getStatusColor(assignment.status)} 
                  />
                </View>
                <View style={styles.headerContent}>
                  <Title style={styles.roleTitle}>New Task Assignment</Title>
                  <Text style={styles.dateText}>{formatDate(assignment.assignment_date)}</Text>
                </View>
                <Chip 
                  style={[styles.statusChip, { backgroundColor: getStatusColor(assignment.status) }]}
                  textStyle={styles.statusText}
                >
                  {assignment.status || 'Pending'}
                </Chip>
              </View>

              <Divider style={styles.divider} />

              <View style={styles.detailsContainer}>
                <View style={styles.detailRow}>
                  <MaterialCommunityIcons name="briefcase" size={20} color="#666" />
                  <Text style={styles.detailLabel}>Role:</Text>
                  <Text style={styles.detailValue}>{assignment.role_name || 'Not specified'}</Text>
                </View>

                <View style={styles.detailRow}>
                  <MaterialCommunityIcons name="chart-line" size={20} color="#666" />
                  <Text style={styles.detailLabel}>Fit Score:</Text>
                  <Text style={styles.detailValue}>
                    {assignment.fit_score ? `${(assignment.fit_score * 100).toFixed(0)}%` : 'N/A'}
                  </Text>
                </View>

                {assignment.predicted_performance && (
                  <View style={styles.detailRow}>
                    <MaterialCommunityIcons name="star" size={20} color="#666" />
                    <Text style={styles.detailLabel}>Expected Performance:</Text>
                    <Text style={styles.detailValue}>
                      {(assignment.predicted_performance * 100).toFixed(0)}%
                    </Text>
                  </View>
                )}

                {assignment.notes && (
                  <View style={styles.notesContainer}>
                    <MaterialCommunityIcons name="note-text" size={20} color="#666" />
                    <Text style={styles.notesLabel}>Notes:</Text>
                    <Text style={styles.notesText}>{assignment.notes}</Text>
                  </View>
                )}
              </View>

              {assignment.feedback && (
                <View style={styles.feedbackContainer}>
                  <Text style={styles.feedbackLabel}>Feedback:</Text>
                  <Text style={styles.feedbackText}>{assignment.feedback}</Text>
                </View>
              )}
            </Card.Content>
          </Card>
        ))
      )}
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
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  emptyCard: {
    margin: 16,
    marginTop: 32,
  },
  emptyContent: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyTitle: {
    marginTop: 16,
    fontSize: 20,
    color: '#666',
  },
  emptyText: {
    marginTop: 8,
    color: '#999',
    textAlign: 'center',
  },
  notificationCard: {
    margin: 16,
    marginBottom: 8,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#f5f5f5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  headerContent: {
    flex: 1,
  },
  roleTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 2,
  },
  dateText: {
    fontSize: 12,
    color: '#666',
  },
  statusChip: {
    height: 28,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
  },
  divider: {
    marginVertical: 12,
  },
  detailsContainer: {
    marginTop: 8,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  detailLabel: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
    marginRight: 4,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  notesContainer: {
    flexDirection: 'column',
    marginTop: 8,
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
  },
  notesLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: '#666',
    marginBottom: 4,
  },
  notesText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
  },
  feedbackContainer: {
    marginTop: 12,
    padding: 12,
    backgroundColor: '#e8f5e9',
    borderRadius: 8,
  },
  feedbackLabel: {
    fontSize: 12,
    fontWeight: '500',
    color: '#2e7d32',
    marginBottom: 4,
  },
  feedbackText: {
    fontSize: 14,
    color: '#1b5e20',
  },
});
