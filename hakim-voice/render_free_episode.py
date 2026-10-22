#!/usr/bin/env python3
"""Hakim AI metadata-driven free Piper/Pillow/FFmpeg renderer; NOT hardcoded to C0041."""
import sys, json, subprocess, shutil, wave, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features

BASE=Path(__file__).resolve().parent
EPFILE=Path(sys.argv[1])
E=json.loads(EPFILE.read_text(encoding="utf-8"))
ID=E["id"]
OUTPUT=BASE/"output"/ID
OUTPUT.mkdir(parents=True,exist_ok=True)
FF=shutil.which("ffmpeg")
if not FF: raise RuntimeError("ffmpeg is required")
VOICE=BASE/"model/ar_JO-kareem-medium.onnx"
CONF=BASE/"model/ar_JO-kareem-medium.onnx.json"
if not VOICE.exists() or not CONF.exists(): raise RuntimeError("Arabic Piper voice files missing")
if not features.check("raqm"): raise RuntimeError("Arabic RAQM text support required")
FONT="/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf"
BOLD="/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf"
LAT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not Path(FONT).exists(): raise RuntimeError("Noto Arabic font missing")
W,H=720,1280
C={"ink":"#0E2132","dark":"#071725","teal":"#2CE6CC","pale":"#D8EFF4","yellow":"#FFD366","dim":"#AAC9D5","orange":"#FA8E74","blue":"#77CCF5"}
def font(sz,b=False,latin=False): return ImageFont.truetype(LAT if latin else (BOLD if b else FONT),sz)
def ar(d,s,x,y,sz=38,c="#FFFFFF",bold=False):
    d.text((x,y),s,fill=c,font=font(sz,bold),anchor="mm",direction="rtl",language="ar",stroke_width=0)
def en(d,s,x,y,sz=28,c="#2CE6CC",bold=False):
    d.text((x,y),s,fill=c,font=font(sz,bold,True),anchor="mm")
def rect(d,p,fill,r=24,outline=None,w=2):
    d.rounded_rectangle(p,radius=r,fill=fill,outline=outline,width=w)
def robot(d):
    # Simple original geometric Hakim AI pictogram, not a borrowed character
    d.line((360,78,360,98),fill=C["teal"],width=4)
    d.ellipse((354,69,366,81),fill=C["yellow"])
    rect(d,(317,94,403,151),"#164C5E",20,C["teal"],2)
    for x in (342,378): d.ellipse((x-9,113,x+9,131),fill=C["teal"])
    d.arc((340,124,380,146),8,172,fill=C["yellow"],width=3)
def scene(i,seg):
    im=Image.new("RGB",(W,H),C["dark"]);d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H;d.line((0,y,W,y),fill=(int(7+8*t),int(23+19*t),int(37+19*t)))
    d.ellipse((495,-160,870,210),outline="#1B5860",width=5)
    d.ellipse((-300,935,170,1400),outline="#175064",width=5)
    rect(d,(40,32,680,184),"#10384C",26,"#255E65",2)
    en(d,"HAKIM AI",360,58,23,C["teal"],True);robot(d)
    en(d,ID+" • "+str(i+1)+"/"+str(len(E["segments"])),360,171,17,C["dim"])
    ar(d,seg["head"],360,253,43,"#FFFFFF",True)
    en(d,E.get("english","ARTIFICIAL INTELLIGENCE"),360,310,24,C["yellow"],True)
    rect(d,(55,362,665,1010),"#133347",32,"#246076",3)
    v=seg.get("visual","takeaway")
    if v=="question":
        en(d,"AI MODEL",360,470,37,C["blue"],True)
        for x in (200,360,520):
            rect(d,(x-55,562,x+55,705),"#1D6680",20,C["teal"],3)
            for y in (590,623,656):d.line((x-28,y,x+28,y),fill="#CBF4F3",width=6)
        ar(d,"هل يمكن أن يصبح أخف؟",360,853,39,C["yellow"],True)
    elif v=="bits":
        en(d,"FP32",201,467,35,C["blue"],True)
        en(d,"INT8",522,467,35,C["teal"],True)
        for j in range(32):
            x=95+(j%8)*26;y=526+(j//8)*34
            rect(d,(x,y,x+21,y+28),"#3870A3",4)
        for j in range(8):
            x=423+(j%4)*44;y=550+(j//4)*62
            rect(d,(x,y,x+35,y+47),"#1DAF9B",6)
        d.line((332,604,393,604),fill=C["yellow"],width=7)
        d.polygon([(381,587),(406,604),(381,621)],fill=C["yellow"])
        ar(d,"أرقام بدقة أقل",360,862,38,C["yellow"],True)
    elif v=="memory":
        ar(d,"تمثيل الأوزان",360,465,37,"#FFFFFF",True)
        rect(d,(125,557,595,618),"#336185",15)
        rect(d,(125,557,595,618),"#4E91C9",15)
        rect(d,(125,698,595,759),"#204A5A",15)
        rect(d,(125,698,260,759),"#24CCAD",15)
        en(d,"32 bit / weight",360,652,24,C["blue"])
        en(d,"8 bit / weight",360,799,24,C["teal"])
        ar(d,"لا يعني ربع حجم التطبيق كله",360,890,28,C["yellow"],True)
    elif v=="device":
        rect(d,(136,487,318,811),"#143F56",26,C["teal"],5)
        rect(d,(159,537,296,743),"#235C71",13)
        d.ellipse((218,767,237,786),fill=C["yellow"])
        rect(d,(384,526,584,719),"#23546C",18,C["blue"],4)
        for x in (423,459,495,531):
            for y in (555,591,627,663):rect(d,(x,y,x+21,y+21),"#339AAB",4)
        ar(d,"الجهاز يحدد المكسب",360,865,35,C["yellow"],True)
    elif v=="tradeoff":
        ar(d,"حجم النموذج",215,481,29,C["teal"],True)
        ar(d,"جودة الإجابات",518,481,29,C["orange"],True)
        d.line((360,518,360,729),fill="#6CBFCC",width=9)
        d.line((192,577,528,668),fill=C["yellow"],width=13)
        d.ellipse((183,567,202,587),fill=C["teal"])
        d.ellipse((518,658,537,677),fill=C["orange"])
        rect(d,(135,752,585,835),"#25546A",20)
        ar(d,"المهم اختبار النتائج",360,795,34,"#FFFFFF",True)
    elif v=="emailbatch":
        en(d,"1,000 EMAILS",360,471,39,C["blue"],True)
        for j in range(48):
            x=102+(j%8)*64;y=541+(j//8)*53
            rect(d,(x,y,x+47,y+35),C["orange"] if j<1 else "#257E82",7)
        ar(d,"10 مزعجة فقط من كل ألف",360,906,32,C["yellow"],True)
    elif v=="predictnormal":
        for j in range(5):
            x=106+j*104
            rect(d,(x,511,x+77,604),C["orange"] if j==0 else "#23687C",11)
            d.line((x+14,539,x+59,539),fill=C["pale"],width=4)
            d.line((x+14,563,x+48,563),fill=C["pale"],width=4)
        d.line((359,644,359,722),fill=C["yellow"],width=8)
        d.polygon([(344,708),(374,708),(359,739)],fill=C["yellow"])
        rect(d,(150,759,570,860),"#257866",20)
        en(d,"ALL NORMAL",360,808,33,"#FFFFFF",True)
    elif v=="accuracy99":
        en(d,"990 / 1000",360,525,55,C["blue"],True)
        d.line((149,589,575,589),fill=C["teal"],width=5)
        en(d,"= 99%",360,696,77,C["yellow"],True)
        ar(d,"دقة إجمالية مرتفعة",360,849,34,C["pale"],True)
    elif v=="missedspam":
        en(d,"10 SPAM MISSED",360,463,35,C["orange"],True)
        for j in range(10):
            x=144+(j%5)*93;y=559+(j//5)*116
            rect(d,(x,y,x+66,y+82),"#7D3D4C",13,C["orange"],2)
            d.line((x+11,y+20,x+56,y+62),fill="#FFBBBB",width=4)
            d.line((x+56,y+20,x+11,y+62),fill="#FFBBBB",width=4)
        en(d,"RECALL = 0%",360,871,39,C["yellow"],True)
    elif v=="accuracyformula":
        en(d,"ACCURACY",360,470,44,C["blue"],True)
        rect(d,(135,566,585,795),"#1F5670",19)
        en(d,"Correct predictions",360,619,25,C["pale"])
        d.line((185,664,535,664),fill=C["yellow"],width=5)
        en(d,"All predictions",360,715,26,C["pale"])
        ar(d,"قد يخفي إخفاق الفئة النادرة",360,864,28,C["yellow"],True)
    elif v=="accuracymetrics":
        rect(d,(128,476,592,610),"#215E6B",18,C["teal"],2)
        en(d,"RECALL",360,525,33,C["yellow"],True)
        ar(d,"كم حالة إيجابية اكتشفنا؟",360,577,26,C["pale"])
        rect(d,(128,666,592,801),"#215E6B",18,C["teal"],2)
        en(d,"PRECISION",360,713,32,C["yellow"],True)
        ar(d,"كم إنذارًا إيجابيًا صحيح؟",360,765,25,C["pale"])
        ar(d,"لا تحكم من رقم واحد",360,899,32,C["orange"],True)

    elif v=="precisionquestion":
        ar(d,"إنذارات النموذج",360,455,36,C["pale"],True)
        for j in range(10):
            x=135+(j%5)*95;y=525+(j//5)*137
            rect(d,(x,y,x+68,y+94),C["teal"] if j<8 else C["orange"],14)
            d.ellipse((x+28,y+16,x+40,y+29),fill=C["dark"])
            d.line((x+34,y+40,x+34,y+69),fill=C["dark"],width=5)
        ar(d,"هل جميعها صحيحة؟",360,901,34,C["yellow"],True)
    elif v=="precisioncounts":
        en(d,"10 POSITIVE ALERTS",360,461,29,C["pale"],True)
        for j in range(10):
            x=124+(j%5)*99;y=549+(j//5)*132
            rect(d,(x,y,x+78,y+87),"#236D64" if j<8 else "#964A4B",13)
            en(d,"OK" if j<8 else "X",x+39,y+43,29,C["teal"] if j<8 else C["orange"],True)
        ar(d,"٨ صحيحة و٢ خاطئة",360,895,35,C["yellow"],True)
    elif v=="precisionformula":
        en(d,"PRECISION",360,465,39,C["blue"],True)
        rect(d,(119,538,601,783),"#20566A",19)
        en(d,"TRUE POSITIVE",360,593,24,C["pale"],True)
        d.line((179,645,542,645),fill=C["yellow"],width=5)
        en(d,"ALL PREDICTED POSITIVE",360,707,18,C["pale"],True)
        ar(d,"من تنبأنا بأنها إيجابية",360,864,28,C["yellow"],True)
    elif v=="precision80":
        en(d,"8 / (8 + 2)",360,507,49,C["blue"],True)
        d.line((150,599,570,599),fill=C["teal"],width=5)
        en(d,"80%",360,727,98,C["yellow"],True)
        ar(d,"إنذاران خاطئان",360,893,33,C["pale"],True)
    elif v=="precisionmiss":
        ar(d,"إنذارات صحيحة",360,474,31,C["teal"],True)
        for j in range(8):
            x=146+(j%4)*110;y=526+(j//4)*85
            rect(d,(x,y,x+81,y+57),"#278873",11)
        d.line((125,760,595,760),fill=C["orange"],width=4)
        ar(d,"لكن بعض الحالات قد تفوت",360,857,32,C["yellow"],True)
    elif v=="precisionboth":
        rect(d,(97,503,331,763),"#235A6A",20,C["teal"],2)
        rect(d,(390,503,624,763),"#235A6A",20,C["yellow"],2)
        en(d,"PRECISION",214,565,24,C["teal"],True)
        en(d,"RECALL",507,565,28,C["yellow"],True)
        ar(d,"صدق الإنذارات",214,674,24,C["pale"],True)
        ar(d,"اكتشاف الحالات",507,674,24,C["pale"],True)
        ar(d,"قيّم المقياسين معًا",360,889,33,C["yellow"],True)
    elif v=="recallquestion":
        ar(d,"أمامك عشر رسائل مزعجة",360,461,32,C["pale"],True)
        for j in range(10):
            x=125+(j%5)*97;y=543+(j//5)*133
            rect(d,(x,y,x+73,y+89),"#257E82" if j<8 else "#964A4B",13)
            d.line((x+10,y+27,x+62,y+27),fill=C["pale"],width=4)
            d.line((x+10,y+53,x+50,y+53),fill=C["pale"],width=4)
        ar(d,"كم رسالة اكتشف النموذج؟",360,882,30,C["yellow"],True)
    elif v=="recallcounts":
        en(d,"10 ACTUAL POSITIVES",360,465,30,C["pale"],True)
        for j in range(10):
            x=126+(j%5)*97;y=546+(j//5)*139
            good=j<8
            rect(d,(x,y,x+74,y+92),"#236D64" if good else "#964A4B",13)
            en(d,"OK" if good else "X",x+37,y+47,30,C["teal"] if good else C["orange"],True)
        ar(d,"اكتشف ٨ وفاتته ٢",360,897,35,C["yellow"],True)
    elif v=="recallformula":
        en(d,"RECALL",360,465,46,C["blue"],True)
        rect(d,(114,536,606,796),"#20566A",18)
        en(d,"TRUE POSITIVES FOUND",360,597,22,C["pale"],True)
        d.line((169,655,550,655),fill=C["yellow"],width=5)
        en(d,"ALL ACTUAL POSITIVES",360,715,21,C["pale"],True)
        ar(d,"من بين الحالات الحقيقية",360,877,30,C["yellow"],True)
    elif v=="recall80":
        en(d,"8 / (8 + 2)",360,512,46,C["blue"],True)
        d.line((154,604,567,604),fill=C["teal"],width=5)
        en(d,"80%",360,735,97,C["yellow"],True)
        ar(d,"لم يكتشف حالتين",360,892,33,C["pale"],True)
    elif v=="recalltradeoff":
        rect(d,(105,482,615,661),"#20566A",24,C["teal"],2)
        en(d,"RECALL",360,539,37,C["yellow"],True)
        ar(d,"من الحالات الحقيقية",360,609,30,C["pale"])
        rect(d,(105,712,615,865),"#20566A",24,C["orange"],2)
        en(d,"PRECISION",360,761,34,C["teal"],True)
        ar(d,"من الإنذارات الإيجابية",360,827,28,C["pale"])
    elif v=="recalltakeaway":
        for j,(eng,cap) in enumerate([("RECALL","كم حالة اكتشفنا؟"),("PRECISION","كم إنذارًا صحيح؟")]):
            y=484+j*177
            rect(d,(104,y,616,y+140),"#235A6A",21,C["teal"] if j==0 else C["yellow"],2)
            en(d,eng,360,y+45,33,C["yellow"],True)
            ar(d,cap,360,y+100,29,C["pale"],True)
        ar(d,"راقب النوعين من الأخطاء",360,904,30,C["orange"],True)
    elif v=="specificityquestion":
        en(d,"100 ACTUAL NEGATIVES",360,454,28,C["pale"],True)
        for j in range(100):
            x=116+(j%10)*49;y=520+(j//10)*33
            rect(d,(x,y,x+34,y+25),"#247E79" if j<90 else "#99544F",5)
        ar(d,"كم حالة سليمة عرفها؟",360,921,31,C["yellow"],True)
    elif v=="specificitycounts":
        en(d,"90 TRUE NEGATIVES",360,465,28,C["teal"],True)
        for j in range(90):
            x=117+(j%10)*49;y=531+(j//10)*31
            rect(d,(x,y,x+34,y+23),"#2A927F",5)
        rect(d,(126,838,596,900),"#964A4B",16)
        ar(d,"عشرة إنذارات خاطئة",360,868,29,C["pale"],True)
    elif v=="specificityformula":
        en(d,"SPECIFICITY",360,468,39,C["blue"],True)
        rect(d,(111,540,609,797),"#20566A",19)
        en(d,"TRUE NEGATIVES",360,605,27,C["pale"],True)
        d.line((178,654,548,654),fill=C["yellow"],width=5)
        en(d,"ALL ACTUAL NEGATIVES",360,721,23,C["pale"],True)
        ar(d,"السلبيات الصحيحة من الكل",360,880,27,C["yellow"])
    elif v=="specificity90":
        en(d,"90 / (90 + 10)",360,513,38,C["blue"],True)
        d.line((146,610,573,610),fill=C["teal"],width=5)
        en(d,"90%",360,743,103,C["yellow"],True)
        ar(d,"حالة سليمة لم تُنذر",360,898,29,C["pale"])
    elif v=="specificitycompare":
        rect(d,(100,499,331,787),"#20566A",21,C["teal"],2)
        rect(d,(390,499,621,787),"#20566A",21,C["yellow"],2)
        en(d,"SPECIFICITY",215,567,23,C["teal"],True)
        en(d,"RECALL",506,567,31,C["yellow"],True)
        ar(d,"السلبيات",215,678,28,C["pale"],True)
        ar(d,"الإيجابيات",506,678,28,C["pale"],True)
        ar(d,"كلاهما مهم",360,904,34,C["yellow"],True)
    elif v=="specificitytakeaway":
        en(d,"THRESHOLD",360,474,31,C["blue"],True)
        d.line((130,644,594,644),fill=C["pale"],width=10)
        for xx in [166,235,304,373,442,511,580]:
            d.ellipse((xx-9,635,xx+9,653),fill=C["teal"])
        d.ellipse((405,625,443,663),fill=C["yellow"])
        ar(d,"عتبة القرار تغيّر الأخطاء",360,750,30,C["pale"],True)
        rect(d,(136,813,585,902),"#20566A",19)
        ar(d,"اختبر الحساسية والنوعية",360,858,30,C["yellow"],True)
    elif v=="falsepositivequestion":
        rect(d,(177,480,543,775),"#23566E",28,C["teal"],4)
        d.polygon([(200,520),(360,655),(520,520)],outline=C["pale"],width=7)
        en(d,"NORMAL EMAIL",360,721,27,C["pale"],True)
        d.ellipse((481,447,562,528),fill=C["orange"])
        en(d,"!",521,487,40,C["dark"],True)
        ar(d,"لماذا ظهر إنذار؟",360,887,35,C["yellow"],True)
    elif v=="falsepositiveprediction":
        rect(d,(99,503,321,802),"#235A6A",24,C["teal"],2)
        rect(d,(398,503,620,802),"#5B3C49",24,C["orange"],2)
        en(d,"ACTUAL",211,553,31,C["teal"],True)
        en(d,"PREDICTED",509,553,26,C["orange"],True)
        en(d,"NORMAL",211,677,26,C["pale"],True)
        en(d,"SPAM",509,677,31,C["pale"],True)
        ar(d,"الحقيقة ليست التوقع",360,910,31,C["yellow"],True)
    elif v=="falsepositivematrix":
        en(d,"CONFUSION MATRIX",360,472,28,C["blue"],True)
        for j,(x,y,code) in enumerate([(133,533,"TP"),(376,533,"FP"),(133,711,"FN"),(376,711,"TN")]):
            rect(d,(x,y,x+212,y+142),"#934E4C" if code=="FP" else "#20566A",18,C["orange"] if code=="FP" else "#2B7585",3)
            en(d,code,x+105,y+72,49,C["yellow"] if code=="FP" else C["pale"],True)
        ar(d,"إنذار إيجابي لكنه خاطئ",360,902,27,C["yellow"],True)
    elif v=="falsepositiveimpact":
        rect(d,(129,482,590,631),"#235A6A",20,C["teal"],2)
        ar(d,"رسالة سليمة",360,544,37,C["pale"],True)
        d.line((359,654,359,727),fill=C["yellow"],width=7)
        d.polygon([(346,717),(372,717),(359,742)],fill=C["yellow"])
        rect(d,(129,763,590,881),"#894B50",20,C["orange"],2)
        ar(d,"ذهبت بالخطأ للمزعج",360,820,29,C["pale"],True)
    elif v=="falsepositivethreshold":
        en(d,"DECISION THRESHOLD",360,470,28,C["blue"],True)
        d.line((140,640,579,640),fill=C["pale"],width=12)
        for xx in (166,248,330,412,494,572):d.ellipse((xx-9,631,xx+9,649),fill=C["teal"])
        d.ellipse((371,620,411,660),fill=C["yellow"])
        ar(d,"تغيير العتبة يغير الأخطاء",360,781,30,C["pale"],True)
        ar(d,"لا توجد عتبة مثالية دائمًا",360,871,27,C["yellow"],True)
    elif v=="falsepositivetakeaway":
        rect(d,(108,488,612,636),"#20566A",19,C["teal"],2)
        en(d,"FALSE POSITIVE",360,540,30,C["orange"],True)
        ar(d,"إنذار لحالة غير موجودة",360,597,28,C["pale"])
        rect(d,(108,695,612,857),"#20566A",19,C["yellow"],2)
        ar(d,"تحقق من النتيجة والأثر",360,751,30,C["pale"],True)
        ar(d,"وقس معدل الإنذارات الخاطئة",360,819,25,C["yellow"])
    elif v=="fnquestion":
        en(d,"FALSE NEGATIVE",360,456,36,C["blue"],True)
        for j in range(9):
            x=148+(j%3)*151;y=553+(j//3)*113
            d.polygon([(x,y+65),(x+40,y),(x+82,y+65)],fill=C["teal"] if j<8 else C["orange"])
        ar(d,"هل كشف كل المثلثات؟",360,908,35,C["yellow"],True)
    elif v=="fnactual":
        rect(d,(99,489,324,815),"#20566A",22,C["teal"],3)
        rect(d,(393,489,622,815),"#20566A",22,C["orange"],3)
        en(d,"REALITY",210,550,29,C["teal"],True)
        en(d,"AI OUTPUT",508,550,27,C["orange"],True)
        d.polygon([(164,739),(211,635),(258,739)],fill=C["teal"])
        en(d,"NONE",507,688,35,C["orange"],True)
        ar(d,"الموجود غير المكتشف",360,902,31,C["yellow"],True)
    elif v=="fnmissed":
        en(d,"10 ACTUAL TRIANGLES",360,464,27,C["pale"],True)
        for j in range(10):
            x=122+(j%5)*98;y=550+(j//5)*135
            d.polygon([(x,y+82),(x+42,y),(x+84,y+82)],fill="#278873" if j<8 else "#965051")
            if j>=8:
                d.line((x+8,y+9,x+75,y+80),fill=C["yellow"],width=4)
                d.line((x+74,y+9,x+8,y+80),fill=C["yellow"],width=4)
        ar(d,"اكتشف ٨ وفاته ٢",360,907,35,C["yellow"],True)
    elif v=="fnmatrix":
        en(d,"CONFUSION MATRIX",360,463,28,C["blue"],True)
        for x,y,code in [(132,530,"TP"),(380,530,"FP"),(132,704,"FN"),(380,704,"TN")]:
            color="#915052" if code=="FN" else "#20566A"
            rect(d,(x,y,x+205,y+142),color,19,C["orange"] if code=="FN" else C["teal"],3)
            en(d,code,x+101,y+70,51,C["yellow"] if code=="FN" else C["pale"],True)
        ar(d,"FN حالة موجودة لم تُكتشف",360,905,26,C["yellow"],True)
    elif v=="fnrecall":
        en(d,"RECALL",360,476,37,C["blue"],True)
        rect(d,(120,539,600,808),"#20566A",24)
        en(d,"TP / (TP + FN)",360,615,36,C["pale"],True)
        d.line((177,677,545,677),fill=C["yellow"],width=5)
        en(d,"8 / 10 = 80%",360,748,43,C["teal"],True)
        ar(d,"الفائت يُنقص الاسترجاع",360,896,30,C["yellow"],True)
    elif v=="fntakeaway":
        rect(d,(102,498,621,656),"#20566A",20,C["orange"],3)
        en(d,"NO ALERT",360,554,38,C["orange"],True)
        ar(d,"ليس دليلًا قاطعًا على الغياب",360,621,27,C["pale"])
        rect(d,(102,717,621,864),"#20566A",20,C["teal"],3)
        ar(d,"قارن التوقع بالمرجع",360,767,31,C["pale"],True)
        ar(d,"وافحص الحالات التي فاتت",360,828,29,C["yellow"],True)
    elif v=="cmquestion":
        en(d,"CONFUSION MATRIX",360,448,29,C["blue"],True)
        for x,y,code in [(136,523,"TP"),(381,523,"FN"),(136,718,"FP"),(381,718,"TN")]:
            rect(d,(x,y,x+205,y+161),"#26566D",20,C["teal"],3)
            en(d,code,x+101,y+78,45,C["yellow"],True)
        ar(d,"أربع خانات للفهم",360,920,32,C["pale"],True)
    elif v=="cmaxes":
        en(d,"PREDICTED",360,468,29,C["blue"],True)
        en(d,"POSITIVE",240,524,25,C["teal"],True)
        en(d,"NEGATIVE",495,524,23,C["orange"],True)
        for x,y,code in [(135,560,"TP"),(380,560,"FN"),(135,728,"FP"),(380,728,"TN")]:
            rect(d,(x,y,x+208,y+137),"#245970",18,C["teal"],2)
            en(d,code,x+103,y+66,47,C["yellow"],True)
        ar(d,"أعلى: واقع إيجابي، أسفل: سلبي",360,931,25,C["pale"])
    elif v=="cmcorrect":
        en(d,"CORRECT PREDICTIONS",360,454,26,C["teal"],True)
        for x,y,code in [(132,532,"TP"),(378,532,"FN"),(132,708,"FP"),(378,708,"TN")]:
            good=code in ("TP","TN")
            rect(d,(x,y,x+213,y+147),"#267D69" if good else "#24485C",20,C["teal"] if good else "#416375",3)
            en(d,code,x+105,y+71,49,C["yellow"] if good else C["pale"],True)
        ar(d,"TP و TN توقعان صحيحان",360,925,31,C["yellow"],True)
    elif v=="cmerrors":
        en(d,"MISCLASSIFICATIONS",360,455,29,C["orange"],True)
        for x,y,code in [(132,532,"TP"),(378,532,"FN"),(132,708,"FP"),(378,708,"TN")]:
            wrong=code in ("FP","FN")
            rect(d,(x,y,x+213,y+147),"#8B4650" if wrong else "#24485C",20,C["orange"] if wrong else "#416375",3)
            en(d,code,x+105,y+71,49,C["yellow"] if wrong else C["pale"],True)
        ar(d,"FP و FN نوعا الخطأ",360,922,33,C["yellow"],True)
    elif v=="cmnumbers":
        en(d,"EXAMPLE: 20 CASES",360,455,29,C["blue"],True)
        for x,y,code,val in [(132,528,"TP","8"),(378,528,"FN","2"),(132,706,"FP","3"),(378,706,"TN","7")]:
            rect(d,(x,y,x+213,y+151),"#20566A",19,C["teal"],3)
            en(d,code,x+105,y+42,24,C["pale"],True)
            en(d,val,x+105,y+107,53,C["yellow"],True)
        en(d,"(8 + 7) / 20 = 75%",360,934,26,C["teal"],True)
    elif v=="cmtakeaway":
        rect(d,(105,491,614,633),"#20566A",21,C["teal"],3)
        en(d,"STEP 1",360,543,28,C["yellow"],True)
        ar(d,"اقرأ المحاور والفئات",360,597,31,C["pale"],True)
        rect(d,(105,697,614,842),"#20566A",21,C["orange"],3)
        en(d,"STEP 2",360,748,28,C["yellow"],True)
        ar(d,"افحص الأخطاء الصحيحة والفائتة",360,803,26,C["pale"],True)
        ar(d,"لا تحفظ مواضع الخانات فقط",360,921,27,C["yellow"])
    else:
        for j,(cap,eng) in enumerate([("الجودة","QUALITY"),("الذاكرة","MEMORY"),("السرعة","LATENCY")]):
            y=462+j*152
            rect(d,(116,y,601,y+121),"#21576B",19,C["teal"] if j==0 else "#347489",2)
            ar(d,cap,360,y+43,37,C["yellow"],True)
            en(d,eng,360,y+90,19,C["pale"],True)
    sub=seg.get("sub","")
    if sub.isascii(): en(d,sub,360,1067,27,C["teal"])
    else: ar(d,sub,360,1067,29,C["teal"])
    d.line((59,1151,660,1151),fill="#1A6571",width=2)
    en(d,r"Dr\Amr kamel kahlil ahmed",360,1203,20,C["dim"])
    file=OUTPUT/("scene_%02d.png"%i);im.save(file);return file

def run(cmd,stdin=None):
    r=subprocess.run(cmd, input=stdin, text=(stdin is not None),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode: raise RuntimeError("Failed: "+" ".join(map(str,cmd[:4]))+"\n"+r.stderr.decode(errors="replace")[-2000:] if isinstance(r.stderr,bytes) else r.stderr[-2000:])
    return r

durations=[];wav_files=[]
for i,seg in enumerate(E["segments"]):
    raw=OUTPUT/("audio_%02d_raw.wav"%i)
    wav=OUTPUT/("audio_%02d.wav"%i)
    run(["piper","--model",str(VOICE),"--config",str(CONF),"--output_file",str(raw)],stdin=seg["text"]+"\n")
    run([FF,"-y","-loglevel","error","-i",str(raw),"-filter:a","atempo=1.13,loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ac", "1","-ar","22050","-c:a","pcm_s16le",str(wav)])
    with wave.open(str(wav),"rb") as f: dur=f.getnframes()/f.getframerate()
    if dur<1: raise RuntimeError("Unexpected short audio in segment "+str(i))
    durations.append(dur); wav_files.append(wav)
    scene(i,seg)
af=OUTPUT/"audio.ffconcat"
vf=OUTPUT/"video.ffconcat"
af.write_text("ffconcat version 1.0\n"+"".join("file '"+str(x)+"'\n" for x in wav_files),encoding="utf8")
vf.write_text("ffconcat version 1.0\n"+"".join("file '"+str(OUTPUT/('scene_%02d.png'%i))+"'\n"+"duration %.5f\n"%d for i,d in enumerate(durations))+
    "file '"+str(OUTPUT/('scene_%02d.png'%(len(durations)-1)))+"'\n",encoding="utf8")
full=OUTPUT/"full.wav"
run([FF,"-y","-loglevel","error","-safe","0","-f","concat","-i",str(af),"-ar","22050","-ac","1","-c:a","pcm_s16le",str(full)])
with wave.open(str(full),"rb") as f: full_duration=f.getnframes()/f.getframerate()
if full_duration>120: raise RuntimeError("Video too long")
video=OUTPUT/(ID+"-FREE-MALE.mp4")
run([FF,"-y","-loglevel","error","-safe","0","-f","concat","-i",str(vf),
     "-i",str(full),"-vf","fps=30,format=yuv420p","-r","30","-c:v","libx264","-preset","fast","-crf","23",
     "-c:a","aac","-b:a","128k","-movflags","+faststart","-t",str(full_duration),"-shortest",str(video)])
report={"id":ID,"duration_s":round(full_duration,2),"segment_durations_s":[round(x,2) for x in durations],
 "video":str(video),"bytes":video.stat().st_size,"voice":"Piper ar_JO-kareem-medium, atempo=1.13",
 "caption":E.get("caption",""),"references":[E.get("reference","")]}
(OUTPUT/"production_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(report,ensure_ascii=False))
