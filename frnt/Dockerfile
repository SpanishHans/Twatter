# Stage 1: Build the Next.js app
FROM node:20 AS builder

WORKDIR /app

# Install pnpm manually
RUN npm install -g pnpm

# Copy dependencies and install only production dependencies
COPY ./app/pnpm-lock.yaml ./app/package.json ./
RUN pnpm install --frozen-lockfile --prod

# Copy the rest of the app and build
COPY ./app .
RUN pnpm build

# Stage 2: Run the app
FROM node:20 AS runner

WORKDIR /app

# Copy the standalone output
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
