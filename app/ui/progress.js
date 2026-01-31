class ProgressBar {
  constructor(total, title = 'Progress') {
    this.total = total;
    this.current = 0;
    this.title = title;
    this.barLength = 30;
  }

  update(current, status = '') {
    this.current = current;
    const percentage = Math.floor((this.current / this.total) * 100);
    const filledLength = Math.floor((this.current / this.total) * this.barLength);
    const emptyLength = this.barLength - filledLength;
    const bar = '#'.repeat(filledLength) + '-'.repeat(emptyLength);
    const progress = `${this.current}/${this.total}`;
    process.stdout.write(`\r${this.title}: [${bar}] ${percentage}% (${progress}) ${status}`);
    if (current >= this.total) {
      console.log('');
    }
  }

  increment(status = '') {
    this.update(this.current + 1, status);
  }
}

module.exports = ProgressBar;
