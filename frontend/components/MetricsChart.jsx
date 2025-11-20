import React from 'react';
import { Doughnut } from 'react-chartjs-2';

const MetricsChart = ({ metrics }) => {
    const data = {
        labels: ['Total Requests', 'Blocked Requests', 'Clean Requests'],
        datasets: [{
            data: [metrics.totalRequests, metrics.blockedRequests, metrics.cleanRequests],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
    };

    return (
        <div>
            <h2>Metrics Chart</h2>
            <Doughnut data={data} />
            <div>
                <h4>Statistics</h4>
                <ul>
                    <li>Total Requests: {metrics.totalRequests}</li>
                    <li>Unique IPs: {metrics.uniqueIPs}</li>
                    <li>Average Response Time: {metrics.avgResponseTime} ms</li>
                    <li>Attacks Detected: {metrics.attacksDetected}</li>
                </ul>
            </div>
        </div>
    );
};

export default MetricsChart;