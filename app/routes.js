const express = require('express');
const { getAllCompanies, loadQuestions, filterByDifficulty } = require('./utils');
const logger = require('./logger');

const router = express.Router();

// List all companies
router.get('/companies', (req, res) => {
  try {
    const companies = getAllCompanies();
    logger.info(`Returning ${companies.length} companies`);
    res.json({ companies });
  } catch (error) {
    logger.error(`Error listing companies: ${error.message}`);
    res.status(500).json({ detail: 'Internal server error' });
  }
});

// Get questions by company and optional difficulty
router.get('/questions', (req, res) => {
  try {
    const { company, difficulty } = req.query;
    logger.info(`Fetching questions for company: ${company}, difficulty: ${difficulty}`);

    if (!company) {
      return res.status(400).json({ detail: 'Company parameter is required' });
    }

    const companies = getAllCompanies();
    if (!companies.includes(company)) {
      logger.error(`Company not found: ${company}`);
      return res.status(404).json({ detail: `Company '${company}' not found` });
    }

    const allQuestions = loadQuestions(company);
    if (!allQuestions.length) {
      logger.warning(`No questions found for company: ${company}`);
      return res.json([]);
    }

    const filtered = filterByDifficulty(allQuestions, difficulty);
    logger.info(`Returning ${filtered.length} questions`);
    res.json(filtered);
  } catch (error) {
    logger.error(`Error fetching questions: ${error.message}`);
    res.status(500).json({ detail: 'Internal server error' });
  }
});

// Get all questions from all companies
router.get('/questions/all', (req, res) => {
  try {
    logger.info('Fetching all questions');
    const allData = [];
    
    getAllCompanies().forEach(company => {
      const companyQuestions = loadQuestions(company);
      allData.push(...companyQuestions);
      logger.info(`Added ${companyQuestions.length} questions from ${company}`);
    });

    logger.info(`Returning ${allData.length} total questions`);
    res.json(allData);
  } catch (error) {
    logger.error(`Error fetching all questions: ${error.message}`);
    res.status(500).json({ detail: 'Internal server error' });
  }
});

module.exports = { router };