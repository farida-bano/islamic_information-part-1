import streamlit as st
import datetime
import json
import random
import os
from PIL import Image

# --- Helper Functions (Added/Modified for better structure) ---

def get_accurate_hijri_date():
    """
    NOTE: For live accurate Hijri date, you must use a library 
    like 'hijri-converter' or an external API. 
    For now, this function returns a fixed date (Oct 18, 2025 = 18 Jumada al-Thani 1446 AH)
    You should run: pip install hijri-converter and update the function.
    """
    # Placeholder for live functionality:
    # from hijri_converter import Gregorian
    # today = datetime.date.today()
    # hijri_date = Gregorian(today.year, today.month, today.day).to_hijri()
    # return f"{hijri_date.day} {hijri_date.get_month_name(lang='ur')}, {hijri_date.year} ہجری"
    
    return "18 جمادی الثانی, 1446 ہجری"

def get_current_islamic_month():
    """Get current Islamic month - Placeholder"""
    return "جمادی الثانی"

def get_prayer_times(city="Karachi"):
    """Get prayer times for different cities - Fixed data for example"""
    prayer_times_data = {
        "Karachi": {
            "فجر": "05:15 AM",
            "طلوع آفتاب": "06:45 AM", 
            "ظہر": "12:30 PM",
            "عصر": "04:00 PM",
            "مغرب": "06:45 PM",
            "عشاء": "08:15 PM"
        },
        "Lahore": {
            "فجر": "04:45 AM",
            "طلوع آفتاب": "06:15 AM",
            "ظہر": "12:15 PM",
            "عصر": "03:45 PM",
            "مغرب": "06:30 PM",
            "عشاء": "08:00 PM"
        },
        "Islamabad": {
            "فجر": "04:30 AM",
            "طلوع آفتاب": "06:00 AM",
            "ظہر": "12:10 PM",
            "عصر": "03:40 PM",
            "مغرب": "06:25 PM",
            "عشاء": "07:55 PM"
        },
        "Peshawar": {
            "فجر": "04:35 AM",
            "طلوع آفتاب": "06:05 AM",
            "ظہر": "12:20 PM",
            "عصر": "03:50 PM",
            "مغرب": "06:35 PM",
            "عشاء": "08:05 PM"
        },
        "Quetta": {
            "فجر": "05:00 AM",
            "طلوع آفتاب": "06:30 AM",
            "ظہر": "12:40 PM",
            "عصر": "04:10 PM",
            "مغرب": "07:00 PM",
            "عشاء": "08:30 PM"
        }
    }
    
    return prayer_times_data.get(city, prayer_times_data["Karachi"])

def get_zawal_time(dhuhr_time):
    """Calculate Zawal time (midday when sun is at zenith)"""
    try:
        # Convert Urdu time names to English for parsing if necessary, but using the existing structure:
        # We need the Dhuhr time key, which is "ظہر" in the dictionary, but the function input expects the time string.
        dhuhr_dt = datetime.datetime.strptime(dhuhr_time, "%I:%M %p")
        # Zawal time is typically a few minutes before Dhuhr. Let's use 5 minutes.
        zawal_dt = dhuhr_dt - datetime.timedelta(minutes=5)
        return zawal_dt.strftime("%I:%M %p")
    except Exception as e:
        # st.error(f"Error calculating Zawal: {e}") # for debugging
        return "11:45 AM" # Fallback time

def load_islamic_images():
    """Load Islamic images from local folder"""
    images = {}
    image_folder = "islamic"  # Folder name where images are stored
    
    # Check if folder exists
    if not os.path.exists(image_folder):
        st.warning(f"📁 '{image_folder}' فولڈر نہیں ملا۔ براہ کرم چیک کریں کہ فولڈر موجود ہے۔")
        return images
    
    # Define image mappings
    image_files = {
        "masjid_haram": "101.jpg",
        "masjid_nabwi": "102.jpg", 
        "masjid_aqsa": "103.jpg",
        "fateh_makkah": "104.jpg"
    }
    
    # Load images
    for image_name, filename in image_files.items():
        image_path = os.path.join(image_folder, filename)
        if os.path.exists(image_path):
            try:
                images[image_name] = Image.open(image_path)
            except Exception as e:
                st.warning(f"تصویر لوڈ نہیں ہو سکی {filename}: {e}")
        else:
            st.warning(f"📄 فائل نہیں ملی: {image_path}")
    
    return images

# --- Islamic Data (No changes needed, data is comprehensive) ---
HADITHS = [
    {"arabic": "إنما الأعمال بالنيات", "urdu": "اعمال کا دارومدار نیتوں پر ہے", "reference": "بخاری"},
    {"arabic": "من حسن إسلام المرء تركه ما لا يعنيه", "urdu": "آدمی کے اسلام کے اچھا ہونے کی علامت یہ ہے کہ وہ بیکار باتوں کو چھوڑ دے", "reference": "ترمذی"},
    {"arabic": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه", "urdu": "تم میں سے کوئی شخص اس وقت تک مومن نہیں ہوسکتا جب تک اپنے بھائی کے لیے وہی پسند نہ کرے جو اپنے لیے پسند کرتا ہے", "reference": "بخاری"},
    {"arabic": "الكلمة الطيبة صدقة", "urdu": "اچھی بات بھی صدقہ ہے", "reference": "بخاری"},
    {"arabic": "اتق الله حيثما كنت", "urdu": "جہاں کہیں بھی ہو اللہ سے ڈرو", "reference": "ترمذی"},
    {"arabic": "الطهور شطر الإيمان", "urdu": "پاکیزگی آدھا ایمان ہے", "reference": "مسلم"},
]

QURAN_VERSES = [
    {"arabic": "إِنَّ مَعَ الْعُسْرِ يُسْرًا", "urdu": "بے شک مشکل کے ساتھ آسانی ہے", "surah": "الشرح", "verse": "6"},
    {"arabic": "وَإِنَّ اللَّهَ مَعَ الصَّابِرِينَ", "urdu": "اور بے شک اللہ صبر کرنے والوں کے ساتھ ہے", "surah": "البقرة", "verse": "153"},
    {"arabic": "رَبِّ زِدْنِي عِلْمًا", "urdu": "اے میرے رب، میرے علم میں اضافہ فرما", "surah": "طہ", "verse": "114"},
    {"arabic": "إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ وَيُحِبُّ الْمُتَطَهِّرِينَ", "urdu": "بے شک اللہ توبہ کرنے والوں اور پاک رہنے والوں کو پسند فرماتا ہے", "surah": "البقرة", "verse": "222"},
    {"arabic": "قُلْ هُوَ اللَّهُ أَحَدٌ", "urdu": "کہو وہ اللہ ایک ہے", "surah": "الاخلاص", "verse": "1"},
    {"arabic": "لَا إِلَٰهَ إِلَّا اللَّهُ", "urdu": "اللہ کے سوا کوئی معبود نہیں", "surah": "الصافات", "verse": "35"},
]

KIDS_SECTION = {
    "stories": [
        {"title": "حضرت ابراہیم علیہ السلام کی کہانی", "content": "حضرت ابراہیم علیہ السلام نے اللہ کو پانے کے لیے بہت کوشش کی۔ وہ سورج، چاند اور ستاروں کو پوجتے ہوئے لوگوں کو سمجھاتے تھے کہ یہ سب اللہ کی بنائی ہوئی مخلوق ہیں۔ انہوں نے بتوں کو توڑا اور لوگوں کو توحید کی دعوت دی۔"},
        {"title": "حضرت یوسف علیہ السلام کی کہانی", "content": "حضرت یوسف علیہ السلام کو ان کے بھائیوں نے کنویں میں ڈال دیا تھا۔ پھر وہ مصر پہنچے اور بادشاہ کے خوابوں کی تعبیر بتا کر مصر کے خزانے کے وزیر بن گئے۔ آخرکار ان کے بھائی ان کے پاس آئے اور سب مل گئے۔"},
        {"title": "ہاتھی والوں کی کہانی", "content": "ایک بادشاہ جس کا نام ابرہہ تھا، اس نے کعبہ کو گرانے کے لیے ہاتھیوں کی فوج بھیجی۔ اللہ نے چھوٹے چھوٹے پرندے بھیجے جنہوں نے پتھر برسائے اور ابرہہ کی فوج تباہ ہو گئی۔"},
    ],
    "duas": [
        {"arabic": "رَبِّ زِدْنِي عِلْمًا", "urdu": "اے میرے رب، میرے علم میں اضافہ فرما", "source": "سورۃ طہ - آیت 114"},
        {"arabic": "رَبِّ اشْرَحْ لِي صَدْرِي", "urdu": "اے میرے رب، میرے سینے کو کشادہ فرما", "source": "سورۃ طہ - آیت 25"},
        {"arabic": "رَبِّ أَعُوذُ بِكَ مِنْ هَمَزَاتِ الشَّيَاطِينِ", "urdu": "اے میرے رب، میں شیطانوں کے وسوسوں سے تیری پناہ مانگتا ہوں", "source": "سورۃ المؤمنون - آیت 97"},
        {"arabic": "اَللّٰهُمَّ اِنِّیْ اَعُوْذُ بِکَ مِنْ عَذَابِ الْقَبْرِ", "urdu": "اے اللہ میں قبر کے عذاب سے تیری پناہ مانگتا ہوں", "source": "صحیح مسلم"},
    ]
}

TAUHEED_SECTION = {
    "definition": {
        "title": "توحید - اسلام کی بنیاد",
        "description": "توحید کا مطلب ہے اللہ تعالیٰ کو ایک ماننا، اس کے ساتھ کسی کو شریک نہ کرنا۔ یہ اسلام کی سب سے اہم بنیاد ہے۔",
        "importance": "توحید پورے دین کی بنیاد ہے۔ نبی کریم ﷺ نے سب سے پہلے لوگوں کو توحید کی دعوت دی۔"
    },
    "types": {
        "rububiyyah": {
            "title": "توحید الربوبیت",
            "description": "اللہ کو رب کے طور پر ایک ماننا",
            "points": [
                "اللہ ہی خالق ہے",
                "اللہ ہی رازق ہے", 
                "اللہ ہی زندگی اور موت دینے والا ہے",
                "اللہ ہی تمام کائنات کا مالک ہے",
                "اللہ ہی ہر چیز کا انتظام کرنے والا ہے"
            ]
        },
        "uluhiyyah": {
            "title": "توحید الالوہیت",
            "description": "اللہ کی عبادت میں کسی کو شریک نہ کرنا",
            "points": [
                "صرف اللہ کی عبادت کرنا",
                "صرف اللہ سے دعا مانگنا",
                "صرف اللہ سے مدد طلب کرنا",
                "صرف اللہ کے آئے ہوئے قانون پر چلنا",
                "صرف اللہ کے لیے نذر و نیاز کرنا"
            ]
        },
        "asma_was_sifat": {
            "title": "توحید الاسماء والصفات",
            "description": "اللہ کے ناموں اور صفات میں اسے یکتا ماننا",
            "points": [
                "اللہ کے ناموں میں اسے یکتا ماننا",
                "اللہ کی صفات میں اسے یکتا ماننا",
                "اللہ کی صفات میں مشابہت نہ کرنا",
                "اللہ کے ناموں اور صفات کی توقیر کرنا",
                "اللہ کی صفات کو بغیر کیفیات کے ماننا"
            ]
        }
    },
    "benefits": [
        "اللہ کی محبت حاصل ہوتی ہے",
        "دل میں اطمینان پیدا ہوتی ہے",
        "گناہوں سے معافی ملتی ہے",
        "جنت میں داخلہ ملتا ہے",
        "خوف و غم سے نجات ملتی ہے",
        "عملوں میں برکت ہوتی ہے"
    ],
    "kids_learning": [
        "کلمہ طیبہ: لا الہ الا اللہ محمد رسول اللہ",
        "اللہ کی وحدانیت کی کہانیاں پڑھیں",
        "توحید کے بارے میں سوالات پوچھیں",
        "توحید سے متعلق کارٹونز دیکھیں",
        "توحید کی مشق کریں (صرف اللہ سے دعا مانگنا)"
    ],
    "quran_verses": [
        {"arabic": "قُلْ هُوَ اللَّهُ أَحَدٌ", "urdu": "کہو وہ اللہ ایک ہے", "surah": "الاخلاص", "verse": "1"},
        {"arabic": "وَإِلَٰهُكُمْ إِلَٰهٌ وَاحِدٌ", "urdu": "اور تمہارا معبود ایک ہی معبود ہے", "surah": "البقرة", "verse": "163"},
        {"arabic": "لَا إِلَٰهَ إِلَّا أَنَا فَاعْبُدُونِ", "urdu": "میرے سوا کوئی معبود نہیں، پس تم میری عبادت کرو", "surah": "الانبیاء", "verse": "25"}
    ]
}

ISLAMIC_PILLARS = {
    "salah": {
        "title": "نماز - دین کا ستون",
        "description": "نماز اللہ سے بات چیت کا ذریعہ ہے۔ یہ دن میں 5 وقت فرض ہے۔",
        "times": [
            "فجر: صبح صادق سے سورج نکلنے سے پہلے",
            "ظہر: دوپہر ڈھلنے کے بعد",
            "عصر: سایہ ہر چیز سے دوگنا ہونے تک",
            "مغرب: سورج ڈوبنے کے بعد",
            "عشاء: شفق غائب ہونے سے صبح صادق تک"
        ],
        "benefits": [
            "اللہ کا قرب حاصل ہوتا ہے",
            "دل پاکیزہ ہوتا ہے",
            "برائیوں سے بچاؤ ہوتا ہے",
            "دن کی ترتیب بنتی ہے",
            "صبر کی عادت پڑتی ہے"
        ],
        "kids_practice": [
            "چھوٹی چھوٹی نمازیں پڑھنا سیکھیں",
            "وضو کا طریقہ سیکھیں",
            "نماز کی سورتیں یاد کریں",
            "نماز کے قواعد سیکھیں",
            "خاندان کے ساتھ نماز پڑھیں"
        ],
        "importance": "نماز اسلام کا دوسرا رکن ہے۔ ہر مسلمان پر دن میں 5 وقت فرض ہے۔ قیامت میں سب سے پہلے نماز کا حساب ہوگا۔"
    },
    "fasting": {
        "title": "روزہ - صبر کی تربیت",
        "description": "صبح صادق سے لے کر سورج ڈوبنے تک کھانے پینے اور بری باتوں سے رکنا۔",
        "types": [
            "رمضان کے روزے: فرض",
            "نفلی روزے: سنت",
            "قضا روزے: چھوٹے ہوئے روزے",
            "کفارے کے روزے: گناہوں کے لیے"
        ],
        "conditions": [
            "بچوں پر بلوغت کے بعد فرض ہیں",
            "بیمار اور مسافر کے لیے رعایت ہے",
            "حائضہ عورت کے لیے رعایت ہے"
        ],
        "benefits": [
            "صبر کی عادت پڑتی ہے",
            "غریبوں کی مشکلات کا احساس ہوتا ہے",
            "نفس پر قابو پاتے ہیں",
            "صحت کے لیے فائدہ مند ہے",
            "گناہوں کی معافی ہوتی ہے"
        ],
        "kids_tips": [
            "چھوٹے روزے رکھیں (نصف دن)",
            "رمضان میں کچھ روزے رکھیں",
            "سحری و افطار میں شامل ہوں",
            "روزہ کی برکات کے بارے میں سیکھیں"
        ]
    },
    "zakat": {
        "title": "زکواۃ - مال کی پاکیزگی",
        "description": "ہر سال اپنے مال کا 2.5% غریبوں کو دینا۔",
        "conditions": [
            "عاقل و بالغ مسلمان پر",
            "صاحب نصاب ہو (ساڑھے سات تولہ سونا یا ساڑھے باون تولہ چاندی کا مالک ہو)",
            "مال پر پورا سال گزر چکا ہو"
        ],
        "recipients": [
            "غریب اور مسکین",
            "زکواۃ وصول کرنے والے",
            "اسلام قبول کرنے والے",
            "قرض دار",
            "مسافر"
        ],
        "benefits": [
            "مال پاک ہوتا ہے",
            "غریبوں کی مدد ہوتی ہے",
            "معاشرے سے غربت ختم ہوتی ہے",
            "اللہ کی رضا ملتی ہے",
            "مال میں برکت ہوتی ہے"
        ],
        "kids_practice": [
            "اپنی جیب خرچی سے کچھ پیسے غریبوں کو دیں",
            "صدقہ دینے کی عادت ڈالیں",
            "زکواۃ کی اہمیت سیکھیں",
            "غریبوں کی مدد کرنا سیکھیں"
        ]
    },
    "hajj": {
        "title": "حج - زندگی کی سب سے بڑی عبادت",
        "description": "زندگی میں ایک بار مکہ مکرمہ جا کر اللہ کے گھر کی زیارت کرنا۔",
        "conditions": [
            "عاقل و بالغ مسلمان پر",
            "صحت مند ہو",
            "راستہ محفوظ ہو",
            "گھر کے اخراجات کے علاوہ ضروری رقم ہو"
        ],
        "steps": [
            "احرام: خاص لباس پہننا",
            "طواف: کعبہ کے گرد سات چکر لگانا",
            "سعی: صفا اور مروہ کے درمیان سات چکر لگانا",
            "عرفات: 9 ذوالحجہ کو عرفات میں ٹھہرنا",
            "رمی جمرات: شیطان کو پتھر مارنا"
        ],
        "benefits": [
            "گناہ معاف ہوتے ہیں",
            "مسلمانوں کی بھائی چارگی بڑھتی ہے",
            "اللہ کا قرب حاصل ہوتا ہے",
            "دنیا بھر کے مسلمانوں سے ملاقات ہوتی ہے",
            "ایمان تازہ ہوتا ہے"
        ],
        "kids_learning": [
            "حج کی کہانیاں پڑھیں",
            "حج کے طریقے سیکھیں",
            "کعبہ کی تصاویر دیکھیں",
            "حج کی ویڈیوز دیکھیں"
        ]
    },
    "jihad": {
        "title": "جہاد - دین کی سربلندی کی جدوجہد",
        "description": "جہاد کا مطلب ہے اللہ کی راہ میں کوشش کرنا۔ یہ مختلف شکلوں میں ہوتا ہے۔",
        "types": [
            "جہاد بالنفس: نفس کے خلاف جدوجہد",
            "جہاد بالمال: مال خرچ کرنا",
            "جہاد باللسان: زبان سے حق کی تبلیغ",
            "جہاد بالید: ہاتھ سے برائی روکنا",
            "جہاد بالسيف: دفاعی جنگ"
        ],
        "conditions": [
            "مسلمان حکمران کی اجازت سے",
            "صرف دفاعی مقاصد کے لیے",
            "عوام کو نقصان نہ پہنچانا",
            "معاہدوں کی پاسداری کرنا"
        ],
        "benefits": [
            "اللہ کی رضا حاصل ہوتی ہے",
            "دین کی سربلندی ہوتی ہے",
            "مظلوموں کی مدد ہوتی ہے",
            "ایمان مضبوط ہوتا ہے",
            "شہادت کا درجہ ملتا ہے"
        ],
        "misconceptions": [
            "جہاد صرف جنگ نہیں ہے",
            "جہاد دہشت گردی نہیں ہے",
            "جہاد میں عورتوں، بچوں اور بوڑھوں کو نقصان نہیں پہنچایا جا سکتا",
            "جہاد صرف مسلمانوں کے خلاف نہیں ہے"
        ],
        "kids_learning": [
            "جہاد کے صحیح معنی سیکھیں",
            "اپنے نفس کے خلاف جہاد کریں",
            "برائیوں کے خلاف آواز اٹھائیں",
            "دین کی تبلیغ کریں"
        ]
    }
}

TAHARAT_SECTION = {
    "wudu": {
        "farz": [
            "چہرہ دھونا (منہ کے بالوں سے لے کر ٹھوڑی تک اور ایک کان سے دوسرے کان تک)",
            "دونوں ہاتھ کہنیوں سمیت دھونا",
            "سر کا مسح کرنا (چوتھائی سر پر مسح کرنا فرض ہے)",
            "دونوں پاؤں ٹخنوں سمیت دھونا"
        ],
        "sunnat": [
            "وضو شروع میں بسم اللہ پڑھنا",
            "تین بار کلی کرنا",
            "تین بار ناک میں پانی ڈالنا", 
            "داڑھی کا خلال کرنا",
            "ہاتھ پاؤں تین بار دھونا",
            "مسلسل وضو کرنا (ایک عضو خشک ہونے سے پہلے دوسرا دھونا)"
        ],
        "mustahab": [
            "وضو قبلہ رخ ہو کر کرنا",
            "کسی جگہ بیٹھ کر وضو کرنا",
            "دانتوں کا خلال کرنا",
            "وضو کے بعد کلمہ شہادت پڑھنا"
        ],
        "makruh": [
            "پانی ضائع کرنا",
            "بلا ضرورت بات چیت کرنا",
            "تین سے زیادہ بار دھونا",
            "چہرہ دھوتے وقت آنکھیں بند کرنا"
        ]
    },
    "ghusal": {
        "farz": [
            "کلی کرنا (منہ میں پانی پہنچانا)",
            "ناک میں پانی ڈالنا (نرم ہڈی تک)",
            "سارے بدن پر پانی بہانا (بال، ناخن اور جلد کا کوئی حصہ خشک نہ رہے)"
        ],
        "sunnat": [
            "غسل شروع میں بسم اللہ پڑھنا",
            "ہاتھ دھونا",
            "پہلے وضو کرنا",
            "پورے بدن پر تین بار پانی ڈالنا",
            "پہلے دائیں طرف پھر بائیں طرف پانی ڈالنا"
        ],
        "mustahab": [
            "غسل قبلہ رخ ہو کر کرنا",
            "کسی جگہ بیٹھ کر غسل کرنا",
            "غسل کے بعد نئے کپڑے پہننا"
        ],
        "makruh": [
            "غسل میں بلا ضرورت بات چیت کرنا",
            "پانی ضائع کرنا",
            "کھلے آسمان تلے غسل کرنا"
        ]
    },
    "conditions": {
        "wudu_breaks": [
            "پیشاب یا پاخانہ کا آنا",
            "ہوا کا خارج ہونا",
            "نیند آنا (اگر ٹیک لگا کر سویا ہو)",
            "بے ہوشی طاری ہونا",
            "قے آنا (بھر منہ)",
            "نماز میں قہقہہ لگنا"
        ],
        "ghusal_required": [
            "جنابت (احتلام یا جماع کے بعد)",
            "حیض (ماہواری) ختم ہونے پر",
            "نفاس (بچے کی پیدائش کے بعد خون) ختم ہونے پر"
        ]
    }
}

# --- Main Streamlit App ---

def main():
    # Page configuration
    st.set_page_config(
        page_title="اسلامی معلومات کا مرکز",
        page_icon="🕌",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load Islamic images
    islamic_images = load_islamic_images()

    # Custom CSS for better styling and font import
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Jameel+Noori+Nastaleeq:wght@400;700&display=swap');
        
        .main-header {
            font-size: 2.5rem;
            color: #2E86AB;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
            font-family: 'Jameel Noori Nastaleeq', 'Arial', sans-serif;
        }
        .section-header {
            font-size: 1.8rem;
            color: #A23B72;
            margin: 1rem 0;
            font-weight: bold;
            font-family: 'Jameel Noori Nastaleeq', 'Arial', sans-serif;
        }
        .arabic-text {
            font-size: 1.6rem;
            text-align: right;
            direction: rtl;
            font-family: 'Noto Naskh Arabic', 'Traditional Arabic', serif;
            line-height: 2;
        }
        .urdu-text {
            font-size: 1.3rem;
            text-align: right;
            direction: rtl;
            font-family: 'Jameel Noori Nastaleeq', 'Arial', serif;
            line-height: 2;
        }
        .highlight-box {
            background-color: #F8F9FA;
            padding: 1.5rem;
            border-radius: 10px;
            border-right: 5px solid #2E86AB;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .prayer-time {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem;
        }
        .date-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem;
        }
        .taharat-box {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 0.5rem;
        }
        .tauheed-box {
            background: linear-gradient(135deg, #ff6b6b 0%, #ffa8a8 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 0.5rem;
            text-align: center;
        }
        .kids-section {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .jihad-box {
            background: linear-gradient(135deg, #ff7eb3 0%, #ff758c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 0.5rem;
        }
        .image-container {
            text-align: center;
            margin: 1rem 0;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .video-container {
            text-align: center;
            margin: 1rem 0;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .developer-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main header with developer name
    st.markdown("""
    <div class="main-header">
        🕌 اسلامی معلومات کا مرکز
        <br>
        <small style="font-size: 1rem; color: #666;">تیار کردہ: فریدہ بانو</small>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Sidebar ---
    with st.sidebar:
        st.title("⚙️ ترتیبات")
        selected_city = st.selectbox("شہر منتخب کریں", ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"])
        
        st.markdown("---")
        st.subheader("📚 فہرست")
        st.markdown("""
        - 🌐 تعارف
        - 📅 تاریخوں کا نظام
        - 🕋 نماز کے اوقات  
        - 💎 توحید کی تعلیمات
        - 🌟 دین کے ارکان
        - 💧 وضو و غسل
        - 📖 احادیث مبارکہ و آیات
        - 👶 بچوں کا کونہ
        - 🎬 میڈیا گیلری
        - 👩‍💻 ڈویلپر کے بارے میں
        """)
        
        st.markdown("---")
        
        # Developer Info in Sidebar
        st.markdown("### 👩‍💻 ڈویلپر کی معلومات")
        st.markdown("""
        **نام:** فریدہ بانو  
        **مقصد:** اسلامی تعلیمات کو عام کرنا  
        **ورژن:** 1.0
        **📧:** farida.bano@example.com
        """)
        
        st.markdown("---")
        st.info("""
        **نوٹ:** یہ ایپلیکیشن اسلامی معلومات فراہم کرنے کے لیے بنائی گئی ہے۔ 
        فقہی مسائل کی مزید تفصیلات کے لیے اپنے مقامی **عالم دین** یا **مفتی** سے رجوع کریں۔
        """)
    
    # --- Introduction Section ---
    st.markdown("---")
    st.markdown('<div class="section-header">🌐 ہمارا تعارف</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="urdu-text">یہ پلیٹ فارم مسلمانوں کے لیے **قرآن و سنت** کی روشنی میں **صحیح اسلامی معلومات** کی فراہمی کے لیے بنایا گیا ہے۔ ہمارا مقصد **توحید، عبادات، اخلاقیات** اور دیگر دینی احکام کو **آسان اور منظم** انداز میں پیش کرنا ہے تاکہ ہر عمر کے افراد، خاص طور پر **نوجوان اور بچے**، اپنے دین کی بنیادی باتوں کو اچھی طرح سمجھ سکیں۔</div>', unsafe_allow_html=True)

    # --- Current date section ---
    st.markdown("---")
    st.markdown('<div class="section-header">📅 آج کی تاریخ</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gregorian_date = datetime.date.today().strftime("%d %B, %Y")
        st.markdown(f'<div class="date-box"><h4>عیسوی تاریخ</h4><h3>{gregorian_date}</h3></div>', unsafe_allow_html=True)
    
    with col2:
        hijri_date = get_accurate_hijri_date()
        st.markdown(f'<div class="date-box"><h4>ہجری تاریخ</h4><h3>{hijri_date}</h3></div>', unsafe_allow_html=True)
    
    with col3:
        current_islamic_month = get_current_islamic_month()
        st.markdown(f'<div class="date-box"><h4>اسلامی مہینہ</h4><h3>{current_islamic_month}</h3></div>', unsafe_allow_html=True)
    
    # --- Prayer times section ---
    st.markdown("---")
    st.markdown('<div class="section-header">🕋 نماز کے اوقات</div>', unsafe_allow_html=True)
    
    prayer_times = get_prayer_times(selected_city)
    
    # Display prayer times in columns
    cols = st.columns(6)
    prayers = list(prayer_times.items())
    
    for i, (prayer, time) in enumerate(prayers):
        with cols[i]:
            st.markdown(f'<div class="prayer-time"><h4>{prayer}</h4><h3>{time}</h3></div>', unsafe_allow_html=True)
    
    # Zawal time
    dhuhr_time = prayer_times.get("ظہر", "12:30 PM")
    zawal_time = get_zawal_time(dhuhr_time)
    st.success(f"**⏰ زوال کا وقت:** **{zawal_time}** (اس وقت نماز مکروہ ہے)")
    
    st.info("⚠️ **نوٹ:** یہ اوقات صرف ایک تخمینہ ہیں؛ درست وقت کے لیے مقامی مسجد کے کیلنڈر پر انحصار کریں۔")

    
    # --- Tauheed (توحید) Section ---
    st.markdown("---")
    st.markdown('<div class="section-header">💎 توحید - اسلام کی بنیاد</div>', unsafe_allow_html=True)
    
    tauheed_tab1, tauheed_tab2, tauheed_tab3, tauheed_tab4 = st.tabs(["تعارف", "اقسام", "فوائد", "قرآنی آیات"])
    
    with tauheed_tab1:
        st.subheader(TAUHEED_SECTION["definition"]["title"])
        st.markdown(f'<div class="urdu-text">{TAUHEED_SECTION["definition"]["description"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 توحید کی اہمیت")
            st.info(TAUHEED_SECTION["definition"]["importance"])
            
            st.markdown("### 👶 بچوں کے لیے سیکھنے کے طریقے")
            for learning in TAUHEED_SECTION["kids_learning"]:
                st.success(f"• {learning}")
        
        with col2:
            st.markdown("### 💫 توحید کے فوائد")
            for benefit in TAUHEED_SECTION["benefits"]:
                st.warning(f"• {benefit}")
            
            st.markdown("### 🕌 کلمہ طیبہ")
            st.error("**لَا إِلَٰهَ إِلَّا ٱللَّٰهُ مُحَمَّدٌ رَسُولُ ٱللَّٰهِ**")
            st.markdown("**مطلب:** اللہ کے سوا کوئی معبود نہیں، محمد ﷺ اللہ کے رسول ہیں")
    
    with tauheed_tab2:
        st.subheader("توحید کی اقسام")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'### {TAUHEED_SECTION["types"]["rububiyyah"]["title"]}')
            st.info(TAUHEED_SECTION["types"]["rububiyyah"]["description"])
            for point in TAUHEED_SECTION["types"]["rububiyyah"]["points"]:
                st.markdown(f'<div class="tauheed-box"><p class="urdu-text" style="font-size:1.1rem; color:white;">{point}</p></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'### {TAUHEED_SECTION["types"]["uluhiyyah"]["title"]}')
            st.success(TAUHEED_SECTION["types"]["uluhiyyah"]["description"])
            for point in TAUHEED_SECTION["types"]["uluhiyyah"]["points"]:
                st.markdown(f'<div class="tauheed-box"><p class="urdu-text" style="font-size:1.1rem; color:white;">{point}</p></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'### {TAUHEED_SECTION["types"]["asma_was_sifat"]["title"]}')
            st.warning(TAUHEED_SECTION["types"]["asma_was_sifat"]["description"])
            for point in TAUHEED_SECTION["types"]["asma_was_sifat"]["points"]:
                st.markdown(f'<div class="tauheed-box"><p class="urdu-text" style="font-size:1.1rem; color:white;">{point}</p></div>', unsafe_allow_html=True)
    
    with tauheed_tab3:
        st.subheader("توحید کے فوائد اور برکات")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### روحانی فوائد")
            benefits_spiritual = [
                "اللہ کی محبت حاصل ہوتی ہے",
                "دل میں اطمینان پیدا ہوتی ہے",
                "گناہوں سے معافی ملتی ہے",
                "جنت میں داخلہ ملتا ہے"
            ]
            for benefit in benefits_spiritual:
                st.success(f"🌟 {benefit}")
        
        with col2:
            st.markdown("### دنیاوی فوائد")
            benefits_worldly = [
                "خوف و غم سے نجات ملتی ہے",
                "عملوں میں برکت ہوتی ہے",
                "دل کی پاکیزگی ہوتی ہے",
                "شیطان کے شر سے حفاظت ہوتی ہے"
            ]
            for benefit in benefits_worldly:
                st.info(f"💫 {benefit}")
    
    with tauheed_tab4:
        st.subheader("توحید کے بارے میں قرآنی آیات")
        
        for verse in TAUHEED_SECTION["quran_verses"]:
            st.markdown(f"""
            <div class="highlight-box">
                <div class="arabic-text">{verse["arabic"]}</div>
                <div class="urdu-text">{verse["urdu"]}</div>
                <p style="text-align: left; color: #666;">📖 سورۃ **{verse["surah"]}** - آیت **{verse["verse"]}**</p>
            </div>
            """, unsafe_allow_html=True)

    
    # --- Islamic Pillars Section for Kids ---
    st.markdown("---")
    st.markdown('<div class="section-header">🌟 دین کے ارکان - بچوں کے لیے</div>', unsafe_allow_html=True)
    
    pillars_tab1, pillars_tab2, pillars_tab3, pillars_tab4, pillars_tab5 = st.tabs(["🕌 نماز", "🌙 روزہ", "💰 زکواۃ", "🕋 حج", "⚔️ جہاد"])
    
    with pillars_tab1:
        st.subheader(ISLAMIC_PILLARS["salah"]["title"])
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🕐 نماز کے اوقات")
            for time in ISLAMIC_PILLARS["salah"]["times"]:
                st.info(f"• **{time}**")
        
        with col2:
            st.markdown("### 📝 بچوں کے لیے مشقیں")
            for practice in ISLAMIC_PILLARS["salah"]["kids_practice"]:
                st.warning(f"• **{practice}**")
            
            st.markdown("### 🎯 نماز کی اہمیت")
            st.error(ISLAMIC_PILLARS["salah"]["importance"])
    
    with pillars_tab2:
        st.subheader(ISLAMIC_PILLARS["fasting"]["title"])
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌅 روزہ کی اقسام")
            for type_fast in ISLAMIC_PILLARS["fasting"]["types"]:
                st.info(f"• **{type_fast}**")
            
            st.markdown("### 👶 بچوں کے لیے تجاویز")
            for tip in ISLAMIC_PILLARS["fasting"]["kids_tips"]:
                st.error(f"• **{tip}**")
        
        with col2:
            st.markdown("### 💫 روزہ کے فوائد")
            for benefit in ISLAMIC_PILLARS["fasting"]["benefits"]:
                st.success(f"• **{benefit}**")

    with pillars_tab3:
        st.subheader(ISLAMIC_PILLARS["zakat"]["title"])
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 زکواۃ کی شرائط")
            for condition in ISLAMIC_PILLARS["zakat"]["conditions"]:
                st.info(f"• **{condition}**")
        
        with col2:
            st.markdown("### 🤲 زکواۃ کے مصارف")
            for recipient in ISLAMIC_PILLARS["zakat"]["recipients"]:
                st.warning(f"• **{recipient}**")
    
    with pillars_tab4:
        st.subheader(ISLAMIC_PILLARS["hajj"]["title"])
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚶 حج کے مراحل")
            for step in ISLAMIC_PILLARS["hajj"]["steps"]:
                st.warning(f"• **{step}**")
        
        with col2:
            st.markdown("### 💫 حج کے فوائد")
            for benefit in ISLAMIC_PILLARS["hajj"]["benefits"]:
                st.success(f"• **{benefit}**")
    
    with pillars_tab5:
        st.subheader(ISLAMIC_PILLARS["jihad"]["title"])
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚔️ جہاد کی اقسام")
            for type_jihad in ISLAMIC_PILLARS["jihad"]["types"]:
                st.markdown(f'<div class="jihad-box"><p class="urdu-text" style="font-size:1.1rem; color:white;">{type_jihad}</p></div>', unsafe_allow_html=True)
            
            st.markdown("### 📋 شرائط")
            for condition in ISLAMIC_PILLARS["jihad"]["conditions"]:
                st.info(f"• **{condition}**")
        
        with col2:
            st.markdown("### 💫 فوائد")
            for benefit in ISLAMIC_PILLARS["jihad"]["benefits"]:
                st.success(f"• **{benefit}**")
            
            st.markdown("### ❌ غلط فہمیاں")
            for misconception in ISLAMIC_PILLARS["jihad"]["misconceptions"]:
                st.error(f"• **{misconception}**")
    
    # --- Taharat (Wudu & Ghusal) Section ---
    st.markdown("---")
    st.markdown('<div class="section-header">💧 وضو و غسل</div>', unsafe_allow_html=True)
    
    taharat_tab1, taharat_tab2, taharat_tab3 = st.tabs(["وضو کے احکام", "غسل کے احکام", "اہم شرائط"])
    
    with taharat_tab1:
        st.subheader("🕌 وضو کے فرض، سنن اور آداب")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### فرض (4)")
            for i, farz in enumerate(TAHARAT_SECTION["wudu"]["farz"], 1):
                st.markdown(f'<div class="taharat-box" style="background: #2E86AB;"><p class="urdu-text" style="font-size:1rem; color:white;">**{i}.** {farz}</p></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### سنتیں")
            for i, sunnat in enumerate(TAHARAT_SECTION["wudu"]["sunnat"], 1):
                st.info(f"**{i}.** {sunnat}")
            
        with col3:
            st.markdown("### مکروہات")
            for i, makruh in enumerate(TAHARAT_SECTION["wudu"]["makruh"], 1):
                st.error(f"**{i}.** {makruh}")
        
        st.caption("✅ **یاد رکھیں:** وضو کے چار فرائض ادا نہ ہونے سے وضو نہیں ہوتا۔")
    
    with taharat_tab2:
        st.subheader("🚿 غسل کے فرض، سنن اور آداب")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### فرض (3)")
            for i, farz in enumerate(TAHARAT_SECTION["ghusal"]["farz"], 1):
                st.markdown(f'<div class="taharat-box" style="background: #A23B72;"><p class="urdu-text" style="font-size:1rem; color:white;">**{i}.** {farz}</p></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### سنتیں")
            for i, sunnat in enumerate(TAHARAT_SECTION["ghusal"]["sunnat"], 1):
                st.info(f"**{i}.** {sunnat}")
            
        st.caption("⚠️ **انتباہ:** غسل کے تین فرائض میں سے کسی ایک کا بھی رہ جانا غسل کو نامکمل کر دیتا ہے۔")
    
    with taharat_tab3:
        st.subheader("🔴 وضو توڑنے والی اور غسل فرض ہونے والی چیزیں")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### وضو ٹوٹنے کی وجوہات")
            for i, condition in enumerate(TAHARAT_SECTION["conditions"]["wudu_breaks"], 1):
                st.error(f"**{i}.** {condition}")
        
        with col2:
            st.markdown("### غسل فرض ہونے کے اوقات")
            for i, condition in enumerate(TAHARAT_SECTION["conditions"]["ghusal_required"], 1):
                st.warning(f"**{i}.** {condition}")
    
    st.info("💡 **نوٹ:** وضو اور غسل کے احکام میں فقہی مکاتب فکر کے مطابق معمولی فرق ہو سکتا ہے۔")

    # --- Hadith & Quran Verses Section ---
    st.markdown("---")
    st.markdown('<div class="section-header">📖 احادیث مبارکہ اور قرآنی آیات</div>', unsafe_allow_html=True)
    
    # Combined Tabs
    hadith_tab1, hadith_tab2, hadith_tab3 = st.tabs(["📜 احادیث دیکھیں", "📘 آیات دیکھیں", "🔍 تلاش کریں"])
    
    with hadith_tab1:
        st.subheader("مشہور احادیث")
        for i, hadith in enumerate(HADITHS, 1):
            with st.expander(f"حدیث نمبر {i} - **{hadith['reference']}**", expanded=False):
                st.markdown(f'<div class="arabic-text">{hadith["arabic"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="urdu-text">{hadith["urdu"]}</div>', unsafe_allow_html=True)
    
    with hadith_tab2:
        st.subheader("منتخب قرآنی آیات")
        for verse in QURAN_VERSES:
            st.markdown(f"""
            <div class="highlight-box">
                <div class="arabic-text">{verse["arabic"]}</div>
                <div class="urdu-text">{verse["urdu"]}</div>
                <p style="text-align: left; color: #666;">📖 سورۃ **{verse["surah"]}** - آیت **{verse["verse"]}**</p>
            </div>
            """, unsafe_allow_html=True)
            
    with hadith_tab3:
        search_term = st.text_input("🔍 حدیث یا آیت تلاش کریں (عربی یا اردو میں)")
        if search_term:
            # Search Hadiths
            found_hadiths = [h for h in HADITHS if search_term.lower() in h["arabic"].lower() or search_term in h["urdu"]]
            # Search Verses
            found_verses = [v for v in QURAN_VERSES if search_term.lower() in v["arabic"].lower() or search_term in v["urdu"]]
            
            if found_hadiths or found_verses:
                st.markdown("### 📜 احادیث کے نتائج")
                for hadith in found_hadiths:
                    st.markdown(f"""
                    <div class="highlight-box" style="border-right: 5px solid #A23B72;">
                        <div class="arabic-text">{hadith["arabic"]}</div>
                        <div class="urdu-text">{hadith["urdu"]}</div>
                        <p style="text-align: left;">📚 حوالہ: {hadith['reference']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("### 📘 آیات کے نتائج")
                for verse in found_verses:
                    st.markdown(f"""
                    <div class="highlight-box" style="border-right: 5px solid #2E86AB;">
                        <div class="arabic-text">{verse["arabic"]}</div>
                        <div class="urdu-text">{verse["urdu"]}</div>
                        <p style="text-align: left; color: #666;">📖 سورۃ **{verse["surah"]}** - آیت **{verse["verse"]}**</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("آپ کی تلاش سے متعلق کوئی حدیث یا آیت نہیں ملی۔")

    # --- Kids section ---
    st.markdown("---")
    st.markdown('<div class="section-header">👶 بچوں کا کونہ</div>', unsafe_allow_html=True)
    
    kids_tab1, kids_tab2, kids_tab3 = st.tabs(["📚 اسلامی کہانیاں", "🤲 چھوٹی دعائیں", "🎨 سرگرمیاں"])
    
    with kids_tab1:
        st.subheader("چھوٹے بچوں کے لیے اسلامی کہانیاں")
        for story in KIDS_SECTION["stories"]:
            st.markdown(f"""
            <div class="kids-section">
                <h4 style="color:#A23B72;">{story["title"]}</h4>
                <p class="urdu-text" style="font-size:1.1rem; direction:rtl;">{story["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with kids_tab2:
        st.subheader("روزمرہ کی چھوٹی دعائیں")
        for i, dua in enumerate(KIDS_SECTION["duas"], 1):
            st.markdown(f"""
            <div class="highlight-box" style="border-right: 5px solid #A23B72;">
                <h5 style="text-align: right; direction: rtl;">{i}. {dua["urdu"]}</h5>
                <div class="arabic-text">{dua["arabic"]}</div>
                <p style="text-align: left; color: #666;">📚 ماخذ: {dua['source']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with kids_tab3:
        st.subheader("بچوں کے لیے دینی سرگرمیاں")
        st.markdown("""
        <div class="kids-section" style="background-color:#E3F2FD;">
            <p class="urdu-text">
                - **نماز کا چارٹ:** ایک چارٹ بنائیں اور روزانہ کی پانچ نمازوں کو نشان زد کریں۔ <br>
                - **اللہ کے ناموں کا کھیل:** اللہ کے 99 ناموں میں سے ہر ہفتے ایک نام یاد کریں اور اس کا مطلب سمجھیں۔ <br>
                - **صدقہ کا ڈبہ:** ایک ڈبہ بنائیں اور روزانہ اس میں چند سکے ڈالیں تاکہ صدقہ کی عادت ڈالی جا سکے۔ <br>
                - **وضو کا عملی مظاہرہ:** وضو کے مراحل کو عملی طور پر کر کے دکھائیں۔ 
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("📣 مزید معلومات جلد شامل کی جائیں گی! بچوں کے لیے کارٹونز اور ویڈیوز کے لنکس بھی یہاں شامل کیے جا سکتے ہیں۔")

    # --- Media Gallery Section (Updated to use local images) ---
    st.markdown("---")
    st.markdown('<div class="section-header">🎬 میڈیا گیلری</div>', unsafe_allow_html=True)
    
    media_tab1, media_tab2 = st.tabs(["🖼️ تصاویر", "🎥 ویڈیوز"])
    
    with media_tab1:
        st.subheader("اسلامی مقامات کی تصاویر")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown("### مسجد الحرام، مکہ")
            if "masjid_haram" in islamic_images:
                st.image(islamic_images["masjid_haram"], use_container_width=True, caption="مسجد الحرام، مکہ مکرمہ")
            else:
                st.info("📷 مسجد الحرام کی تصویر 'islamic/101.jpg' فائل میں شامل کریں")
            st.markdown("**مکہ مکرمہ، سعودی عرب**")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown("### مسجد نبوی، مدینہ")
            if "masjid_nabwi" in islamic_images:
                st.image(islamic_images["masjid_nabwi"], use_container_width=True, caption="مسجد نبوی، مدینہ منورہ")
            else:
                st.info("📷 مسجد نبوی کی تصویر 'islamic/102.jpg' فائل میں شامل کریں")
            st.markdown("**مدینہ منورہ، سعودی عرب**")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown("### مسجد اقصیٰ، فلسطین")
            if "masjid_aqsa" in islamic_images:
                st.image(islamic_images["masjid_aqsa"], use_container_width=True, caption="مسجد اقصیٰ، بیت المقدس")
            else:
                st.info("📷 مسجد اقصیٰ کی تصویر 'islamic/103.jpg' فائل میں شامل کریں")
            st.markdown("**بیت المقدس، فلسطین**")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown("### فتح مکہ")
            if "fateh_makkah" in islamic_images:
                st.image(islamic_images["fateh_makkah"], use_container_width=True, caption="فتح مکہ کا منظر")
            else:
                st.info("📷 فتح مکہ کی تصویر 'islamic/104.jpg' فائل میں شامل کریں")
            st.markdown("**8ھ میں رسول اللہ ﷺ کا مکہ فتح کرنا**")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with media_tab2:
        st.subheader("تعلیمی ویڈیوز")
        
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.markdown("### وضو کا صحیح طریقہ")
        st.video("https://youtu.be/3ecRdD9HqZY?si=xD06iq_8kazGiiFG")  # Replace with actual Islamic educational video URL
        st.markdown("**وضو کے فرائض، سنن اور طریقہ کار**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.markdown("### نماز کا مکمل طریقہ")
        st.video("https://youtu.be/flzX2XGwrdA?si=whqRSkqoFGDIf8tF")  # Replace with actual Islamic educational video URL
        st.markdown("**نماز کے تمام ارکان اور شرائط**")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- About Developer Section ---
    st.markdown("---")
    st.markdown('<div class="section-header">👩‍💻 ڈویلپر کے بارے میں</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        width: 150px; height: 150px; border-radius: 50%; 
                        margin: 0 auto; display: flex; align-items: center; 
                        justify-content: center; color: white; font-size: 3rem;">
                👩‍💻
            </div>
            <h3>فریدہ بانو</h3>
            <p>ڈویلپر اور ڈیزائنر</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="urdu-text">
        <h4>میرے بارے میں</h4>
        <p>میں فریدہ بانو ہوں اور میں نے یہ اسلامی ایپلیکیشن مسلمانوں کو ان کے دین کی بنیادی باتوں سے روشناس کرانے کے لیے بنائی ہے۔ میرا مقصد قرآن و سنت کی روشنی میں صحیح اسلامی معلومات کو آسان اور منظم انداز میں پیش کرنا ہے۔</p>
        
        <h4>مقاصد</h4>
        <ul>
            <li>✅ اسلامی تعلیمات کو ڈیجیٹل پلیٹ فارم پر لانا</li>
            <li>✅ نوجوانوں اور بچوں کے لیے اسلامی مواد کو پرکشش بنانا</li>
            <li>✅ روزمرہ کی عبادات کو سمجھنے میں مدد فراہم کرنا</li>
            <li>✅ امت مسلمہ کے لیے مفید ٹولز تیار کرنا</li>
        </ul>
        
        <h4>رابطہ</h4>
        <p> 📧 : faridabano159@gmail.com<br>
        🌐: www.islamicapp.com</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Footer with Developer Info ---
    st.markdown("---")
    st.markdown("""
    <div class="developer-card">
        <h4>🕌 اسلامی معلومات کا مرکز</h4>
        <p>تیار کردہ: <strong>فریدہ بانو</strong></p>
        <p>📧 رابطہ: faridabano159@gmail.com</p>
        <p style="font-size: 0.8rem;">© 2024 تمام حقوق محفوظ ہیں</p>
    </div>
    """, unsafe_allow_html=True)

# --- Run the App ---
if __name__ == "__main__":
    main()