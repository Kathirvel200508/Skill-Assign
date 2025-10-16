import React, { useState, useEffect, useRef } from 'react';
import { View, ScrollView, StyleSheet, Animated, Dimensions } from 'react-native';
import { Card, Title, Paragraph, Chip, Avatar, ProgressBar, Text, Button } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import workerData from '../data/workerData.json';

const { width } = Dimensions.get('window');

export default function GamificationScreen() {
  const [data, setData] = useState(workerData);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  
  // Animation values
  const xpBarAnimation = useRef(new Animated.Value(0)).current;
  const toastAnimation = useRef(new Animated.Value(0)).current;
  const badgeScaleAnimation = useRef(new Animated.Value(1)).current;
  const levelPulseAnimation = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // Animate XP bar on mount
    animateXPBar();
  }, []);

  const animateXPBar = () => {
    Animated.timing(xpBarAnimation, {
      toValue: data.currentWorker.currentXP / data.currentWorker.xpToNextLevel,
      duration: 1500,
      useNativeDriver: false,
    }).start();
  };

  const updateXP = (xpAmount, reason = 'Task completed') => {
    const newXP = data.currentWorker.currentXP + xpAmount;
    const leveledUp = newXP >= data.currentWorker.xpToNextLevel;
    
    // Update data
    const updatedWorker = {
      ...data.currentWorker,
      currentXP: leveledUp ? newXP - data.currentWorker.xpToNextLevel : newXP,
      level: leveledUp ? data.currentWorker.level + 1 : data.currentWorker.level,
    };
    
    setData({
      ...data,
      currentWorker: updatedWorker,
    });

    // Show toast notification
    setToastMessage(`+${xpAmount} XP Earned! ${reason}`);
    setShowToast(true);
    
    // Animate toast
    Animated.sequence([
      Animated.timing(toastAnimation, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.delay(2000),
      Animated.timing(toastAnimation, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start(() => setShowToast(false));

    // Animate XP bar
    Animated.timing(xpBarAnimation, {
      toValue: updatedWorker.currentXP / updatedWorker.xpToNextLevel,
      duration: 800,
      useNativeDriver: false,
    }).start();

    // If leveled up, animate level badge
    if (leveledUp) {
      Animated.sequence([
        Animated.timing(levelPulseAnimation, {
          toValue: 1.3,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.timing(levelPulseAnimation, {
          toValue: 1,
          duration: 200,
          useNativeDriver: true,
        }),
      ]).start();
    }

    // Animate badge unlock if applicable
    Animated.sequence([
      Animated.timing(badgeScaleAnimation, {
        toValue: 1.1,
        duration: 150,
        useNativeDriver: true,
      }),
      Animated.timing(badgeScaleAnimation, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const completeChallenge = (challenge) => {
    updateXP(challenge.xpReward, challenge.title);
  };

  const xpPercentage = (data.currentWorker.currentXP / data.currentWorker.xpToNextLevel) * 100;

  return (
    <ScrollView style={styles.container}>
      {/* Toast Notification */}
      {showToast && (
        <Animated.View
          style={[
            styles.toast,
            {
              opacity: toastAnimation,
              transform: [
                {
                  translateY: toastAnimation.interpolate({
                    inputRange: [0, 1],
                    outputRange: [-50, 0],
                  }),
                },
              ],
            },
          ]}
        >
          <MaterialCommunityIcons name="star" size={20} color="#fff" />
          <Text style={styles.toastText}>{toastMessage}</Text>
        </Animated.View>
      )}

      {/* Profile Card */}
      <Card style={styles.profileCard}>
        <Card.Content>
          <View style={styles.profileHeader}>
            <Avatar.Text
              size={70}
              label={data.currentWorker.avatar}
              style={styles.avatar}
            />
            <View style={styles.profileInfo}>
              <Title style={styles.profileName}>{data.currentWorker.name}</Title>
              <View style={styles.levelContainer}>
                <Animated.View style={{ transform: [{ scale: levelPulseAnimation }] }}>
                  <Chip
                    icon="trophy"
                    style={styles.levelChip}
                    textStyle={styles.levelText}
                  >
                    Level {data.currentWorker.level}
                  </Chip>
                </Animated.View>
                <Chip
                  icon="medal"
                  style={styles.rankChip}
                  textStyle={styles.rankText}
                >
                  Rank #{data.currentWorker.rank}
                </Chip>
              </View>
            </View>
          </View>

          {/* XP Progress Bar */}
          <View style={styles.xpContainer}>
            <View style={styles.xpHeader}>
              <Text style={styles.xpLabel}>Experience Points</Text>
              <Text style={styles.xpValue}>
                {data.currentWorker.currentXP} / {data.currentWorker.xpToNextLevel} XP
              </Text>
            </View>
            <View style={styles.progressBarContainer}>
              <Animated.View
                style={[
                  styles.progressBarFill,
                  {
                    width: xpBarAnimation.interpolate({
                      inputRange: [0, 1],
                      outputRange: ['0%', '100%'],
                    }),
                  },
                ]}
              />
            </View>
            <Text style={styles.xpPercentage}>{xpPercentage.toFixed(0)}% to next level</Text>
          </View>

          {/* Stats Row */}
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <MaterialCommunityIcons name="shield-star" size={24} color="#4caf50" />
              <Text style={styles.statValue}>{data.currentWorker.totalBadges}</Text>
              <Text style={styles.statLabel}>Badges</Text>
            </View>
            <View style={styles.statItem}>
              <MaterialCommunityIcons name="fire" size={24} color="#ff9800" />
              <Text style={styles.statValue}>{data.currentWorker.level * 100}</Text>
              <Text style={styles.statLabel}>Streak</Text>
            </View>
            <View style={styles.statItem}>
              <MaterialCommunityIcons name="star" size={24} color="#ffc107" />
              <Text style={styles.statValue}>{data.currentWorker.currentXP}</Text>
              <Text style={styles.statLabel}>Total XP</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Daily/Weekly Challenges */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.sectionHeader}>
            <MaterialCommunityIcons name="target" size={24} color="#2196f3" />
            <Title style={styles.sectionTitle}>Daily Challenges</Title>
          </View>
          {data.challenges.daily.map((challenge) => (
            <View key={challenge.id} style={styles.challengeItem}>
              <View style={styles.challengeHeader}>
                <MaterialCommunityIcons name={challenge.icon} size={20} color="#2196f3" />
                <View style={styles.challengeInfo}>
                  <Text style={styles.challengeTitle}>{challenge.title}</Text>
                  <Text style={styles.challengeDesc}>{challenge.description}</Text>
                </View>
                <Chip
                  icon="star"
                  style={styles.xpChip}
                  textStyle={styles.xpChipText}
                >
                  +{challenge.xpReward}
                </Chip>
              </View>
              <View style={styles.challengeProgress}>
                <ProgressBar
                  progress={challenge.progress / challenge.target}
                  color="#4caf50"
                  style={styles.challengeProgressBar}
                />
                <Text style={styles.challengeProgressText}>
                  {challenge.progress}/{challenge.target}
                </Text>
              </View>
              <Text style={styles.challengeExpiry}>Expires in {challenge.expiresIn}</Text>
            </View>
          ))}
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.sectionHeader}>
            <MaterialCommunityIcons name="calendar-star" size={24} color="#9c27b0" />
            <Title style={styles.sectionTitle}>Weekly Challenges</Title>
          </View>
          {data.challenges.weekly.map((challenge) => (
            <View key={challenge.id} style={styles.challengeItem}>
              <View style={styles.challengeHeader}>
                <MaterialCommunityIcons name={challenge.icon} size={20} color="#9c27b0" />
                <View style={styles.challengeInfo}>
                  <Text style={styles.challengeTitle}>{challenge.title}</Text>
                  <Text style={styles.challengeDesc}>{challenge.description}</Text>
                </View>
                <Chip
                  icon="star"
                  style={[styles.xpChip, { backgroundColor: '#f3e5f5' }]}
                  textStyle={[styles.xpChipText, { color: '#9c27b0' }]}
                >
                  +{challenge.xpReward}
                </Chip>
              </View>
              <View style={styles.challengeProgress}>
                <ProgressBar
                  progress={challenge.progress / challenge.target}
                  color="#9c27b0"
                  style={styles.challengeProgressBar}
                />
                <Text style={styles.challengeProgressText}>
                  {challenge.progress}/{challenge.target}
                </Text>
              </View>
              <Text style={styles.challengeExpiry}>Expires in {challenge.expiresIn}</Text>
            </View>
          ))}
        </Card.Content>
      </Card>

      {/* Badges Grid */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.sectionHeader}>
            <MaterialCommunityIcons name="shield-star" size={24} color="#4caf50" />
            <Title style={styles.sectionTitle}>Badges</Title>
          </View>
          <View style={styles.badgesGrid}>
            {data.badges.filter(badge => badge.earned).map((badge) => (
              <Animated.View
                key={badge.id}
                style={[
                  styles.badgeItem,
                  { transform: [{ scale: badgeScaleAnimation }] },
                ]}
              >
                <View
                  style={[
                    styles.badgeIcon,
                    { backgroundColor: badge.color },
                  ]}
                >
                  <MaterialCommunityIcons
                    name={badge.icon}
                    size={28}
                    color="#fff"
                  />
                </View>
                <Text style={styles.badgeName} numberOfLines={2}>
                  {badge.name}
                </Text>
              </Animated.View>
            ))}
          </View>
        </Card.Content>
      </Card>

      {/* Leaderboard */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.sectionHeader}>
            <MaterialCommunityIcons name="podium" size={24} color="#ffc107" />
            <Title style={styles.sectionTitle}>Leaderboard</Title>
          </View>
          {data.leaderboard.map((worker, index) => (
            <View
              key={worker.id}
              style={[
                styles.leaderboardItem,
                worker.isCurrentUser && styles.leaderboardItemHighlight,
              ]}
            >
              <View style={styles.leaderboardRank}>
                {index === 0 && (
                  <MaterialCommunityIcons name="trophy" size={24} color="#ffc107" />
                )}
                {index === 1 && (
                  <MaterialCommunityIcons name="trophy" size={24} color="#c0c0c0" />
                )}
                {index === 2 && (
                  <MaterialCommunityIcons name="trophy" size={24} color="#cd7f32" />
                )}
                {index > 2 && <Text style={styles.rankNumber}>#{worker.rank}</Text>}
              </View>
              <Avatar.Text
                size={40}
                label={worker.avatar}
                style={[
                  styles.leaderboardAvatar,
                  worker.isCurrentUser && styles.leaderboardAvatarHighlight,
                ]}
              />
              <View style={styles.leaderboardInfo}>
                <Text style={styles.leaderboardName}>
                  {worker.name} {worker.isCurrentUser && '(You)'}
                </Text>
                <View style={styles.leaderboardStats}>
                  <Chip icon="trophy" style={styles.leaderboardChip} textStyle={styles.leaderboardChipText}>
                    Lvl {worker.level}
                  </Chip>
                  <Chip icon="star" style={styles.leaderboardChip} textStyle={styles.leaderboardChipText}>
                    {worker.xp} XP
                  </Chip>
                  <Chip icon="shield-star" style={styles.leaderboardChip} textStyle={styles.leaderboardChipText}>
                    {worker.badges} badges
                  </Chip>
                </View>
              </View>
            </View>
          ))}
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
  toast: {
    position: 'absolute',
    top: 10,
    left: 20,
    right: 20,
    backgroundColor: '#4caf50',
    padding: 16,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
    zIndex: 1000,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  toastText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  profileCard: {
    margin: 16,
    elevation: 4,
    backgroundColor: '#fff',
  },
  profileHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  avatar: {
    backgroundColor: '#6200ee',
  },
  profileInfo: {
    marginLeft: 16,
    flex: 1,
  },
  profileName: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  levelContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  levelChip: {
    backgroundColor: '#4caf50',
  },
  levelText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  rankChip: {
    backgroundColor: '#2196f3',
  },
  rankText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  xpContainer: {
    marginTop: 16,
  },
  xpHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  xpLabel: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  xpValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2196f3',
  },
  progressBarContainer: {
    height: 12,
    backgroundColor: '#e0e0e0',
    borderRadius: 6,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#4caf50',
    borderRadius: 6,
  },
  xpPercentage: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 20,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  card: {
    margin: 16,
    marginTop: 8,
    elevation: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 8,
    color: '#333',
  },
  challengeItem: {
    marginBottom: 16,
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2196f3',
  },
  challengeHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  challengeInfo: {
    flex: 1,
    marginLeft: 8,
  },
  challengeTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  challengeDesc: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  xpChip: {
    backgroundColor: '#e3f2fd',
    height: 28,
  },
  xpChipText: {
    color: '#2196f3',
    fontSize: 12,
    fontWeight: 'bold',
  },
  challengeProgress: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  challengeProgressBar: {
    flex: 1,
    height: 8,
    borderRadius: 4,
  },
  challengeProgressText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 8,
    fontWeight: '500',
  },
  challengeExpiry: {
    fontSize: 11,
    color: '#999',
    marginTop: 4,
    fontStyle: 'italic',
  },
  badgesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  badgeItem: {
    width: (width - 64) / 3,
    alignItems: 'center',
    marginBottom: 16,
  },
  badgeIcon: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  badgeName: {
    fontSize: 11,
    textAlign: 'center',
    color: '#333',
    fontWeight: '500',
  },
  badgeProgress: {
    width: '100%',
    marginTop: 4,
  },
  badgeProgressBar: {
    height: 4,
    borderRadius: 2,
  },
  badgeProgressText: {
    fontSize: 9,
    color: '#666',
    textAlign: 'center',
    marginTop: 2,
  },
  leaderboardItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginBottom: 8,
  },
  leaderboardItemHighlight: {
    backgroundColor: '#e3f2fd',
    borderWidth: 2,
    borderColor: '#2196f3',
  },
  leaderboardRank: {
    width: 40,
    alignItems: 'center',
  },
  rankNumber: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#666',
  },
  leaderboardAvatar: {
    backgroundColor: '#9e9e9e',
  },
  leaderboardAvatarHighlight: {
    backgroundColor: '#6200ee',
  },
  leaderboardInfo: {
    flex: 1,
    marginLeft: 12,
  },
  leaderboardName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  leaderboardStats: {
    flexDirection: 'row',
    gap: 4,
  },
  leaderboardChip: {
    height: 24,
    backgroundColor: '#fff',
  },
  leaderboardChipText: {
    fontSize: 10,
    color: '#666',
  },
});
