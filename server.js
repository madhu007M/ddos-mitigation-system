const express = require('express');
const mongoose = require('mongoose');
const morgan = require('morgan');
const helmet = require('helmet');
const requestLogger = require('./middleware/requestLogger');
const ddosDetector = require('./middleware/ddosDetector');
const trafficRoutes = require('./routes/trafficRoutes');
const metricsRoutes = require('./routes/metricsRoutes');
require('dotenv').config();

const app = express();
app.use(helmet());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/ddos-mitigation', { useNewUrlParser: true, useUnifiedTopology: true });

app.use(requestLogger);
app.use(ddosDetector);
app.use('/api/traffic', trafficRoutes);
app.use('/api/metrics', metricsRoutes);

app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy', timestamp: new Date() });
});

app.get('/', (req, res) => {
    res.status(200).json({ message: 'DDoS Mitigation System Server Running', version: '1.0.0' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
