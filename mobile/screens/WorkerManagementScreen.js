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
  FAB,
  Portal,
  Modal,
  TextInput,
  Text,
  IconButton,
} from 'react-native-paper';
import { workerAPI } from '../api/client';

export default function WorkerManagementScreen() {
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingWorker, setEditingWorker] = useState(null);
  
  // Form state
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [experience, setExperience] = useState('');
  const [skills, setSkills] = useState('');
  const [fatigueLevel, setFatigueLevel] = useState('0.2');
  const [performanceScore, setPerformanceScore] = useState('0.75');

  useEffect(() => {
    loadWorkers();
  }, []);

  const loadWorkers = async () => {
    try {
      const response = await workerAPI.getAll();
      setWorkers(response.data);
    } catch (error) {
      console.error('Error loading workers:', error);
      Alert.alert('Error', 'Failed to load workers');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadWorkers();
  };

  const handleAddWorker = () => {
    setEditingWorker(null);
    resetForm();
    setShowModal(true);
  };

  const handleEditWorker = (worker) => {
    setEditingWorker(worker);
    setName(worker.name);
    setAge(worker.age.toString());
    setExperience(worker.experience.toString());
    setSkills(worker.skills.join(', '));
    setFatigueLevel(worker.fatigue_level.toString());
    setPerformanceScore(worker.performance_score.toString());
    setShowModal(true);
  };

  const handleDeleteWorker = (worker) => {
    Alert.alert(
      'Delete Worker',
      `Are you sure you want to delete ${worker.name}?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await workerAPI.delete(worker.id);
              Alert.alert('Success', 'Worker deleted successfully');
              loadWorkers();
            } catch (error) {
              console.error('Error deleting worker:', error);
              Alert.alert('Error', 'Failed to delete worker');
            }
          },
        },
      ]
    );
  };

  const handleSaveWorker = async () => {
    // Validation
    if (!name || !age || !experience || !skills) {
      Alert.alert('Error', 'Please fill in all required fields');
      return;
    }

    const workerData = {
      name,
      age: parseInt(age),
      experience: parseFloat(experience),
      skills: skills.split(',').map((s) => s.trim()).filter((s) => s),
      fatigue_level: parseFloat(fatigueLevel),
      performance_score: parseFloat(performanceScore),
    };

    try {
      if (editingWorker) {
        await workerAPI.update(editingWorker.id, workerData);
        Alert.alert('Success', 'Worker updated successfully');
      } else {
        await workerAPI.add(workerData);
        Alert.alert('Success', 'Worker added successfully');
      }
      setShowModal(false);
      loadWorkers();
    } catch (error) {
      console.error('Error saving worker:', error);
      Alert.alert('Error', 'Failed to save worker');
    }
  };

  const resetForm = () => {
    setName('');
    setAge('');
    setExperience('');
    setSkills('');
    setFatigueLevel('0.2');
    setPerformanceScore('0.75');
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
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        <Card style={styles.headerCard}>
          <Card.Content>
            <Title>Worker Management</Title>
            <Paragraph>Total Workers: {workers.length}</Paragraph>
          </Card.Content>
        </Card>

        {workers.map((worker) => (
          <Card key={worker.id} style={styles.workerCard}>
            <Card.Content>
              <View style={styles.workerHeader}>
                <View style={styles.workerInfo}>
                  <Title>{worker.name}</Title>
                  <Paragraph>
                    Age: {worker.age} | Experience: {worker.experience} years
                  </Paragraph>
                </View>
                <View style={styles.actions}>
                  <IconButton
                    icon="pencil"
                    size={20}
                    onPress={() => handleEditWorker(worker)}
                  />
                  <IconButton
                    icon="delete"
                    size={20}
                    onPress={() => handleDeleteWorker(worker)}
                  />
                </View>
              </View>

              <View style={styles.metricsContainer}>
                <View style={styles.metric}>
                  <Text style={styles.metricLabel}>Performance</Text>
                  <Chip style={styles.performanceChip}>
                    {(worker.performance_score * 100).toFixed(0)}%
                  </Chip>
                </View>
                <View style={styles.metric}>
                  <Text style={styles.metricLabel}>Fatigue</Text>
                  <Chip
                    style={[
                      styles.fatigueChip,
                      { backgroundColor: getFatigueColor(worker.fatigue_level) },
                    ]}
                  >
                    {(worker.fatigue_level * 100).toFixed(0)}%
                  </Chip>
                </View>
              </View>

              {worker.current_role && (
                <Chip icon="briefcase" style={styles.roleChip}>
                  Current: {worker.current_role}
                </Chip>
              )}

              <View style={styles.skillsContainer}>
                {worker.skills.map((skill, index) => (
                  <Chip key={index} style={styles.skillChip} mode="outlined" compact>
                    {skill}
                  </Chip>
                ))}
              </View>
            </Card.Content>
          </Card>
        ))}
      </ScrollView>

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={handleAddWorker}
        label="Add Worker"
      />

      {/* Add/Edit Worker Modal */}
      <Portal>
        <Modal
          visible={showModal}
          onDismiss={() => setShowModal(false)}
          contentContainerStyle={styles.modalContainer}
        >
          <ScrollView>
            <Title style={styles.modalTitle}>
              {editingWorker ? 'Edit Worker' : 'Add New Worker'}
            </Title>

            <TextInput
              label="Name *"
              value={name}
              onChangeText={setName}
              style={styles.input}
              mode="outlined"
            />

            <TextInput
              label="Age *"
              value={age}
              onChangeText={setAge}
              keyboardType="numeric"
              style={styles.input}
              mode="outlined"
            />

            <TextInput
              label="Experience (years) *"
              value={experience}
              onChangeText={setExperience}
              keyboardType="decimal-pad"
              style={styles.input}
              mode="outlined"
            />

            <TextInput
              label="Skills (comma separated) *"
              value={skills}
              onChangeText={setSkills}
              placeholder="e.g., welding, assembly, quality_check"
              style={styles.input}
              mode="outlined"
              multiline
            />

            <TextInput
              label="Fatigue Level (0-1)"
              value={fatigueLevel}
              onChangeText={setFatigueLevel}
              keyboardType="decimal-pad"
              style={styles.input}
              mode="outlined"
            />

            <TextInput
              label="Performance Score (0-1)"
              value={performanceScore}
              onChangeText={setPerformanceScore}
              keyboardType="decimal-pad"
              style={styles.input}
              mode="outlined"
            />

            <View style={styles.modalActions}>
              <Button mode="outlined" onPress={() => setShowModal(false)} style={styles.button}>
                Cancel
              </Button>
              <Button mode="contained" onPress={handleSaveWorker} style={styles.button}>
                {editingWorker ? 'Update' : 'Add'}
              </Button>
            </View>
          </ScrollView>
        </Modal>
      </Portal>
    </View>
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
  scrollView: {
    flex: 1,
  },
  headerCard: {
    margin: 16,
    marginBottom: 8,
  },
  workerCard: {
    margin: 16,
    marginTop: 8,
  },
  workerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  workerInfo: {
    flex: 1,
  },
  actions: {
    flexDirection: 'row',
  },
  metricsContainer: {
    flexDirection: 'row',
    marginTop: 12,
    marginBottom: 8,
  },
  metric: {
    marginRight: 16,
  },
  metricLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  performanceChip: {
    backgroundColor: '#e3f2fd',
  },
  fatigueChip: {
    color: 'white',
  },
  roleChip: {
    marginTop: 8,
    marginBottom: 8,
    backgroundColor: '#fff3e0',
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
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#6200ee',
  },
  modalContainer: {
    backgroundColor: 'white',
    margin: 20,
    padding: 20,
    borderRadius: 8,
    maxHeight: '90%',
  },
  modalTitle: {
    marginBottom: 16,
  },
  input: {
    marginBottom: 12,
  },
  modalActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 16,
  },
  button: {
    marginLeft: 8,
  },
});
