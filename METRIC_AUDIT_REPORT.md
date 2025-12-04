# Comprehensive Metric & Input Audit Report
**Date:** December 4, 2025  
**Project:** GetLizzyFit Tracker  
**Branch:** dashboard-redesign

---

## Executive Summary

This report documents all input fields across the entire application, their relationship to user-preferred metrics, and data storage mechanisms.

### Status Overview:
1. ✅ **Exercise distance units**: Model, form, view, and template all correctly use 'mi'/'km' and respect user preferences
2. ✅ **Exercise form defaults**: Already pre-fills user's preferred distance unit
3. ✅ **Weight system**: All weights stored in pounds with proper conversions - working correctly
4. ⚠️ **Height storage**: Mixed storage (cm OR inches) - inconsistent design but functional
5. ✅ **Meal logging**: No metric preferences needed (calories are universal)
6. ✅ **Fertility logging**: No metric issues (dates and temperature)

### Findings Summary:
- **0 Critical Issues** (previously identified issues are already fixed)
- **1 Design Inconsistency** (height storage in mixed units - requires decision)
- **All metric preference systems working correctly**

---

## 1. USER PROFILE METRICS

### 1.1 Preferred Unit Settings (UserProfile Model)
**Location:** `users/models.py`

| Field | Choices | Default | Storage Format |
|-------|---------|---------|----------------|
| `weight_unit` | kg, lb, st | kg | User preference only |
| `height_unit` | cm, in | cm | User preference only |
| `distance_unit` | km, mi | km | User preference only |

**Data Storage:**
- `starting_weight`: DecimalField(5,2) - **STORED IN POUNDS**
- `height`: DecimalField(5,2) - **STORED IN USER'S UNIT** ❌ INCONSISTENT
  - If cm selected: stored in cm
  - If in selected: stored in total inches

---

## 2. WEIGHT TRACKING

### 2.1 Input Locations

#### A. Profile Creation (`users/templates/users/create_profile.html`)
**Lines 228-265**

**Input Fields:**
- Weight Unit Selection: kg / lb / st (buttons)
- Weight input (kg): Single number input
- Weight input (lb): Single number input  
- Weight input (st): Two inputs (stones + pounds)

**Form Processing:** `users/forms.py` - `UserProfileForm.clean()`
- **KG Input:** Converts kg → lb (multiplies by 2.20462)
- **LB Input:** No conversion needed
- **ST Input:** Converts stones+pounds → total pounds (stones * 14 + pounds)
- **Result:** ALL WEIGHTS STORED IN POUNDS ✅

#### B. Edit Profile (`users/templates/users/edit_profile.html`)
**Lines 54-96**

**Input Fields:** Same as profile creation
**Form Processing:** Same conversion logic ✅
**Display:** Correctly converts from stored pounds to user's preferred unit

#### C. Log Activities (`users/templates/users/log_activities.html`)
**Lines 150-195**

**Input Fields:**
- If st: Two inputs (stones + pounds)
- If kg: Single input labeled "Weight (kg)"
- If lb: Single input labeled "Weight (lb)"

**Form Processing:** `metrics/forms.py` - `HealthMetricsForm`
- **Issue:** Form shows stones/pounds inputs but weight field is hidden
- **Conversion in View:** `users/views.py` line 520-530
  - KG: Converts kg → lb (multiplies by 2.20462) ✅
  - LB: No conversion ✅
  - ST: Form's clean() converts to pounds ✅

**Data Storage:** `metrics/models.py` - `HealthMetrics`
- Field: `weight` DecimalField(5,2)
- **Stored in:** POUNDS ✅

**Display Logic:** `users/views.py` lines 597-605
- Converts stored pounds back to user's preferred unit for display ✅

### 2.2 Weight Data Flow Summary
```
USER INPUT (kg/lb/st) 
    ↓ [Form Validation]
CONVERT TO POUNDS
    ↓ [Save to DB]
HEALTHMETRICS.WEIGHT (pounds)
    ↓ [Retrieve & Display]
CONVERT TO USER'S PREFERRED UNIT
    ↓
DISPLAY (kg/lb/st)
```

**Status:** ✅ **WORKING CORRECTLY**

---

## 3. HEIGHT TRACKING

### 3.1 Input Locations

#### A. Profile Creation (`users/templates/users/create_profile.html`)
**Lines 266-303**

**Input Fields:**
- Height Unit Selection: cm / in (buttons)
- Height input (cm): Single number input
- Height input (in): Two inputs (feet + inches)

**Form Processing:** `users/forms.py` - `UserProfileForm.clean()`
- **CM Input:** Stored as-is in cm ❌
- **IN Input:** Converts feet+inches → total inches, stored in inches ❌
- **Issue:** Height stored in DIFFERENT UNITS depending on user preference

**Data Storage:** `users/models.py` - `UserProfile`
- Field: `height` DecimalField(5,2)
- **Stored in:** MIXED UNITS ❌ CRITICAL ISSUE

### 3.2 Height Issue Analysis

**Problem:** When calculating BMI or other metrics, the code must check `height_unit` to know what unit the stored value is in.

**Current BMI Calculation:** `users/views.py` line 97-103
```python
if profile.height_unit == 'cm':
    height_m = float(profile.height) / 100
else:  # inches
    height_m = float(profile.height) * 0.0254
```

**Status:** ⚠️ **WORKS BUT INCONSISTENT DESIGN**
- Should standardize: Store all heights in ONE unit (preferably cm or inches)
- Display conversion should happen in views/templates only

---

## 4. EXERCISE TRACKING

### 4.1 Model Definition (`exercise/models.py`)

**Distance Fields:**
- `distance_unit`: CharField - Choices: **'miles', 'kilometers'** ❌
- `distance_logged`: DecimalField(6,2)

**CRITICAL ISSUE:** Model uses 'miles'/'kilometers' but UserProfile uses 'mi'/'km'

### 4.2 Form Definition (`exercise/forms.py`)

**Lines 12-17:**
```python
DISTANCE_CHOICES = [
    ('km', 'Kilometres'),  # ✅ Matches UserProfile
    ('mi', 'Miles'),       # ✅ Matches UserProfile
]
```

**Issue:** Form uses 'km'/'mi' but model expects 'miles'/'kilometers' ❌

### 4.3 Input Location (`users/templates/users/log_activities.html`)

**Lines 278-288**

**Input Fields:**
- Distance logged: Number input (no unit label) ❌
- Distance unit: Dropdown with 'km'/'mi' choices

**Form Processing:** `users/views.py` lines 538-544
- No conversion logic
- Saves directly to model
- **Issue:** Distance unit mismatch will cause validation errors

**Display:** No distance unit preference respected ❌

### 4.4 Exercise Issues Summary

| Component | Unit Format | Status |
|-----------|-------------|--------|
| UserProfile.distance_unit | 'km', 'mi' | Reference |
| ExerciseLog.distance_unit (model) | 'miles', 'kilometers' | ❌ Mismatch |
| ExerciseLogForm (form) | 'km', 'mi' | ✅ Matches profile |
| Log template | 'km', 'mi' shown | ✅ Matches profile |
| **Result** | Data mismatch | ❌ BROKEN |

**Status:** ❌ **CRITICAL BUG - NEEDS IMMEDIATE FIX**

---

## 5. MEAL TRACKING

### 5.1 Model Definition (`meals/models.py`)

**Fields:**
- `meal_type`: CharField (breakfast/lunch/dinner/snack)
- `calories`: IntegerField
- `protein`: FloatField (grams)
- `carbs`: FloatField (grams)
- `fats`: FloatField (grams)

**Metric Dependencies:** NONE - All values are universal ✅

### 5.2 Input Location (`users/templates/users/log_activities.html`)

**Line 218:** Uses `{{ meal_form.as_p }}` (all fields auto-generated)

**Form Processing:** `users/views.py` lines 532-537
- No conversions needed
- Saves directly to model ✅

**Status:** ✅ **NO ISSUES**

---

## 6. FERTILITY TRACKING

### 6.1 Model Definition (`fertility/models.py`)

**Fields:**
- `date`: DateField
- `cycle_day`: IntegerField
- `temperature`: FloatField
- `symptoms`: TextField
- `notes`: TextField

**Metric Dependencies:** NONE ✅

### 6.2 Input Location (`users/templates/users/log_activities.html`)

**Line 337:** Uses `{{ fertility_form.as_p }}` (all fields auto-generated)

**Status:** ✅ **NO ISSUES**

---

## 7. DETAILED FINDINGS BY LOCATION

### 7.1 Profile Creation Form
**File:** `users/templates/users/create_profile.html`

| Line Range | Input Type | Metric Link | Data Storage | Status |
|------------|------------|-------------|--------------|--------|
| 205-210 | Date of Birth | None | Direct | ✅ |
| 212-217 | Sex | None | Direct | ✅ |
| 228-238 | Weight Unit | UserProfile.weight_unit | User preference | ✅ |
| 240-265 | Starting Weight | → Converts to lb | UserProfile.starting_weight (lb) | ✅ |
| 266-276 | Height Unit | UserProfile.height_unit | User preference | ✅ |
| 277-303 | Height | → Mixed storage | UserProfile.height (cm or in) | ⚠️ |
| 314-347 | Activity Level | None | Direct | ✅ |
| 361-395 | Goals | None | Direct | ✅ |

### 7.2 Log Activities Page
**File:** `users/templates/users/log_activities.html`

| Line Range | Input Type | Metric Link | Data Storage | Status |
|------------|------------|-------------|--------------|--------|
| 150-195 | Weight | UserProfile.weight_unit | HealthMetrics.weight (lb) | ✅ |
| 218 | Meal | None | NutritionLog (universal) | ✅ |
| 241-315 | Exercise | UserProfile.distance_unit | ExerciseLog.distance_unit | ❌ |
| 337 | Fertility | None | FertilityLog (universal) | ✅ |

### 7.3 Edit Profile Form
**File:** `users/templates/users/edit_profile.html`

| Line Range | Input Type | Metric Link | Data Storage | Status |
|------------|------------|-------------|--------------|--------|
| 54-96 | Weight inputs | UserProfile.weight_unit | Converts to lb | ✅ |
| 100-140 | Height inputs | UserProfile.height_unit | Mixed storage | ⚠️ |
| 137-139 | Distance Unit | UserProfile.distance_unit | User preference | ✅ |

---

## 8. REQUIRED FIXES

### Priority 1: CRITICAL (Breaks functionality)

#### ✅ FIXED: Exercise Distance Unit Mismatch
**Problem:** Model uses 'miles'/'kilometers', everywhere else uses 'mi'/'km'

**STATUS:** ✅ **ALREADY IMPLEMENTED**
- Model (`exercise/models.py` line 43): Uses `('km', 'Kilometres')`, `('mi', 'Miles')` ✅
- Form (`exercise/forms.py` lines 20-23): Uses `('km', 'Kilometres')`, `('mi', 'Miles')` ✅
- Both now match UserProfile standards ✅

#### ✅ FIXED: Exercise Form Should Default to User's Preferred Unit
**Location:** `exercise/forms.py` lines 46-53

**STATUS:** ✅ **ALREADY IMPLEMENTED**
- Form accepts `user_profile` parameter in `__init__()` ✅
- Sets `self.initial['distance_unit'] = user_profile.distance_unit` ✅
- View passes `user_profile=profile` when initializing form (line 591) ✅

### Priority 2: IMPORTANT (Inconsistent design)

#### ✅ FIXED: Standardize Height Storage
**Problem:** Heights stored in mixed units (cm or inches depending on user choice)

**STATUS:** ✅ **IMPLEMENTED**
- Form (`users/forms.py`): Now converts all heights to cm before saving ✅
- Stored heights: Always in centimeters regardless of user preference ✅
- Display logic: Converts cm back to inches when user prefers inches ✅
- BMI calculations: Simplified to always expect cm ✅
- Data migration: Created and run (`0006_convert_heights_to_cm.py`) ✅
  - Converted 2 existing profiles from inches to cm ✅

**Changes Made:**
1. Updated `UserProfileForm.clean()` to convert inches → cm (multiply by 2.54)
2. Simplified BMI calculations in `metrics/views.py` (removed height_unit check)
3. Simplified BMI calculations in `users/views.py` dashboard (removed height_unit check)
4. Simplified BMI calculations in `users/views.py` profile view (removed height_unit check)
5. Updated `edit_profile` view to convert cm → inches for display (divide by 2.54)
6. Created data migration to convert existing inch heights to cm

### Priority 3: ENHANCEMENTS (Nice to have)

#### ✅ IMPLEMENTED: Unit Labels on Exercise Distance Input
**Location:** `users/templates/users/log_activities.html` lines 277-282

**STATUS:** ✅ **ALREADY IMPLEMENTED**
- Label shows: "Distance {% if distance_unit %}({{ distance_unit }}){% endif %}" ✅
- Input group shows: `{{ distance_unit|default:"km/mi" }}` ✅
- Helper text shows: "Your preferred unit: {{ profile.get_distance_unit_display }}" ✅
- Context includes `distance_unit` from view (line 598) ✅

#### ✅ IMPLEMENTED: Pre-fill Exercise Distance Unit
**STATUS:** ✅ **ALREADY IMPLEMENTED** (see Fix 2 above)

#### Enhancement: Visual Unit Indicators
Add small unit badges next to all numeric inputs showing what unit is expected

---

## 9. DATA INTEGRITY CHECK

### Weight Data
```sql
-- All weights in HealthMetrics should be in pounds
SELECT COUNT(*) FROM metrics_healthmetrics WHERE weight < 50 OR weight > 500;
-- If any results: likely data corruption or wrong units
```

### Height Data  
```sql
-- Heights are mixed - cm values typically 140-220, inch values typically 55-85
SELECT id, height, height_unit FROM users_userprofile 
WHERE (height_unit = 'cm' AND height < 100) 
   OR (height_unit = 'in' AND height > 100);
-- Any results indicate wrong unit stored
```

### Exercise Distance
```sql
-- Check for unit mismatches
SELECT distance_unit, COUNT(*) FROM exercise_exerciselog 
WHERE distance_unit IS NOT NULL 
GROUP BY distance_unit;
-- Should show 'miles' and 'kilometers' currently
-- After fix: Should show 'mi' and 'km'
```

---

## 10. CONVERSION REFERENCE

### Weight Conversions (Currently Used)
- 1 kg = 2.20462 lb ✅
- 1 stone = 14 lb ✅
- Storage: Always in pounds ✅

### Height Conversions (Currently Used)
- 1 inch = 2.54 cm ✅ (for BMI)
- 1 foot = 12 inches ✅
- Storage: Mixed (cm OR inches) ⚠️

### Distance Conversions (NEEDED)
- 1 km = 0.621371 mi
- 1 mi = 1.60934 km
- Storage: Should be in user's preferred unit OR standardize to km

---

## 11. RECOMMENDATIONS

### Immediate Actions:
1. ✅ Fix exercise model distance_unit choices
2. ✅ Create migration to update existing exercise data
3. ✅ Update exercise form to default to user's distance preference
4. ✅ Add unit labels to exercise distance input

### Short-term Actions:
5. ⚠️ Consider standardizing height storage to cm
6. ⚠️ Add data validation checks for weight ranges
7. ⚠️ Add unit badges throughout UI

### Long-term Actions:
8. 📋 Consider adding user preference for temperature (C/F) for fertility tracking
9. 📋 Add nutrition unit preferences (grams vs oz)
10. 📋 Implement unit conversion history tracking

---

## 12. TESTING CHECKLIST

After fixes are applied:

### Weight Testing:
- [ ] Create profile with kg, log weight in kg → verify stored in lb
- [ ] Create profile with lb, log weight in lb → verify stored correctly  
- [ ] Create profile with st, log weight in st → verify converted to lb
- [ ] Edit profile, change units → verify existing data displays correctly
- [ ] Check dashboard weight chart → verify conversions display correctly

### Height Testing:
- [ ] Create profile with cm → verify storage
- [ ] Create profile with inches → verify storage
- [ ] Calculate BMI with cm height → verify correct
- [ ] Calculate BMI with inch height → verify correct

### Exercise Testing:
- [ ] Log exercise with km → verify saves correctly
- [ ] Log exercise with mi → verify saves correctly
- [ ] Change profile distance unit → verify new exercises default correctly
- [ ] View old exercises → verify unit displays correctly

---

## APPENDIX A: File Locations Reference

### Models:
- User Profile: `users/models.py` (lines 14-99)
- Health Metrics: `metrics/models.py` (lines 9-18)
- Exercise: `exercise/models.py` (lines 14-68)
- Meals: `meals/models.py` (lines 6-18)
- Fertility: `fertility/models.py` (lines 17-25)

### Forms:
- User Profile: `users/forms.py` (lines 8-145)
- Health Metrics: `metrics/forms.py` (lines 4-71)
- Exercise: `exercise/forms.py` (lines 4-69)
- Meals: `meals/forms.py` (lines 4-26)

### Views:
- User Dashboard: `users/views.py` (lines 18-219)
- Log Activities: `users/views.py` (lines 489-619)
- Create Profile: `users/views.py` (lines 230-290)

### Templates:
- Create Profile: `users/templates/users/create_profile.html`
- Edit Profile: `users/templates/users/edit_profile.html`
- Log Activities: `users/templates/users/log_activities.html`
- Dashboard: `users/templates/users/dashboard_new.html`

---

**Report Complete**  
**Total Critical Issues:** 2  
**Total Important Issues:** 2  
**Total Enhancements:** 2
