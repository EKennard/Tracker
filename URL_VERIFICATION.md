# URL and Button Verification for Dashboard Redesign

## Dashboard Page (`/users/dashboard/`)
### Buttons/Links:
- ✅ **View Profile** → `/users/profile/` (profile_view)
- ✅ **Log Weight** → `/users/log/` (log_activities)
- ✅ **Log Activities** → `/users/log/` (log_activities)
- ✅ **View Friends** → `/social/` (social_hub)
- ✅ **My Milestones** → `/milestones/list/` (milestones_list)
- ✅ **+ Log New** → `/users/log/` (log_activities)
- ✅ **View All** (Milestones) → `/milestones/list/`
- ✅ **View All** (Friends) → `/social/` (social_hub)

### Fixed Issues:
- ✅ Changed `milestone.achieved` → `milestone.date_achieved`
- ✅ Changed `activity.timestamp` → `activity.created_at`
- ✅ Changed `activity.activity_text` → `activity.description`

## Log Activities Page (`/users/log/`)
### Modal Forms Submit To:
- ✅ **Weight Modal** → `/metrics/summary/` (POST)
- ✅ **Meal Modal** → `/meals/log/` (POST)
- ✅ **Exercise Modal** → `/exercise/log/` (POST)
- ✅ **Habit Modal** → `/habits/log/` (POST)
- ✅ **Fertility Modal** → `/fertility/` (POST)

### Verified Endpoints Exist:
- ✅ `/metrics/summary/` - metrics_summary view
- ✅ `/meals/log/` - meal_log view
- ✅ `/exercise/log/` - exercise_log view
- ✅ `/habits/log/` - habits_log view
- ✅ `/fertility/` - fertility views

## Profile & Settings Page (`/users/profile/`)
### Expected Features:
- Avatar selection (12 options)
- Privacy settings for 5 features
- Personal information display
- Account settings

## Social Hub Page (`/social/`)
### Features:
- ✅ Friend requests (accept/decline)
- ✅ Friends list
- ✅ Group invitations
- ✅ Activity feed

## Navigation (Base Template)
### Burger Menu Links:
- ✅ Dashboard → `/users/dashboard/`
- ✅ Log Activities → `/users/log/`
- ✅ Profile & Settings → `/users/profile/`
- ✅ Social → `/social/`
- ✅ Logout → `/accounts/logout/`

## Model Field Mappings

### Milestone Model:
- `profile` (ForeignKey)
- `title` (CharField)
- `description` (TextField)
- `date_achieved` (DateField) - ✅ Used for "achieved" check
- `target_date` (DateField)
- `milestone_type` (CharField)

### GlobalActivity Model:
- `profile` (ForeignKey)
- `activity_type` (CharField)
- `description` (TextField) - ✅ Used for display text
- `icon` (CharField)
- `created_at` (DateTimeField) - ✅ Used for timestamp

### UserProfile Model (New Fields):
- `avatar` (CharField) - default='default'
- `weight_privacy` (CharField)
- `meals_privacy` (CharField)
- `exercise_privacy` (CharField)
- `fertility_privacy` (CharField)
- `habits_privacy` (CharField)

## All URL Names Registry

### users/ app:
- `user_dashboard` - /users/dashboard/
- `log_activities` - /users/log/
- `profile_view` - /users/profile/
- `edit_profile` - /users/edit-profile/
- `create_profile` - /users/create-profile/
- `user_list` - /users/users/
- `send_friend_request` - /users/send_friend_request/<id>/
- `accept_friend_request` - /users/accept_friend_request/<id>/

### social/ app:
- `social_hub` - /social/
- `global_feed` - /social/feed/
- `search_users` - /social/search/
- `friend_requests` - /social/friend-requests/
- `groups` - /social/groups/
- `group_detail` - /social/group/<id>/

### metrics/ app:
- `metrics_summary` - /metrics/summary/

### meals/ app:
- `meal_log` - /meals/log/

### exercise/ app:
- `exercise_log` - /exercise/log/

### habits/ app:
- `habits_log` - /habits/log/

### milestones/ app:
- `milestones_list` - /milestones/list/

## Data Recording Formats

### Weight Entry:
- Stored in: **lb** (pounds)
- Displayed in: User preference (lb, kg, st)
- Form accepts: User preference unit

### Height:
- Stored in: User choice (cm or in)
- Form accepts: cm or in based on user preference

### Dates:
- All dates use: YYYY-MM-DD format
- Display format: Various (M d, Y format for readability)

### Timestamps:
- All timestamps use: Django's DateTimeField with timezone support
- Format: auto_now_add or default=timezone.now

## Status: ✅ All Links Verified and Fixed

### Issues Fixed:
1. ✅ Milestone import duplicate removed
2. ✅ GlobalActivity timestamp field corrected
3. ✅ Home page redirect to dashboard for authenticated users
4. ✅ Dashboard template field names corrected
5. ✅ Min-height added to dashboard for full page display

### Deployment:
- All fixes committed to `dashboard-redesign` branch
- Deployed to Heroku production
