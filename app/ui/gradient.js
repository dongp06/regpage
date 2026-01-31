const RESET = '\x1b[0m';

function gradient(text, startRGB = [0, 200, 255], endRGB = [180, 100, 255]) {
  if (!text || text.length === 0) return text;
  const [r1, g1, b1] = startRGB;
  const [r2, g2, b2] = endRGB;
  let out = '';
  const n = text.length;
  for (let i = 0; i < n; i++) {
    const t = n > 1 ? i / (n - 1) : 1;
    const r = Math.round(r1 + (r2 - r1) * t);
    const g = Math.round(g1 + (g2 - g1) * t);
    const b = Math.round(b1 + (b2 - b1) * t);
    out += `\x1b[38;2;${r};${g};${b}m${text[i]}`;
  }
  return out + RESET;
}

module.exports = { gradient, RESET };
