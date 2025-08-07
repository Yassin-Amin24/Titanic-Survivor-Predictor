FROM node:20-alpine AS builder


WORKDIR /app

RUN apk add --no-cache bash && \
npm install -g pnpm --unsafe-perm

COPY package*.json ./
COPY pnpm-lock.yaml ./


RUN pnpm install --frozen-lockfile

RUN yes | pnpm approve-builds && pnpm rebuild esbuild

COPY . .



RUN pnpm run build

FROM caddy:2-alpine

COPY --from=builder /app/dist /usr/share/caddy

COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 80




