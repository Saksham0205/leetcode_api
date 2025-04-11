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
    description: 'Fetch DSA questions by company and difficulty',
    version: '1.0'
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