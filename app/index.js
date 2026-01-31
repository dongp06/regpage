require('dotenv').config();
const { main } = require('./app');
const FacebookPageManager = require('./manager');
const InteractiveCLI = require('./cli');
const LoadingSpinner = require('./ui/spinner');
const ProgressBar = require('./ui/progress');

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { FacebookPageManager, InteractiveCLI, LoadingSpinner, ProgressBar, main };
