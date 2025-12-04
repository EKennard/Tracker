# INPUT METRICS AUDIT REPORT
## GetLizzyFit Tracker Application

**Generated:** December 4, 2025  
**Purpose:** Comprehensive audit of all input fields, their metric preferences, and data storage consistency

---

## EXECUTIVE SUMMARY

### Critical Issues Found:
1. ❌ **INCONSISTENT DISTANCE UNITS** - Exercise form uses different choices than user profile
2. ❌ **NO DISTANCE UNIT PREFERENCE USED** - Exercise distance ignores user's preferred distance unit
3. ⚠️ **WEIGHT STORAGE INCONSISTENCY** - Multiple conversion points with potential for errors
4. ⚠️ **HEIGHT STORAGE INCONSISTENCY** - Mixed storage methods across forms

---

## 1. USER PROFILE METRICS

### Location: `users/models.py` - UserProfile model

#### Stored Metrics:
| Field | Type | Storage Unit | User Preference Field | Notes |
|-------|------|--------------|---------------------|-------|
| `starting_weight` | DecimalField(5,2) | **Pounds (lb)** | `weight_unit` (kg/lb/st) | ✅ Always converted to lb for storage |
| `height` | DecimalField(5,2) | **Mixed** | `height_unit` (cm/in) | ⚠️ Stores in cm OR inches depending on unit |
| `weight_unit` | CharField | N/A | N/A | User preference: kg/lb/st |
| `distance_unit` | CharField | N/A | N/A | User preference: km/mi |
| `height_unit` | CharField | N/A | N/A | User preference: cm/in |

---

## 2. WEIGHT INPUT ANALYSIS

### 2.1 Profile Creation Form
**Location:** `users/forms.py` - UserProfileForm  
**Template:** `users/templates/users/create_profile.html`

#### Input Fields:
| Input Box | Field Name | Visible When | Converts To | Storage |
|-----------|------------|--------------|-------------|---------|
| Weight (kg) | `starting_weight` | weight_unit='kg' | **lb** (×2.20462) | ✅ Always stores as lb |
| Weight (lb) | `starting_weight` | weight_unit='lb' | **lb** (no conversion) | ✅ Stored as-is |
| Stones | `weight_stones` | weight_unit='st' | **lb** (×14 + pounds) | ✅ Converted to lb |
| Pounds | `weight_pounds_extra` | weight_unit='st' | **lb** (added to stones) | ✅ Converted to lb |

**Form Conversion Logic (Line 77-112):**
```python
if weight_unit == 'st':
    stones = cleaned_data.get('weight_stones')
    pounds = cleaned_data.get('weight_pounds_extra', 0)
    total_pounds = (float(stones) * 14) + float(pounds or 0)
    cleaned_data['starting_weight'] = total_pounds  # ✅ CORRECT
elif weight_unit == 'kg':
    kg_weight = cleaned_data.get('starting_weight')
    cleaned_data['starting_weight'] = float(kg_weight) * 2.20462  # ✅ CORRECT
else:
    # lb - no conversion needed ✅ CORRECT
```

**Status:** ✅ **CONSISTENT** - All weight inputs properly convert to pounds for storage

---

### 2.2 Weight Logging Form
**Location:** `metrics/forms.py` - HealthMetricsForm  
**Template:** `users/templates/users/log_activities.html` (lines 129-208)

#### Input Fields:
| Input Box | Field Name | Visible When | Converts To | Storage |
|-----------|------------|--------------|-------------|---------|
| Weight (kg) | `weight` | weight_unit='kg' | **lb** (×2.20462) | ✅ Converts in view |
| Weight (lb) | `weight` | weight_unit='lb' | **lb** (no conversion) | ✅ Stored as-is |
| Stones | `weight_stones` | weight_unit='st' | **lb** (×14 + pounds) | ✅ Converts in form |
| Pounds | `weight_pounds` | weight_unit='st' | **lb** (added to stones) | ✅ Converts in form |

**Form Conversion Logic (Line 52-58):**
```python
def clean(self):
    cleaned_data = super().clean()
    weight_stones = cleaned_data.get('weight_stones')
    weight_pounds = cleaned_data.get('weight_pounds')
    if weight_stones is not None:
        total_pounds = (weight_stones * 14) + (weight_pounds or 0)
        cleaned_data['weight'] = total_pounds  # ✅ CORRECT
```

**View Conversion Logic (`users/views.py`, Line 506-519):**
```python
if form_type == 'weight':
    form = HealthMetricsForm(request.POST, user_profile=profile)
    if form.is_valid():
        entry = form.save(commit=False)
        entered_weight = float(entry.weight)
        if profile.weight_unit == 'kg':
            entry.weight = entered_weight * 2.20462  # ✅ CORRECT
        elif profile.weight_unit == 'lb':
            pass  # ✅ CORRECT
        # For stones, already converted in form ✅ CORRECT
        entry.save()
```

**Status:** ✅ **CONSISTENT** - Weight logging properly converts to pounds

---

### 2.3 Weight Display
**Locations:** Multiple views convert lb back to user's preferred unit

**Display Conversion Function (users/views.py, Line 53-61):**
```python
def format_weight_for_display(weight_in_lb):
    if profile.weight_unit == 'st':
        total_pounds = float(weight_in_lb)
        stones = int(total_pounds // 14)
        pounds = round(total_pounds % 14, 1)
        return f"{stones}st {pounds}lb"  # ✅ CORRECT
    elif profile.weight_unit == 'kg':
        kg = float(weight_in_lb) * 0.453592
        return f"{kg:.1f}"  # ✅ CORRECT
    else:
        return f"{float(weight_in_lb):.1f}"  # ✅ CORRECT
```

**Status:** ✅ **CONSISTENT** - Weight display properly converts from pounds

---

## 3. HEIGHT INPUT ANALYSIS

### 3.1 Profile Creation/Edit Form
**Location:** `users/forms.py` - UserProfileForm  
**Template:** `users/templates/users/create_profile.html` (lines 272-306)

#### Input Fields:
| Input Box | Field Name | Visible When | Storage Unit | Issue |
|-----------|------------|--------------|--------------|-------|
| Height (cm) | `height` | height_unit='cm' | **cm** | ⚠️ Stored as cm |
| Feet | `height_feet` | height_unit='in' | **inches** (total) | ⚠️ Stored as inches |
| Inches | `height_inches` | height_unit='in' | **inches** (total) | ⚠️ Stored as inches |

**Form Conversion Logic (Line 114-135):**
```python
if height_unit == 'in':
    feet = cleaned_data.get('height_feet')
    inches = cleaned_data.get('height_inches', 0)
    if feet is not None:
        total_inches = (float(feet) * 12) + float(inches or 0)
        cleaned_data['height'] = total_inches  # ⚠️ Stores in INCHES
elif height_unit == 'cm':
    if not cleaned_data.get('height'):
        raise forms.ValidationError('Please enter your height.')
    # ⚠️ Stores in CM (no conversion)
```

**Status:** ⚠️ **INCONSISTENT** - Height stored in different units (cm vs inches) based on user preference
- If user selects CM: stores in CM
- If user selects INCHES: stores in INCHES (total)
- This works but is inconsistent with weight storage pattern

**Recommendation:** Standardize to always store in one unit (e.g., cm or inches)

---

## 4. DISTANCE INPUT ANALYSIS (EXERCISE)

### 4.1 Exercise Logging Form
**Location:** `exercise/forms.py` - ExerciseLogForm  
**Template:** `users/templates/users/log_activities.html` (lines 276-284)

#### Input Fields:
| Input Box | Field Name | Storage | User Preference Used? | Issue |
|-----------|------------|---------|----------------------|-------|
| Distance | `distance_logged` | **As entered** | ❌ NO | ⚠️ Not converted |
| Distance Unit | `distance_unit` | **As selected** | ❌ NO | ❌ **CRITICAL** |

**CRITICAL ISSUE #1: Incompatible Choices**
```python
# In exercise/models.py (Line 42-43):
DISTANCE_LOGGED_CHOICES = [
    ('miles', 'Miles'),           # ❌ Uses 'miles'
    ('kilometers', 'Kilometres')  # ❌ Uses 'kilometers'
]

# In users/models.py (Line 33):
DISTANCE_UNIT_CHOICES = [
    ('km', 'Kilometres'),  # ✅ Uses 'km'
    ('mi', 'Miles')        # ✅ Uses 'mi'
]
```

**CRITICAL ISSUE #2: Form Override**
```python
# In exercise/forms.py (Line 14-18):
DISTANCE_CHOICES = [
    ('km', 'Kilometres'),   # Different from model!
    ('mi', 'Miles'),        # Different from model!
]
distance_unit = forms.ChoiceField(
    choices=DISTANCE_CHOICES,  # Overrides model choices
    required=False
)
```

**CRITICAL ISSUE #3: No Default from User Preference**
- Form does NOT initialize with user's preferred distance unit
- User must manually select km/mi every time
- No conversion happens between units

**Status:** ❌ **BROKEN** - Multiple critical issues:
1. Model choices don't match user profile choices
2. Form choices don't match model choices  
3. User preference is completely ignored
4. No conversion between units

---

## 5. MEAL INPUT ANALYSIS

### Location: `meals/forms.py` - NutritionLogForm
**Template:** `users/templates/users/log_activities.html` (lines 214-228)

#### Input Fields:
| Input Box | Field Name | Type | Unit | Preference Used? |
|-----------|------------|------|------|-----------------|
| Calories | `calories` | Integer | kcal | N/A |
| Protein | `protein` | Float | grams | N/A |
| Carbs | `carbs` | Float | grams | N/A |
| Fats | `fats` | Float | grams | N/A |
| Description | `description` | Text | N/A | N/A |

**Status:** ✅ **CONSISTENT** - No unit preferences needed (international standards)

---

## 6. FERTILITY INPUT ANALYSIS

### Location: `fertility/forms.py` - FertilityLogForm
**Template:** `users/templates/users/log_activities.html` (lines 337-348)

#### Input Fields:
| Input Box | Field Name | Type | Unit | Preference Used? |
|-----------|------------|------|------|-----------------|
| Temperature | `temperature` | Float | °C/°F | ❌ NO |
| Symptoms | `symptoms` | Text | N/A | N/A |
| Notes | `notes` | Text | N/A | N/A |

**Status:** ⚠️ **INCOMPLETE** - Temperature should respect user preference (Celsius vs Fahrenheit)
- No temperature unit preference exists in profile
- Should add `temperature_unit` to UserProfile

---

## 7. DATA FLOW SUMMARY

### Weight Data Flow:
```
User Input (kg/lb/st) 
    → Form Conversion 
    → Storage (ALWAYS lb) 
    → Database (ALWAYS lb)
    → Retrieval (ALWAYS lb)
    → Display Conversion 
    → User Display (kg/lb/st)
```
**Status:** ✅ CONSISTENT

### Height Data Flow:
```
User Input (cm OR ft/in) 
    → Form Conversion 
    → Storage (cm OR inches) ⚠️
    → Database (MIXED UNITS) ⚠️
    → Retrieval (MIXED UNITS) ⚠️
    → Display Conversion 
    → User Display (cm OR ft/in)
```
**Status:** ⚠️ WORKS BUT INCONSISTENT

### Distance Data Flow:
```
User Input (km/mi) 
    → NO CONVERSION ❌
    → Storage (as entered) ❌
    → Database (MIXED UNITS) ❌
    → NO PREFERENCE CHECK ❌
    → User Display (as stored) ❌
```
**Status:** ❌ BROKEN

---

## 8. RECOMMENDATIONS

### CRITICAL (Must Fix):
1. **Fix Exercise Distance Unit Mismatch**
   - Change `ExerciseLog.DISTANCE_LOGGED_CHOICES` to match UserProfile choices
   - OR change UserProfile choices to match ExerciseLog
   - **Recommended:** Use 'km' and 'mi' everywhere

2. **Use Distance Preference in Exercise Form**
   - Initialize form with `initial={'distance_unit': profile.distance_unit}`
   - Show user's preferred unit first

3. **Add Distance Unit Label**
   - Display which unit is being used next to the input box

### HIGH PRIORITY (Should Fix):
4. **Standardize Height Storage**
   - Convert all heights to CM for storage (like weight → lb)
   - Update conversion functions
   - Run migration to convert existing data

5. **Add Temperature Unit Preference**
   - Add `temperature_unit` field to UserProfile (C/F)
   - Update FertilityLog to convert temperatures

### MEDIUM PRIORITY (Nice to Have):
6. **Add Unit Indicators to All Input Boxes**
   - Show "(kg)", "(mi)", etc. next to input fields
   - Make it clearer which unit is being used

7. **Add Conversion Helper Text**
   - Show equivalent in other units while user types
   - Example: "75 kg (165.3 lb)"

---

## 9. FILES REQUIRING CHANGES

### To Fix Distance Issues:
1. `exercise/models.py` - Line 42-43 (Change DISTANCE_LOGGED_CHOICES)
2. `exercise/forms.py` - Line 14-18 (Remove override or fix)
3. `exercise/forms.py` - `__init__` method (Add distance_unit default)
4. `users/views.py` - log_activities view (Pass profile to exercise form)

### To Standardize Height:
1. `users/models.py` - Add migration to convert all heights to cm
2. `users/forms.py` - Update conversion logic
3. `users/views.py` - Update all height conversions

### To Add Temperature Preference:
1. `users/models.py` - Add temperature_unit field
2. `fertility/models.py` - Update FertilityLog
3. `fertility/forms.py` - Add conversion logic

---

## 10. TESTING CHECKLIST

After fixes, test:
- [ ] Create profile with kg - verify weight saves as lb
- [ ] Create profile with st - verify weight saves as lb  
- [ ] Create profile with cm - verify height saves correctly
- [ ] Create profile with in - verify height saves correctly
- [ ] Log weight in kg - verify converts to lb
- [ ] Log weight in st - verify converts to lb
- [ ] Log exercise with km - verify uses profile preference
- [ ] Log exercise with mi - verify uses profile preference
- [ ] View dashboard - verify all units display in user preference
- [ ] Edit profile units - verify existing data displays correctly

---

**END OF REPORT**
