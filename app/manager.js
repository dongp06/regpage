const axios = require('axios');
const LoadingSpinner = require('./ui/spinner');
const ProgressBar = require('./ui/progress');
const { gradient } = require('./ui/gradient');

const DEFAULT_API_BASE_URL = 'https://minhdong.site/api/v1/facebook';

class FacebookPageManager {
  constructor(apiKey) {
    const baseURL = process.env.API_BASE_URL || DEFAULT_API_BASE_URL;
    this.client = axios.create({
      baseURL,
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    this.stats = {
      total: 0,
      success: 0,
      failed: 0,
      skipped: 0
    };
  }

  async regAndTransfer(quantity, config) {
    const { cookieGoc, passGoc, uidNhan, cookieNhan } = config;

    console.log('\n' + gradient('+----------------------------------------------------------+'));
    console.log(gradient('|   REG & TRANSFER PAGE AUTOMATION                         |'));
    console.log(gradient('+----------------------------------------------------------+') + '\n');
    console.log(`So luong Page can tao: ${quantity}`);
    console.log(`UID nhan: ${uidNhan}\n`);

    this.stats = { total: quantity, success: 0, failed: 0, skipped: 0 };
    const progressBar = new ProgressBar(quantity, 'Tien trinh');

    for (let i = 1; i <= quantity; i++) {
      console.log(`\n${'='.repeat(60)}`);
      console.log(gradient(`[${i}/${quantity}] Bat dau quy trinh...`));
      console.log('='.repeat(60));

      try {
        const spinner1 = new LoadingSpinner('Đang tạo Page mới');
        spinner1.start();

        await this._delay(1000);
        const regRes = await this.client.post('/page/create-cookie', {
          cookie: cookieGoc,
          use_random_name: true,
          use_random_avatar: true,
          use_random_bio: true
        });

        if (!regRes.data.success) {
          spinner1.fail(`Tao Page that bai: ${regRes.data.error || 'Loi khong xac dinh'}`);
          this.stats.failed++;
          progressBar.update(i, '[FAIL]');
          continue;
        }

        const newPage = {
          profile_plus_id: regRes.data.profile_plus_id,
          name: regRes.data.name,
          page_cookie: `${cookieGoc}; i_user=${regRes.data.profile_plus_id}`
        };

        spinner1.succeed(`Tao Page thanh cong: ${newPage.name}`);
        console.log(`   Page ID: ${newPage.profile_plus_id}`);

        const transferSuccess = await this._processSinglePage(newPage, passGoc, uidNhan, cookieNhan);

        if (transferSuccess) {
          this.stats.success++;
          progressBar.update(i, '[OK]');
        } else {
          this.stats.failed++;
          progressBar.update(i, '[FAIL]');
        }

        if (i < quantity) {
          const delayTime = 120000;
          const spinner2 = new LoadingSpinner(`Cho ${delayTime / 1000}s truoc khi tiep tuc`);
          spinner2.start();
          await this._delay(delayTime);
          spinner2.info('Tiep tuc...');
        }

      } catch (err) {
        spinner1.stop();
        console.error(`Loi nghiem trong tai buoc ${i}:`, err.message);
        this.stats.failed++;
        progressBar.update(i, '[FAIL]');
      }
    }

    this._displayFinalReport();
  }

  async _processSinglePage(page, passGoc, uidNhan, cookieNhan) {
    const { profile_plus_id, name, page_cookie } = page;

    try {
      console.log('\n  [1/3] Gui loi moi Admin...');
      const spinner1 = new LoadingSpinner('  Đang xử lý lời mời');
      spinner1.start();

      const addRes = await this.client.post('/page/add-permission-cookie', {
        cookie: page_cookie,
        target_user_id: uidNhan,
        password: passGoc
      });

      if (!addRes.data.success) {
        spinner1.fail(`Loi gui loi moi: ${addRes.data.error}`);
        return false;
      }

      const inviteId = addRes.data.invite_id;
      spinner1.succeed(`Gui loi moi thanh cong (ID: ${inviteId})`);

      console.log('  [2/3] Chap nhan loi moi...');
      const spinner2 = new LoadingSpinner('  Nick nhận đang xử lý');
      spinner2.start();

      const acceptRes = await this.client.post('/page/accept-invitation-cookie', {
        cookie: cookieNhan,
        profile_admin_invite_id: inviteId,
        user_id: profile_plus_id,
        accept: true
      });

      if (!acceptRes.data.success) {
        spinner2.fail(`Loi chap nhan: ${acceptRes.data.error}`);
        return false;
      }

      spinner2.succeed('Chap nhan loi moi thanh cong');

      const uidGoc = this._extractUid(page_cookie);
      console.log('  [3/3] Go quyen nick goc...');
      const spinner3 = new LoadingSpinner(`  Đang gỡ admin ${uidGoc}`);
      spinner3.start();

      const removeRes = await this.client.post('/page/remove-admin-cookie', {
        cookie: page_cookie,
        admin_id: uidGoc,
        password: passGoc,
        profile_plus_id: profile_plus_id
      });

      if (removeRes.data.success) {
        spinner3.succeed('Go quyen thanh cong');
        console.log(`\n  Hoan tat ban giao: ${name}`);
        return true;
      } else {
        spinner3.fail(`Loi go quyen: ${removeRes.data.error}`);
        return false;
      }

    } catch (error) {
      console.error(`  Loi trong qua trinh transfer:`, error.response?.data || error.message);
      return false;
    }
  }

  _displayFinalReport() {
    console.log('\n\n' + gradient('+----------------------------------------------------------+'));
    console.log(gradient('|                    BAO CAO KET QUA                       |'));
    console.log(gradient('+----------------------------------------------------------+'));

    const successRate = ((this.stats.success / this.stats.total) * 100).toFixed(1);

    console.log(`\nThong ke:`);
    console.log(`   Tong so: ${this.stats.total}`);
    console.log(`   Thanh cong: ${this.stats.success}`);
    console.log(`   That bai: ${this.stats.failed}`);
    console.log(`   Ty le thanh cong: ${successRate}%`);

    console.log(`\nThoi gian hoan thanh: ${new Date().toLocaleString('vi-VN')}\n`);
  }

  _extractUid(cookie) {
    const match = cookie.match(/c_user=(\d+)/);
    return match ? match[1] : null;
  }

  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  _getRandomDelay(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
}

module.exports = FacebookPageManager;
