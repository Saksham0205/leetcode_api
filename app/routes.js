const express = require('express');
const { getAllCompanies, loadQuestions, filterByDifficulty, searchQuestions } = require('./utils');
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
    const { company, difficulty, search } = req.query;
    logger.info(`Fetching questions for company: ${company}, difficulty: ${difficulty}, search: ${search}`);

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

    // Apply filters
    let filtered = filterByDifficulty(allQuestions, difficulty);
    filtered = searchQuestions(filtered, search);
    
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
    const { difficulty, search } = req.query;
    logger.info(`Fetching all questions - difficulty: ${difficulty}, search: ${search}`);
    const allData = [];
    
    getAllCompanies().forEach(company => {
      const companyQuestions = loadQuestions(company);
      allData.push(...companyQuestions);
      logger.info(`Added ${companyQuestions.length} questions from ${company}`);
    });

    // Apply filters
    let filtered = filterByDifficulty(allData, difficulty);
    filtered = searchQuestions(filtered, search);

    logger.info(`Returning ${filtered.length} total questions`);
    res.json(filtered);
  } catch (error) {
    logger.error(`Error fetching all questions: ${error.message}`);
    res.status(500).json({ detail: 'Internal server error' });
  }
});

module.exports = { router };