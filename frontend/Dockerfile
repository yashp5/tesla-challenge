# Use an official Node runtime as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Install a simple server to serve static content
RUN npm install -g serve

# Expose port 8000
EXPOSE 8000

# Start the server
CMD ["serve", "-s", "build", "-l", "8000"]