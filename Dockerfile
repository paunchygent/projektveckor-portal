# syntax=docker/dockerfile:1

FROM python:3.13-slim AS python-base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PDM_CHECK_UPDATE=false
WORKDIR /app
ENV PYTHONPATH=/app/src

FROM python-base AS deps
RUN pip install --no-cache-dir pdm==2.26.2
COPY pyproject.toml README.md /app/
RUN pdm config python.use_venv false \
    && pdm install --prod --no-editable --no-self

FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml* /app/frontend/
RUN corepack enable && pnpm install --frozen-lockfile=false
COPY frontend /app/frontend
RUN pnpm build

FROM python-base AS production
RUN pip install --no-cache-dir pdm==2.26.2
COPY --from=deps /app/__pypackages__ /app/__pypackages__
COPY src /app/src
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist
EXPOSE 8000
CMD ["pdm", "run", "serve:lan"]
