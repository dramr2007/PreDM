import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, Pressable, TextInput,
  Modal, Platform, Alert,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useHealth } from '@/context/HealthContext';
import Colors from '@/constants/colors';
import * as Haptics from 'expo-haptics';

type LogType = 'glucose' | 'weight' | 'exercise' | 'bp';

function TabBtn({ label, active, onPress }: { label: string; active: boolean; onPress: () => void }) {
  return (
    <Pressable style={[styles.tabBtn, active && styles.tabBtnActive]} onPress={() => { Haptics.selectionAsync(); onPress(); }}>
      <Text style={[styles.tabBtnText, active && styles.tabBtnTextActive]}>{label}</Text>
    </Pressable>
  );
}

function ReadingRow({ icon, value, unit, date, sub, color }: {
  icon: string; value: string; unit: string; date: string; sub?: string; color: string;
}) {
  const d = new Date(date);
  const dateStr = d.toLocaleDateString('ar-SA', { month: 'short', day: 'numeric' });
  const timeStr = d.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
  return (
    <View style={styles.readingRow}>
      <View style={[styles.readingIcon, { backgroundColor: color + '20' }]}>
        <MaterialCommunityIcons name={icon as any} size={20} color={color} />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={styles.readingValue}>{value} <Text style={styles.readingUnit}>{unit}</Text></Text>
        {sub && <Text style={[styles.readingSub, { color }]}>{sub}</Text>}
      </View>
      <View style={{ alignItems: 'flex-end' }}>
        <Text style={styles.readingDate}>{dateStr}</Text>
        <Text style={styles.readingTime}>{timeStr}</Text>
      </View>
    </View>
  );
}

function LogModal({ visible, type, onClose }: { visible: boolean; type: LogType; onClose: () => void }) {
  const { addGlucoseReading, addWeightReading, addExerciseLog, addBpReading, profile } = useHealth();
  const [val1, setVal1] = useState('');
  const [val2, setVal2] = useState('');
  const [glucoseType, setGlucoseType] = useState<'fasting' | 'postmeal' | 'a1c' | 'random'>('fasting');
  const [exerciseType, setExerciseType] = useState<'walking' | 'running' | 'cycling' | 'swimming' | 'gym' | 'other'>('walking');
  const [notes, setNotes] = useState('');

  async function save() {
    try {
      const now = new Date().toISOString();
      if (type === 'glucose') {
        const v = parseFloat(val1);
        if (!v) { Alert.alert('تنبيه', 'أدخل قيمة صحيحة'); return; }
        await addGlucoseReading({ date: now, value: v, type: glucoseType, notes });
      } else if (type === 'weight') {
        const v = parseFloat(val1);
        if (!v) { Alert.alert('تنبيه', 'أدخل قيمة صحيحة'); return; }
        const h = profile?.height || 170;
        const bmi = parseFloat((v / Math.pow(h / 100, 2)).toFixed(1));
        await addWeightReading({ date: now, value: v, bmi });
      } else if (type === 'exercise') {
        const v = parseInt(val1);
        if (!v) { Alert.alert('تنبيه', 'أدخل عدد الدقائق'); return; }
        await addExerciseLog({ date: now, minutes: v, type: exerciseType });
      } else if (type === 'bp') {
        const s = parseInt(val1), d = parseInt(val2);
        if (!s || !d) { Alert.alert('تنبيه', 'أدخل الضغط الانقباضي والانبساطي'); return; }
        await addBpReading({ date: now, systolic: s, diastolic: d });
      }
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setVal1(''); setVal2(''); setNotes('');
      onClose();
    } catch (e) {
      Alert.alert('خطأ', 'حدث خطأ أثناء الحفظ');
    }
  }

  const GLUCOSE_TYPES = [['fasting','صائم'], ['postmeal','بعد الأكل'], ['a1c','HbA1c'], ['random','عشوائي']];
  const EX_TYPES = [['walking','مشي'], ['running','جري'], ['cycling','دراجة'], ['swimming','سباحة'], ['gym','صالة'], ['other','أخرى']];

  return (
    <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}>
      <View style={styles.modal}>
        <View style={styles.modalHeader}>
          <Pressable onPress={onClose} style={styles.modalClose}>
            <Ionicons name="close" size={22} color={Colors.light.text} />
          </Pressable>
          <Text style={styles.modalTitle}>
            {type === 'glucose' ? 'تسجيل سكر الدم' : type === 'weight' ? 'تسجيل الوزن' : type === 'exercise' ? 'تسجيل التمرين' : 'تسجيل ضغط الدم'}
          </Text>
        </View>
        <ScrollView contentContainerStyle={styles.modalContent} showsVerticalScrollIndicator={false}>
          {type === 'glucose' && (
            <>
              <Text style={styles.modalLabel}>نوع القياس</Text>
              <View style={styles.typeRow}>
                {GLUCOSE_TYPES.map(([v, l]) => (
                  <Pressable key={v} style={[styles.typeBtn, glucoseType === v && styles.typeBtnActive]} onPress={() => setGlucoseType(v as any)}>
                    <Text style={[styles.typeBtnText, glucoseType === v && styles.typeBtnTextActive]}>{l}</Text>
                  </Pressable>
                ))}
              </View>
              <Text style={styles.modalLabel}>{glucoseType === 'a1c' ? 'قيمة HbA1c (%)' : 'مستوى السكر (mg/dL)'}</Text>
              <TextInput style={styles.modalInput} value={val1} onChangeText={setVal1} keyboardType="decimal-pad" placeholder={glucoseType === 'a1c' ? 'مثال: 5.9' : 'مثال: 95'} placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
              {glucoseType !== 'a1c' && (
                <View style={styles.refCard}>
                  <Text style={styles.refTitle}>المرجع ADA 2026</Text>
                  <Text style={styles.refText}>صائم: طبيعي &lt;100 | ما قبل السكري 100-125 | سكري &ge;126</Text>
                  <Text style={styles.refText}>بعد الأكل: طبيعي &lt;140 | ما قبل السكري 140-199 | سكري &ge;200</Text>
                </View>
              )}
            </>
          )}
          {type === 'weight' && (
            <>
              <Text style={styles.modalLabel}>الوزن (كغ)</Text>
              <TextInput style={styles.modalInput} value={val1} onChangeText={setVal1} keyboardType="decimal-pad" placeholder="مثال: 78.5" placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
            </>
          )}
          {type === 'exercise' && (
            <>
              <Text style={styles.modalLabel}>نوع التمرين</Text>
              <View style={styles.typeRow}>
                {EX_TYPES.map(([v, l]) => (
                  <Pressable key={v} style={[styles.typeBtn, exerciseType === v && styles.typeBtnActive]} onPress={() => setExerciseType(v as any)}>
                    <Text style={[styles.typeBtnText, exerciseType === v && styles.typeBtnTextActive]}>{l}</Text>
                  </Pressable>
                ))}
              </View>
              <Text style={styles.modalLabel}>المدة (دقيقة)</Text>
              <TextInput style={styles.modalInput} value={val1} onChangeText={setVal1} keyboardType="number-pad" placeholder="مثال: 30" placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
              <View style={styles.refCard}>
                <Text style={styles.refTitle}>توصية ADA</Text>
                <Text style={styles.refText}>150 دقيقة أسبوعياً من التمرين متوسط الشدة تقلل خطر السكري بنسبة 58%</Text>
              </View>
            </>
          )}
          {type === 'bp' && (
            <>
              <Text style={styles.modalLabel}>الضغط الانقباضي (mmHg)</Text>
              <TextInput style={styles.modalInput} value={val1} onChangeText={setVal1} keyboardType="number-pad" placeholder="مثال: 120" placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
              <Text style={styles.modalLabel}>الضغط الانبساطي (mmHg)</Text>
              <TextInput style={styles.modalInput} value={val2} onChangeText={setVal2} keyboardType="number-pad" placeholder="مثال: 80" placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
              <View style={styles.refCard}>
                <Text style={styles.refTitle}>المرجع</Text>
                <Text style={styles.refText}>طبيعي: &lt;120/80 | مرتفع: 130/80 أو أكثر</Text>
                <Text style={styles.refText}>ضغط الدم المرتفع يزيد خطر السكري</Text>
              </View>
            </>
          )}
          <Pressable style={styles.saveBtn} onPress={save}>
            <Text style={styles.saveBtnText}>حفظ القياس</Text>
          </Pressable>
        </ScrollView>
      </View>
    </Modal>
  );
}

export default function MetricsScreen() {
  const insets = useSafeAreaInsets();
  const isWeb = Platform.OS === 'web';
  const topPad = isWeb ? 67 : insets.top;
  const bottomPad = isWeb ? 34 : 0;

  const { glucoseReadings, weightReadings, exerciseLogs, bpReadings } = useHealth();
  const [activeTab, setActiveTab] = useState<LogType>('glucose');
  const [modalType, setModalType] = useState<LogType | null>(null);

  function openModal(t: LogType) {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setModalType(t);
  }

  function glucoseStatus(val: number, type: string) {
    if (type === 'a1c') {
      if (val < 5.7) return { label: 'طبيعي', color: Colors.success };
      if (val < 6.5) return { label: 'ما قبل السكري', color: Colors.warning };
      return { label: 'سكري', color: Colors.danger };
    }
    if (type === 'fasting') {
      if (val < 100) return { label: 'طبيعي', color: Colors.success };
      if (val < 126) return { label: 'ما قبل السكري', color: Colors.warning };
      return { label: 'سكري', color: Colors.danger };
    }
    if (type === 'postmeal') {
      if (val < 140) return { label: 'طبيعي', color: Colors.success };
      if (val < 200) return { label: 'ما قبل السكري', color: Colors.warning };
      return { label: 'سكري', color: Colors.danger };
    }
    return { label: '', color: Colors.primary };
  }

  function bpStatus(s: number, d: number) {
    if (s < 120 && d < 80) return { label: 'طبيعي', color: Colors.success };
    if (s < 130 && d < 80) return { label: 'مرتفع قليلاً', color: Colors.accent };
    if (s < 140 || d < 90) return { label: 'مرتفع', color: Colors.warning };
    return { label: 'مرتفع جداً', color: Colors.danger };
  }

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      <View style={[styles.header, { paddingTop: topPad + 8 }]}>
        <Text style={styles.screenTitle}>المقاييس الصحية</Text>
        <Pressable style={styles.addBtn} onPress={() => openModal(activeTab)}>
          <Ionicons name="add" size={22} color="#fff" />
        </Pressable>
      </View>
      <View style={styles.tabs}>
        <TabBtn label="سكر" active={activeTab === 'glucose'} onPress={() => setActiveTab('glucose')} />
        <TabBtn label="وزن" active={activeTab === 'weight'} onPress={() => setActiveTab('weight')} />
        <TabBtn label="رياضة" active={activeTab === 'exercise'} onPress={() => setActiveTab('exercise')} />
        <TabBtn label="ضغط" active={activeTab === 'bp'} onPress={() => setActiveTab('bp')} />
      </View>
      <ScrollView contentContainerStyle={[styles.list, { paddingBottom: bottomPad + 100 }]} showsVerticalScrollIndicator={false}>
        {activeTab === 'glucose' && (
          glucoseReadings.length === 0 ? (
            <View style={styles.empty}>
              <Ionicons name="water-outline" size={40} color={Colors.light.textTertiary} />
              <Text style={styles.emptyText}>لا توجد قراءات بعد</Text>
              <Text style={styles.emptySub}>اضغط + لتسجيل قياس جديد</Text>
            </View>
          ) : glucoseReadings.map(r => {
            const s = glucoseStatus(r.value, r.type);
            const typeLabel = r.type === 'fasting' ? 'صائم' : r.type === 'postmeal' ? 'بعد الأكل' : r.type === 'a1c' ? 'HbA1c' : 'عشوائي';
            return (
              <ReadingRow key={r.id} icon="water" value={`${r.value} (${typeLabel})`} unit={r.type === 'a1c' ? '%' : 'mg/dL'} date={r.date} sub={s.label} color={s.color} />
            );
          })
        )}
        {activeTab === 'weight' && (
          weightReadings.length === 0 ? (
            <View style={styles.empty}>
              <MaterialCommunityIcons name="scale-bathroom" size={40} color={Colors.light.textTertiary} />
              <Text style={styles.emptyText}>لا توجد قراءات بعد</Text>
              <Text style={styles.emptySub}>اضغط + لتسجيل قياس جديد</Text>
            </View>
          ) : weightReadings.map(r => (
            <ReadingRow key={r.id} icon="weight-kilogram" value={r.value.toString()} unit="كغ" date={r.date} sub={r.bmi ? `BMI: ${r.bmi}` : undefined} color={Colors.primary} />
          ))
        )}
        {activeTab === 'exercise' && (
          exerciseLogs.length === 0 ? (
            <View style={styles.empty}>
              <Ionicons name="fitness-outline" size={40} color={Colors.light.textTertiary} />
              <Text style={styles.emptyText}>لا يوجد نشاط مسجل</Text>
              <Text style={styles.emptySub}>اضغط + لتسجيل تمرين</Text>
            </View>
          ) : exerciseLogs.map(l => {
            const typeLabel = { walking: 'مشي', running: 'جري', cycling: 'دراجة', swimming: 'سباحة', gym: 'صالة', other: 'أخرى' }[l.type];
            return (
              <ReadingRow key={l.id} icon="run" value={l.minutes.toString()} unit="دقيقة" date={l.date} sub={typeLabel} color={Colors.success} />
            );
          })
        )}
        {activeTab === 'bp' && (
          bpReadings.length === 0 ? (
            <View style={styles.empty}>
              <MaterialCommunityIcons name="heart-pulse" size={40} color={Colors.light.textTertiary} />
              <Text style={styles.emptyText}>لا توجد قراءات بعد</Text>
              <Text style={styles.emptySub}>اضغط + لتسجيل قياس ضغط الدم</Text>
            </View>
          ) : bpReadings.map(r => {
            const s = bpStatus(r.systolic, r.diastolic);
            return (
              <ReadingRow key={r.id} icon="heart-pulse" value={`${r.systolic}/${r.diastolic}`} unit="mmHg" date={r.date} sub={s.label} color={s.color} />
            );
          })
        )}
      </ScrollView>
      {modalType && <LogModal visible={true} type={modalType} onClose={() => setModalType(null)} />}
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: 24, paddingBottom: 12, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-end', backgroundColor: Colors.light.background },
  screenTitle: { fontFamily: 'Nunito_800ExtraBold', fontSize: 26, color: Colors.light.text },
  addBtn: { width: 40, height: 40, borderRadius: 12, backgroundColor: Colors.primary, justifyContent: 'center', alignItems: 'center' },
  tabs: { flexDirection: 'row', paddingHorizontal: 20, gap: 8, paddingBottom: 12, backgroundColor: Colors.light.background },
  tabBtn: { flex: 1, paddingVertical: 8, borderRadius: 10, backgroundColor: Colors.light.card, borderWidth: 1, borderColor: Colors.light.border, alignItems: 'center' },
  tabBtnActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  tabBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 13, color: Colors.light.textSecondary },
  tabBtnTextActive: { color: '#fff' },
  list: { paddingHorizontal: 20, paddingTop: 4, gap: 0 },
  readingRow: { backgroundColor: Colors.light.card, borderRadius: 14, padding: 14, flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 10, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  readingIcon: { width: 40, height: 40, borderRadius: 10, justifyContent: 'center', alignItems: 'center' },
  readingValue: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.light.text, textAlign: 'right' },
  readingUnit: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.light.textSecondary },
  readingSub: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, textAlign: 'right' },
  readingDate: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, color: Colors.light.textSecondary, textAlign: 'right' },
  readingTime: { fontFamily: 'Nunito_400Regular', fontSize: 11, color: Colors.light.textTertiary, textAlign: 'right' },
  empty: { padding: 48, alignItems: 'center', gap: 10 },
  emptyText: { fontFamily: 'Nunito_600SemiBold', fontSize: 16, color: Colors.light.textSecondary, textAlign: 'center' },
  emptySub: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textTertiary, textAlign: 'center' },
  modal: { flex: 1, backgroundColor: Colors.light.background },
  modalHeader: { flexDirection: 'row', alignItems: 'center', padding: 20, borderBottomWidth: 1, borderBottomColor: Colors.light.border, gap: 12 },
  modalClose: { width: 36, height: 36, borderRadius: 10, backgroundColor: Colors.light.card, justifyContent: 'center', alignItems: 'center' },
  modalTitle: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.light.text, flex: 1, textAlign: 'right' },
  modalContent: { padding: 20, gap: 8 },
  modalLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary, textAlign: 'right', marginTop: 8 },
  modalInput: { backgroundColor: Colors.light.card, borderWidth: 1, borderColor: Colors.light.border, borderRadius: 12, paddingHorizontal: 16, paddingVertical: 14, fontFamily: 'Nunito_400Regular', fontSize: 18, color: Colors.light.text },
  typeRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginVertical: 4 },
  typeBtn: { paddingHorizontal: 14, paddingVertical: 8, borderRadius: 10, borderWidth: 1, borderColor: Colors.light.border, backgroundColor: Colors.light.card },
  typeBtnActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  typeBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 13, color: Colors.light.textSecondary },
  typeBtnTextActive: { color: '#fff' },
  refCard: { backgroundColor: Colors.primaryLight, borderRadius: 10, padding: 12, gap: 4, marginTop: 8 },
  refTitle: { fontFamily: 'Nunito_700Bold', fontSize: 13, color: Colors.primaryDark, textAlign: 'right' },
  refText: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.primaryDark, textAlign: 'right', lineHeight: 18 },
  saveBtn: { backgroundColor: Colors.primary, borderRadius: 14, paddingVertical: 16, alignItems: 'center', marginTop: 16 },
  saveBtnText: { fontFamily: 'Nunito_700Bold', fontSize: 17, color: '#fff' },
});
