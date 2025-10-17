import React, { useState, useEffect } from 'react';
import { View, ScrollView, StyleSheet, RefreshControl } from 'react-native';
import { Card, Title, Paragraph, Chip, ActivityIndicator, Text, Badge, Divider } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import axios from 'axios';
import config from '../config';

export default function NotificationsScreen() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // Rajesh Kumar's Worker ID (Worker ID 1)
  // In production, this would come from authentication
  const workerId = 1;

  const loadNotifications = async () => {
    try {
      const response = await axios.get(
        `${config.API_BASE_URL}/task/worker/${workerId}/notifications`
      );
      setNotifications(response.data.notifications || []);
    } catch (error) {
      console.error('Error loading notifications:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    console.log('[MOBILE APP] NotificationsScreen loaded for Rajesh Kumar');
    loadNotifications();
    // Auto-refresh every 2 seconds for instant updates from supervisor
    const interval = setInterval(() => {
      console.log('[MOBILE APP] Checking for new notifications...');
      loadNotifications();
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadNotifications();
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
          {notifications.length} active {notifications.length === 1 ? 'task' : 'tasks'}
        </Paragraph>
      </View>

      {notifications.length === 0 ? (
        <Card style={styles.emptyCard}>
          <Card.Content style={styles.emptyContent}>
            <MaterialCommunityIcons name="bell-off-outline" size={64} color="#ccc" />
            <Title style={styles.emptyTitle}>No Active Tasks</Title>
            <Paragraph style={styles.emptyText}>
              You don't have any pending or in-progress tasks.
            </Paragraph>
          </Card.Content>
        </Card>
      ) : (
        notifications.map((notification, index) => (
          <Card key={notification.id || index} style={[
            styles.notificationCard,
            notification.is_new && styles.newNotificationCard
          ]}>
            <Card.Content>
              {notification.is_new && (
                <Badge style={styles.newBadge} size={8} />
              )}
              <View style={styles.cardHeader}>
                <View style={styles.iconContainer}>
                  <MaterialCommunityIcons 
                    name={getStatusIcon(notification.status)} 
                    size={24} 
                    color={getStatusColor(notification.status)} 
                  />
                </View>
                <View style={styles.headerContent}>
                  <Title style={styles.roleTitle}>{notification.title}</Title>
                  <Text style={styles.dateText}>{formatDate(notification.created_at)}</Text>
                </View>
                <Chip 
                  style={[styles.statusChip, { backgroundColor: getStatusColor(notification.status) }]}
                  textStyle={styles.statusText}
                >
                  {notification.status.replace('_', ' ')}
                </Chip>
              </View>

              <Divider style={styles.divider} />

              {notification.description && (
                <Paragraph style={styles.description}>{notification.description}</Paragraph>
              )}

              <View style={styles.detailsContainer}>
                <View style={styles.detailRow}>
                  <MaterialCommunityIcons name="briefcase" size={20} color="#666" />
                  <Text style={styles.detailLabel}>Role:</Text>
                  <Text style={styles.detailValue}>{notification.role_name}</Text>
                </View>

                <View style={styles.detailRow}>
                  <MaterialCommunityIcons name="account" size={20} color="#666" />
                  <Text style={styles.detailLabel}>Assigned by:</Text>
                  <Text style={styles.detailValue}>{notification.assigned_by}</Text>
                </View>

                <View style={styles.detailRow}>
                  <MaterialCommunityIcons 
                    name={notification.priority === 'high' ? 'alert-circle' : notification.priority === 'medium' ? 'alert' : 'information'} 
                    size={20} 
                    color={notification.priority === 'high' ? '#f44336' : notification.priority === 'medium' ? '#ff9800' : '#2196f3'} 
                  />
                  <Text style={styles.detailLabel}>Priority:</Text>
                  <Text style={[styles.detailValue, { textTransform: 'capitalize' }]}>
                    {notification.priority}
                  </Text>
                </View>

                {notification.due_date && (
                  <View style={styles.detailRow}>
                    <MaterialCommunityIcons name="calendar-clock" size={20} color="#666" />
                    <Text style={styles.detailLabel}>Due:</Text>
                    <Text style={styles.detailValue}>
                      {new Date(notification.due_date).toLocaleDateString()}
                    </Text>
                  </View>
                )}
              </View>
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
  newNotificationCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#6200ee',
  },
  newBadge: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: '#f44336',
  },
  description: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
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
