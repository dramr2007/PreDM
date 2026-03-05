import React, { createContext, useContext, useState, useEffect, useMemo, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface PatientProfile {
  name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  nationalId: string;
  height: number;
  weight: number;
  waistCircumference: number;
  bloodPressureHigh: boolean;
  familyHistory: boolean;
  gestationalDiabetes: boolean;
  activityLevel: 'sedentary' | 'low' | 'moderate' | 'active';
  smokingStatus: 'never' | 'former' | 'current';
  ethnicity: 'arab' | 'asian' | 'african' | 'hispanic' | 'caucasian' | 'other';
  healthRecordId: string;
  ministry: string;
  onboardingCompleted: boolean;
}

export interface GlucoseReading {
  id: string;
  date: string;
  value: number;
  type: 'fasting' | 'postmeal' | 'a1c' | 'random';
  notes?: string;
}

export interface WeightReading {
  id: string;
  date: string;
  value: number;
  bmi?: number;
}

export interface ExerciseLog {
  id: string;
  date: string;
  minutes: number;
  type: 'walking' | 'running' | 'cycling' | 'swimming' | 'gym' | 'other';
}

export interface BpReading {
  id: string;
  date: string;
  systolic: number;
  diastolic: number;
}

export interface Medication {
  id: string;
  name: string;
  dose: string;
  frequency: string;
  startDate: string;
  type: 'corticosteroid' | 'immunosuppressant' | 'antipsychotic' | 'statin' | 'diuretic' | 'other';
  raisesGlucose: boolean;
  notes?: string;
  active: boolean;
}

export interface HealthAlert {
  id: string;
  date: string;
  type: 'weight_gain' | 'low_exercise' | 'high_glucose' | 'medication_risk' | 'a1c_high';
  message: string;
  severity: 'info' | 'warning' | 'danger';
  read: boolean;
}

interface HealthContextValue {
  profile: PatientProfile | null;
  glucoseReadings: GlucoseReading[];
  weightReadings: WeightReading[];
  exerciseLogs: ExerciseLog[];
  bpReadings: BpReading[];
  medications: Medication[];
  alerts: HealthAlert[];
  riskScore: number;
  riskCategory: 'low' | 'moderate' | 'high' | 'very-high';
  bmi: number;
  isLoading: boolean;
  saveProfile: (p: PatientProfile) => Promise<void>;
  addGlucoseReading: (r: Omit<GlucoseReading, 'id'>) => Promise<void>;
  addWeightReading: (r: Omit<WeightReading, 'id'>) => Promise<void>;
  addExerciseLog: (l: Omit<ExerciseLog, 'id'>) => Promise<void>;
  addBpReading: (r: Omit<BpReading, 'id'>) => Promise<void>;
  addMedication: (m: Omit<Medication, 'id'>) => Promise<void>;
  toggleMedication: (id: string) => Promise<void>;
  deleteMedication: (id: string) => Promise<void>;
  markAlertRead: (id: string) => Promise<void>;
  unreadAlertCount: number;
}

const HealthContext = createContext<HealthContextValue | null>(null);

const genId = () => Date.now().toString() + Math.random().toString(36).substr(2, 9);

const HIGH_GLUCOSE_MEDS = ['corticosteroid', 'antipsychotic', 'immunosuppressant'];

function calcBmi(weight: number, height: number): number {
  if (!height || !weight) return 0;
  const hm = height / 100;
  return parseFloat((weight / (hm * hm)).toFixed(1));
}

function calcRisk(profile: PatientProfile, bmi: number): number {
  let score = 0;
  if (profile.age >= 45 && profile.age < 55) score += 2;
  else if (profile.age >= 55 && profile.age < 65) score += 3;
  else if (profile.age >= 65) score += 4;
  if (bmi >= 25 && bmi < 30) score += 1;
  else if (bmi >= 30 && bmi < 35) score += 3;
  else if (bmi >= 35) score += 4;
  if (profile.familyHistory) score += 3;
  if (profile.bloodPressureHigh) score += 2;
  if (profile.gestationalDiabetes) score += 3;
  if (profile.activityLevel === 'sedentary') score += 2;
  else if (profile.activityLevel === 'low') score += 1;
  if (profile.smokingStatus === 'current') score += 1;
  if (profile.waistCircumference > (profile.gender === 'male' ? 102 : 88)) score += 2;
  if (profile.ethnicity === 'arab' || profile.ethnicity === 'asian') score += 2;
  return Math.min(score, 20);
}

export function HealthProvider({ children }: { children: ReactNode }) {
  const [profile, setProfile] = useState<PatientProfile | null>(null);
  const [glucoseReadings, setGlucoseReadings] = useState<GlucoseReading[]>([]);
  const [weightReadings, setWeightReadings] = useState<WeightReading[]>([]);
  const [exerciseLogs, setExerciseLogs] = useState<ExerciseLog[]>([]);
  const [bpReadings, setBpReadings] = useState<BpReading[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [alerts, setAlerts] = useState<HealthAlert[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const keys = ['profile', 'glucose', 'weight', 'exercise', 'bp', 'medications', 'alerts'];
      const results = await AsyncStorage.multiGet(keys);
      const map: Record<string, string | null> = {};
      results.forEach(([k, v]) => { map[k] = v; });
      if (map.profile) setProfile(JSON.parse(map.profile));
      if (map.glucose) setGlucoseReadings(JSON.parse(map.glucose));
      if (map.weight) setWeightReadings(JSON.parse(map.weight));
      if (map.exercise) setExerciseLogs(JSON.parse(map.exercise));
      if (map.bp) setBpReadings(JSON.parse(map.bp));
      if (map.medications) setMedications(JSON.parse(map.medications));
      if (map.alerts) setAlerts(JSON.parse(map.alerts));
    } catch (e) {
      console.error('Error loading health data', e);
    } finally {
      setIsLoading(false);
    }
  }

  async function saveProfile(p: PatientProfile) {
    setProfile(p);
    await AsyncStorage.setItem('profile', JSON.stringify(p));
  }

  async function addGlucoseReading(r: Omit<GlucoseReading, 'id'>) {
    const newR = { ...r, id: genId() };
    const updated = [newR, ...glucoseReadings];
    setGlucoseReadings(updated);
    await AsyncStorage.setItem('glucose', JSON.stringify(updated));
    checkGlucoseAlerts(newR, updated);
  }

  function checkGlucoseAlerts(newR: GlucoseReading, all: GlucoseReading[]) {
    let triggered = false;
    if (newR.type === 'fasting' && newR.value >= 100) triggered = true;
    if (newR.type === 'postmeal' && newR.value >= 140) triggered = true;
    if (newR.type === 'a1c' && newR.value >= 5.7) triggered = true;
    if (triggered) {
      addAlert({
        date: new Date().toISOString(),
        type: 'high_glucose',
        message: newR.type === 'a1c'
          ? `HbA1c ${newR.value}% - ضمن نطاق ما قبل السكري حسب ADA 2026`
          : `سكر الدم ${newR.value} ${newR.type === 'fasting' ? '(صائم)' : '(بعد الأكل)'} - مستوى تحذيري`,
        severity: newR.value >= (newR.type === 'a1c' ? 6.0 : newR.type === 'fasting' ? 110 : 160) ? 'danger' : 'warning',
        read: false,
      });
    }
  }

  async function addWeightReading(r: Omit<WeightReading, 'id'>) {
    const newR = { ...r, id: genId() };
    const updated = [newR, ...weightReadings];
    setWeightReadings(updated);
    await AsyncStorage.setItem('weight', JSON.stringify(updated));
    if (weightReadings.length > 0) {
      const prev = weightReadings[0].value;
      if (r.value - prev >= 2) {
        addAlert({
          date: new Date().toISOString(),
          type: 'weight_gain',
          message: `زيادة في الوزن ${(r.value - prev).toFixed(1)} كغ منذ آخر قياس`,
          severity: 'warning',
          read: false,
        });
      }
    }
  }

  async function addExerciseLog(l: Omit<ExerciseLog, 'id'>) {
    const newL = { ...l, id: genId() };
    const updated = [newL, ...exerciseLogs];
    setExerciseLogs(updated);
    await AsyncStorage.setItem('exercise', JSON.stringify(updated));
  }

  async function addBpReading(r: Omit<BpReading, 'id'>) {
    const newR = { ...r, id: genId() };
    const updated = [newR, ...bpReadings];
    setBpReadings(updated);
    await AsyncStorage.setItem('bp', JSON.stringify(updated));
  }

  async function addAlert(a: Omit<HealthAlert, 'id'>) {
    const newA = { ...a, id: genId() };
    setAlerts(prev => {
      const updated = [newA, ...prev];
      AsyncStorage.setItem('alerts', JSON.stringify(updated));
      return updated;
    });
  }

  async function addMedication(m: Omit<Medication, 'id'>) {
    const newM = { ...m, id: genId() };
    const updated = [newM, ...medications];
    setMedications(updated);
    await AsyncStorage.setItem('medications', JSON.stringify(updated));
    if (HIGH_GLUCOSE_MEDS.includes(m.type) || m.raisesGlucose) {
      addAlert({
        date: new Date().toISOString(),
        type: 'medication_risk',
        message: `تنبيه: ${m.name} قد يرفع مستوى السكر في الدم - يُنصح بمتابعة أكثر`,
        severity: 'warning',
        read: false,
      });
    }
  }

  async function toggleMedication(id: string) {
    const updated = medications.map(m => m.id === id ? { ...m, active: !m.active } : m);
    setMedications(updated);
    await AsyncStorage.setItem('medications', JSON.stringify(updated));
  }

  async function deleteMedication(id: string) {
    const updated = medications.filter(m => m.id !== id);
    setMedications(updated);
    await AsyncStorage.setItem('medications', JSON.stringify(updated));
  }

  async function markAlertRead(id: string) {
    const updated = alerts.map(a => a.id === id ? { ...a, read: true } : a);
    setAlerts(updated);
    await AsyncStorage.setItem('alerts', JSON.stringify(updated));
  }

  const bmi = useMemo(() => {
    if (!profile) return 0;
    return calcBmi(profile.weight, profile.height);
  }, [profile]);

  const riskScore = useMemo(() => {
    if (!profile) return 0;
    return calcRisk(profile, bmi);
  }, [profile, bmi]);

  const riskCategory = useMemo((): 'low' | 'moderate' | 'high' | 'very-high' => {
    if (riskScore <= 3) return 'low';
    if (riskScore <= 7) return 'moderate';
    if (riskScore <= 12) return 'high';
    return 'very-high';
  }, [riskScore]);

  const unreadAlertCount = useMemo(() => alerts.filter(a => !a.read).length, [alerts]);

  const value = useMemo(() => ({
    profile,
    glucoseReadings,
    weightReadings,
    exerciseLogs,
    bpReadings,
    medications,
    alerts,
    riskScore,
    riskCategory,
    bmi,
    isLoading,
    saveProfile,
    addGlucoseReading,
    addWeightReading,
    addExerciseLog,
    addBpReading,
    addMedication,
    toggleMedication,
    deleteMedication,
    markAlertRead,
    unreadAlertCount,
  }), [profile, glucoseReadings, weightReadings, exerciseLogs, bpReadings, medications, alerts, riskScore, riskCategory, bmi, isLoading, unreadAlertCount]);

  return <HealthContext.Provider value={value}>{children}</HealthContext.Provider>;
}

export function useHealth() {
  const ctx = useContext(HealthContext);
  if (!ctx) throw new Error('useHealth must be used within HealthProvider');
  return ctx;
}
