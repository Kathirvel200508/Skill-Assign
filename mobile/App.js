import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Provider as PaperProvider } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';

import DashboardScreen from './screens/DashboardScreen';
import WorkerManagementScreen from './screens/WorkerManagementScreen';
import RoleManagementScreen from './screens/RoleManagementScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
              let iconName;

              if (route.name === 'Dashboard') {
                iconName = focused ? 'view-dashboard' : 'view-dashboard-outline';
              } else if (route.name === 'Workers') {
                iconName = focused ? 'account-group' : 'account-group-outline';
              } else if (route.name === 'Roles') {
                iconName = focused ? 'briefcase' : 'briefcase-outline';
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
            name="Dashboard" 
            component={DashboardScreen}
            options={{ title: 'Role Assignments' }}
          />
          <Tab.Screen 
            name="Workers" 
            component={WorkerManagementScreen}
            options={{ title: 'Worker Management' }}
          />
          <Tab.Screen 
            name="Roles" 
            component={RoleManagementScreen}
            options={{ title: 'Role Management' }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
