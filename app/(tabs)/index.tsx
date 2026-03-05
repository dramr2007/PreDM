import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, Pressable, Platform,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useHealth } from '@/context/HealthContext';
import Colors from '@/constants/colors';
import * as Haptics from 'expo-haptics';

const RISK_CONFIG = {
  low: { label: 'منخفض', color: Colors.success, bg: Colors.successLight, icon: 'shield-checkmark', desc: 'مخاطر السكري منخفضة. استمر بنمط الحياة الصحي.' },
  moderate: { label: 'متوسط', color: Colors.accent, bg: Colors.accentLight, icon: 'shield-half', desc: 'خطر متوسط. ابدأ بتحسين نمط حياتك الآن.' },
  high: { label: 'مرتفع', color: Colors.warning, bg: Colors.warningLight, icon: 'warning', desc: 'أنت في مرحلة ما قبل السكري. تحرك الآن.' },
  'very-high': { label: 'مرتفع جداً', color: Colors.danger, bg: Colors.dangerLight, icon: 'alert-circle', desc: 'خطر جداً مرتفع. استشر طبيبك فوراً.' },
};

function RiskGauge({ score, category }: { score: number; category: string }) {
  const cfg = RISK_CONFIG[category as keyof typeof RISK_CONFIG];
  const percent = Math.min((score / 20) * 100, 100);
  return (
    <LinearGradient colors={['#0D9488', '#0F766E']} style={styles.riskCard} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}>
      <View style={styles.riskTop}>
        <View>
          <Text style={styles.riskLabel}>درجة الخطر ADA 2026</Text>
          <Text style={styles.riskScore}>{score}<Text style={styles.riskMax}>/20</Text></Text>
        </View>
        <View style={[styles.riskBadge, { backgroundColor: cfg.color }]}>
          <Ionicons name={cfg.icon as any} size={16} color="#fff" />
          <Text style={styles.riskBadgeText}>{cfg.label}</Text>
        </View>
      </View>
      <View style={styles.progressBar}>
        <View style={[styles.progressFill, { width: `${percent}%` as any, backgroundColor: cfg.color }]} />
      </View>
      <Text style={styles.riskDesc}>{cfg.desc}</Text>
    </LinearGradient>
  );
}

function MetricCard({ icon, label, value, unit, sub, color }: {
  icon: string; label: string; value: string; unit: string; sub?: string; color: string;
}) {
  return (
    <View style={[styles.metricCard, { borderLeftColor: color, borderLeftWidth: 4 }]}>
      <View style={[styles.metricIcon, { backgroundColor: color + '20' }]}>
        <MaterialCommunityIcons name={icon as any} size={22} color={color} />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={styles.metricLabel}>{label}</Text>
        <Text style={styles.metricValue}>{value} <Text style={styles.metricUnit}>{unit}</Text></Text>
        {sub && <Text style={styles.metricSub}>{sub}</Text>}
      </View>
    </View>
  );
}

function AlertCard({ alert, onRead }: { alert: any; onRead: () => void }) {
  const colors = {
    info: { bg: Colors.primaryLight, border: Colors.primary, icon: Colors.primary },
    warning: { bg: Colors.accentLight, border: Colors.accent, icon: Colors.accent },
    danger: { bg: Colors.dangerLight, border: Colors.danger, icon: Colors.danger },
  };
  const c = colors[alert.severity as keyof typeof colors];
  return (
    <Pressable style={[styles.alertCard, { backgroundColor: c.bg, borderLeftColor: c.border }]} onPress={onRead}>
      <View style={styles.alertRow}>
        <Ionicons name={alert.severity === 'danger' ? 'alert-circle' : alert.severity === 'warning' ? 'warning' : 'information-circle'} size={18} color={c.icon} />
        <Text style={[styles.alertText, { color: Colors.light.text }]}>{alert.message}</Text>
        {!alert.read && <View style={[styles.alertDot, { backgroundColor: c.icon }]} />}
      </View>
    </Pressable>
  );
}

export default function DashboardScreen() {
  const insets = useSafeAreaInsets();
  const { profile, bmi, riskScore, riskCategory, glucoseReadings, weightReadings, exerciseLogs, alerts, markAlertRead } = useHealth();
  const isWeb = Platform.OS === 'web';
  const topPad = isWeb ? 67 : insets.top;
  const bottomPad = isWeb ? 34 : 0;

  const latestGlucose = glucoseReadings[0];
  const latestWeight = weightReadings[0];

  const weekExercise = exerciseLogs
    .filter(e => {
      const d = new Date(e.date);
      const now = new Date();
      const diff = (now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24);
      return diff <= 7;
    })
    .reduce((acc, e) => acc + e.minutes, 0);

  const unreadAlerts = alerts.filter(a => !a.read).slice(0, 3);

  function getBmiStatus(bmi: number) {
    if (bmi < 18.5) return 'نقص الوزن';
    if (bmi < 25) return 'طبيعي';
    if (bmi < 30) return 'وزن زائد';
    return 'سمنة';
  }

  function getGlucoseStatus(val: number, type: string) {
    if (type === 'a1c') {
      if (val < 5.7) return 'طبيعي';
      if (val < 6.5) return 'ما قبل السكري';
      return 'سكري';
    }
    if (type === 'fasting') {
      if (val < 100) return 'طبيعي';
      if (val < 126) return 'ما قبل السكري';
      return 'سكري';
    }
    return '';
  }

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: Colors.light.background }}
      contentContainerStyle={{ paddingBottom: bottomPad + 100 }}
      showsVerticalScrollIndicator={false}
    >
      <View style={[styles.headerArea, { paddingTop: topPad + 8 }]}>
        <View>
          <Text style={styles.greeting}>مرحباً،</Text>
          <Text style={styles.userName}>{profile?.name || 'مستخدم'}</Text>
        </View>
        <View style={styles.headerBadge}>
          <MaterialCommunityIcons name="heart-circle" size={22} color={Colors.primary} />
        </View>
      </View>

      <View style={styles.padH}>
        <RiskGauge score={riskScore} category={riskCategory} />

        <Text style={styles.sectionTitle}>المؤشرات الصحية</Text>
        <MetricCard icon="scale-bathroom" label="مؤشر كتلة الجسم BMI" value={bmi.toString()} unit="" sub={getBmiStatus(bmi)} color={bmi >= 30 ? Colors.danger : bmi >= 25 ? Colors.warning : Colors.success} />
        {latestGlucose && (
          <MetricCard
            icon="water"
            label={latestGlucose.type === 'a1c' ? 'HbA1c' : latestGlucose.type === 'fasting' ? 'سكر صائم' : 'سكر بعد الأكل'}
            value={latestGlucose.value.toString()}
            unit={latestGlucose.type === 'a1c' ? '%' : 'mg/dL'}
            sub={getGlucoseStatus(latestGlucose.value, latestGlucose.type)}
            color={latestGlucose.type === 'fasting' && latestGlucose.value >= 100 ? Colors.warning : Colors.success}
          />
        )}
        <MetricCard icon="run" label="نشاط هذا الأسبوع" value={weekExercise.toString()} unit="دقيقة" sub={weekExercise >= 150 ? 'ممتاز' : weekExercise >= 75 ? 'جيد' : 'أقل من الموصى به'} color={weekExercise >= 150 ? Colors.success : weekExercise >= 75 ? Colors.accent : Colors.warning} />
        {latestWeight && (
          <MetricCard icon="weight-kilogram" label="الوزن الحالي" value={latestWeight.value.toString()} unit="كغ" color={Colors.primary} />
        )}

        {!latestGlucose && !latestWeight && (
          <View style={styles.emptyMetrics}>
            <Ionicons name="pulse-outline" size={32} color={Colors.light.textTertiary} />
            <Text style={styles.emptyText}>سجّل قياساتك من تبويب المقاييس للبدء</Text>
          </View>
        )}

        {unreadAlerts.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>التنبيهات</Text>
            {unreadAlerts.map(a => (
              <AlertCard key={a.id} alert={a} onRead={() => { Haptics.selectionAsync(); markAlertRead(a.id); }} />
            ))}
          </>
        )}

        <Text style={styles.sectionTitle}>معيار ADA 2026 لما قبل السكري</Text>
        <View style={styles.adaCard}>
          {[
            { label: 'سكر صائم', range: '100-125 mg/dL', icon: 'water' },
            { label: 'سكر 2 ساعة', range: '140-199 mg/dL', icon: 'time' },
            { label: 'HbA1c', range: '5.7-6.4%', icon: 'analytics' },
          ].map(item => (
            <View key={item.label} style={styles.adaRow}>
              <Ionicons name={item.icon as any} size={16} color={Colors.primary} />
              <Text style={styles.adaLabel}>{item.label}</Text>
              <Text style={styles.adaRange}>{item.range}</Text>
            </View>
          ))}
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  headerArea: { paddingHorizontal: 24, paddingBottom: 16, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  greeting: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.light.textSecondary, textAlign: 'right' },
  userName: { fontFamily: 'Nunito_800ExtraBold', fontSize: 26, color: Colors.light.text, textAlign: 'right' },
  headerBadge: { width: 44, height: 44, borderRadius: 14, backgroundColor: Colors.primaryLight, justifyContent: 'center', alignItems: 'center' },
  padH: { paddingHorizontal: 20, gap: 0 },
  riskCard: { borderRadius: 20, padding: 20, marginBottom: 20, gap: 12 },
  riskTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  riskLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 13, color: 'rgba(255,255,255,0.8)', textAlign: 'right' },
  riskScore: { fontFamily: 'Nunito_800ExtraBold', fontSize: 48, color: '#fff' },
  riskMax: { fontFamily: 'Nunito_400Regular', fontSize: 20, color: 'rgba(255,255,255,0.7)' },
  riskBadge: { borderRadius: 10, paddingHorizontal: 12, paddingVertical: 6, flexDirection: 'row', gap: 6, alignItems: 'center' },
  riskBadgeText: { fontFamily: 'Nunito_700Bold', fontSize: 13, color: '#fff' },
  progressBar: { height: 8, backgroundColor: 'rgba(255,255,255,0.25)', borderRadius: 4, overflow: 'hidden' },
  progressFill: { height: 8, borderRadius: 4 },
  riskDesc: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: 'rgba(255,255,255,0.9)', textAlign: 'right' },
  sectionTitle: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.light.text, marginTop: 20, marginBottom: 12, textAlign: 'right' },
  metricCard: { backgroundColor: Colors.light.card, borderRadius: 14, padding: 14, flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 10, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 6, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  metricIcon: { width: 44, height: 44, borderRadius: 12, justifyContent: 'center', alignItems: 'center' },
  metricLabel: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textSecondary, textAlign: 'right' },
  metricValue: { fontFamily: 'Nunito_700Bold', fontSize: 22, color: Colors.light.text, textAlign: 'right' },
  metricUnit: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.light.textSecondary },
  metricSub: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, color: Colors.light.textTertiary, textAlign: 'right' },
  emptyMetrics: { backgroundColor: Colors.light.card, borderRadius: 14, padding: 24, alignItems: 'center', gap: 10, marginBottom: 10 },
  emptyText: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.light.textTertiary, textAlign: 'center' },
  alertCard: { borderRadius: 12, padding: 12, marginBottom: 8, borderLeftWidth: 4 },
  alertRow: { flexDirection: 'row', gap: 8, alignItems: 'flex-start' },
  alertText: { fontFamily: 'Nunito_400Regular', fontSize: 13, flex: 1, textAlign: 'right', lineHeight: 20 },
  alertDot: { width: 8, height: 8, borderRadius: 4, marginTop: 4 },
  adaCard: { backgroundColor: Colors.light.card, borderRadius: 14, overflow: 'hidden', marginBottom: 10 },
  adaRow: { flexDirection: 'row', alignItems: 'center', gap: 10, padding: 14, borderBottomWidth: 1, borderBottomColor: Colors.light.border },
  adaLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.text, flex: 1, textAlign: 'right' },
  adaRange: { fontFamily: 'Nunito_700Bold', fontSize: 14, color: Colors.primary },
});
