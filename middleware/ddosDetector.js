'use strict';

const rateLimit = require('express-rate-limit');

// Set up the rate limiter: maximum of 100 requests per IP per 15 minutes
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later.',
  statusCode: 429,
});

// Middleware to detect DDoS attacks
const ddosDetector = (req, res, next) => {
  // Example logic for detecting DDoS attacks
  // Replace this with your actual detection service logic
  if (req.rateLimit && req.rateLimit.remaining === 0) {
    return res.status(429).send('DDoS attack detected.');
  }

  next();
};

// Export the middleware
module.exports = { limiter, ddosDetector };