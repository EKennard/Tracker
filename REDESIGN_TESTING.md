# Dashboard Redesign - Testing Checklist

## Branch: `dashboard-redesign`
**Date**: November 29, 2025

---

## ✅ COMPLETED FEATURES

### 1. **Simplified Navigation** (4 Main Pages)
- 🏠 Dashboard - Central hub with activity feed
- 📝 Log Activities - Unified logging page
- 👤 Profile & Settings - Account, privacy, avatar
- 👥 Social - Friends, groups, activity

### 2. **Dashboard (`/users/dashboard/`)** - NEW LAYOUT
**Left Column:**
- User avatar (emoji-based)
- Quick stats (Activities, Friends, Milestones)
- Weight summary
- Quick action buttons

**Center Column:**
- Activity feed with color-coded borders by type
- Empty state with call-to-action
- Recent activities from all categories

**Right Column:**
- Mini weight trend chart (last 7 entries)
- Progress bar to goal
- Active milestones widget
- Friends' recent activity

### 3. **Log Activities (`/users/log/`)** - NEW PAGE
**Left Column:**
- 5 clickable tiles: Weight, Meals, Exercise, Habits, Fertility
- Each tile opens a modal form

**Center Column:**
- Interactive calendar
- Click any date to select it for logging
- Month navigation (prev/next)

**Right Column:**
- Recent entries summary for each category
- Last 3 entries per type

**Modal Forms:**
- Forms respect user unit preferences (kg/lb/st, cm/in)
- Submit to existing endpoints
- Close on successful save

### 4. **Profile & Settings (`/users/profile/`)** - ENHANCED
**Left Column:**
- **Avatar Selector**: 12 emoji options
  - Male: 💪 🏃‍♂️ 🚴‍♂️
  - Female: 💃 🏃‍♀️ 🚴‍♀️
  - Fitness: 🏋️ 🤸 🧘
  - Wellness: ❤️ 🌟
  - Default: 👤
- Account info (username, email, member since)
- Personal key for friend discovery
- Password change link

**Center Column:**
- **Privacy Settings** for each feature:
  - Global profile visibility (Private/Public)
  - Weight & Body Stats
  - Meal Diary
  - Exercise Logs
  - Habits
  - Fertility Tracking
- Each with 4 options: Private / Friends Only / Groups Only / Public

**Right Column:**
- Personal information summary
- Unit preferences
- Goals (weight goal, deadline)
- Edit profile link

### 5. **Social Hub (`/social/`)** - NEW PAGE
**Left Column:**
- Friend requests (pending)
- Friends list
- Group invitations (pending)
- My groups

**Center Column:**
- Activity feed from friends
- Recent activities with timestamps

**Features:**
- Accept/decline friend requests
- Accept/decline group invitations
- Search for friends modal
- View all friends/groups links

---

## 🗄️ DATABASE CHANGES

### New Fields Added to `UserProfile`:
```python
avatar = CharField(max_length=50, default='default')
weight_privacy = CharField(max_length=20, default='private')
meals_privacy = CharField(max_length=20, default='private')
exercise_privacy = CharField(max_length=20, default='private')
fertility_privacy = CharField(max_length=20, default='private')
habits_privacy = CharField(max_length=20, default='private')
```

**Migration**: `users/migrations/0004_userprofile_avatar_userprofile_exercise_privacy_and_more.py`
**Status**: ✅ Applied locally

---

## 🧪 TESTING REQUIRED

### Dashboard Tests:
- [ ] Dashboard loads without errors
- [ ] Avatar displays correctly
- [ ] Stats show accurate counts
- [ ] Weight summary displays with correct units
- [ ] Mini weight chart renders (if data exists)
- [ ] Activity feed shows recent activities
- [ ] Color-coded borders match activity types
- [ ] Milestones widget displays
- [ ] Friends activity widget works
- [ ] All links navigate correctly

### Log Activities Tests:
- [ ] Page loads with calendar visible
- [ ] Calendar displays current month
- [ ] Can navigate months (prev/next)
- [ ] Clicking date selects it
- [ ] Clicking Weight tile opens modal
- [ ] Clicking Meals tile opens modal
- [ ] Clicking Exercise tile opens modal
- [ ] Clicking Habits tile opens modal
- [ ] Clicking Fertility tile opens modal
- [ ] Forms use correct units (kg/lb/st)
- [ ] Forms save successfully
- [ ] Modal closes after save
- [ ] Recent entries update after save

### Profile & Settings Tests:
- [ ] Page loads with avatar displayed
- [ ] Avatar dropdown shows all options
- [ ] Avatar updates and saves
- [ ] Avatar preview updates on selection
- [ ] Privacy settings load current values
- [ ] Privacy settings save successfully
- [ ] Personal key displays correctly
- [ ] All info displays with correct formatting
- [ ] Password change link works
- [ ] Edit profile link works

### Social Hub Tests:
- [ ] Friend requests display if any
- [ ] Can accept friend request
- [ ] Can decline friend request
- [ ] Friends list displays
- [ ] Group invitations display if any
- [ ] Can accept group invitation
- [ ] Can decline group invitation
- [ ] My groups display
- [ ] Activity feed shows friend activities
- [ ] Search modal opens
- [ ] Search functionality works

### Navigation Tests:
- [ ] Burger menu opens on all screen sizes
- [ ] All 4 nav items present
- [ ] Links navigate to correct pages
- [ ] Active page indicator works (if implemented)
- [ ] Logout works

---

## 🐛 KNOWN ISSUES

### Fertility Browser Extension Warning:
- **Error**: "A listener indicated an asynchronous response by returning true, but the message channel closed before a response was received"
- **Source**: Browser extension (Content Script Bridge)
- **Impact**: None - cosmetic console warning only
- **Action**: Can be ignored, not a code issue

---

## 🚀 DEPLOYMENT CHECKLIST

Before merging to production:
- [ ] All tests pass locally
- [ ] Migration runs successfully
- [ ] All forms save correctly
- [ ] Avatar system works
- [ ] Privacy settings persist
- [ ] No console errors (except extension warnings)
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Create backup of production database
- [ ] Run migration on production
- [ ] Test on production environment

---

## 📝 NOTES

### Unit Preferences:
- All forms respect user's selected units
- Weight: kg, lb, st (stones)
- Height: cm, inches
- Distance: km, miles

### Color Scheme:
- Purple (#9C27B0): Primary, Weight
- Pink (#E91E63): Meals, Social
- Orange (#FF6F00): Exercise
- Yellow (#FFD600): Habits
- Green (#00C853): Fertility, Success

### Form Endpoints:
- Weight: `/metrics/summary/` (POST with metrics_submit=1)
- Meals: `/meals/log/` (POST)
- Exercise: `/exercise/log/` (POST)
- Habits: `/habits/log/` (POST)
- Fertility: `/fertility/` (POST)

---

## 🔄 ROLLBACK PLAN

If issues occur:
1. Switch to `newdesign` branch (previous stable)
2. Run: `git checkout newdesign`
3. Restart server
4. Database migration rollback if needed:
   ```bash
   python manage.py migrate users 0003
   ```
