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
  const partnerMatch = /^partner-(forcoda|pureblue|larsen)-([a-z0-9-]+)$/.exec(source);
  const partnerNames = { forcoda: 'Forcoda', pureblue: 'Pureblue.ai', larsen: 'Larsen Code Labs' };
  const partnerName = partnerMatch ? partnerNames[partnerMatch[1]] : '';
  const solutionCode = partnerMatch ? partnerMatch[2] : '';
  const solutionLabel = solutionCode.replace(/-/g, ' ');
  const partnerContext = document.getElementById('review-partner-context');
  const directServiceRoutes = {
    'solutions-ai-consulting': { en: 'AI consulting and training', es: 'asesoría y capacitación en IA' },
    'solutions-websites': { en: 'website design and maintenance', es: 'diseño y mantenimiento web' },
    'solutions-automation': { en: 'software and workflow automation', es: 'software y automatización' },
    'solutions-social-ai': { en: 'social media workflows', es: 'procesos para redes sociales' },
    'solutions-sales-systems': { en: 'sales workflows', es: 'procesos de ventas' },
    'solutions-client-intake': { en: 'client intake and follow-up', es: 'atención y seguimiento de clientes' },
    'seo-web-diseno-mx': { en: 'website design and maintenance', es: 'diseño y mantenimiento web' }
  };
  const directService = directServiceRoutes[source] || null;
  const directCategory = directService ? 'Sovtiva service: ' + directService.en : '';
  let directServiceOption = null;
  if (directService) {
    directServiceOption = document.createElement('option');
    directServiceOption.value = directCategory;
    document.getElementById('review-category').appendChild(directServiceOption);
    document.getElementById('review-category').value = directCategory;
    form.querySelector('input[name="_subject"]').value = 'Sovtiva service inquiry | ' + directService.en + ' | ' + source;
    partnerContext.hidden = false;
  }
  if (partnerMatch) {
    document.getElementById('review-partner').value = partnerName;
    document.getElementById('review-solution').value = solutionCode;
    document.getElementById('review-category').value = 'Find a technology specialist';
    form.querySelector('input[name="_subject"]').value = 'Sovtiva specialist inquiry | ' + partnerName + ' | ' + source;
    partnerContext.hidden = false;
  }
  const contact = 'sofia.delgado@sovtiva.com';
  const spanish = () => document.documentElement.lang === 'es';
  function translateDirectService() {
    if (!directService) return;
    const name = spanish() ? directService.es : directService.en;
    directServiceOption.textContent = (spanish() ? 'Servicio de Sovtiva: ' : 'Sovtiva service: ') + name;
    document.getElementById('review-partner-kicker').textContent = spanish()
      ? 'CONSULTA DE SERVICIO / SOVTIVA' : 'DIRECT SERVICE REQUEST / SOVTIVA';
    document.getElementById('review-partner-title').textContent = spanish()
      ? 'Hablemos de ' + name : 'Let’s talk about ' + name;
    document.getElementById('review-partner-description').textContent = spanish()
      ? 'Cuéntanos qué necesitas. Sovtiva revisa el alcance contigo; cualquier proyecto se cotiza por separado.'
      : 'Tell us what you need. Sovtiva reviews the scope with you; project work is quoted separately.';
    const heading = document.getElementById('review-title');
    const headingEmphasis = document.createElement('em');
    headingEmphasis.textContent = spanish() ? 'construir o mejorar.' : 'build or improve.';
    heading.replaceChildren(
      document.createTextNode(spanish() ? 'Cuéntanos qué quieres ' : 'Tell us what you want to '),
      headingEmphasis
    );
    document.querySelector('.review-lede').textContent = spanish()
      ? 'Empecemos con tu necesidad concreta. Describe el proyecto y te responderemos por correo.'
      : 'Start with the project you have in mind. Describe what you need and we’ll reply by email.';
    document.querySelector('.review-card h2').textContent = spanish()
      ? 'Cuéntanos sobre tu proyecto.' : 'Tell us about your project.';
    document.querySelector('label[for="review-task"]').textContent = spanish()
      ? '¿Qué necesitas lograr?' : 'What would you like to achieve?';
    document.getElementById('review-task').placeholder = spanish()
      ? 'Describe tu negocio, lo que quieres construir o mejorar y el resultado que buscas.'
      : 'Describe your business, what you want to build or improve, and your intended outcome.';
    document.querySelector('.review-facts li').textContent = spanish()
      ? 'La consulta inicial es gratuita; el trabajo del proyecto se cotiza aparte.'
      : 'The initial inquiry is free; project work is quoted separately.';
    submitButton.textContent = spanish() ? 'Enviar mi consulta →' : 'Send my inquiry →';
    document.querySelector('.review-steps .review-eyebrow').textContent = spanish()
      ? 'SIN BRIEF COMPLICADO' : 'NO LENGTHY PROJECT BRIEF';
    const stepHeading = document.getElementById('review-steps-title');
    const stepEmphasis = document.createElement('em');
    stepEmphasis.textContent = spanish() ? 'Sin procesos eternos.' : 'No drawn-out process.';
    stepHeading.replaceChildren(
      document.createTextNode(spanish() ? 'Un comienzo claro. ' : 'A clear starting point. '),
      stepEmphasis
    );
    const stepText = spanish() ? [
      ['01 / TU PROYECTO', 'Cuéntanos qué necesitas.', 'Describe tu objetivo y las herramientas o la página que usas hoy. Bastan unas frases.'],
      ['02 / ALCANCE', 'Revisamos el proyecto.', 'Aclaramos el alcance y si Sovtiva puede realizarlo o conviene un especialista independiente.'],
      ['03 / SIGUIENTE PASO', 'Tú decides cómo avanzar.', 'Podemos recomendar un primer paso, preparar una cotización aparte o conversar sobre una presentación a un especialista con tu autorización.']
    ] : [
      ['01 / YOUR PROJECT', 'Tell us what you need.', 'Describe your goal and the tools or website you have today. A few sentences are enough.'],
      ['02 / SCOPE & FIT', 'We review the project.', 'We clarify the scope and whether Sovtiva can deliver it or an independent specialist is a better fit.'],
      ['03 / NEXT STEP', 'You choose how to proceed.', 'We can suggest a first step, prepare a separate quote, or discuss a specialist introduction with your permission.']
    ];
    document.querySelectorAll('.review-steps .review-step').forEach((step, index) => {
      if (!stepText[index]) return;
      step.querySelector('span').textContent = stepText[index][0];
      step.querySelector('h3').textContent = stepText[index][1];
      step.querySelector('p').textContent = stepText[index][2];
    });
  }
  function translatePartnerContext() {
    if (!partnerMatch) return;
    document.getElementById('review-partner-kicker').textContent = spanish()
      ? 'CONSULTA DE ESPECIALISTA / POR MEDIO DE SOVTIVA'
      : 'SPECIALIST REQUEST / THROUGH SOVTIVA';
    document.getElementById('review-partner-title').textContent = spanish()
      ? 'Interés en ' + partnerName + ' · ' + solutionLabel
      : 'Interested in ' + partnerName + ' · ' + solutionLabel;
    document.getElementById('review-partner-description').textContent = spanish()
      ? 'Sovtiva recibe tu solicitud primero, valida el encaje y las condiciones de referido. Solo compartiremos tus datos con el especialista si tú lo autorizas.'
      : 'Sovtiva receives your request first, checks fit and referral eligibility, and asks your permission before sharing any details with the provider.';
  }
  document.addEventListener('sovtiva:language', translatePartnerContext);
  if (partnerMatch) translatePartnerContext();
  document.addEventListener('sovtiva:language', translateDirectService);
  if (directService) translateDirectService();
  let prepared = '';

  function prepareFallback() {
    const name = document.getElementById('review-name').value.trim();
    const email = document.getElementById('review-email').value.trim();
    const category = document.getElementById('review-category').value;
    const task = document.getElementById('review-task').value.trim();
    const subject = directService
      ? (spanish() ? 'Consulta de servicio | Sovtiva | ' + directService.es : 'Service inquiry | Sovtiva | ' + directService.en)
      : (spanish() ? 'Diagnóstico gratuito de IA | Sovtiva' : 'Free AI Leverage Review | Sovtiva');
    const body = (spanish() ? [
      'Hola, Sofía:', '', directService ? 'Quisiera consultar un proyecto de ' + directService.es + '.' : 'Me gustaría revisar una tarea que podríamos simplificar.', '',
      `Nombre: ${name}`, `Correo: ${email}`, `Tipo de trabajo: ${category}`, '',
      directService ? 'Lo que necesito:' : 'Así funciona hoy:', task, '',
      `Origen en el sitio: ${source}`, ...(partnerMatch ? [`Especialista: ${partnerName}`, `Solución solicitada: ${solutionLabel}`] : []), '', '¡Gracias!'
    ] : [
      'Hi Sofia,', '', directService ? 'I would like to discuss ' + directService.en + '.' : "I'd like a free first look at a workflow.", '',
      `Name: ${name}`, `Email: ${email}`, `Type of work: ${category}`, '',
      directService ? 'What I need:' : 'What happens now:', task, '',
      `Website source: ${source}`, ...(partnerMatch ? [`Delivery partner: ${partnerName}`, `Requested solution: ${solutionLabel}`] : []), '', 'Thanks!'
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
      // Form reset restores default hidden fields; keep attribution for another request.
      document.getElementById('review-source').value = source;
      if (partnerMatch) {
        document.getElementById('review-partner').value = partnerName;
        document.getElementById('review-solution').value = solutionCode;
        document.getElementById('review-category').value = 'Find a technology specialist';
        form.querySelector('input[name="_subject"]').value = 'Sovtiva specialist inquiry | ' + partnerName + ' | ' + source;
      }
      if (directService) {
        document.getElementById('review-category').value = directCategory;
        form.querySelector('input[name="_subject"]').value = 'Sovtiva service inquiry | ' + directService.en + ' | ' + source;
      }
      status.className = 'review-status review-status-success';
      status.textContent = spanish() ? 'Listo. Recibimos tu solicitud en Sovtiva y te responderemos por correo.' : 'Got it. Your request has been sent to Sovtiva. We’ll reply by email.';
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', {
          method: 'formspree',
          form_id: 'ai_review',
          inquiry_source: source,
          inquiry_type: directService ? 'direct_service' : (partnerMatch ? 'partner_referral' : 'general')
        });
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
