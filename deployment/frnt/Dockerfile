# Stage 1: Build the Next.js app
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy the rest of the application code
COPY ../../modules/frnt/app .

# Build the Next.js app
RUN npm run build

# Stage 2: Create a minimal runtime image
FROM node:20-alpine

# Set working directory in the production container
WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./next.config.js

# Install only production dependencies
RUN npm ci --omit=dev

# Expose port 3000 for the Next.js app
EXPOSE 3000

# Run the Next.js app in production mode
CMD ["node", ".next/standalone/server.js"]
