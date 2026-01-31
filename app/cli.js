const readline = require('readline');
const fs = require('fs').promises;
const path = require('path');
const { gradient } = require('./ui/gradient');

const ENV_KEYS = {
  API_KEY: 'API_KEY',
  API_BASE_URL: 'API_BASE_URL',
  SOURCE_COOKIE: 'SOURCE_COOKIE',
  SOURCE_PASSWORD: 'SOURCE_PASSWORD',
  TARGET_UID: 'TARGET_UID',
  TARGET_COOKIE: 'TARGET_COOKIE'
};

class InteractiveCLI {
  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    this.envPath = path.join(__dirname, '..', '.env');
  }

  question(query) {
    return new Promise(resolve => {
      this.rl.question(query, resolve);
    });
  }

  async prompt(message, defaultValue = '') {
    const answer = await this.question(`${message}${defaultValue ? ` [${defaultValue}]` : ''}: `);
    return answer.trim() || defaultValue;
  }

  async promptNumber(message, defaultValue = 1) {
    const answer = await this.prompt(message, defaultValue.toString());
    const num = parseInt(answer);
    return isNaN(num) ? defaultValue : num;
  }

  async confirm(message) {
    const answer = await this.question(`${message} (y/n): `);
    return answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes';
  }

  close() {
    this.rl.close();
  }

  displayHeader() {
    console.clear();
    console.log(gradient('+----------------------------------------------------------+'));
    console.log(gradient('|                                                            |'));
    console.log(gradient('|     FACEBOOK PAGE REG & TRANSFER MANAGER v2.0             |'));
    console.log(gradient('|     Tao va ban giao Page tu dong                         |'));
    console.log(gradient('|                                                            |'));
    console.log(gradient('+----------------------------------------------------------+') + '\n');
  }

  displayMenu() {
    console.log('\n' + gradient('+----------------------------------------------------------+'));
    console.log(gradient('|   MENU CHINH                                              |'));
    console.log(gradient('+----------------------------------------------------------+'));
    console.log('  1. Reg & Transfer Page');
    console.log('  2. Quan ly cau hinh');
    console.log('  3. Xem huong dan');
    console.log('  4. Xem thong ke (Coming soon)');
    console.log('  5. Thoat\n');
  }

  displayConfigMenu() {
    console.log('\n' + gradient('+----------------------------------------------------------+'));
    console.log(gradient('|   QUAN LY CAU HINH (.env)                                 |'));
    console.log(gradient('+----------------------------------------------------------+'));
    console.log('  1. Tao config moi (luu vao .env)');
    console.log('  2. Tai lai config tu .env');
    console.log('  3. Xem config hien tai');
    console.log('  4. Luu config vao .env');
    console.log('  5. Quay lai\n');
  }

  async loadConfig() {
    try {
      require('dotenv').config({ path: this.envPath });
    } catch (_) {}
    const apiKey = process.env.API_KEY;
    const sourceCookie = process.env.SOURCE_COOKIE;
    const sourcePassword = process.env.SOURCE_PASSWORD;
    const targetUid = process.env.TARGET_UID;
    const targetCookie = process.env.TARGET_COOKIE;
    if (!apiKey || !sourceCookie || !sourcePassword || !targetUid || !targetCookie) {
      return null;
    }
    return {
      apiKey,
      sourceAccount: { cookie: sourceCookie, password: sourcePassword },
      targetAccount: { uid: targetUid, cookie: targetCookie }
    };
  }

  _escapeEnvValue(val) {
    if (val == null) return '""';
    const s = String(val).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
    return `"${s}"`;
  }

  async saveConfig(config) {
    try {
      const lines = [
        '# Facebook Page Reg & Transfer - cau hinh',
        `${ENV_KEYS.API_KEY}=${this._escapeEnvValue(config.apiKey)}`,
        `${ENV_KEYS.API_BASE_URL}=${this._escapeEnvValue(process.env.API_BASE_URL || 'https://minhdong.site/api/v1/facebook')}`,
        `${ENV_KEYS.SOURCE_COOKIE}=${this._escapeEnvValue(config.sourceAccount.cookie)}`,
        `${ENV_KEYS.SOURCE_PASSWORD}=${this._escapeEnvValue(config.sourceAccount.password)}`,
        `${ENV_KEYS.TARGET_UID}=${this._escapeEnvValue(config.targetAccount.uid)}`,
        `${ENV_KEYS.TARGET_COOKIE}=${this._escapeEnvValue(config.targetAccount.cookie)}`
      ];
      await fs.writeFile(this.envPath, lines.join('\n') + '\n', 'utf8');
      return true;
    } catch (error) {
      console.error('Loi khi luu .env:', error.message);
      return false;
    }
  }

  maskSensitiveData(str, showLength = 10) {
    if (!str || str.length <= showLength) return str;
    return str.substring(0, showLength) + '...';
  }

  displayConfig(config) {
    console.log('\n' + gradient('+----------------------------------------------------------+'));
    console.log(gradient('|   CAU HINH HIEN TAI                                      |'));
    console.log(gradient('+----------------------------------------------------------+'));
    console.log(`\nAPI Key: ${this.maskSensitiveData(config.apiKey)}`);
    console.log(`\nNick goc (Tao Page):`);
    console.log(`   Cookie: ${this.maskSensitiveData(config.sourceAccount.cookie, 20)}`);
    console.log(`   Password: ${'*'.repeat(config.sourceAccount.password.length)}`);
    console.log(`\nNick nhan (Nhan Page):`);
    console.log(`   UID: ${config.targetAccount.uid}`);
    console.log(`   Cookie: ${this.maskSensitiveData(config.targetAccount.cookie, 20)}\n`);
  }
}

module.exports = InteractiveCLI;
