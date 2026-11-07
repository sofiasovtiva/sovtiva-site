(() => {
  const form = document.getElementById('review-form');
  const status = document.getElementById('review-status');
  const fallback = document.getElementById('review-fallback');
  const output = document.getElementById('review-copy-text');
  const copyButton = document.getElementById('review-copy');
  const submitButton = form?.querySelector('[type="submit"]');
  if (!form || !status || !fallback || !output || !copyButton || !submitButton) return;

  const params = new URLSearchParams(location.search);
  const source = (params.get('from') || 'direct').replace(/[^a-z0-9-]/gi, '').slice(0,45) || 'direct';
  document.getElementById('review-source').value = source;
  const contact = 'sofia.delgado@sovtiva.com';
  const spanish = () => document.documentElement.lang === 'es';
  let prepared = '';

  function prepareFallback() {
    const name = document.getElementById('review-name').value.trim();
    const email = document.getElementById('review-email').value.trim();
    const category = document.getElementById('review-category').value;
    const task = document.getElementById('review-task').value.trim();
    const subject = spanish() ? 'Diagnóstico gratuito de IA | Sovtiva' : 'Free AI Leverage Review | Sovtiva';
    const body = (spanish() ? [
      'Hola, Sofía:', '', 'Me gustaría revisar una tarea que podríamos simplificar.', '',
      `Nombre: ${name}`, `Correo: ${email}`, `Tipo de trabajo: ${category}`, '',
      'Así funciona hoy:', task, '',
      `Origen en el sitio: ${source}`, '', '¡Gracias!'
    ] : [
      'Hi Sofia,', '', "I'd like a free first look at a workflow.", '',
      `Name: ${name}`, `Email: ${email}`, `Type of work: ${category}`, '',
      'What happens now:', task, '',
      `Website source: ${source}`, '', 'Thanks!'
    ]).join('\n');
    prepared = `To: ${contact}\nSubject: ${subject}\n\n${body}`;
    output.value = prepared;
    fallback.hidden = false;
    copyButton.textContent = spanish() ? 'Copiar mensaje' : 'Copy note';
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    fallback.hidden = true;
    status.hidden = false;
    status.className = 'review-status';
    status.textContent = spanish() ? 'Enviando tu solicitud…' : 'Sending your request…';
    submitButton.disabled = true;

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) {
        const result = await response.json().catch(() => ({}));
        const error = Array.isArray(result.errors) ? result.errors.map(item => item.message).join(' ') : '';
        throw new Error(error || 'The form service could not accept your request.');
      }
      form.reset();
      status.className = 'review-status review-status-success';
      status.textContent = spanish() ? 'Listo. Recibimos tu solicitud en Sovtiva y te responderemos por correo.' : 'Got it. Your request has been sent to Sovtiva. We’ll reply by email.';
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { method: 'formspree', form_id: 'ai_review' });
      }
    } catch (error) {
      status.className = 'review-status review-status-error';
      status.textContent = spanish()
        ? `No se pudo enviar. ${error.message || 'Inténtalo de nuevo.'} Puedes usar la opción de correo de abajo.`
        : `Not sent. ${error.message || 'Please try again.'} You can use the email option below.`;
      prepareFallback();
    } finally {
      submitButton.disabled = false;
    }
  });

  copyButton.addEventListener('click', async () => {
    if (!prepared) return;
    try {
      await navigator.clipboard.writeText(prepared);
      copyButton.textContent = spanish() ? 'Copiado ✓' : 'Copied ✓';
    } catch {
      output.focus();
      output.select();
      copyButton.textContent = spanish() ? 'Selecciona y copia el mensaje de arriba' : 'Select and copy the note above';
    }
  });
})();
