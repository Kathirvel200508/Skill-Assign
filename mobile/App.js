import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Provider as PaperProvider } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';

import ProfileScreen from './screens/ProfileScreen';
import NotificationsScreen from './screens/NotificationsScreen';
import GamificationScreen from './screens/GamificationScreen';
import TasksScreen from './screens/TasksScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
              let iconName;

              if (route.name === 'Tasks') {
                iconName = focused ? 'clipboard-check' : 'clipboard-check-outline';
              } else if (route.name === 'Profile') {
                iconName = focused ? 'account' : 'account-outline';
              } else if (route.name === 'Notifications') {
                iconName = focused ? 'bell' : 'bell-outline';
              } else if (route.name === 'Gamification') {
                iconName = focused ? 'trophy' : 'trophy-outline';
              } 

              return <MaterialCommunityIcons name={iconName} size={size} color={color} />;
            },
            tabBarActiveTintColor: '#6200ee',
            tabBarInactiveTintColor: 'gray',
            headerStyle: {
              backgroundColor: '#6200ee',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          })}
        >
          <Tab.Screen 
            name="Tasks" 
            component={TasksScreen}
            options={{ title: 'My Tasks' }}
            initialParams={{ workerId: 1 }}
          />
          <Tab.Screen 
            name="Profile" 
            component={ProfileScreen}
            options={{ title: 'My Profile' }}
          />
          <Tab.Screen 
            name="Notifications" 
            component={NotificationsScreen}
            options={{ title: 'Task Notifications' }}
          />
          <Tab.Screen 
            name="Gamification" 
            component={GamificationScreen}
            options={{ title: 'Achievements' }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
