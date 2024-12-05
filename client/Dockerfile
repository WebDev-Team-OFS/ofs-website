# Use the Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose port 5173 for the Vite dev server
EXPOSE 5173

# Start the frontend dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]