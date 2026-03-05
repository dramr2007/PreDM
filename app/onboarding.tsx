import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  Pressable,
  Platform,
  KeyboardAvoidingView,
  Dimensions,
  Alert,
} from 'react-native';
import { router } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useHealth, PatientProfile } from '@/context/HealthContext';
import Colors from '@/constants/colors';
import * as Haptics from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

const STEPS = [
  { id: 'welcome', title: '' },
  { id: 'personal', title: 'المعلومات الشخصية' },
  { id: 'measurements', title: 'القياسات الجسدية' },
  { id: 'risk', title: 'عوامل الخطر' },
  { id: 'health_record', title: 'السجل الصحي' },
];

function OptionButton({ label, selected, onPress }: { label: string; selected: boolean; onPress: () => void }) {
  return (
    <Pressable
      style={[styles.optionBtn, selected && styles.optionBtnSelected]}
      onPress={() => { Haptics.selectionAsync(); onPress(); }}
    >
      {selected && <Ionicons name="checkmark-circle" size={16} color={Colors.primary} style={{ marginRight: 6 }} />}
      <Text style={[styles.optionText, selected && styles.optionTextSelected]}>{label}</Text>
    </Pressable>
  );
}

function Field({ label, value, onChangeText, placeholder, keyboardType = 'default', unit }: {
  label: string; value: string; onChangeText: (v: string) => void;
  placeholder?: string; keyboardType?: any; unit?: string;
}) {
  return (
    <View style={styles.fieldWrap}>
      <Text style={styles.fieldLabel}>{label}</Text>
      <View style={styles.inputRow}>
        <TextInput
          style={[styles.input, unit ? { flex: 1 } : {}]}
          value={value}
          onChangeText={onChangeText}
          placeholder={placeholder}
          placeholderTextColor={Colors.light.textTertiary}
          keyboardType={keyboardType}
        />
        {unit && <Text style={styles.unit}>{unit}</Text>}
      </View>
    </View>
  );
}

export default function OnboardingScreen() {
  const insets = useSafeAreaInsets();
  const { saveProfile } = useHealth();
  const [step, setStep] = useState(0);

  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState<'male' | 'female' | 'other'>('male');
  const [nationalId, setNationalId] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [waist, setWaist] = useState('');
  const [familyHistory, setFamilyHistory] = useState(false);
  const [bloodPressureHigh, setBloodPressureHigh] = useState(false);
  const [gestationalDiabetes, setGestationalDiabetes] = useState(false);
  const [activityLevel, setActivityLevel] = useState<'sedentary' | 'low' | 'moderate' | 'active'>('low');
  const [smokingStatus, setSmokingStatus] = useState<'never' | 'former' | 'current'>('never');
  const [ethnicity, setEthnicity] = useState<'arab' | 'asian' | 'african' | 'hispanic' | 'caucasian' | 'other'>('arab');
  const [healthRecordId, setHealthRecordId] = useState('');
  const [ministry, setMinistry] = useState('');

  function nextStep() {
    if (step === 1 && (!name || !age)) {
      Alert.alert('تنبيه', 'يرجى إدخال الاسم والعمر');
      return;
    }
    if (step === 2 && (!height || !weight)) {
      Alert.alert('تنبيه', 'يرجى إدخال الطول والوزن');
      return;
    }
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setStep(s => s + 1);
  }

  async function finish() {
    const profile: PatientProfile = {
      name,
      age: parseInt(age) || 0,
      gender,
      nationalId,
      height: parseFloat(height) || 0,
      weight: parseFloat(weight) || 0,
      waistCircumference: parseFloat(waist) || 0,
      familyHistory,
      bloodPressureHigh,
      gestationalDiabetes,
      activityLevel,
      smokingStatus,
      ethnicity,
      healthRecordId,
      ministry: ministry || 'وزارة الصحة',
      onboardingCompleted: true,
    };
    await saveProfile(profile);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    router.replace('/(tabs)');
  }

  const isWeb = Platform.OS === 'web';
  const topPad = isWeb ? 67 : insets.top;
  const bottomPad = isWeb ? 34 : insets.bottom;

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      {step === 0 ? (
        <LinearGradient colors={['#0D9488', '#0F766E', '#134E4A']} style={[styles.welcomeContainer, { paddingTop: topPad + 20, paddingBottom: bottomPad + 20 }]}>
          <View style={styles.welcomeContent}>
            <View style={styles.welcomeIconWrap}>
              <MaterialCommunityIcons name="heart-circle" size={64} color="#fff" />
            </View>
            <Text style={styles.welcomeTitle}>PreDM</Text>
            <Text style={styles.welcomeSubtitle}>مرشدك الذكي لرصد{'\n'}مرحلة ما قبل السكري</Text>
            <Text style={styles.welcomeDesc}>
              تطبيق متخصص مبني على معايير الجمعية الأمريكية للسكري{'\n'}ADA 2026 لمساعدتك على فهم وإدارة مخاطر السكري
            </Text>
            <View style={styles.featureList}>
              {['تقييم مخاطر دقيق وفق ADA 2026', 'تتبع سكر الدم والوزن', 'تنبيهات الأدوية المؤثرة', 'ربط بالسجل الصحي الإلكتروني'].map(f => (
                <View key={f} style={styles.featureItem}>
                  <Ionicons name="checkmark-circle" size={18} color="#5EEAD4" />
                  <Text style={styles.featureText}>{f}</Text>
                </View>
              ))}
            </View>
          </View>
          <Pressable style={styles.startBtn} onPress={nextStep}>
            <Text style={styles.startBtnText}>ابدأ الآن</Text>
            <Ionicons name="arrow-back" size={20} color={Colors.primary} />
          </Pressable>
        </LinearGradient>
      ) : (
        <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
          <View style={[styles.header, { paddingTop: topPad + 8 }]}>
            <Pressable onPress={() => setStep(s => s - 1)} style={styles.backBtn}>
              <Ionicons name="arrow-forward" size={22} color={Colors.light.text} />
            </Pressable>
            <View style={styles.stepsIndicator}>
              {STEPS.slice(1).map((_, i) => (
                <View key={i} style={[styles.stepDot, i < step ? styles.stepDotActive : i === step - 1 ? styles.stepDotCurrent : {}]} />
              ))}
            </View>
            <View style={{ width: 36 }} />
          </View>
          <ScrollView style={{ flex: 1 }} contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPad + 40 }]} showsVerticalScrollIndicator={false}>
            <Text style={styles.stepTitle}>{STEPS[step].title}</Text>

            {step === 1 && (
              <>
                <Field label="الاسم الكامل" value={name} onChangeText={setName} placeholder="أدخل اسمك" />
                <Field label="العمر" value={age} onChangeText={setAge} placeholder="السن" keyboardType="number-pad" unit="سنة" />
                <Field label="رقم الهوية / الإقامة" value={nationalId} onChangeText={setNationalId} placeholder="10 أرقام" keyboardType="number-pad" />
                <Text style={styles.fieldLabel}>الجنس</Text>
                <View style={styles.optionRow}>
                  <OptionButton label="ذكر" selected={gender === 'male'} onPress={() => setGender('male')} />
                  <OptionButton label="أنثى" selected={gender === 'female'} onPress={() => setGender('female')} />
                </View>
                <Text style={styles.fieldLabel}>الجنسية / الأصل العرقي</Text>
                <View style={styles.optionGrid}>
                  {[['arab','عربي'], ['asian','آسيوي'], ['african','أفريقي'], ['hispanic','لاتيني'], ['caucasian','قوقازي'], ['other','أخرى']].map(([val, lbl]) => (
                    <OptionButton key={val} label={lbl} selected={ethnicity === val} onPress={() => setEthnicity(val as any)} />
                  ))}
                </View>
              </>
            )}

            {step === 2 && (
              <>
                <Field label="الطول" value={height} onChangeText={setHeight} placeholder="170" keyboardType="decimal-pad" unit="سم" />
                <Field label="الوزن" value={weight} onChangeText={setWeight} placeholder="75" keyboardType="decimal-pad" unit="كغ" />
                <Field label="محيط الخصر" value={waist} onChangeText={setWaist} placeholder="90" keyboardType="decimal-pad" unit="سم" />
                <View style={styles.bmiNote}>
                  <Ionicons name="information-circle" size={16} color={Colors.primary} />
                  <Text style={styles.bmiNoteText}>محيط الخصر الطبيعي: أقل من 94 للرجال و80 للنساء</Text>
                </View>
              </>
            )}

            {step === 3 && (
              <>
                <Text style={styles.fieldLabel}>هل لديك تاريخ عائلي بمرض السكري؟</Text>
                <View style={styles.optionRow}>
                  <OptionButton label="نعم" selected={familyHistory} onPress={() => setFamilyHistory(true)} />
                  <OptionButton label="لا" selected={!familyHistory} onPress={() => setFamilyHistory(false)} />
                </View>
                <Text style={styles.fieldLabel}>هل تعاني من ضغط الدم المرتفع؟</Text>
                <View style={styles.optionRow}>
                  <OptionButton label="نعم" selected={bloodPressureHigh} onPress={() => setBloodPressureHigh(true)} />
                  <OptionButton label="لا" selected={!bloodPressureHigh} onPress={() => setBloodPressureHigh(false)} />
                </View>
                {gender === 'female' && (
                  <>
                    <Text style={styles.fieldLabel}>هل عانيت من سكري الحمل؟</Text>
                    <View style={styles.optionRow}>
                      <OptionButton label="نعم" selected={gestationalDiabetes} onPress={() => setGestationalDiabetes(true)} />
                      <OptionButton label="لا" selected={!gestationalDiabetes} onPress={() => setGestationalDiabetes(false)} />
                    </View>
                  </>
                )}
                <Text style={styles.fieldLabel}>مستوى النشاط البدني</Text>
                <View style={styles.optionGrid}>
                  {[['sedentary','خامل'], ['low','منخفض'], ['moderate','متوسط'], ['active','نشيط']].map(([val, lbl]) => (
                    <OptionButton key={val} label={lbl} selected={activityLevel === val} onPress={() => setActivityLevel(val as any)} />
                  ))}
                </View>
                <Text style={styles.fieldLabel}>التدخين</Text>
                <View style={styles.optionGrid}>
                  {[['never','لم أدخن'], ['former','سابقاً'], ['current','حالياً']].map(([val, lbl]) => (
                    <OptionButton key={val} label={lbl} selected={smokingStatus === val} onPress={() => setSmokingStatus(val as any)} />
                  ))}
                </View>
              </>
            )}

            {step === 4 && (
              <>
                <View style={styles.minCard}>
                  <MaterialCommunityIcons name="hospital-building" size={32} color={Colors.primary} />
                  <Text style={styles.minCardText}>يمكنك ربط تطبيق PreDM بسجلك الصحي الإلكتروني لدى وزارة الصحة للاطلاع على نتائجك المخبرية وتاريخك الطبي.</Text>
                </View>
                <Field label="الجهة الصحية / المستشفى" value={ministry} onChangeText={setMinistry} placeholder="مثال: مستشفى الملك فهد" />
                <Field label="رقم السجل الصحي (اختياري)" value={healthRecordId} onChangeText={setHealthRecordId} placeholder="رقم السجل" keyboardType="number-pad" />
                <View style={styles.bmiNote}>
                  <Ionicons name="shield-checkmark" size={16} color={Colors.primary} />
                  <Text style={styles.bmiNoteText}>بياناتك محفوظة محلياً بشكل آمن على جهازك</Text>
                </View>
              </>
            )}
          </ScrollView>
          <View style={[styles.footer, { paddingBottom: bottomPad + 16 }]}>
            <Pressable style={styles.nextBtn} onPress={step === 4 ? finish : nextStep}>
              <Text style={styles.nextBtnText}>{step === 4 ? 'ابدأ رحلتك الصحية' : 'التالي'}</Text>
              {step !== 4 && <Ionicons name="arrow-back" size={18} color="#fff" />}
            </Pressable>
          </View>
        </KeyboardAvoidingView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  welcomeContainer: { flex: 1, justifyContent: 'space-between', paddingHorizontal: 28 },
  welcomeContent: { flex: 1, justifyContent: 'center', alignItems: 'center', gap: 16 },
  welcomeIconWrap: { width: 100, height: 100, borderRadius: 28, backgroundColor: 'rgba(255,255,255,0.15)', justifyContent: 'center', alignItems: 'center' },
  welcomeTitle: { fontSize: 48, fontFamily: 'Nunito_800ExtraBold', color: '#fff', letterSpacing: -1 },
  welcomeSubtitle: { fontSize: 22, fontFamily: 'Nunito_700Bold', color: '#fff', textAlign: 'center', lineHeight: 32 },
  welcomeDesc: { fontSize: 14, fontFamily: 'Nunito_400Regular', color: 'rgba(255,255,255,0.8)', textAlign: 'center', lineHeight: 22 },
  featureList: { gap: 10, alignSelf: 'stretch', marginTop: 8 },
  featureItem: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  featureText: { fontFamily: 'Nunito_600SemiBold', color: '#fff', fontSize: 15 },
  startBtn: { backgroundColor: '#fff', borderRadius: 16, paddingVertical: 16, paddingHorizontal: 32, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 10, marginBottom: 16 },
  startBtnText: { fontFamily: 'Nunito_700Bold', fontSize: 18, color: Colors.primary },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 20, paddingBottom: 12 },
  backBtn: { width: 36, height: 36, justifyContent: 'center', alignItems: 'center' },
  stepsIndicator: { flexDirection: 'row', gap: 6 },
  stepDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: Colors.light.border },
  stepDotActive: { backgroundColor: Colors.primary },
  stepDotCurrent: { backgroundColor: Colors.primary, width: 20 },
  scrollContent: { paddingHorizontal: 24, paddingTop: 8, gap: 4 },
  stepTitle: { fontSize: 26, fontFamily: 'Nunito_800ExtraBold', color: Colors.light.text, marginBottom: 16, textAlign: 'right' },
  fieldWrap: { marginBottom: 14 },
  fieldLabel: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary, marginBottom: 8, textAlign: 'right' },
  inputRow: { flexDirection: 'row', alignItems: 'center' },
  input: { backgroundColor: Colors.light.card, borderWidth: 1, borderColor: Colors.light.border, borderRadius: 12, paddingHorizontal: 16, paddingVertical: 14, fontFamily: 'Nunito_400Regular', fontSize: 16, color: Colors.light.text, textAlign: 'right' },
  unit: { marginLeft: 10, fontFamily: 'Nunito_600SemiBold', color: Colors.light.textSecondary, fontSize: 14 },
  optionRow: { flexDirection: 'row', gap: 10, marginBottom: 14 },
  optionGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 14 },
  optionBtn: { paddingHorizontal: 16, paddingVertical: 10, borderRadius: 10, borderWidth: 1.5, borderColor: Colors.light.border, backgroundColor: Colors.light.card, flexDirection: 'row', alignItems: 'center' },
  optionBtnSelected: { borderColor: Colors.primary, backgroundColor: Colors.primaryLight },
  optionText: { fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary },
  optionTextSelected: { color: Colors.primary },
  bmiNote: { flexDirection: 'row', gap: 8, backgroundColor: Colors.primaryLight, borderRadius: 10, padding: 12, alignItems: 'flex-start', marginTop: 4 },
  bmiNoteText: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.primaryDark, flex: 1, textAlign: 'right', lineHeight: 20 },
  minCard: { backgroundColor: Colors.primaryLight, borderRadius: 14, padding: 16, gap: 10, alignItems: 'center', marginBottom: 16 },
  minCardText: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.primaryDark, textAlign: 'center', lineHeight: 22 },
  footer: { paddingHorizontal: 24, paddingTop: 12, backgroundColor: Colors.light.background, borderTopWidth: 1, borderTopColor: Colors.light.border },
  nextBtn: { backgroundColor: Colors.primary, borderRadius: 16, paddingVertical: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 10 },
  nextBtnText: { fontFamily: 'Nunito_700Bold', fontSize: 17, color: '#fff' },
});
