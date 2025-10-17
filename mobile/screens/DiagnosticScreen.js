import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import axios from 'axios';
import config from '../config';

export default function DiagnosticScreen() {
  const [status, setStatus] = useState({
    backendReachable: null,
    tasksCount: null,
    workersCount: null,
    lastError: null,
  });
  const [logs, setLogs] = useState([]);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [{timestamp, message, type}, ...prev].slice(0, 20));
    console.log(`[DIAGNOSTIC] ${message}`);
  };

  useEffect(() => {
    runDiagnostics();
    const interval = setInterval(runDiagnostics, 5000);
    return () => clearInterval(interval);
  }, []);

  const runDiagnostics = async () => {
    addLog('Running diagnostics...');
    
    // Test 1: Backend connection
    try {
      const response = await axios.get(`${config.API_BASE_URL}/worker/all`);
      setStatus(prev => ({ ...prev, backendReachable: true, workersCount: response.data.length }));
      addLog(`✅ Backend OK: ${response.data.length} workers found`, 'success');
    } catch (error) {
      setStatus(prev => ({ ...prev, backendReachable: false, lastError: error.message }));
      addLog(`❌ Backend ERROR: ${error.message}`, 'error');
      return;
    }

    // Test 2: Tasks for Worker ID 1
    try {
      const response = await axios.get(`${config.API_BASE_URL}/task/worker/1`);
      setStatus(prev => ({ ...prev, tasksCount: response.data.length }));
      addLog(`✅ Tasks OK: ${response.data.length} tasks for Worker 1`, 'success');
      
      if (response.data.length > 0) {
        const latestTask = response.data[0];
        addLog(`Latest task: "${latestTask.title}" (${latestTask.status})`);
      }
    } catch (error) {
      addLog(`❌ Tasks ERROR: ${error.message}`, 'error');
    }
  };

  const createTestTask = async () => {
    addLog('Creating test task...');
    try {
      const taskData = {
        worker_id: 1,
        title: `🧪 DIAGNOSTIC TEST ${new Date().toLocaleTimeString()}`,
        description: 'Automated diagnostic test task',
        priority: 'high',
        assigned_by: 'Diagnostic Screen',
      };
      
      const response = await axios.post(`${config.API_BASE_URL}/task/create`, taskData);
      addLog(`✅ Test task created! ID: ${response.data.id}`, 'success');
      Alert.alert('Success', `Task created with ID: ${response.data.id}\n\nGo to Tasks tab to see it!`);
      runDiagnostics();
    } catch (error) {
      addLog(`❌ Create task ERROR: ${error.message}`, 'error');
      Alert.alert('Error', error.message);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🔧 System Diagnostics</Text>
        <Text style={styles.subtitle}>Real-time sync testing</Text>
      </View>

      <View style={styles.statusCard}>
        <Text style={styles.cardTitle}>Connection Status</Text>
        <View style={styles.statusRow}>
          <Text style={styles.label}>Backend URL:</Text>
          <Text style={styles.value}>{config.API_BASE_URL}</Text>
        </View>
        <View style={styles.statusRow}>
          <Text style={styles.label}>Backend:</Text>
          <Text style={[styles.value, status.backendReachable ? styles.success : styles.error]}>
            {status.backendReachable === null ? '⏳ Checking...' : 
             status.backendReachable ? '✅ Connected' : '❌ Disconnected'}
          </Text>
        </View>
        <View style={styles.statusRow}>
          <Text style={styles.label}>Workers:</Text>
          <Text style={styles.value}>{status.workersCount ?? '...'}</Text>
        </View>
        <View style={styles.statusRow}>
          <Text style={styles.label}>Tasks (Worker 1):</Text>
          <Text style={styles.value}>{status.tasksCount ?? '...'}</Text>
        </View>
        {status.lastError && (
          <View style={styles.errorBox}>
            <Text style={styles.errorText}>{status.lastError}</Text>
          </View>
        )}
      </View>

      <TouchableOpacity style={styles.testButton} onPress={createTestTask}>
        <Text style={styles.testButtonText}>🧪 Create Test Task</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.refreshButton} onPress={runDiagnostics}>
        <Text style={styles.refreshButtonText}>🔄 Refresh Diagnostics</Text>
      </TouchableOpacity>

      <View style={styles.logsCard}>
        <Text style={styles.cardTitle}>Activity Log</Text>
        {logs.map((log, index) => (
          <View key={index} style={styles.logEntry}>
            <Text style={styles.logTime}>{log.timestamp}</Text>
            <Text style={[styles.logMessage, log.type === 'error' && styles.logError, log.type === 'success' && styles.logSuccess]}>
              {log.message}
            </Text>
          </View>
        ))}
      </View>

      <View style={styles.instructions}>
        <Text style={styles.instructionsTitle}>📝 How to Test Sync:</Text>
        <Text style={styles.instructionText}>1. Keep this screen open</Text>
        <Text style={styles.instructionText}>2. Click "Create Test Task" button above</Text>
        <Text style={styles.instructionText}>3. Go to "Tasks" tab (bottom navigation)</Text>
        <Text style={styles.instructionText}>4. You should see the new task immediately!</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#6200ee',
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
  },
  statusCard: {
    backgroundColor: '#fff',
    margin: 15,
    padding: 15,
    borderRadius: 10,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
  },
  value: {
    fontSize: 14,
    color: '#666',
  },
  success: {
    color: '#4caf50',
    fontWeight: 'bold',
  },
  error: {
    color: '#f44336',
    fontWeight: 'bold',
  },
  errorBox: {
    backgroundColor: '#ffebee',
    padding: 10,
    borderRadius: 5,
    marginTop: 10,
  },
  errorText: {
    color: '#f44336',
    fontSize: 12,
  },
  testButton: {
    backgroundColor: '#ff9800',
    margin: 15,
    marginTop: 0,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  testButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  refreshButton: {
    backgroundColor: '#2196f3',
    margin: 15,
    marginTop: 0,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  refreshButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  logsCard: {
    backgroundColor: '#fff',
    margin: 15,
    padding: 15,
    borderRadius: 10,
    elevation: 2,
  },
  logEntry: {
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    paddingVertical: 8,
  },
  logTime: {
    fontSize: 11,
    color: '#999',
  },
  logMessage: {
    fontSize: 13,
    marginTop: 3,
  },
  logError: {
    color: '#f44336',
  },
  logSuccess: {
    color: '#4caf50',
  },
  instructions: {
    backgroundColor: '#e3f2fd',
    margin: 15,
    padding: 15,
    borderRadius: 10,
  },
  instructionsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  instructionText: {
    fontSize: 14,
    marginBottom: 5,
  },
});
