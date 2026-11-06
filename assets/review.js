(() => {
  const form = document.getElementById('review-form');
  const fallback = document.getElementById('review-fallback');
  const output = document.getElementById('review-copy-text');
  const copyButton = document.getElementById('review-copy');
  if (!form || !fallback || !output || !copyButton) return;

  const params = new URLSearchParams(location.search);
  const source = (params.get('from') || 'direct').replace(/[^a-z0-9-]/gi, '').slice(0,45) || 'direct';
  const contact = 'sofia.delgado@sovtiva.com';
  let prepared = '';

  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const category = document.getElementById('review-category').value;
    const task = document.getElementById('review-task').value.trim();
    if (task.length < 12) {
      document.getElementById('review-task').setCustomValidity('Please tell us a little more about the task.');
      form.reportValidity();
      return;
    }

    const subject = 'Free AI Leverage Review | SOVTIVA';
    const body = [
      'Hi Sofia,',
      '',
      "I'd like a free first look at a workflow.",
      '',
      `Type of work: ${category}`,
      '',
      'What happens now:',
      task,
      '',
      `Website source: ${source}`,
      '',
      'Thanks!'
    ].join('\n');
    prepared = `To: ${contact}\nSubject: ${subject}\n\n${body}`;
    output.value = prepared;
    fallback.hidden = false;
    copyButton.textContent = 'Copy note';
    location.href = `mailto:${contact}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });

  document.getElementById('review-task').addEventListener('input', event => {
    event.target.setCustomValidity('');
  });

  copyButton.addEventListener('click', async () => {
    if (!prepared) return;
    try {
      await navigator.clipboard.writeText(prepared);
      copyButton.textContent = 'Copied ✓';
    } catch {
      output.focus();
      output.select();
      copyButton.textContent = 'Select and copy the note above';
    }
  });
})();
