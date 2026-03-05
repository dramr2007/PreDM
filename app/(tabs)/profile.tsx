import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, Pressable, TextInput,
  Platform, Alert, Modal,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useHealth, PatientProfile } from '@/context/HealthContext';
import Colors from '@/constants/colors';
import * as Haptics from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';

function InfoRow({ icon, label, value, color }: { icon: string; label: string; value: string; color?: string }) {
  return (
    <View style={styles.infoRow}>
      <Ionicons name={icon as any} size={16} color={color || Colors.primary} style={{ marginTop: 1 }} />
      <Text style={styles.infoLabel}>{label}</Text>
      <Text style={styles.infoValue}>{value}</Text>
    </View>
  );
}

function StatBox({ label, value, sub, color }: { label: string; value: string; sub?: string; color: string }) {
  return (
    <View style={[styles.statBox, { borderTopColor: color, borderTopWidth: 3 }]}>
      <Text style={[styles.statValue, { color }]}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
      {sub && <Text style={styles.statSub}>{sub}</Text>}
    </View>
  );
}

function EditProfileModal({ visible, onClose }: { visible: boolean; onClose: () => void }) {
  const { profile, saveProfile } = useHealth();
  const [name, setName] = useState(profile?.name || '');
  const [age, setAge] = useState(profile?.age?.toString() || '');
  const [height, setHeight] = useState(profile?.height?.toString() || '');
  const [weight, setWeight] = useState(profile?.weight?.toString() || '');
  const [waist, setWaist] = useState(profile?.waistCircumference?.toString() || '');
  const [healthRecordId, setHealthRecordId] = useState(profile?.healthRecordId || '');
  const [ministry, setMinistry] = useState(profile?.ministry || '');

  async function save() {
    if (!profile) return;
    const updated: PatientProfile = {
      ...profile,
      name,
      age: parseInt(age) || profile.age,
      height: parseFloat(height) || profile.height,
      weight: parseFloat(weight) || profile.weight,
      waistCircumference: parseFloat(waist) || profile.waistCircumference,
      healthRecordId,
      ministry,
    };
    await saveProfile(updated);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    onClose();
  }

  function Field({ label, value, onChange, keyboardType = 'default', unit }: any) {
    return (
      <View style={{ marginBottom: 14 }}>
        <Text style={styles.fieldLabel}>{label}</Text>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <TextInput
            style={[styles.modalInput, unit ? { flex: 1 } : {}]}
            value={value}
            onChangeText={onChange}
            keyboardType={keyboardType}
            placeholderTextColor={Colors.light.textTertiary}
            textAlign="right"
          />
          {unit && <Text style={styles.unit}>{unit}</Text>}
        </View>
      </View>
    );
  }

  return (
    <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}>
      <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
        <View style={styles.modalHeader}>
          <Pressable onPress={onClose} style={styles.modalClose}>
            <Ionicons name="close" size={22} color={Colors.light.text} />
          </Pressable>
          <Text style={styles.modalTitle}>تعديل الملف الصحي</Text>
        </View>
        <ScrollView contentContainerStyle={{ padding: 20, paddingBottom: 40 }} showsVerticalScrollIndicator={false}>
          <Field label="الاسم" value={name} onChange={setName} />
          <Field label="العمر" value={age} onChange={setAge} keyboardType="number-pad" unit="سنة" />
          <Field label="الطول" value={height} onChange={setHeight} keyboardType="decimal-pad" unit="سم" />
          <Field label="الوزن" value={weight} onChange={setWeight} keyboardType="decimal-pad" unit="كغ" />
          <Field label="محيط الخصر" value={waist} onChange={setWaist} keyboardType="decimal-pad" unit="سم" />
          <Field label="الجهة الصحية" value={ministry} onChange={setMinistry} />
          <Field label="رقم السجل الصحي" value={healthRecordId} onChange={setHealthRecordId} keyboardType="number-pad" />
          <Pressable style={styles.saveBtn} onPress={save}>
            <Text style={styles.saveBtnText}>حفظ التغييرات</Text>
          </Pressable>
        </ScrollView>
      </View>
    </Modal>
  );
}

export default function ProfileScreen() {
  const insets = useSafeAreaInsets();
  const isWeb = Platform.OS === 'web';
  const topPad = isWeb ? 67 : insets.top;
  const bottomPad = isWeb ? 34 : 0;

  const { profile, bmi, riskScore, riskCategory, glucoseReadings, weightReadings, exerciseLogs, medications } = useHealth();
  const [showEdit, setShowEdit] = useState(false);

  if (!profile) return null;

  const genderLabel = { male: 'ذكر', female: 'أنثى', other: 'أخرى' }[profile.gender];
  const activityLabel = { sedentary: 'خامل', low: 'منخفض', moderate: 'متوسط', active: 'نشيط' }[profile.activityLevel];
  const smokingLabel = { never: 'لم يدخن', former: 'سابقاً', current: 'حالياً' }[profile.smokingStatus];
  const ethnicityLabel = { arab: 'عربي', asian: 'آسيوي', african: 'أفريقي', hispanic: 'لاتيني', caucasian: 'قوقازي', other: 'أخرى' }[profile.ethnicity];
  const riskLabel = { low: 'منخفض', moderate: 'متوسط', high: 'مرتفع', 'very-high': 'مرتفع جداً' }[riskCategory];
  const riskColor = { low: Colors.success, moderate: Colors.accent, high: Colors.warning, 'very-high': Colors.danger }[riskCategory];

  const weekExercise = exerciseLogs.filter(e => {
    const diff = (Date.now() - new Date(e.date).getTime()) / (1000 * 60 * 60 * 24);
    return diff <= 7;
  }).reduce((acc, e) => acc + e.minutes, 0);

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: Colors.light.background }}
      contentContainerStyle={{ paddingBottom: bottomPad + 100 }}
      showsVerticalScrollIndicator={false}
    >
      <LinearGradient colors={['#0D9488', '#0F766E']} style={[styles.profileHeader, { paddingTop: topPad + 12 }]}>
        <View style={styles.avatarWrap}>
          <Text style={styles.avatarText}>{profile.name.charAt(0)}</Text>
        </View>
        <Text style={styles.profileName}>{profile.name}</Text>
        <Text style={styles.profileSub}>{profile.age} سنة • {genderLabel}</Text>
        {profile.healthRecordId ? (
          <View style={styles.recordBadge}>
            <Ionicons name="shield-checkmark" size={14} color="#fff" />
            <Text style={styles.recordText}>رقم السجل: {profile.healthRecordId}</Text>
          </View>
        ) : null}
        <Pressable style={styles.editBtn} onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); setShowEdit(true); }}>
          <Ionicons name="pencil" size={16} color="#fff" />
          <Text style={styles.editBtnText}>تعديل</Text>
        </Pressable>
      </LinearGradient>

      <View style={styles.statsRow}>
        <StatBox label="مؤشر الخطر" value={riskScore.toString()} sub={riskLabel} color={riskColor} />
        <StatBox label="BMI" value={bmi.toString()} sub={bmi < 25 ? 'طبيعي' : bmi < 30 ? 'زائد' : 'سمنة'} color={bmi >= 30 ? Colors.danger : bmi >= 25 ? Colors.warning : Colors.success} />
        <StatBox label="قراءات السكر" value={glucoseReadings.length.toString()} color={Colors.primary} />
      </View>

      <View style={styles.padH}>
        <Text style={styles.sectionTitle}>البيانات الأساسية</Text>
        <View style={styles.card}>
          <InfoRow icon="person" label="الاسم" value={profile.name} />
          <InfoRow icon="calendar" label="العمر" value={`${profile.age} سنة`} />
          <InfoRow icon="male-female" label="الجنس" value={genderLabel} />
          <InfoRow icon="card" label="رقم الهوية" value={profile.nationalId || 'غير مدخل'} />
          <InfoRow icon="earth" label="الأصل العرقي" value={ethnicityLabel} />
        </View>

        <Text style={styles.sectionTitle}>القياسات الجسدية</Text>
        <View style={styles.card}>
          <InfoRow icon="resize" label="الطول" value={`${profile.height} سم`} />
          <InfoRow icon="scale" label="الوزن" value={`${profile.weight} كغ`} />
          <InfoRow icon="body" label="محيط الخصر" value={`${profile.waistCircumference} سم`} />
          <InfoRow icon="analytics" label="مؤشر كتلة الجسم" value={bmi.toString()} color={bmi >= 30 ? Colors.danger : Colors.primary} />
        </View>

        <Text style={styles.sectionTitle}>عوامل الخطر</Text>
        <View style={styles.card}>
          <InfoRow icon="people" label="تاريخ عائلي بالسكري" value={profile.familyHistory ? 'نعم' : 'لا'} color={profile.familyHistory ? Colors.warning : Colors.success} />
          <InfoRow icon="heart" label="ضغط الدم المرتفع" value={profile.bloodPressureHigh ? 'نعم' : 'لا'} color={profile.bloodPressureHigh ? Colors.warning : Colors.success} />
          {profile.gender === 'female' && <InfoRow icon="woman" label="سكري الحمل السابق" value={profile.gestationalDiabetes ? 'نعم' : 'لا'} color={profile.gestationalDiabetes ? Colors.warning : Colors.success} />}
          <InfoRow icon="walk" label="مستوى النشاط" value={activityLabel} color={profile.activityLevel === 'active' ? Colors.success : profile.activityLevel === 'moderate' ? Colors.accent : Colors.warning} />
          <InfoRow icon="flame" label="التدخين" value={smokingLabel} color={profile.smokingStatus === 'never' ? Colors.success : Colors.warning} />
        </View>

        <Text style={styles.sectionTitle}>السجل الصحي الإلكتروني</Text>
        <View style={[styles.card, { gap: 0 }]}>
          <View style={styles.recordHeader}>
            <MaterialCommunityIcons name="hospital-building" size={24} color={Colors.primary} />
            <View style={{ flex: 1 }}>
              <Text style={styles.recordMinistry}>{profile.ministry || 'وزارة الصحة'}</Text>
              {profile.healthRecordId ? (
                <Text style={styles.recordId}>رقم السجل: {profile.healthRecordId}</Text>
              ) : (
                <Text style={styles.recordIdEmpty}>لم يتم ربط السجل بعد</Text>
              )}
            </View>
            {profile.healthRecordId ? (
              <View style={styles.connectedBadge}>
                <Ionicons name="checkmark-circle" size={16} color={Colors.success} />
                <Text style={styles.connectedText}>مرتبط</Text>
              </View>
            ) : (
              <Pressable style={styles.connectBtn} onPress={() => setShowEdit(true)}>
                <Text style={styles.connectBtnText}>ربط</Text>
              </Pressable>
            )}
          </View>
          <View style={styles.recordNote}>
            <Ionicons name="shield-checkmark" size={14} color={Colors.primary} />
            <Text style={styles.recordNoteText}>بياناتك محفوظة بشكل آمن على جهازك</Text>
          </View>
        </View>

        <Text style={styles.sectionTitle}>إحصائيات التتبع</Text>
        <View style={styles.card}>
          <InfoRow icon="water" label="قراءات سكر الدم" value={`${glucoseReadings.length} قراءة`} />
          <InfoRow icon="scale" label="قياسات الوزن" value={`${weightReadings.length} قياس`} />
          <InfoRow icon="fitness" label="نشاط هذا الأسبوع" value={`${weekExercise} دقيقة`} color={weekExercise >= 150 ? Colors.success : Colors.warning} />
          <InfoRow icon="medical" label="أدوية نشطة" value={`${medications.filter(m => m.active).length} دواء`} />
        </View>
      </View>
      <EditProfileModal visible={showEdit} onClose={() => setShowEdit(false)} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  profileHeader: { paddingHorizontal: 24, paddingBottom: 28, alignItems: 'center', gap: 8 },
  avatarWrap: { width: 72, height: 72, borderRadius: 36, backgroundColor: 'rgba(255,255,255,0.25)', justifyContent: 'center', alignItems: 'center', marginBottom: 4 },
  avatarText: { fontFamily: 'Nunito_800ExtraBold', fontSize: 28, color: '#fff' },
  profileName: { fontFamily: 'Nunito_800ExtraBold', fontSize: 22, color: '#fff' },
  profileSub: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: 'rgba(255,255,255,0.85)' },
  recordBadge: { flexDirection: 'row', gap: 6, backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: 20, paddingHorizontal: 12, paddingVertical: 4, alignItems: 'center' },
  recordText: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, color: '#fff' },
  editBtn: { flexDirection: 'row', gap: 6, backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, alignItems: 'center', marginTop: 4 },
  editBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: '#fff' },
  statsRow: { flexDirection: 'row', paddingHorizontal: 20, paddingVertical: 16, gap: 10 },
  statBox: { flex: 1, backgroundColor: Colors.light.card, borderRadius: 14, padding: 14, alignItems: 'center', gap: 4, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  statValue: { fontFamily: 'Nunito_800ExtraBold', fontSize: 22 },
  statLabel: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textSecondary, textAlign: 'center' },
  statSub: { fontFamily: 'Nunito_600SemiBold', fontSize: 11, color: Colors.light.textTertiary, textAlign: 'center' },
  padH: { paddingHorizontal: 20 },
  sectionTitle: { fontFamily: 'Nunito_700Bold', fontSize: 16, color: Colors.light.text, textAlign: 'right', marginTop: 16, marginBottom: 10 },
  card: { backgroundColor: Colors.light.card, borderRadius: 14, overflow: 'hidden', shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, shadowOffset: { width: 0, height: 2 }, elevation: 2, marginBottom: 4 },
  infoRow: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 13, paddingHorizontal: 16, borderBottomWidth: 1, borderBottomColor: Colors.light.border },
  infoLabel: { flex: 1, fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary, textAlign: 'right' },
  infoValue: { fontFamily: 'Nunito_700Bold', fontSize: 14, color: Colors.light.text },
  recordHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, padding: 16 },
  recordMinistry: { fontFamily: 'Nunito_700Bold', fontSize: 15, color: Colors.light.text, textAlign: 'right' },
  recordId: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textSecondary, textAlign: 'right' },
  recordIdEmpty: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textTertiary, textAlign: 'right' },
  connectedBadge: { flexDirection: 'row', gap: 4, alignItems: 'center', backgroundColor: Colors.successLight, borderRadius: 10, paddingHorizontal: 8, paddingVertical: 4 },
  connectedText: { fontFamily: 'Nunito_600SemiBold', fontSize: 12, color: Colors.success },
  connectBtn: { backgroundColor: Colors.primary, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 6 },
  connectBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 13, color: '#fff' },
  recordNote: { flexDirection: 'row', gap: 8, alignItems: 'center', paddingHorizontal: 16, paddingVertical: 10, backgroundColor: Colors.primaryLight, borderTopWidth: 1, borderTopColor: Colors.light.border },
  recordNoteText: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.primaryDark },
  modalHeader: { flexDirection: 'row', alignItems: 'center', padding: 20, borderBottomWidth: 1, borderBottomColor: Colors.light.border, gap: 12 },
  modalClose: { width: 36, height: 36, borderRadius: 10, backgroundColor: Colors.light.card, justifyContent: 'center', alignItems: 'center' },
  modalTitle: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.light.text, flex: 1, textAlign: 'right' },
  fieldLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary, marginBottom: 8, textAlign: 'right' },
  modalInput: { backgroundColor: Colors.light.card, borderWidth: 1, borderColor: Colors.light.border, borderRadius: 12, paddingHorizontal: 16, paddingVertical: 14, fontFamily: 'Nunito_400Regular', fontSize: 16, color: Colors.light.text },
  unit: { marginLeft: 10, fontFamily: 'Nunito_600SemiBold', color: Colors.light.textSecondary, fontSize: 14 },
  saveBtn: { backgroundColor: Colors.primary, borderRadius: 14, paddingVertical: 16, alignItems: 'center', marginTop: 16 },
  saveBtnText: { fontFamily: 'Nunito_700Bold', fontSize: 17, color: '#fff' },
});
