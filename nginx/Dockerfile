FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create a simple index page
RUN echo '<!DOCTYPE html><html><head><title>FastAPI Smart Library</title></head><body><h1>FastAPI Smart Library - Microservices</h1><p>Available endpoints:</p><ul><li><a href="/api/users">/api/users</a> - User Service</li><li><a href="/api/books">/api/books</a> - Book Service</li><li><a href="/api/loans">/api/loans</a> - Loan Service</li><li><a href="/health">/health</a> - Health Check</li></ul></body></html>' > /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
