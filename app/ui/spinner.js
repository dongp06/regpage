class LoadingSpinner {
  constructor(text = 'Loading') {
    this.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
    this.text = text;
    this.currentFrame = 0;
    this.interval = null;
    this.isSpinning = false;
  }

  start() {
    if (this.isSpinning) return;
    this.isSpinning = true;
    process.stdout.write('\x1B[?25l');
    this.interval = setInterval(() => {
      const frame = this.frames[this.currentFrame];
      process.stdout.write(`\r${frame} ${this.text}...`);
      this.currentFrame = (this.currentFrame + 1) % this.frames.length;
    }, 80);
  }

  updateText(newText) {
    this.text = newText;
  }

  stop(finalText = null) {
    if (!this.isSpinning) return;
    clearInterval(this.interval);
    this.isSpinning = false;
    process.stdout.write('\r\x1B[K');
    if (finalText) {
      console.log(finalText);
    }
    process.stdout.write('\x1B[?25h');
  }

  succeed(text) {
    this.stop(`[OK] ${text}`);
  }

  fail(text) {
    this.stop(`[FAIL] ${text}`);
  }

  info(text) {
    this.stop(`[INFO] ${text}`);
  }
}

module.exports = LoadingSpinner;
