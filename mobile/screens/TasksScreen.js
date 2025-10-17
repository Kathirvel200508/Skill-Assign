import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
} from 'react-native';
import axios from 'axios';
import config from '../config';

export default function TasksScreen({ route }) {
  const [tasks, setTasks] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [previousTaskCount, setPreviousTaskCount] = useState(0);
  const [showNewTaskAlert, setShowNewTaskAlert] = useState(false);
  // Rajesh Kumar's Worker ID
  const workerId = route.params?.workerId || 1; // Worker ID 1 = Rajesh Kumar

  useEffect(() => {
    console.log('[MOBILE APP] TasksScreen loaded for Rajesh Kumar (Worker ID: 1)');
    loadTasks();
    // Auto-refresh every 2 seconds for instant updates
    const interval = setInterval(() => {
      console.log('[MOBILE APP] Auto-checking for new tasks...');
      loadTasks();
    }, 2000);
    return () => clearInterval(interval);
  }, [workerId]);

  const loadTasks = async () => {
    try {
      const response = await axios.get(
        `${config.API_BASE_URL}/task/worker/${workerId}`
      );
      
      console.log(`[MOBILE APP] ✅ Tasks loaded: ${response.data.length} tasks for Rajesh Kumar`);
      
      // Check if new tasks were added
      if (previousTaskCount > 0 && response.data.length > previousTaskCount) {
        const newTasksCount = response.data.length - previousTaskCount;
        console.log(`[MOBILE APP] 🎉🎉🎉 ${newTasksCount} NEW TASK(S) ASSIGNED FROM SUPERVISOR!`);
        console.log(`[MOBILE APP] New task title: ${response.data[0].title}`);
        setShowNewTaskAlert(true);
        setTimeout(() => setShowNewTaskAlert(false), 5000);
      }
      
      setPreviousTaskCount(response.data.length);
      setTasks(response.data);
      
      if (response.data.length > 0 && tasks.length === 0) {
        console.log(`[MOBILE APP] Current tasks: ${response.data.length}`);
      }
    } catch (error) {
      console.error('[MOBILE APP] ❌ Error loading tasks:', error.message);
      // Don't show alert on every refresh error
    } finally {
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadTasks();
  };

  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      await axios.put(`${config.API_BASE_URL}/task/${taskId}`, {
        status: newStatus,
      });
      loadTasks();
      Alert.alert('Success', `Task marked as ${newStatus.replace('_', ' ')}`);
    } catch (error) {
      console.error('Error updating task:', error);
      Alert.alert('Error', 'Failed to update task status');
    }
  };

  const handleTaskAction = (task) => {
    const actions = [];
    
    if (task.status === 'pending') {
      actions.push({
        text: 'Start Task',
        onPress: () => updateTaskStatus(task.id, 'in_progress'),
      });
    }
    
    if (task.status === 'in_progress') {
      actions.push({
        text: 'Mark as Completed',
        onPress: () => updateTaskStatus(task.id, 'completed'),
      });
    }
    
    actions.push({ text: 'Cancel', style: 'cancel' });

    Alert.alert('Task Actions', `What would you like to do with "${task.title}"?`, actions);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return '#f44336';
      case 'medium':
        return '#ff9800';
      case 'low':
        return '#2196f3';
      default:
        return '#757575';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#4caf50';
      case 'in_progress':
        return '#2196f3';
      case 'pending':
        return '#757575';
      default:
        return '#757575';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const pendingTasks = tasks.filter((t) => t.status === 'pending');
  const inProgressTasks = tasks.filter((t) => t.status === 'in_progress');
  const completedTasks = tasks.filter((t) => t.status === 'completed');

  const renderTask = (task) => (
    <View key={task.id} style={styles.taskCard}>
      <TouchableOpacity
        onPress={() => handleTaskAction(task)}
        style={styles.taskContent}
      >
        <View style={styles.taskHeader}>
          <Text style={styles.taskTitle}>{task.title}</Text>
          <View
            style={[styles.priorityBadge, { backgroundColor: getPriorityColor(task.priority) }]}
          >
            <Text style={styles.priorityText}>{task.priority.toUpperCase()}</Text>
          </View>
        </View>

        {task.description && (
          <Text style={styles.taskDescription}>{task.description}</Text>
        )}

        <View style={styles.taskFooter}>
          <View style={[styles.statusBadge, { backgroundColor: getStatusColor(task.status) }]}>
            <Text style={styles.statusText}>{task.status.replace('_', ' ').toUpperCase()}</Text>
          </View>
          <Text style={styles.taskDate}>Due: {formatDate(task.due_date)}</Text>
        </View>

        <Text style={styles.assignedBy}>Assigned by: {task.assigned_by}</Text>
      </TouchableOpacity>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        {task.status === 'pending' && (
          <>
            <TouchableOpacity
              style={styles.startButton}
              onPress={() => updateTaskStatus(task.id, 'in_progress')}
            >
              <Text style={styles.buttonIcon}>▶️</Text>
              <Text style={styles.buttonText}>Start</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.completeButton}
              onPress={() => updateTaskStatus(task.id, 'completed')}
            >
              <Text style={styles.buttonIcon}>✅</Text>
              <Text style={styles.buttonText}>Complete</Text>
            </TouchableOpacity>
          </>
        )}
        
        {task.status === 'in_progress' && (
          <TouchableOpacity
            style={styles.completeButton}
            onPress={() => updateTaskStatus(task.id, 'completed')}
          >
            <Text style={styles.buttonIcon}>✅</Text>
            <Text style={styles.buttonText}>Complete</Text>
          </TouchableOpacity>
        )}
        
        {task.status === 'completed' && (
          <View style={styles.completedIndicator}>
            <Text style={styles.buttonIcon}>✅</Text>
            <Text style={styles.completedText}>Done</Text>
          </View>
        )}
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      {showNewTaskAlert && (
        <View style={styles.newTaskAlert}>
          <Text style={styles.newTaskAlertText}>🎉 New Task Assigned!</Text>
        </View>
      )}
      <ScrollView
        style={styles.scrollContainer}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        <View style={styles.header}>
          <Text style={styles.headerTitle}>My Tasks - Rajesh Kumar</Text>
          <Text style={styles.headerSubtitle}>
            Worker ID: {workerId} | Total: {tasks.length} tasks
          </Text>
          <Text style={styles.headerSubtitle}>
            {pendingTasks.length} pending • {inProgressTasks.length} in progress •{' '}
            {completedTasks.length} completed
          </Text>
          <Text style={[styles.headerSubtitle, { fontSize: 11, marginTop: 5, color: '#81c784', fontWeight: 'bold' }]}>
            ⚡ Auto-updates every 2 seconds - Tasks from supervisor appear instantly!
          </Text>
        </View>

      {tasks.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>No tasks assigned yet</Text>
          <Text style={styles.emptySubtext}>Pull down to refresh</Text>
        </View>
      ) : (
        <>
          {pendingTasks.length > 0 && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>📋 Pending Tasks</Text>
              {pendingTasks.map(renderTask)}
            </View>
          )}

          {inProgressTasks.length > 0 && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>⚡ In Progress</Text>
              {inProgressTasks.map(renderTask)}
            </View>
          )}

          {completedTasks.length > 0 && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>✅ Completed</Text>
              {completedTasks.map(renderTask)}
            </View>
          )}
        </>
      )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContainer: {
    flex: 1,
  },
  newTaskAlert: {
    backgroundColor: '#4caf50',
    padding: 15,
    alignItems: 'center',
    justifyContent: 'center',
    borderBottomWidth: 2,
    borderBottomColor: '#388e3c',
  },
  newTaskAlertText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  header: {
    backgroundColor: '#2196f3',
    padding: 20,
    paddingTop: 40,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
  },
  section: {
    marginTop: 20,
    paddingHorizontal: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  taskCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 10,
  },
  priorityBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  priorityText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  taskDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
  },
  taskFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
  },
  statusText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  taskDate: {
    fontSize: 12,
    color: '#666',
  },
  assignedBy: {
    fontSize: 11,
    color: '#999',
    fontStyle: 'italic',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 18,
    color: '#999',
    marginBottom: 5,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#bbb',
  },
  taskContent: {
    flex: 1,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 10,
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#2196f3',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    shadowColor: '#2196f3',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 3,
  },
  completeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#4caf50',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    shadowColor: '#4caf50',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 3,
  },
  completedIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e8f5e9',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
  },
  buttonIcon: {
    fontSize: 16,
    marginRight: 6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  completedText: {
    color: '#4caf50',
    fontSize: 14,
    fontWeight: 'bold',
  },
});
