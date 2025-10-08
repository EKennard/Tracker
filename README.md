

# GetLizzyFit

## Project Overview

GetLizzyFit is my modular, extensible health and wellness tracker. I built it to help myself and others set, track, and achieve personal goals—whether that’s weight loss, fitness, nutrition, fertility, or just staying motivated with friends. Everything is wrapped in a modern, user-friendly web app that I can use anywhere.

## My Aims and Objectives

- Give myself (and users) a single place to track health, fitness, and wellness
- Provide actionable insights through metrics, milestones, and analytics
- Stay motivated and accountable with social features and group challenges
- Keep privacy in my control—deciding what I share and with whom
- Make the experience beautiful, accessible, and responsive on any device

## Technology Stack

- **Backend:** Django 4.2+, Django REST Framework, PostgreSQL (Heroku-ready)
- **Frontend:** Django Templates, Tailwind CSS for a modern, responsive look
- **Authentication:** Django’s built-in auth (login, logout, registration, password management)
- **Other:** dj-database-url, Pillow, Whitenoise, Heroku deployment support

## How I Designed the UI Flow

1. **Landing/Login:** Secure login and registration, with password management
2. **Dashboard:** A unified view of my recent meals, metrics, milestones, habits, exercise, and fertility logs
3. **Module Pages:**
	 - Meals: Log and view nutrition entries
	 - Metrics: Track health metrics and measurements
	 - Milestones: Set, view, and share milestones
	 - Habits: Log daily habits and streaks
	 - Exercise: Log workouts and activity
	 - Fertility: Track cycles and fertility data
	 - Notifications: View reminders and alerts
	 - Social: Join groups, send/accept friend requests, share progress
4. **Sharing:** Share any log or milestone with specific friends or groups, with full privacy control
5. **Admin:** Manage all data via Django admin

## Wireframes & Visual Design Choices

- **Wireframes:** I structured the app around a top navigation bar, with each module accessible via clear links. Forms and lists are in card-style containers for clarity and focus.
- **Coloor Choices:**
	- **Primary:** Blue (#2563eb, Tailwind’s blue-600) for navigation and action buttons—trustworthy and motivating
	- **Background:** Light gray (#f3f4f6) for a clean, modern look
	- **Accents:** White cards, subtle shadows, and hover effects for interactivity
	- **Feedback:** Green for success, red for errors, yellow for warnings, all using Tailwind’s palette
- **Typography:** Sans-serif fonts for readability and a modern feel
- **Responsiveness:** Every page is mobile-friendly and adapts to different screen sizes

## Visual Aspects I Focused On

- **Tailwind CSS:** Used throughout for rapid, consistent, and beautiful styling
- **Forms:** Clean, accessible, and easy to use, with clear labels and error feedback
- **Tables & Lists:** Data is presented in easy-to-read tables or cards, with sorting and filtering where appropriate
- **Navigation:** Persistent top navigation bar with context-aware links (login/logout, dashboard, modules, find friends)
- **Accessibility:** High-contrast colors, focus states, and semantic HTML for screen readers

## Key Features

- Secure user authentication and profile management
- Nutrition, metrics, milestones, habits, exercise, fertility, and notifications modules
- Social features: friend requests, groups, sharing with granular privacy controls
- Admin interface for full data management
- Heroku-ready deployment with PostgreSQL

## What I Plan to Add Next

- Advanced analytics and charts
- Push notifications and reminders
- More granular sharing (e.g., share with groups, temporary sharing)
- API endpoints for mobile app integration
- More customization for user dashboards and reports

---
GetLizzyFit is my all-in-one health and wellness companion, supporting my journey (and hopefully yours) with powerful features and a delightful user experience.

