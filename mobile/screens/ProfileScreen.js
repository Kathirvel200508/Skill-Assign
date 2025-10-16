import React, { useState, useEffect } from 'react';
import { View, ScrollView, StyleSheet, RefreshControl } from 'react-native';
import { Card, Title, Paragraph, Chip, Avatar, ActivityIndicator, Text } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import apiClient from '../api/client';

export default function ProfileScreen() {
  const [worker, setWorker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // For demo purposes, using worker ID 1. In production, this would come from authentication
  const workerId = 1;

  const loadWorkerProfile = async () => {
    try {
      const response = await apiClient.get(`/worker/${workerId}`);
      setWorker(response.data);
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadWorkerProfile();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadWorkerProfile();
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#6200ee" />
      </View>
    );
  }

  if (!worker) {
    return (
      <View style={styles.centerContainer}>
        <Text>Unable to load profile</Text>
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
      {/* Profile Header */}
      <Card style={styles.headerCard}>
        <Card.Content style={styles.headerContent}>
          <Avatar.Text 
            size={80} 
            label={worker.name.split(' ').map(n => n[0]).join('')}
            style={styles.avatar}
          />
          <Title style={styles.name}>{worker.name}</Title>
          <Paragraph style={styles.role}>{worker.current_role || 'Worker'}</Paragraph>
        </Card.Content>
      </Card>

      {/* Basic Info */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.sectionTitle}>Basic Information</Title>
          
          <View style={styles.infoRow}>
            <MaterialCommunityIcons name="cake-variant" size={24} color="#6200ee" />
            <View style={styles.infoText}>
              <Text style={styles.infoLabel}>Age</Text>
              <Text style={styles.infoValue}>{worker.age} years</Text>
            </View>
          </View>

          <View style={styles.infoRow}>
            <MaterialCommunityIcons name="briefcase" size={24} color="#6200ee" />
            <View style={styles.infoText}>
              <Text style={styles.infoLabel}>Experience</Text>
              <Text style={styles.infoValue}>{worker.experience} years</Text>
            </View>
          </View>

          <View style={styles.infoRow}>
            <MaterialCommunityIcons name="clock-outline" size={24} color="#6200ee" />
            <View style={styles.infoText}>
              <Text style={styles.infoLabel}>Hours per Week</Text>
              <Text style={styles.infoValue}>{worker.hours_per_week} hours</Text>
            </View>
          </View>

          <View style={styles.infoRow}>
            <MaterialCommunityIcons name="chart-line" size={24} color="#6200ee" />
            <View style={styles.infoText}>
              <Text style={styles.infoLabel}>Performance Score</Text>
              <Text style={styles.infoValue}>{(worker.performance_score * 100).toFixed(0)}%</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Skills */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.sectionTitle}>My Skills</Title>
          <View style={styles.skillsContainer}>
            {worker.skills && worker.skills.length > 0 ? (
              worker.skills.map((skill, index) => (
                <Chip 
                  key={index} 
                  icon="check-circle"
                  style={styles.skillChip}
                  textStyle={styles.skillText}
                >
                  {skill}
                </Chip>
              ))
            ) : (
              <Text>No skills listed</Text>
            )}
          </View>
        </Card.Content>
      </Card>

      {/* Current Status */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.sectionTitle}>Current Status</Title>
          
          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Fatigue Level:</Text>
            <Chip 
              style={[
                styles.statusChip,
                { backgroundColor: worker.fatigue_level < 0.3 ? '#4caf50' : worker.fatigue_level < 0.6 ? '#ff9800' : '#f44336' }
              ]}
              textStyle={{ color: 'white' }}
            >
              {(worker.fatigue_level * 100).toFixed(0)}%
            </Chip>
          </View>

          <View style={styles.statusRow}>
            <Text style={styles.statusLabel}>Current Role:</Text>
            <Text style={styles.statusValue}>{worker.current_role || 'Not Assigned'}</Text>
          </View>
        </Card.Content>
      </Card>
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
  headerCard: {
    margin: 16,
    marginBottom: 8,
    elevation: 4,
  },
  headerContent: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  avatar: {
    backgroundColor: '#6200ee',
    marginBottom: 12,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  role: {
    fontSize: 16,
    color: '#666',
  },
  card: {
    margin: 16,
    marginTop: 8,
    marginBottom: 8,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#6200ee',
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  infoText: {
    marginLeft: 16,
    flex: 1,
  },
  infoLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 2,
  },
  infoValue: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  skillsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  skillChip: {
    marginRight: 8,
    marginBottom: 8,
    backgroundColor: '#e3f2fd',
  },
  skillText: {
    color: '#1976d2',
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  statusLabel: {
    fontSize: 14,
    color: '#666',
  },
  statusValue: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  statusChip: {
    paddingHorizontal: 8,
  },
});
