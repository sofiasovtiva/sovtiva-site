(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  if (!toggle || !nav) return;
  const close = () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) close();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') close();
  });
  const choices = [...document.querySelectorAll('.intent-choice')];
  const preview = document.querySelector('.intent-preview-text');
  const original = preview?.textContent;
  if (preview && choices.length) {
    const activate = choice => {
      choices.forEach(c => c.classList.toggle('is-active', c === choice));
      preview.textContent = `${choice.dataset.label}: ${choice.dataset.preview}`;
    };
    const reset = () => {
      choices.forEach(c => c.classList.remove('is-active'));
      preview.textContent = original;
    };
    choices.forEach(choice => {
      choice.addEventListener('mouseenter', () => activate(choice));
      choice.addEventListener('focus', () => activate(choice));
      choice.addEventListener('mouseleave', reset);
      choice.addEventListener('blur', reset);
    });
  }
  // Optional editorial exploration: the original three clear destination links always remain.
  const dice = document.getElementById('discover-dice');
  if (dice) {
    const links = [...document.querySelectorAll('.discover-trails .discover-trail[href]')];
    dice.addEventListener('click', () => {
      if (!links.length) return;
      const choice = links[Math.floor(Math.random() * links.length)];
      window.location.assign(choice.href);
    });
  }
})();
