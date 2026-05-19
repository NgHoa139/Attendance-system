# Superpowers Plan: Deploy Online + Attendance Dashboard

## Goals
1. Backend FastAPI → deploy on Render.com (free)
2. DB → migrate to Neon.tech PostgreSQL (free, cloud)
3. Frontend → deploy on Netlify (free, drag & drop)
4. New attendance records API + dashboard page
5. Late check-in logic: after 10:00 AM = LATE

## Steps
1. Backend: Add is_late, check_in_time to models + records router
2. Frontend: New dashboard.html attendance sheet + link from index
3. Backend: Env var config + render.yaml + .env.example
4. Guide: DEPLOY.md step-by-step Neon → Render → Netlify
