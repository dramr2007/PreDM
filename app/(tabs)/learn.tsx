import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, Pressable, TextInput, Platform,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import Colors from '@/constants/colors';
import * as Haptics from 'expo-haptics';

const EDUCATION = [
  {
    id: 'what',
    icon: 'information-circle',
    title: 'ما هو ما قبل السكري؟',
    color: Colors.primary,
    content: `ما قبل السكري (Prediabetes) هو حالة طبية يكون فيها مستوى سكر الدم أعلى من الطبيعي لكنه لم يصل بعد إلى مستوى السكري الكامل.\n\n📌 وفق ADA 2026:\n• سكر صائم 100-125 mg/dL (IFG)\n• سكر ساعتين 140-199 mg/dL (IGT)\n• HbA1c 5.7-6.4%\n\nالخبر السار: مع التدخل المبكر، يمكن إرجاع السكر للطبيعي في 58% من الحالات.`,
  },
  {
    id: 'risk',
    icon: 'warning',
    title: 'عوامل الخطر',
    color: Colors.warning,
    content: `عوامل الخطر الرئيسية وفق ADA 2026:\n\n🔴 عوامل غير قابلة للتعديل:\n• العمر 45 سنة أو أكثر\n• التاريخ العائلي بالسكري\n• الجنسية (العرب، الآسيويون أعلى خطراً)\n• سكري الحمل السابق\n\n🟡 عوامل قابلة للتعديل:\n• زيادة الوزن والسمنة (BMI ≥25)\n• قلة النشاط البدني\n• ضغط الدم المرتفع\n• ارتفاع الكوليسترول\n• التدخين`,
  },
  {
    id: 'exercise',
    icon: 'fitness',
    title: 'الرياضة والحركة',
    color: Colors.success,
    content: `التوصيات الرسمية لما قبل السكري:\n\n🏃 150 دقيقة أسبوعياً:\n• المشي السريع، السباحة، الدراجة\n• تمارين متوسطة الشدة\n• موزعة على 5 أيام على الأقل\n\n💪 تمارين المقاومة:\n• مرتين أسبوعياً على الأقل\n• تزيد حساسية الإنسولين\n\n✅ تأثير مباشر:\n• كل 10 دقائق تمشي = انخفاض 8% في خطر السكري\n• الحركة بعد الأكل مباشرة تخفض ارتفاع السكر`,
  },
  {
    id: 'diet',
    icon: 'restaurant',
    title: 'التغذية والغذاء الصحي',
    color: Colors.accent,
    content: `مبادئ التغذية لما قبل السكري:\n\n🥗 الأولويات:\n• تقليل الكربوهيدرات المكررة (أرز أبيض، خبز أبيض، سكر)\n• زيادة الألياف (خضروات، بقوليات، حبوب كاملة)\n• البروتينات الخالية (دجاج، سمك، بيض)\n• الدهون الصحية (زيت زيتون، أفوكادو، مكسرات)\n\n🚫 تجنب:\n• المشروبات السكرية والعصائر\n• الوجبات السريعة\n• الحلويات والمخبوزات\n• الأطعمة المصنعة\n\n⏰ توقيت الوجبات:\n• 3 وجبات رئيسية منتظمة\n• تجنب تخطي الإفطار\n• وجبة خفيفة صحية عند الجوع`,
  },
  {
    id: 'medications',
    icon: 'medical',
    title: 'الأدوية وما قبل السكري',
    color: Colors.danger,
    content: `بعض الأدوية ترفع مستوى السكر:\n\n⚠️ كورتيكوستيرويدات:\n• بريدنيزون، ديكساميثازون، هيدروكورتيزون\n• تسبب ارتفاعاً حاداً في السكر\n• تزيد مقاومة الإنسولين\n\n⚠️ مضادات الذهان:\n• أولانزابين، كلوزابين\n• تزيد الوزن وتؤثر على السكر\n\n⚠️ مثبطات المناعة:\n• سيكلوسبورين، تاكروليموس\n• تستدعي متابعة السكر\n\n✅ ماذا تفعل؟\n• أخبر طبيبك بأنك في مرحلة ما قبل السكري\n• راقب السكر أكثر عند بدء أي دواء جديد\n• لا توقف الدواء بدون استشارة`,
  },
  {
    id: 'prevention',
    icon: 'shield-checkmark',
    title: 'الوقاية وبرنامج DPP',
    color: Colors.primary,
    content: `برنامج الوقاية من السكري (DPP) المعتمد من ADA:\n\n📊 النتائج المثبتة:\n• تقليل 58% من خطر التحول لسكري\n• في كبار السن: تقليل 71%\n\n🎯 الأهداف:\n• خسارة 7% من وزن الجسم\n• 150 دقيقة تمرين أسبوعياً\n\n💊 متى يبدأ الدواء؟\n• الميتفورمين قد يُوصف لبعض الحالات\n• خاصة من BMI ≥35 أو عمر <60\n• بقرار الطبيب فقط\n\n🔍 المتابعة:\n• فحص HbA1c كل 6-12 شهر\n• زيارة دورية للطبيب`,
  },
];

const FOOD_ITEMS = [
  { name: 'خبز أبيض', carbs: 15, serving: '1 شريحة (30غ)', gi: 'مرتفع', color: Colors.danger },
  { name: 'أرز أبيض', carbs: 45, serving: 'كوب مطبوخ (180غ)', gi: 'مرتفع', color: Colors.danger },
  { name: 'تمر', carbs: 18, serving: '3 حبات (30غ)', gi: 'متوسط', color: Colors.warning },
  { name: 'برتقال', carbs: 15, serving: 'حبة متوسطة', gi: 'منخفض', color: Colors.success },
  { name: 'خبز قمح كامل', carbs: 12, serving: '1 شريحة (30غ)', gi: 'منخفض', color: Colors.success },
  { name: 'عدس مطبوخ', carbs: 20, serving: 'نصف كوب', gi: 'منخفض', color: Colors.success },
  { name: 'حليب كامل', carbs: 12, serving: 'كوب (240مل)', gi: 'منخفض', color: Colors.success },
  { name: 'عصير تفاح', carbs: 28, serving: 'كوب (240مل)', gi: 'مرتفع', color: Colors.danger },
  { name: 'موز', carbs: 27, serving: 'حبة متوسطة', gi: 'متوسط', color: Colors.warning },
  { name: 'طماطم', carbs: 4, serving: 'حبة متوسطة', gi: 'منخفض', color: Colors.success },
];

function ExpandCard({ item }: { item: typeof EDUCATION[0] }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <Pressable style={[styles.eduCard, { borderLeftColor: item.color }]} onPress={() => { Haptics.selectionAsync(); setExpanded(e => !e); }}>
      <View style={styles.eduHeader}>
        <Ionicons name={item.icon as any} size={20} color={item.color} />
        <Text style={styles.eduTitle}>{item.title}</Text>
        <Ionicons name={expanded ? 'chevron-up' : 'chevron-down'} size={18} color={Colors.light.textTertiary} />
      </View>
      {expanded && <Text style={styles.eduContent}>{item.content}</Text>}
    </Pressable>
  );
}

function CarbCalculator() {
  const [grams, setGrams] = useState('');
  const carbs = grams ? parseFloat(grams) * 0.5 : null;
  const portions = carbs ? (carbs / 15).toFixed(1) : null;

  return (
    <View style={styles.calcCard}>
      <View style={styles.calcHeader}>
        <MaterialCommunityIcons name="calculator" size={20} color={Colors.accent} />
        <Text style={styles.calcTitle}>حاسبة الكربوهيدرات</Text>
      </View>
      <Text style={styles.calcDesc}>أدخل كمية الطعام بالغرام لحساب الكربوهيدرات التقريبية</Text>
      <TextInput
        style={styles.calcInput}
        value={grams}
        onChangeText={setGrams}
        keyboardType="decimal-pad"
        placeholder="عدد الغرامات"
        placeholderTextColor={Colors.light.textTertiary}
        textAlign="right"
      />
      {carbs !== null && (
        <View style={styles.calcResult}>
          <View style={styles.calcResultItem}>
            <Text style={styles.calcResultValue}>{carbs.toFixed(0)}غ</Text>
            <Text style={styles.calcResultLabel}>كربوهيدرات</Text>
          </View>
          <View style={styles.calcDivider} />
          <View style={styles.calcResultItem}>
            <Text style={styles.calcResultValue}>{portions}</Text>
            <Text style={styles.calcResultLabel}>حصة (15غ)</Text>
          </View>
          <View style={styles.calcDivider} />
          <View style={styles.calcResultItem}>
            <Text style={styles.calcResultValue}>{(parseFloat(grams) * 4).toFixed(0)}</Text>
            <Text style={styles.calcResultLabel}>سعرة حرارية</Text>
          </View>
        </View>
      )}
      <Text style={styles.calcNote}>ملاحظة: الحساب تقريبي. استشر أخصائي تغذية للحمية الدقيقة</Text>
    </View>
  );
}

export default function LearnScreen() {
  const insets = useSafeAreaInsets();
  const isWeb = Platform.OS === 'web';
  const topPad = isWeb ? 67 : insets.top;
  const bottomPad = isWeb ? 34 : 0;

  const [activeSection, setActiveSection] = useState<'edu' | 'carb' | 'food'>('edu');

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      <View style={[styles.header, { paddingTop: topPad + 8 }]}>
        <Text style={styles.screenTitle}>التوعية الصحية</Text>
      </View>
      <View style={styles.tabs}>
        <Pressable style={[styles.tabBtn, activeSection === 'edu' && styles.tabBtnActive]} onPress={() => { Haptics.selectionAsync(); setActiveSection('edu'); }}>
          <Text style={[styles.tabBtnText, activeSection === 'edu' && styles.tabBtnTextActive]}>التثقيف</Text>
        </Pressable>
        <Pressable style={[styles.tabBtn, activeSection === 'carb' && styles.tabBtnActive]} onPress={() => { Haptics.selectionAsync(); setActiveSection('carb'); }}>
          <Text style={[styles.tabBtnText, activeSection === 'carb' && styles.tabBtnTextActive]}>الكارب</Text>
        </Pressable>
        <Pressable style={[styles.tabBtn, activeSection === 'food' && styles.tabBtnActive]} onPress={() => { Haptics.selectionAsync(); setActiveSection('food'); }}>
          <Text style={[styles.tabBtnText, activeSection === 'food' && styles.tabBtnTextActive]}>الأطعمة</Text>
        </Pressable>
      </View>
      <ScrollView contentContainerStyle={[styles.content, { paddingBottom: bottomPad + 100 }]} showsVerticalScrollIndicator={false}>
        {activeSection === 'edu' && (
          <>
            <Text style={styles.sectionNote}>معلومات مبنية على توصيات ADA 2026</Text>
            {EDUCATION.map(item => <ExpandCard key={item.id} item={item} />)}
          </>
        )}
        {activeSection === 'carb' && (
          <>
            <CarbCalculator />
            <View style={styles.portionGuide}>
              <Text style={styles.portionTitle}>دليل الحصص الغذائية</Text>
              {[
                { label: 'حصة كربوهيدرات', value: '15 غرام', icon: 'grain' },
                { label: 'الهدف اليومي (ما قبل السكري)', value: '130-180 غ', icon: 'target' },
                { label: 'وجبة رئيسية', value: '30-45 غ', icon: 'food' },
                { label: 'وجبة خفيفة', value: '15-20 غ', icon: 'food-apple' },
              ].map(item => (
                <View key={item.label} style={styles.portionRow}>
                  <MaterialCommunityIcons name={item.icon as any} size={18} color={Colors.accent} />
                  <Text style={styles.portionLabel}>{item.label}</Text>
                  <Text style={styles.portionValue}>{item.value}</Text>
                </View>
              ))}
            </View>
          </>
        )}
        {activeSection === 'food' && (
          <>
            <Text style={styles.sectionNote}>الكربوهيدرات في الأطعمة الشائعة</Text>
            <View style={styles.legend}>
              <View style={styles.legendItem}><View style={[styles.legendDot, { backgroundColor: Colors.success }]} /><Text style={styles.legendText}>GI منخفض</Text></View>
              <View style={styles.legendItem}><View style={[styles.legendDot, { backgroundColor: Colors.warning }]} /><Text style={styles.legendText}>GI متوسط</Text></View>
              <View style={styles.legendItem}><View style={[styles.legendDot, { backgroundColor: Colors.danger }]} /><Text style={styles.legendText}>GI مرتفع</Text></View>
            </View>
            {FOOD_ITEMS.map(item => (
              <View key={item.name} style={styles.foodRow}>
                <View style={[styles.foodGiDot, { backgroundColor: item.color }]} />
                <View style={{ flex: 1 }}>
                  <Text style={styles.foodName}>{item.name}</Text>
                  <Text style={styles.foodServing}>{item.serving}</Text>
                </View>
                <Text style={[styles.foodCarbs, { color: item.color }]}>{item.carbs}غ</Text>
              </View>
            ))}
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: 24, paddingBottom: 12, backgroundColor: Colors.light.background },
  screenTitle: { fontFamily: 'Nunito_800ExtraBold', fontSize: 26, color: Colors.light.text },
  tabs: { flexDirection: 'row', paddingHorizontal: 20, gap: 8, paddingBottom: 12, backgroundColor: Colors.light.background },
  tabBtn: { flex: 1, paddingVertical: 8, borderRadius: 10, backgroundColor: Colors.light.card, borderWidth: 1, borderColor: Colors.light.border, alignItems: 'center' },
  tabBtnActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  tabBtnText: { fontFamily: 'Nunito_600SemiBold', fontSize: 13, color: Colors.light.textSecondary },
  tabBtnTextActive: { color: '#fff' },
  content: { paddingHorizontal: 20, paddingTop: 4, gap: 0 },
  sectionNote: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textTertiary, textAlign: 'right', marginBottom: 12 },
  eduCard: { backgroundColor: Colors.light.card, borderRadius: 14, padding: 16, marginBottom: 10, borderLeftWidth: 4, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  eduHeader: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  eduTitle: { flex: 1, fontFamily: 'Nunito_700Bold', fontSize: 15, color: Colors.light.text, textAlign: 'right' },
  eduContent: { fontFamily: 'Nunito_400Regular', fontSize: 14, color: Colors.light.textSecondary, lineHeight: 24, marginTop: 12, textAlign: 'right' },
  calcCard: { backgroundColor: Colors.light.card, borderRadius: 16, padding: 18, marginBottom: 16, shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 6, shadowOffset: { width: 0, height: 2 }, elevation: 2 },
  calcHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  calcTitle: { fontFamily: 'Nunito_700Bold', fontSize: 16, color: Colors.light.text },
  calcDesc: { fontFamily: 'Nunito_400Regular', fontSize: 13, color: Colors.light.textSecondary, textAlign: 'right', marginBottom: 12, lineHeight: 20 },
  calcInput: { backgroundColor: Colors.light.background, borderWidth: 1, borderColor: Colors.light.border, borderRadius: 12, paddingHorizontal: 16, paddingVertical: 14, fontFamily: 'Nunito_400Regular', fontSize: 18, color: Colors.light.text, marginBottom: 12 },
  calcResult: { flexDirection: 'row', backgroundColor: Colors.accentLight, borderRadius: 12, padding: 14, marginBottom: 10 },
  calcResultItem: { flex: 1, alignItems: 'center', gap: 4 },
  calcResultValue: { fontFamily: 'Nunito_800ExtraBold', fontSize: 22, color: Colors.light.text },
  calcResultLabel: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textSecondary },
  calcDivider: { width: 1, backgroundColor: Colors.light.border, marginHorizontal: 8 },
  calcNote: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textTertiary, textAlign: 'right' },
  portionGuide: { backgroundColor: Colors.light.card, borderRadius: 16, padding: 18, gap: 0 },
  portionTitle: { fontFamily: 'Nunito_700Bold', fontSize: 16, color: Colors.light.text, textAlign: 'right', marginBottom: 12 },
  portionRow: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: Colors.light.border },
  portionLabel: { flex: 1, fontFamily: 'Nunito_600SemiBold', fontSize: 14, color: Colors.light.textSecondary, textAlign: 'right' },
  portionValue: { fontFamily: 'Nunito_700Bold', fontSize: 14, color: Colors.accent },
  legend: { flexDirection: 'row', gap: 16, marginBottom: 12, justifyContent: 'flex-end' },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  legendDot: { width: 10, height: 10, borderRadius: 5 },
  legendText: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textSecondary },
  foodRow: { backgroundColor: Colors.light.card, borderRadius: 12, padding: 14, flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 8 },
  foodGiDot: { width: 12, height: 12, borderRadius: 6 },
  foodName: { fontFamily: 'Nunito_700Bold', fontSize: 15, color: Colors.light.text, textAlign: 'right' },
  foodServing: { fontFamily: 'Nunito_400Regular', fontSize: 12, color: Colors.light.textTertiary, textAlign: 'right' },
  foodCarbs: { fontFamily: 'Nunito_800ExtraBold', fontSize: 18 },
});
