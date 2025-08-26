# RHorizon App — RDS + S3 Ready (No Kubernetes)

- Backend (Flask): PostgreSQL (RDS) via SQLAlchemy + uploads S3 (boto3)
- Frontend (Vue + Vite): build static, servi par Nginx ; proxy `/api` -> backend
- Local dev: `docker compose up --build`

## URLs
- Frontend: http://localhost
- Backend:  http://localhost:5000/api, /api/health

## Backend env (prod/staging)
- DB_HOST, DB_PORT=5432, DB_NAME, DB_USER, DB_PASSWORD, DB_SSLMODE=require
- AWS_REGION=eu-west-3, S3_BUCKET_NAME=rhorizon-app-assets

## API
- GET `/api` — hello
- GET `/api/health` — DB+S3
- GET `/api/items` — list
- POST `/api/items` — { "name": "..." }
- POST `/api/upload` — multipart `file`

## Mapping au plan projet
- Données: RDS PostgreSQL, TLS via `sslmode=require`
- S3: assets/uploads (chiffrement/Versioning/BPA à gérer côté infra)
- Secrets: envs (migrables vers AWS Secrets Manager sans changer le code)
- Observabilité: `/api/health` prêt pour probes/monitoring
