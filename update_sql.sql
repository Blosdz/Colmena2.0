-- update_sql.sql
-- Cambios administrativos aplicados a nivel de PostgreSQL (fuera de las migraciones Alembic)
-- al levantar el backend/frontend de Colmena por primera vez en este entorno.
--
-- Contexto: ya existía una base de datos "colmena" en el servidor con datos de otro
-- proyecto/entorno, y el rol "colmena" tenía una contraseña distinta a la esperada por
-- backend/.env.example. Ejecutado como superusuario "postgres".

-- 1. Renombrar la base de datos "colmena" preexistente para no perder sus datos.
ALTER DATABASE colmena RENAME TO "colmena2.0";

-- 2. Restablecer la contraseña del rol "colmena" a la esperada por backend/.env.example
--    (DATABASE_URL=postgresql+asyncpg://colmena:colmena@localhost:5432/colmena).
ALTER ROLE colmena WITH PASSWORD 'colmena';

-- 3. Crear una base de datos "colmena" nueva y limpia para este proyecto, propiedad del rol "colmena".
CREATE DATABASE colmena OWNER colmena;

-- Después de esto, el esquema de la base de datos "colmena" se crea vía:
--   cd backend && .venv/bin/python -m alembic upgrade head
-- (migración 0001: esquema inicial de Colmena, ver backend/migrations/versions/).
