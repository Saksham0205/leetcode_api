const express = require('express');
const cors = require('cors');
const { router } = require('./app/routes');
const logger = require('./app/logger');

const app = express();
const port = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// API Info
app.get('/', (req, res) => {
  res.json({
    title: 'DSA Interview API',
    description: 'Fetch DSA questions by company, difficulty, and search terms with pagination',
    version: '1.1',
    endpoints: {
      '/companies': 'GET - List all companies',
      '/questions': 'GET - Get questions (params: company, difficulty?, search?, page?, limit?)',
      '/questions/all': 'GET - Get all questions (params: difficulty?, search?, page?, limit?)'
    },
    pagination: {
      page: 'Page number (default: 1)',
      limit: 'Items per page (default: 20, max: 100)'
    }
  });
});

// Routes
app.use('/', router);

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error(`Error: ${err.message}`);
  res.status(err.status || 500).json({
    detail: err.message || 'Internal server error'
  });
});

// Start server if not running in Vercel
if (process.env.NODE_ENV !== 'production') {
  app.listen(port, () => {
    logger.info(`Server running at http://localhost:${port}`);
  });
}

// Export for Vercel
module.exports = app;