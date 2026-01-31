const LoadingSpinner = require('./ui/spinner');
const FacebookPageManager = require('./manager');
const InteractiveCLI = require('./cli');
const { gradient } = require('./ui/gradient');

async function main() {
  const cli = new InteractiveCLI();
  let config = null;
  let manager = null;

  try {
    cli.displayHeader();

    const spinner = new LoadingSpinner('Đang kiểm tra config');
    spinner.start();
    await new Promise(r => setTimeout(r, 500));

    config = await cli.loadConfig();
    if (config) {
      spinner.succeed('Đã tải config từ file .env');
      manager = new FacebookPageManager(config.apiKey);
    } else {
      spinner.info('Chưa có config, cần tạo mới');
    }

    let running = true;
    while (running) {
      cli.displayMenu();
      const choice = await cli.prompt('Chọn chức năng (1-5)', '1');

      switch (choice) {
        case '1':
          if (!config) {
            console.log('\nChua co cau hinh! Vui long tao config truoc.');
            await cli.question('Nhan Enter de tiep tuc...');
            break;
          }
          await handleRegAndTransfer(cli, manager, config);
          break;

        case '2':
          config = await handleConfigManagement(cli, config);
          if (config) {
            manager = new FacebookPageManager(config.apiKey);
          }
          break;

        case '3':
          displayGuide();
          await cli.question('\nNhan Enter de tiep tuc...');
          break;

        case '4':
          console.log('\nTinh nang dang phat trien...\n');
          await cli.question('Nhan Enter de tiep tuc...');
          break;

        case '5':
          running = false;
          console.log('\nCam on ban da su dung! Tam biet!\n');
          break;

        default:
          console.log('Lua chon khong hop le!');
      }
    }

  } catch (error) {
    console.error('Loi:', error.message);
  } finally {
    cli.close();
  }
}

async function handleConfigManagement(cli, currentConfig) {
  let config = currentConfig;
  let managing = true;

  while (managing) {
    cli.displayConfigMenu();
    const choice = await cli.prompt('Chọn chức năng (1-5)', '1');

    switch (choice) {
      case '1':
        config = await createNewConfig(cli);
        break;

      case '2':
        const loaded = await cli.loadConfig();
        if (loaded) {
          config = loaded;
          console.log('Da tai lai config tu .env thanh cong!');
        } else {
          console.log('Thieu bien trong .env (API_KEY, SOURCE_*, TARGET_*). Kiem tra .env.example.');
        }
        await cli.question('Nhan Enter de tiep tuc...');
        break;

      case '3':
        if (config) {
          cli.displayConfig(config);
        } else {
          console.log('\nChua co config!');
        }
        await cli.question('Nhan Enter de tiep tuc...');
        break;

      case '4':
        if (config) {
          const saved = await cli.saveConfig(config);
          if (saved) {
            console.log('Da luu config vao .env');
          }
        } else {
          console.log('\nChua co config de luu!');
        }
        await cli.question('Nhan Enter de tiep tuc...');
        break;

      case '5':
        managing = false;
        break;

      default:
        console.log('Lua chon khong hop le!');
    }
  }

  return config;
}

async function createNewConfig(cli) {
  console.log('\n' + gradient('+----------------------------------------------------------+'));
  console.log(gradient('|   TAO CAU HINH MOI                                       |'));
  console.log(gradient('+----------------------------------------------------------+') + '\n');

  const apiKey = await cli.prompt('API Key');

  console.log('\nThong tin nick GOC (tao Page):');
  const cookieGoc = await cli.prompt('   Cookie');
  const passGoc = await cli.prompt('   Password');

  console.log('\nThong tin nick NHAN (nhan Page):');
  const uidNhan = await cli.prompt('   UID');
  const cookieNhan = await cli.prompt('   Cookie');

  const config = {
    apiKey,
    sourceAccount: {
      cookie: cookieGoc,
      password: passGoc
    },
    targetAccount: {
      uid: uidNhan,
      cookie: cookieNhan
    }
  };

  const saveNow = await cli.confirm('\nLuu config nay vao .env?');
  if (saveNow) {
    await cli.saveConfig(config);
    console.log('Da luu config vao .env!');
  }

  return config;
}

async function handleRegAndTransfer(cli, manager, config) {
  console.log('\n' + gradient('╔════════════════════════════════════════════════════════════╗'));
  console.log(gradient('║   REG & TRANSFER PAGE                                    ║'));
  console.log(gradient('╚════════════════════════════════════════════════════════════╝') + '\n');

  const quantity = await cli.promptNumber('So luong Page can tao', 1);

  console.log('\n' + gradient('+----------------------------------------------------------+'));
  console.log(gradient('|   XAC NHAN                                               |'));
  console.log(gradient('+----------------------------------------------------------+'));
  console.log(`Se tao: ${quantity} Page`);
  console.log(`Ban giao cho UID: ${config.targetAccount.uid}\n`);

  const confirmed = await cli.confirm('Bat dau?');

  if (!confirmed) {
    console.log('Da huy!');
    await cli.question('Nhan Enter de tiep tuc...');
    return;
  }

  await manager.regAndTransfer(quantity, {
    cookieGoc: config.sourceAccount.cookie,
    passGoc: config.sourceAccount.password,
    uidNhan: config.targetAccount.uid,
    cookieNhan: config.targetAccount.cookie
  });

  await cli.question('\nNhan Enter de tiep tuc...');
}

function displayGuide() {
  console.log('\n' + gradient('+----------------------------------------------------------+'));
  console.log(gradient('|   HUONG DAN SU DUNG                                      |'));
  console.log(gradient('+----------------------------------------------------------+') + '\n');

  console.log('QUY TRINH HOAT DONG:\n');
  console.log('1. Tao Page moi voi ten/avatar/bio ngau nhien');
  console.log('2. Gui loi moi Admin cho nick nhan');
  console.log('3. Nick nhan tu dong chap nhan');
  console.log('4. Nick goc tu dong go quyen');
  console.log('5. Lap lai cho den khi du so luong\n');

  console.log('CAU HINH:\n');
  console.log('- Sao chep .env.example thanh .env va dien gia tri');
  console.log('- Hoac chon menu 2 de tao/luu config vao .env');
  console.log('- Co the sua truc tiep file .env\n');

  console.log('THOI GIAN:\n');
  console.log('- Moi Page mat khoang 10-15 giay');
  console.log('- Delay 120 giay giua moi lan tao');
  console.log('- Tao 10 Page khoang 20+ phut\n');

  console.log('LUU Y:\n');
  console.log('- Khong tat chuong trinh khi dang chay');
  console.log('- Kiem tra cookie con han');
  console.log('- Khong tao qua nhieu cung luc (khuyen nghi < 20)');
}

module.exports = { main, handleConfigManagement, createNewConfig, handleRegAndTransfer, displayGuide };
