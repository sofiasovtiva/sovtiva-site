/* sovtiva website analytics. No Google request is made before opt-in. */
(() => {
  'use strict';

  const measurementId = 'G-M3D4CMY2XM';
  const consentKey = 'sovtiva_analytics_consent_v1';
  const language = (document.documentElement.lang || '').toLowerCase().startsWith('es') ? 'es' : 'en';

  function storedChoice() {
    try { return localStorage.getItem(consentKey); } catch (_) { return null; }
  }

  function rememberChoice(value) {
    try { localStorage.setItem(consentKey, value); } catch (_) { /* Session-only consent. */ }
  }

  function enableAnalytics() {
    if (typeof window.gtag === 'function') return;

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      send_page_view: true,
      page_location: window.location.origin + window.location.pathname,
      page_referrer: '',
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
    banner.setAttribute('aria-label', language === 'es' ? 'Preferencias de analítica' : 'Analytics preferences');
    const title = document.createElement('strong');
    title.textContent = language === 'es' ? '¿Nos ayudas a mejorar el sitio?' : 'Help us make this site more useful?';
    const description = document.createElement('p');
    description.textContent = language === 'es'
      ? 'Si aceptas, Google Analytics medirá visitas y solicitudes exitosas. No enviamos el contenido de formularios. Puedes rechazarlo y seguir navegando.'
      : 'If you agree, Google Analytics will measure visits and successful inquiries. We do not send form contents. You can say no and keep browsing.';
    const actions = document.createElement('div');
    actions.className = 'actions';
    const yes = document.createElement('button');
    yes.type = 'button';
    yes.id = 'sovtiva-analytics-yes';
    yes.textContent = language === 'es' ? 'Aceptar analítica' : 'Allow analytics';
    const no = document.createElement('button');
    no.type = 'button';
    no.id = 'sovtiva-analytics-no';
    no.textContent = language === 'es' ? 'No, gracias' : 'No, thanks';

    yes.addEventListener('click', () => {
      rememberChoice('yes');
      banner.remove();
      enableAnalytics();
    });
    no.addEventListener('click', () => {
      rememberChoice('no');
      banner.remove();
    });
    actions.append(yes, no);
    banner.append(title, description, actions);
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
