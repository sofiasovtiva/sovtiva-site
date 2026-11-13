/* Sovtiva / Tech Atelier 01
   Original lightweight pointer-responsive network, no WebGL or dependencies.
   Runs only on desktop fine-pointer devices when reduced motion is not requested.
   Renders on interaction, not in a perpetual idle loop.
*/
(() => {
  'use strict';
  const hero = document.querySelector('.hero');
  const canvas = document.getElementById('hero-reactive-field');
  if (!hero || !canvas || !window.matchMedia) return;

  const allowed = window.matchMedia('(min-width:881px) and (hover:hover) and (pointer:fine)');
  const reduced = window.matchMedia('(prefers-reduced-motion:reduce)');
  if (!allowed.matches || reduced.matches) return;

  const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
  if (!ctx) return;

  let width = 0, height = 0, ratio = 1, nodes = [];
  let currentX = 0, currentY = 0, targetX = 0, targetY = 0;
  let glow = 0, targetGlow = 0, frameId = 0, lastDraw = 0;
  let inView = true;
  const clamp = (n, min, max) => Math.min(max, Math.max(min, n));

  function resize() {
    const rect = hero.getBoundingClientRect();
    width = Math.max(1, rect.width);
    height = Math.max(1, rect.height);
    ratio = Math.min(1.75, Math.max(1, window.devicePixelRatio || 1));
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

    const space = clamp(width / 23, 49, 68);
    const cols = Math.ceil(width / space) + 2;
    const rows = Math.ceil(height / space) + 2;
    nodes = [];
    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < cols; col += 1) {
        const variation = Math.sin(col * 2.37 + row * 1.49);
        nodes.push({
          x: col * space - space / 2 + variation * 3,
          y: row * space - space / 2 + Math.cos(row * 1.93 + col * 1.13) * 3,
          col, row,
          right: col + 1 < cols ? row * cols + col + 1 : -1,
          below: row + 1 < rows ? (row + 1) * cols + col : -1
        });
      }
    }
    currentX = targetX = width * .77;
    currentY = targetY = height * .38;
    glow = targetGlow = 0;
    draw();
  }

  function pointPosition(node) {
    const dx = node.x - currentX;
    const dy = node.y - currentY;
    const distance = Math.hypot(dx, dy);
    const influence = Math.pow(Math.max(0, 1 - distance / 265), 2);
    const shift = influence * glow * 25;
    return {
      x: node.x + (distance > 1 ? dx / distance * shift : 0),
      y: node.y + (distance > 1 ? dy / distance * shift : 0),
      influence
    };
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    const active = glow > .015;
    if (active) {
      const radius = 270;
      const aura = ctx.createRadialGradient(currentX, currentY, 0, currentX, currentY, radius);
      aura.addColorStop(0, 'rgba(83,204,216,' + (.16 * glow).toFixed(3) + ')');
      aura.addColorStop(.38, 'rgba(72,164,195,' + (.09 * glow).toFixed(3) + ')');
      aura.addColorStop(1, 'rgba(65,125,160,0)');
      ctx.fillStyle = aura;
      ctx.fillRect(currentX - radius, currentY - radius, radius * 2, radius * 2);
    }

    const placed = nodes.map(pointPosition);
    for (let i = 0; i < nodes.length; i += 1) {
      const a = placed[i];
      const node = nodes[i];
      for (const next of [node.right, node.below]) {
        if (next === -1) continue;
        const b = placed[next];
        const highlight = Math.max(a.influence, b.influence) * glow;
        ctx.strokeStyle = 'rgba(135,212,228,' + (.085 + highlight * .45).toFixed(3) + ')';
        ctx.lineWidth = .7 + highlight * .55;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
      const hot = a.influence * glow;
      ctx.fillStyle = 'rgba(164,235,233,' + (.29 + hot * .66).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(a.x, a.y, .9 + hot * 1.65, 0, Math.PI * 2);
      ctx.fill();
    }

    if (active) {
      ctx.strokeStyle = 'rgba(184,244,239,' + (.5 * glow).toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(currentX, currentY, 40, -.37 * Math.PI, .33 * Math.PI);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(currentX, currentY, 64, .58 * Math.PI, 1.17 * Math.PI);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(currentX - 11, currentY);
      ctx.lineTo(currentX - 5, currentY);
      ctx.moveTo(currentX + 5, currentY);
      ctx.lineTo(currentX + 11, currentY);
      ctx.moveTo(currentX, currentY - 11);
      ctx.lineTo(currentX, currentY - 5);
      ctx.moveTo(currentX, currentY + 5);
      ctx.lineTo(currentX, currentY + 11);
      ctx.stroke();
    }
  }

  function animate(now) {
    frameId = 0;
    if (!inView || document.hidden || !allowed.matches || reduced.matches) return;
    if (now - lastDraw < 30) {
      frameId = window.requestAnimationFrame(animate);
      return;
    }
    lastDraw = now;
    currentX += (targetX - currentX) * .17;
    currentY += (targetY - currentY) * .17;
    glow += (targetGlow - glow) * .15;
    draw();
    const unsettled = Math.abs(targetX - currentX) + Math.abs(targetY - currentY) > .5 ||
      Math.abs(targetGlow - glow) > .009;
    if (unsettled) frameId = window.requestAnimationFrame(animate);
  }

  function schedule() {
    if (!frameId && inView && !document.hidden) {
      frameId = window.requestAnimationFrame(animate);
    }
  }

  hero.addEventListener('pointermove', (event) => {
    if (event.pointerType === 'touch') return;
    const rect = hero.getBoundingClientRect();
    targetX = clamp(event.clientX - rect.left, 0, width);
    targetY = clamp(event.clientY - rect.top, 0, height);
    targetGlow = 1;
    schedule();
  }, { passive: true });

  hero.addEventListener('pointerleave', () => {
    targetGlow = 0;
    schedule();
  }, { passive: true });

  document.querySelectorAll('.hero .intent-choice').forEach(card => {
    card.addEventListener('pointermove', (event) => {
      if (event.pointerType === 'touch') return;
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--hover-x', (event.clientX - rect.left) + 'px');
      card.style.setProperty('--hover-y', (event.clientY - rect.top) + 'px');
    }, { passive: true });
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      inView = !!entries[0]?.isIntersecting;
      if (!inView && frameId) {
        window.cancelAnimationFrame(frameId);
        frameId = 0;
      }
      if (inView) schedule();
    }, { threshold: 0 });
    observer.observe(hero);
  }

  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(hero);
  else window.addEventListener('resize', resize, { passive: true });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden && frameId) {
      window.cancelAnimationFrame(frameId);
      frameId = 0;
    } else if (!document.hidden) schedule();
  });

  resize();
})();
