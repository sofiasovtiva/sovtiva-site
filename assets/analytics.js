/* sovtiva website analytics. No Google request is made before opt-in. */
(() => {
  'use strict';

  const measurementId = 'G-M3D4CMY2XM';
  const consentKey = 'sovtiva_analytics_consent_v1';
  const currentLanguage = () => (document.documentElement.lang || '').toLowerCase().startsWith('es') ? 'es' : 'en';

  function storedChoice() {
    try { return localStorage.getItem(consentKey); } catch (_) { return null; }
  }

  function rememberChoice(value) {
    try { localStorage.setItem(consentKey, value); } catch (_) { /* Session-only consent. */ }
  }

  function enableAnalytics() {
    if (typeof window.gtag === 'function') return;

    // Preserve campaign attribution without sending arbitrary query parameters
    // (which may contain names, emails or other information) to Analytics.
    const publicUrl = new URL(window.location.href);
    const campaignKeys = new Set(['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'from']);
    for (const key of [...publicUrl.searchParams.keys()]) {
      const value = publicUrl.searchParams.get(key) || '';
      if (!campaignKeys.has(key.toLowerCase()) || value.length > 120 || value.includes('@')) {
        publicUrl.searchParams.delete(key);
      }
    }
    publicUrl.hash = '';
    // Keep the referring website, but strip its query string and fragment.
    let safeReferrer = '';
    try {
      const referrer = document.referrer && new URL(document.referrer);
      if (referrer && /^https?:$/.test(referrer.protocol)) safeReferrer = referrer.origin + referrer.pathname;
    } catch (_) { /* An invalid referrer should not prevent the visit. */ }

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      send_page_view: true,
      page_location: publicUrl.toString(),
      page_referrer: safeReferrer,
      page_title: document.title,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });

    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    document.head.appendChild(script);
  }

  function askConsent() {
    const style = document.createElement('style');
    style.textContent = `
      #sovtiva-analytics-choice { position:fixed; bottom:18px; left:18px; right:18px; z-index:9999;
        max-width:560px; padding:19px 21px; border:1px solid #d4cbc1; border-radius:15px;
        background:#f4eee6; box-shadow:0 12px 36px rgba(20,23,23,.20); color:#22252a;
        font:14px/1.5 system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; }
      #sovtiva-analytics-choice strong { display:block; font-size:15px; margin-bottom:5px; }
      #sovtiva-analytics-choice p { margin:0 0 14px; max-width:48ch; }
      #sovtiva-analytics-choice .actions { display:flex; flex-wrap:wrap; gap:10px; }
      #sovtiva-analytics-choice button { cursor:pointer; padding:9px 15px; font:600 13px system-ui,sans-serif;
        border-radius:8px; border:1px solid #383e42; }
      #sovtiva-analytics-yes { color:#fff; background:#383e42; }
      #sovtiva-analytics-no { color:#383e42; background:transparent; }
      #sovtiva-analytics-choice button:focus-visible { outline:3px solid #568fc4; outline-offset:2px; }
      @media (max-width:600px) { #sovtiva-analytics-choice { bottom:10px; left:10px; right:10px; padding:16px; } }
    `;
    document.head.appendChild(style);

    const banner = document.createElement('section');
    banner.id = 'sovtiva-analytics-choice';
    banner.setAttribute('role', 'region');
    const title = document.createElement('strong');
    const description = document.createElement('p');
    const actions = document.createElement('div');
    actions.className = 'actions';
    const yes = document.createElement('button');
    yes.type = 'button';
    yes.id = 'sovtiva-analytics-yes';
    const no = document.createElement('button');
    no.type = 'button';
    no.id = 'sovtiva-analytics-no';
    const translateChoice = () => {
      const spanish = currentLanguage() === 'es';
      banner.setAttribute('aria-label', spanish ? 'Preferencias de analítica' : 'Analytics preferences');
      title.textContent = spanish ? '¿Nos ayudas a mejorar el sitio?' : 'Help us make this site more useful?';
      description.textContent = spanish
        ? 'Si aceptas, Google Analytics medirá visitas y solicitudes exitosas. No enviamos el contenido de formularios. Puedes rechazarlo y seguir navegando.'
        : 'If you agree, Google Analytics will measure visits and successful inquiries. We do not send form contents. You can say no and keep browsing.';
      yes.textContent = spanish ? 'Aceptar analítica' : 'Allow analytics';
      no.textContent = spanish ? 'No, gracias' : 'No, thanks';
    };
    const dismiss = () => {
      document.removeEventListener('sovtiva:language', translateChoice);
      banner.remove();
    };

    yes.addEventListener('click', () => {
      rememberChoice('yes');
      dismiss();
      enableAnalytics();
    });
    no.addEventListener('click', () => {
      rememberChoice('no');
      dismiss();
    });
    actions.append(yes, no);
    banner.append(title, description, actions);
    translateChoice();
    document.addEventListener('sovtiva:language', translateChoice);
    document.body.appendChild(banner);
  }

  function init() {
    const choice = storedChoice();
    if (choice === 'yes') enableAnalytics();
    else if (choice !== 'no') askConsent();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
