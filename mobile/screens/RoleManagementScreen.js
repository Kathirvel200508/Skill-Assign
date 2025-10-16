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
  ProgressBar,
} from 'react-native-paper';
import { roleAPI, workerAPI } from '../api/client';

export default function RoleManagementScreen() {
  const [roles, setRoles] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingRole, setEditingRole] = useState(null);
  
  // Form state
  const [name, setName] = useState('');
  const [requiredSkills, setRequiredSkills] = useState('');
  const [difficultyLevel, setDifficultyLevel] = useState('0.5');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [rolesRes, workersRes] = await Promise.all([
        roleAPI.getAll(),
        workerAPI.getAll(),
      ]);
      setRoles(rolesRes.data);
      setWorkers(workersRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
      Alert.alert('Error', 'Failed to load data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleAddRole = () => {
    setEditingRole(null);
    resetForm();
    setShowModal(true);
  };

  const handleEditRole = (role) => {
    setEditingRole(role);
    setName(role.name);
    setRequiredSkills(role.required_skills.join(', '));
    setDifficultyLevel(role.difficulty_level.toString());
    setShowModal(true);
  };

  const handleDeleteRole = (role) => {
    Alert.alert(
      'Delete Role',
      `Are you sure you want to delete ${role.name}?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await roleAPI.delete(role.id);
              Alert.alert('Success', 'Role deleted successfully');
              loadData();
            } catch (error) {
              console.error('Error deleting role:', error);
              Alert.alert('Error', 'Failed to delete role');
            }
          },
        },
      ]
    );
  };

  const handleSaveRole = async () => {
    // Validation
    if (!name || !requiredSkills) {
      Alert.alert('Error', 'Please fill in all required fields');
      return;
    }

    const roleData = {
      name,
      required_skills: requiredSkills.split(',').map((s) => s.trim()).filter((s) => s),
      difficulty_level: parseFloat(difficultyLevel),
    };

    try {
      if (editingRole) {
        await roleAPI.update(editingRole.id, roleData);
        Alert.alert('Success', 'Role updated successfully');
      } else {
        await roleAPI.add(roleData);
        Alert.alert('Success', 'Role added successfully');
      }
      setShowModal(false);
      loadData();
    } catch (error) {
      console.error('Error saving role:', error);
      Alert.alert('Error', error.response?.data?.detail || 'Failed to save role');
    }
  };

  const resetForm = () => {
    setName('');
    setRequiredSkills('');
    setDifficultyLevel('0.5');
  };

  const getAssigneeName = (assigneeId) => {
    const worker = workers.find((w) => w.id === assigneeId);
    return worker ? worker.name : 'Unknown';
  };

  const getSkillGap = (role) => {
    if (!role.current_assignee_id) return null;
    
    const worker = workers.find((w) => w.id === role.current_assignee_id);
    if (!worker) return null;

    const workerSkills = new Set(worker.skills);
    const requiredSkills = new Set(role.required_skills);
    const matchingSkills = [...requiredSkills].filter((skill) => workerSkills.has(skill));
    const matchPercentage = (matchingSkills.length / requiredSkills.size) * 100;

    return {
      matchPercentage,
      missingSkills: [...requiredSkills].filter((skill) => !workerSkills.has(skill)),
    };
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
            <Title>Role Management</Title>
            <Paragraph>Total Roles: {roles.length}</Paragraph>
            <Paragraph>
              Assigned: {roles.filter((r) => r.current_assignee_id).length} | 
              Available: {roles.filter((r) => !r.current_assignee_id).length}
            </Paragraph>
          </Card.Content>
        </Card>

        {roles.map((role) => {
          const skillGap = getSkillGap(role);
          
          return (
            <Card key={role.id} style={styles.roleCard}>
              <Card.Content>
                <View style={styles.roleHeader}>
                  <View style={styles.roleInfo}>
                    <Title>{role.name}</Title>
                    <View style={styles.difficultyContainer}>
                      <Text style={styles.difficultyLabel}>Difficulty:</Text>
                      <ProgressBar
                        progress={role.difficulty_level}
                        color={
                          role.difficulty_level < 0.5
                            ? '#4caf50'
                            : role.difficulty_level < 0.8
                            ? '#ff9800'
                            : '#f44336'
                        }
                        style={styles.difficultyBar}
                      />
                      <Text style={styles.difficultyValue}>
                        {(role.difficulty_level * 10).toFixed(1)}/10
                      </Text>
                    </View>
                  </View>
                  <View style={styles.actions}>
                    <IconButton
                      icon="pencil"
                      size={20}
                      onPress={() => handleEditRole(role)}
                    />
                    <IconButton
                      icon="delete"
                      size={20}
                      onPress={() => handleDeleteRole(role)}
                    />
                  </View>
                </View>

                <Text style={styles.sectionTitle}>Required Skills:</Text>
                <View style={styles.skillsContainer}>
                  {role.required_skills.map((skill, index) => (
                    <Chip key={index} style={styles.skillChip} mode="outlined" compact>
                      {skill}
                    </Chip>
                  ))}
                </View>

                {role.current_assignee_id ? (
                  <View style={styles.assignmentSection}>
                    <Chip icon="account-check" style={styles.assignedChip}>
                      Assigned to: {getAssigneeName(role.current_assignee_id)}
                    </Chip>
                    
                    {skillGap && (
                      <View style={styles.skillGapSection}>
                        <Text style={styles.skillGapTitle}>Skill Match:</Text>
                        <ProgressBar
                          progress={skillGap.matchPercentage / 100}
                          color={
                            skillGap.matchPercentage > 80
                              ? '#4caf50'
                              : skillGap.matchPercentage > 50
                              ? '#ff9800'
                              : '#f44336'
                          }
                          style={styles.skillMatchBar}
                        />
                        <Text style={styles.skillMatchText}>
                          {skillGap.matchPercentage.toFixed(0)}% match
                        </Text>
                        
                        {skillGap.missingSkills.length > 0 && (
                          <View style={styles.missingSkillsContainer}>
                            <Text style={styles.missingSkillsLabel}>Missing skills:</Text>
                            {skillGap.missingSkills.map((skill, index) => (
                              <Chip
                                key={index}
                                style={styles.missingSkillChip}
                                textStyle={styles.missingSkillText}
                                compact
                              >
                                {skill}
                              </Chip>
                            ))}
                          </View>
                        )}
                      </View>
                    )}
                  </View>
                ) : (
                  <Chip icon="alert-circle" style={styles.availableChip}>
                    Available - No assignment
                  </Chip>
                )}
              </Card.Content>
            </Card>
          );
        })}
      </ScrollView>

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={handleAddRole}
        label="Add Role"
      />

      {/* Add/Edit Role Modal */}
      <Portal>
        <Modal
          visible={showModal}
          onDismiss={() => setShowModal(false)}
          contentContainerStyle={styles.modalContainer}
        >
          <ScrollView>
            <Title style={styles.modalTitle}>
              {editingRole ? 'Edit Role' : 'Add New Role'}
            </Title>

            <TextInput
              label="Role Name *"
              value={name}
              onChangeText={setName}
              style={styles.input}
              mode="outlined"
            />

            <TextInput
              label="Required Skills (comma separated) *"
              value={requiredSkills}
              onChangeText={setRequiredSkills}
              placeholder="e.g., welding, assembly, quality_check"
              style={styles.input}
              mode="outlined"
              multiline
            />

            <TextInput
              label="Difficulty Level (0-1)"
              value={difficultyLevel}
              onChangeText={setDifficultyLevel}
              keyboardType="decimal-pad"
              style={styles.input}
              mode="outlined"
            />
            <Text style={styles.helperText}>
              0 = Easy, 0.5 = Medium, 1 = Very Difficult
            </Text>

            <View style={styles.modalActions}>
              <Button mode="outlined" onPress={() => setShowModal(false)} style={styles.button}>
                Cancel
              </Button>
              <Button mode="contained" onPress={handleSaveRole} style={styles.button}>
                {editingRole ? 'Update' : 'Add'}
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
  roleCard: {
    margin: 16,
    marginTop: 8,
  },
  roleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  roleInfo: {
    flex: 1,
  },
  actions: {
    flexDirection: 'row',
  },
  difficultyContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  difficultyLabel: {
    fontSize: 12,
    color: '#666',
    marginRight: 8,
  },
  difficultyBar: {
    flex: 1,
    height: 8,
    borderRadius: 4,
  },
  difficultyValue: {
    fontSize: 12,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 12,
    marginBottom: 8,
  },
  skillsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  skillChip: {
    marginRight: 8,
    marginBottom: 8,
  },
  assignmentSection: {
    marginTop: 12,
  },
  assignedChip: {
    backgroundColor: '#e8f5e9',
  },
  availableChip: {
    marginTop: 12,
    backgroundColor: '#fff3e0',
  },
  skillGapSection: {
    marginTop: 12,
    padding: 12,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
  },
  skillGapTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  skillMatchBar: {
    height: 8,
    borderRadius: 4,
  },
  skillMatchText: {
    fontSize: 12,
    marginTop: 4,
    textAlign: 'right',
  },
  missingSkillsContainer: {
    marginTop: 8,
  },
  missingSkillsLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  missingSkillChip: {
    marginRight: 4,
    marginBottom: 4,
    backgroundColor: '#ffebee',
  },
  missingSkillText: {
    color: '#c62828',
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
  helperText: {
    fontSize: 12,
    color: '#666',
    marginBottom: 16,
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


