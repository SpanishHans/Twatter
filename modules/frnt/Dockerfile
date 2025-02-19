# Stage 1: Build the Next.js app
FROM node:20 AS builder

WORKDIR /app

# Install dependencies and build
COPY ./app/package*.json ./
RUN npm install
COPY /app .
RUN npm run build

# Stage 2: Run the app
FROM node:20 AS runner

WORKDIR /app

# Copy the standalone output
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
