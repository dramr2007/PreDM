import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, Pressable, TextInput,
  Modal, Platform, Alert, Switch,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useHealth, Medication } from '@/context/HealthContext';
import Colors from '@/constants/colors';
import * as Haptics from 'expo-haptics';

const MED_TYPES = [
  { value: 'corticosteroid', label: 'كورتيكوستيرويد', color: Colors.danger, icon: 'pill', desc: 'يرفع السكر بشدة', raisesGlucose: true },
  { value: 'immunosuppressant', label: 'مثبط المناعة', color: Colors.warning, icon: 'shield-off', desc: 'قد يرفع السكر', raisesGlucose: true },
  { value: 'antipsychotic', label: 'مضاد الذهان', color: Colors.warning, icon: 'brain', desc: 'يزيد الوزن والسكر', raisesGlucose: true },
  { value: 'statin', label: 'ستاتين', color: Colors.accent, icon: 'heart', desc: 'خطر طفيف على السكر', raisesGlucose: false },
  { value: 'diuretic', label: 'مدر للبول', color: Colors.accent, icon: 'water', desc: 'قد يؤثر على السكر', raisesGlucose: false },
  { value: 'other', label: 'أخرى', color: Colors.primary, icon: 'medical', desc: '', raisesGlucose: false },
];

const COMMON_MEDS = [
  { name: 'بريدنيزون', type: 'corticosteroid', raisesGlucose: true },
  { name: 'ديكساميثازون', type: 'corticosteroid', raisesGlucose: true },
  { name: 'ميثيل بريدنيزولون', type: 'corticosteroid', raisesGlucose: true },
  { name: 'هيدروكورتيزون', type: 'corticosteroid', raisesGlucose: true },
  { name: 'سيكلوسبورين', type: 'immunosuppressant', raisesGlucose: true },
  { name: 'تاكروليموس', type: 'immunosuppressant', raisesGlucose: true },
  { name: 'أولانزابين', type: 'antipsychotic', raisesGlucose: true },
  { name: 'كلوزابين', type: 'antipsychotic', raisesGlucose: true },
  { name: 'أتورفاستاتين', type: 'statin', raisesGlucose: false },
  { name: 'هيدروكلوروثيازيد', type: 'diuretic', raisesGlucose: false },
];

function MedCard({ med, onToggle, onDelete }: { med: Medication; onToggle: () => void; onDelete: () => void }) {
  const typeInfo = MED_TYPES.find(t => t.value === med.type) || MED_TYPES[5];
  return (
    <View style={[styles.medCard, !med.active && styles.medCardInactive]}>
      <View style={[styles.medIcon, { backgroundColor: typeInfo.color + '20' }]}>
        <MaterialCommunityIcons name={typeInfo.icon as any} size={22} color={med.active ? typeInfo.color : Colors.light.textTertiary} />
      </View>
      <View style={{ flex: 1 }}>
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
          <Text style={[styles.medName, !med.active && styles.medNameInactive]}>{med.name}</Text>
          {med.raisesGlucose && med.active && (
            <View style={styles.glucoseWarnBadge}>
              <Ionicons name="warning" size={10} color={Colors.danger} />
              <Text style={styles.glucoseWarnText}>يرفع السكر</Text>
            </View>
          )}
        </View>
        <Text style={styles.medDose}>{med.dose} — {med.frequency}</Text>
        <Text style={styles.medType}>{typeInfo.label}</Text>
        {med.notes && <Text style={styles.medNotes}>{med.notes}</Text>}
      </View>
      <View style={{ alignItems: 'flex-end', gap: 10 }}>
        <Switch
          value={med.active}
          onValueChange={() => { Haptics.selectionAsync(); onToggle(); }}
          trackColor={{ false: Colors.light.border, true: Colors.primary + '80' }}
          thumbColor={med.active ? Colors.primary : Colors.light.textTertiary}
        />
        <Pressable onPress={() => {
          Alert.alert('حذف', `حذف ${med.name}؟`, [
            { text: 'إلغاء', style: 'cancel' },
            { text: 'حذف', style: 'destructive', onPress: () => { Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning); onDelete(); } },
          ]);
        }}>
          <Ionicons name="trash-outline" size={18} color={Colors.light.textTertiary} />
        </Pressable>
      </View>
    </View>
  );
}

function AddMedModal({ visible, onClose }: { visible: boolean; onClose: () => void }) {
  const { addMedication } = useHealth();
  const [name, setName] = useState('');
  const [dose, setDose] = useState('');
  const [frequency, setFrequency] = useState('يومياً');
  const [type, setType] = useState<Medication['type']>('other');
  const [raisesGlucose, setRaisesGlucose] = useState(false);
  const [notes, setNotes] = useState('');
  const [showCommon, setShowCommon] = useState(false);

  function selectCommon(m: typeof COMMON_MEDS[0]) {
    setName(m.name);
    setType(m.type as Medication['type']);
    setRaisesGlucose(m.raisesGlucose);
    setShowCommon(false);
  }

  async function save() {
    if (!name || !dose) { Alert.alert('تنبيه', 'أدخل اسم الدواء والجرعة'); return; }
    await addMedication({
      name, dose, frequency,
      type, raisesGlucose,
      startDate: new Date().toISOString(),
      notes, active: true,
    });
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setName(''); setDose(''); setNotes(''); setType('other'); setRaisesGlucose(false);
    onClose();
  }

  return (
    <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}>
      <View style={styles.modal}>
        <View style={styles.modalHeader}>
          <Pressable onPress={onClose} style={styles.modalClose}>
            <Ionicons name="close" size={22} color={Colors.light.text} />
          </Pressable>
          <Text style={styles.modalTitle}>إضافة دواء</Text>
        </View>
        <ScrollView contentContainerStyle={styles.modalContent} showsVerticalScrollIndicator={false}>
          <Pressable style={styles.commonBtn} onPress={() => setShowCommon(!showCommon)}>
            <MaterialCommunityIcons name="list-box" size={16} color={Colors.primary} />
            <Text style={styles.commonBtnText}>اختر من الأدوية الشائعة</Text>
            <Ionicons name={showCommon ? 'chevron-up' : 'chevron-down'} size={16} color={Colors.primary} />
          </Pressable>
          {showCommon && (
            <View style={styles.commonList}>
              {COMMON_MEDS.map(m => (
                <Pressable key={m.name} style={styles.commonItem} onPress={() => selectCommon(m)}>
                  {m.raisesGlucose && <Ionicons name="warning" size={14} color={Colors.danger} />}
                  <Text style={styles.commonItemText}>{m.name}</Text>
                  <Text style={styles.commonItemType}>{MED_TYPES.find(t => t.value === m.type)?.label}</Text>
                </Pressable>
              ))}
            </View>
          )}
          <Text style={styles.modalLabel}>اسم الدواء</Text>
          <TextInput style={styles.modalInput} value={name} onChangeText={setName} placeholder="مثال: بريدنيزون" placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
          <Text style={styles.modalLabel}>الجرعة</Text>
          <TextInput style={styles.modalInput} value={dose} onChangeText={setDose} placeholder="مثال: 20mg" placeholderTextColor={Colors.light.textTertiary} textAlign="right" />
          <Text style={styles.modalLabel}>التكرار</Text>
          <View style={styles.freqRow}>
            {['يومياً', 'مرتين يومياً', 'أسبوعياً', 'عند الحاجة'].map(f => (
              <Pressable key={f} style={[styles.freqBtn, frequency === f && styles.freqBtnActive]} onPress={() => setFrequency(f)}>
                <Text style={[styles.freqBtnText, frequency === f && styles.freqBtnTextActive]}>{f}</Text>
              </Pressable>
            ))}
          </View>
          <Text style={styles.modalLabel}>نوع الدواء</Text>
          <View style={styles.typeGrid}>
            {MED_TYPES.map(t => (
              <Pressable key={t.value} style={[styles.typeBtn, type === t.value && { backgroundColor: t.color, borderColor: t.color }]} onPress={() => { setType(t.value as Medication['type']); if (t.raisesGlucose) setRaisesGlucose(true); }}>
                <MaterialCommunityIcons name={t.icon as any} size={14} color={type === t.value ? '#fff' : t.color} />
                <Text style={[styles.typeBtnText, type === t.value && { color: '#fff' }]}>{t.label}</Text>
              </Pressable>
            ))}
          </View>
          <View style={styles.glucoseToggle}>
            <Text style={styles.glucoseToggleLabel}>هل يرفع هذا الدواء السكر؟</Text>
            <Switch value={raisesGlucose} onValueChange={setRaisesGlucose} trackColor={{ false: Colors.light.border, true: Colors.danger + '80' }} thumbColor={raisesGlucose ? Colors.danger : Colors.light.textTertiary} />
          </View>
          {raisesGlucose && (
            <View style={styles.warnBox}>
              <Ionicons name="warning" size={16} color={Colors.danger} />
              <Text style={styles.warnBoxText}>سيتم إنشاء تنبيه تلقائي لمراقبة مستوى السكر</Text>
            </View>
          )}
          <Text style={styles.modalLabel}>ملاحظات (اختياري)</Text>
          <TextInput style={[styles.modalInput, { height: 80 }]} value={notes} onChangeText={setNotes} placeholder="أي ملاحظات إضافية..." placeholderTextColor={Colors.light.textTertiary} textAlign="right" multiline />
          <Pressable style={styles.saveBtn} onPress={save}>
            <Text style={styles.saveBtnText}>إضافة الدواء</Text>
          </Pressable>
        </ScrollView>
      </View>
    </Modal>
  );
}

export default function MedsScreen() {
  const insets = useSafeAreaInsets();
  const isWeb = Platform.OS === 'web';
  const topPad = isWeb ? 67 : insets.top;
  const bottomPad = isWeb ? 34 : 0;
  const { medications, toggleMedication, deleteMedication } = useHealth();
  const [showModal, setShowModal] = useState(false);

  const activeMeds = medications.filter(m => m.active);
  const inactiveMeds = medications.filter(m => !m.active);
  const riskMeds = activeMeds.filter(m => m.raisesGlucose);

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      <View style={[styles.header, { paddingTop: topPad + 8 }]}>
        <Text style={styles.screenTitle}>الأدوية</Text>
        <Pressable style={styles.addBtn} onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); setShowModal(true); }}>
          <Ionicons name="add" size={22} color="#fff" />
        </Pressable>
      </View>
      <ScrollView contentContainerStyle={[styles.content, { paddingBottom: bottomPad + 100 }]} showsVerticalScrollIndicator={false}>
        {riskMeds.length > 0 && (
          <View style={styles.riskBanner}>
            <Ionicons name="alert-circle" size={20} color={Colors.danger} />
            <View style={{ flex: 1 }}>
              <Text style={styles.riskBannerTitle}>تنبيه مهم</Text>
              <Text style={styles.riskBannerText}>لديك {riskMeds.length} دواء قد يرفع السكر. راقب مستوى السكر بشكل أكثر انتظاماً واستشر طبيبك.</Text>
            </View>
          </View>
        )}

        {medications.length === 0 && (
          <View style={styles.empty}>
            <MaterialCommunityIcons name="pill" size={48} color={Colors.light.textTertiary} />
            <Text style={styles.emptyTitle}>لا توجد أدوية مسجلة</Text>
            <Text style={styles.emptyText}>أضف أدويتك لمراقبة تأثيرها على مستوى السكر</Text>
          </View>
        )}

        {activeMeds.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>الأدوية الحالية</Text>
            {activeMeds.map(m => (
              <MedCard key={m.id} med={m} onToggle={() => toggleMedication(m.id)} onDelete={() => deleteMedication(m.id)} />
            ))}
          </>
        )}

        {inactiveMeds.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>أدوية متوقفة</Text>
            {inactiveMeds.map(m => (
              <MedCard key={m.id} med={m} onToggle={() => toggleMedication(m.id)} onDelete={() => deleteMedication(m.id)} />
            ))}
          </>
        )}

        <View style={styles.infoCard}>
          <MaterialCommunityIcons name="information" size={20} color={Colors.primary} />
          <View style={{ flex: 1 }}>
            <Text style={styles.infoTitle}>أدوية تستدعي الانتباه</Text>
            <Text style={styles.infoText}>
              الكورتيكوستيرويدات • مثبطات المناعة • مضادات الذهان اللانموذجية{'\n'}
              هذه الأدوية قد تسبب ارتفاعاً في السكر أو تزيد خطر التحول لمرض السكري
            </Text>
          </View>
        </View>
      </ScrollView>
      <AddMedModal visible={showModal} onClose={() => setShowModal(false)} />
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: 24, paddingBottom: 12, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-end', backgroundColor: Colors.light.background },
  screenTitle: { fontFamily: 'Nunito_800ExtraBold', fontSize: 26, color: Colors.light.text },
  addBtn: { width: 40, height: 40, borderRadius: 12, backgroundColor: Colors.primary, justifyContent: 'center', alignItems: 'center' },
  content: { paddingHorizontal: 20, paddingTop: 8, gap: 0 },
  riskBanner: { backgroundColor: Colors.dangerLight, borderRadius: 14, padding: 14, flexDirection: 'row', gap: 10, alignItems: 'flex-start', marginBottom: 16, borderLeftWidth: 4, borderLeftColor: Colors.danger },
  riskBannerTitle: { fontFamily: 'Nunito_700Bold', fontSize: 14, color: Colors.danger, textAlign: 'right' },
  riskBannerText: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textSecondary, textAlign: 'right', lineHeight: 20 },
  empty: { padding: 48, alignItems: 'center', gap: 10 },
  emptyTitle: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.light.textSecondary, textAlign: 'center' },
  emptyText: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.light.textTertiary, textAlign: 'center', lineHeight: 20 },
  sectionTitle: { fontFamily: 'Nunito_700Bold', fontSize: 16, color: Colors.light.text, textAlign: 'right', marginBottom: 10, marginTop: 4 },
  medCard: { backgroundColor: Colors.light.card, borderRadius: 14, padding: 14, flexDirection: 'row', alignItems: 'flex-start', gap: 12, marginBottom: 10, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  medCardInactive: { opacity: 0.6 },
  medIcon: { width: 44, height: 44, borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginTop: 2 },
  medName: { fontFamily: 'Nunito_700Bold', fontSize: 16, color: Colors.light.text, textAlign: 'right' },
  medNameInactive: { color: Colors.light.textTertiary },
  glucoseWarnBadge: { backgroundColor: Colors.dangerLight, borderRadius: 6, paddingHorizontal: 6, paddingVertical: 2, flexDirection: 'row', alignItems: 'center', gap: 3 },
  glucoseWarnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 10, color: Colors.danger },
  medDose: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textSecondary, textAlign: 'right', marginTop: 2 },
  medType: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, color: Colors.light.textTertiary, textAlign: 'right' },
  medNotes: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textTertiary, textAlign: 'right', marginTop: 2 },
  infoCard: { backgroundColor: Colors.primaryLight, borderRadius: 14, padding: 14, flexDirection: 'row', gap: 10, alignItems: 'flex-start', marginTop: 8 },
  infoTitle: { fontFamily: 'Nunito_700Bold', fontSize: 14, color: Colors.primaryDark, textAlign: 'right' },
  infoText: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.primaryDark, textAlign: 'right', lineHeight: 20 },
  modal: { flex: 1, backgroundColor: Colors.light.background },
  modalHeader: { flexDirection: 'row', alignItems: 'center', padding: 20, borderBottomWidth: 1, borderBottomColor: Colors.light.border, gap: 12 },
  modalClose: { width: 36, height: 36, borderRadius: 10, backgroundColor: Colors.light.card, justifyContent: 'center', alignItems: 'center' },
  modalTitle: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.light.text, flex: 1, textAlign: 'right' },
  modalContent: { padding: 20, gap: 6 },
  commonBtn: { backgroundColor: Colors.primaryLight, borderRadius: 12, paddingHorizontal: 14, paddingVertical: 12, flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  commonBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.primary, flex: 1, textAlign: 'right' },
  commonList: { backgroundColor: Colors.light.card, borderRadius: 12, overflow: 'hidden', borderWidth: 1, borderColor: Colors.light.border, marginBottom: 8 },
  commonItem: { flexDirection: 'row', alignItems: 'center', gap: 8, padding: 12, borderBottomWidth: 1, borderBottomColor: Colors.light.border },
  commonItemText: { flex: 1, fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.text, textAlign: 'right' },
  commonItemType: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textTertiary },
  modalLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary, textAlign: 'right', marginTop: 8 },
  modalInput: { backgroundColor: Colors.light.card, borderWidth: 1, borderColor: Colors.light.border, borderRadius: 12, paddingHorizontal: 16, paddingVertical: 14, fontFamily: 'Nunito_400Regular', fontSize: 16, color: Colors.light.text, textAlignVertical: 'top' },
  freqRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginVertical: 4 },
  freqBtn: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 10, borderWidth: 1, borderColor: Colors.light.border, backgroundColor: Colors.light.card },
  freqBtnActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  freqBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 13, color: Colors.light.textSecondary },
  freqBtnTextActive: { color: '#fff' },
  typeGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginVertical: 4 },
  typeBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 10, borderWidth: 1, borderColor: Colors.light.border, backgroundColor: Colors.light.card },
  typeBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, color: Colors.light.textSecondary },
  glucoseToggle: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', backgroundColor: Colors.light.card, borderRadius: 12, padding: 14, marginVertical: 4 },
  glucoseToggleLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.text },
  warnBox: { backgroundColor: Colors.dangerLight, borderRadius: 10, padding: 10, flexDirection: 'row', gap: 8, alignItems: 'center' },
  warnBoxText: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.danger, flex: 1, textAlign: 'right' },
  saveBtn: { backgroundColor: Colors.primary, borderRadius: 14, paddingVertical: 16, alignItems: 'center', marginTop: 16 },
  saveBtnText: { fontFamily: 'Nunito_700Bold', fontSize: 17, color: '#fff' },
});
