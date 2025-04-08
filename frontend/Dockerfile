FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package.json .
COPY package-lock.json* .

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Make sure we're not copying over a local node_modules directory
RUN rm -rf node_modules && npm install

EXPOSE 3000

# Use this command format to prevent exiting
CMD ["sh", "-c", "npm start"]