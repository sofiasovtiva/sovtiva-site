/* SOVTIVA / FIELD 03
   Minimal cursor-responsive dot field. Static texture persists in CSS if JS is unavailable.
   No crosshairs, orbital decoration, dependencies, network requests or continuous idle work.
*/
(() => {
  'use strict';
  const hero = document.querySelector('.hero');
  const canvas = document.getElementById('hero-reactive-field');
  if (!hero || !canvas || !window.matchMedia) return;

  const desktop = window.matchMedia('(min-width:881px) and (hover:hover) and (pointer:fine)');
  const reduced = window.matchMedia('(prefers-reduced-motion:reduce)');
  if (!desktop.matches || reduced.matches) return;

  const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
  if (!ctx) return;

  let width = 0;
  let height = 0;
  let ratio = 1;
  let nodes = [];
  let columns = 0;
  let currentX = 0, currentY = 0, targetX = 0, targetY = 0;
  let intensity = 0, targetIntensity = 0, frame = 0;
  let visible = true, lastDraw = 0;

  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));

  function resize() {
    const box = hero.getBoundingClientRect();
    width = Math.max(1, box.width);
    height = Math.max(1, box.height);
    ratio = clamp(window.devicePixelRatio || 1, 1, 1.75);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

    const step = clamp(Math.round(width / 20), 58, 78);
    columns = Math.ceil(width / step) + 2;
    const rows = Math.ceil(height / step) + 2;
    nodes = [];
    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < columns; col += 1) {
        nodes.push({
          x: col * step - step * .36 + Math.sin(row * 1.41 + col * 2.63) * 2,
          y: row * step - step * .36 + Math.cos(row * 2.13 + col * 1.29) * 2
        });
      }
    }
    currentX = targetX = width * .73;
    currentY = targetY = height * .45;
    intensity = targetIntensity = 0;
    paint();
  }

  function paint() {
    ctx.clearRect(0, 0, width, height);
    if (intensity > .009) {
      const radius = 230;
      const halo = ctx.createRadialGradient(currentX, currentY, 0, currentX, currentY, radius);
      halo.addColorStop(0, 'rgba(116,204,210,' + (.07 * intensity).toFixed(3) + ')');
      halo.addColorStop(.5, 'rgba(101,173,185,' + (.025 * intensity).toFixed(3) + ')');
      halo.addColorStop(1, 'rgba(101,173,185,0)');
      ctx.fillStyle = halo;
      ctx.fillRect(currentX - radius, currentY - radius, radius * 2, radius * 2);
    }

    for (let index = 0; index < nodes.length; index += 1) {
      const node = nodes[index];
      const dx = node.x - currentX;
      const dy = node.y - currentY;
      const proximity = Math.max(0, 1 - Math.hypot(dx, dy) / 225);
      const influence = proximity * proximity * intensity;
      const x = node.x + (dx > 0 ? 1 : -1) * influence * 3.5;
      const y = node.y + (dy > 0 ? 1 : -1) * influence * 3.5;

      ctx.beginPath();
      ctx.arc(x, y, .82 + influence * .8, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(169,219,220,' + (.19 + influence * .48).toFixed(3) + ')';
      ctx.fill();

      // A handful of links materialize near the cursor; the rest of the field stays quiet.
      if (influence < .02) continue;
      const right = (index + 1) % columns !== 0 ? nodes[index + 1] : null;
      const down = nodes[index + columns];
      ctx.strokeStyle = 'rgba(158,220,220,' + (influence * .17).toFixed(3) + ')';
      ctx.lineWidth = .75;
      for (const neighbor of [right, down]) {
        if (!neighbor) continue;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(neighbor.x, neighbor.y);
        ctx.stroke();
      }
    }
  }

  function animate(time) {
    frame = 0;
    if (!visible || document.hidden || !desktop.matches || reduced.matches) return;
    if (time - lastDraw < 28) {
      frame = window.requestAnimationFrame(animate);
      return;
    }
    lastDraw = time;
    currentX += (targetX - currentX) * .19;
    currentY += (targetY - currentY) * .19;
    intensity += (targetIntensity - intensity) * .17;
    paint();
    const stillMoving = Math.abs(currentX - targetX) + Math.abs(currentY - targetY) > .55 ||
      Math.abs(intensity - targetIntensity) > .009;
    if (stillMoving) frame = window.requestAnimationFrame(animate);
  }
  function requestPaint() {
    if (!frame && visible && !document.hidden) frame = window.requestAnimationFrame(animate);
  }

  hero.addEventListener('pointermove', event => {
    if (event.pointerType === 'touch') return;
    const box = hero.getBoundingClientRect();
    targetX = clamp(event.clientX - box.left, 0, width);
    targetY = clamp(event.clientY - box.top, 0, height);
    targetIntensity = 1;
    requestPaint();
  }, { passive: true });
  hero.addEventListener('pointerleave', () => {
    targetIntensity = 0;
    requestPaint();
  }, { passive: true });

  document.querySelectorAll('.hero .intent-choice').forEach(card => {
    card.addEventListener('pointermove', event => {
      if (event.pointerType === 'touch') return;
      const box = card.getBoundingClientRect();
      card.style.setProperty('--hover-x', (event.clientX - box.left) + 'px');
      card.style.setProperty('--hover-y', (event.clientY - box.top) + 'px');
    }, { passive: true });
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      visible = Boolean(entries[0] && entries[0].isIntersecting);
      if (!visible && frame) {
        window.cancelAnimationFrame(frame);
        frame = 0;
      }
      if (visible) requestPaint();
    }).observe(hero);
  }
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(hero);
  else window.addEventListener('resize', resize, { passive: true });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && frame) {
      window.cancelAnimationFrame(frame);
      frame = 0;
    } else if (!document.hidden) requestPaint();
  });
  resize();
})();