const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');
const logger = require('./logger');

const DATA_FOLDER = path.join(__dirname, '..', 'data');

// Cache for storing parsed CSV data
const questionCache = new Map();
let companiesCache = null;

function getAllCompanies() {
  try {
    if (companiesCache) return companiesCache;

    if (!fs.existsSync(DATA_FOLDER)) {
      logger.error(`Data folder not found: ${DATA_FOLDER}`);
      return [];
    }

    const files = fs.readdirSync(DATA_FOLDER);
    companiesCache = files
      .filter(file => file.endsWith('.csv'))
      .map(file => file.replace('.csv', ''));

    logger.debug(`Found companies: ${companiesCache}`);
    return companiesCache;
  } catch (error) {
    logger.error(`Error listing companies: ${error.message}`);
    return [];
  }
}

function loadQuestions(company) {
  try {
    // Check cache first
    if (questionCache.has(company)) {
      return questionCache.get(company);
    }

    const filePath = path.join(DATA_FOLDER, `${company}.csv`);
    logger.debug(`Loading CSV from: ${filePath}`);

    if (!fs.existsSync(filePath)) {
      logger.error(`CSV file not found: ${filePath}`);
      return [];
    }

    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true
    });

    const questions = records
      .filter(record => {
        const requiredColumns = ['Difficulty', 'Title', 'Frequency', 'Acceptance Rate', 'Link', 'Topics'];
        return requiredColumns.every(col => record[col] !== undefined && record[col] !== null);
      })
      .map(record => ({
        title: record.Title,
        difficulty: record.Difficulty,
        frequency: parseFloat(record.Frequency),
        acceptance_rate: parseFloat(record['Acceptance Rate']),
        link: record.Link,
        topics: record.Topics
      }));

    // Store in cache
    questionCache.set(company, questions);
    return questions;
  } catch (error) {
    logger.error(`Error loading questions for ${company}: ${error.message}`);
    return [];
  }
}

function filterByDifficulty(questions, difficulty) {
  if (!difficulty) return questions;
  return questions.filter(q => q.difficulty.toLowerCase() === difficulty.toLowerCase());
}

module.exports = {
  getAllCompanies,
  loadQuestions,
  filterByDifficulty
};