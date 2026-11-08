(() => {
  for (const form of document.querySelectorAll('[data-readiness]')) {
    const checks = [...form.querySelectorAll('input[type="checkbox"]')];
    const output = form.querySelector('output');
    const spanish = form.getAttribute('lang') === 'es';
    const update = () => {
      const count = checks.filter(check => check.checked).length;
      output.textContent = spanish
        ? `${count} de ${checks.length} condiciones verificadas. Revisa las que faltan antes de buscar más distribución.`
        : `${count} of ${checks.length} conditions verified. Fix the gaps before adding more distribution.`;
    };
    checks.forEach(check => check.addEventListener('change', update));
    update();
  }
})();
