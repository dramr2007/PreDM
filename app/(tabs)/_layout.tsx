import { isLiquidGlassAvailable } from "expo-glass-effect";
import { Tabs } from "expo-router";
import { NativeTabs, Icon, Label, Badge } from "expo-router/unstable-native-tabs";
import { BlurView } from "expo-blur";
import { Platform, StyleSheet, useColorScheme, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import React from "react";
import { Ionicons } from "@expo/vector-icons";
import Colors from "@/constants/colors";
import { useHealth } from "@/context/HealthContext";

function NativeTabLayout() {
  const { unreadAlertCount } = useHealth();
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <Icon sf={{ default: "house", selected: "house.fill" }} />
        <Label>الرئيسية</Label>
        {unreadAlertCount > 0 && <Badge>{unreadAlertCount}</Badge>}
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="metrics">
        <Icon sf={{ default: "waveform.path.ecg", selected: "waveform.path.ecg" }} />
        <Label>المقاييس</Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="learn">
        <Icon sf={{ default: "book.closed", selected: "book.closed.fill" }} />
        <Label>التوعية</Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="meds">
        <Icon sf={{ default: "pill", selected: "pill.fill" }} />
        <Label>الأدوية</Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="profile">
        <Icon sf={{ default: "person", selected: "person.fill" }} />
        <Label>ملفي</Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}

function ClassicTabLayout() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === "dark";
  const isIOS = Platform.OS === "ios";
  const isWeb = Platform.OS === "web";
  const { unreadAlertCount } = useHealth();
  const C = isDark ? Colors.dark : Colors.light;

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: C.tint,
        tabBarInactiveTintColor: C.tabIconDefault,
        tabBarLabelStyle: { fontFamily: 'Nunito_600SemiBold', fontSize: 11, marginBottom: 2 },
        tabBarStyle: {
          position: "absolute",
          backgroundColor: isIOS ? "transparent" : C.card,
          borderTopWidth: isWeb ? 1 : 0,
          borderTopColor: C.border,
          elevation: 0,
          ...(isWeb ? { height: 84 } : {}),
        },
        tabBarBackground: () =>
          isIOS ? (
            <BlurView intensity={100} tint={isDark ? "dark" : "light"} style={StyleSheet.absoluteFill} />
          ) : isWeb ? (
            <View style={[StyleSheet.absoluteFill, { backgroundColor: C.card }]} />
          ) : null,
      }}
    >
      <Tabs.Screen name="index" options={{
        title: "الرئيسية",
        tabBarBadge: unreadAlertCount > 0 ? unreadAlertCount : undefined,
        tabBarIcon: ({ color }) => <Ionicons name="home" size={22} color={color} />,
      }} />
      <Tabs.Screen name="metrics" options={{
        title: "المقاييس",
        tabBarIcon: ({ color }) => <Ionicons name="pulse" size={22} color={color} />,
      }} />
      <Tabs.Screen name="learn" options={{
        title: "التوعية",
        tabBarIcon: ({ color }) => <Ionicons name="book" size={22} color={color} />,
      }} />
      <Tabs.Screen name="meds" options={{
        title: "الأدوية",
        tabBarIcon: ({ color }) => <Ionicons name="medical" size={22} color={color} />,
      }} />
      <Tabs.Screen name="profile" options={{
        title: "ملفي",
        tabBarIcon: ({ color }) => <Ionicons name="person" size={22} color={color} />,
      }} />
    </Tabs>
  );
}

export default function TabLayout() {
  if (isLiquidGlassAvailable()) {
    return <NativeTabLayout />;
  }
  return <ClassicTabLayout />;
}
