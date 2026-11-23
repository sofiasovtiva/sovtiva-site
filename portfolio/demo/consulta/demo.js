(()=>{
'use strict';
const dialog=document.getElementById('appointment');
const service=document.getElementById('sample-service');
const message=document.getElementById('appointment-response');
const continueButton=document.getElementById('simulate-next');
document.querySelectorAll('[data-open-appointment]').forEach(button=>button.addEventListener('click',()=>{if(!dialog||typeof dialog.showModal!=='function')return;service.value='';message.textContent='Selecciona una opción para conocer el siguiente paso.';dialog.showModal()}));
document.querySelectorAll('[data-close-appointment]').forEach(button=>button.addEventListener('click',()=>dialog?.close()));
continueButton?.addEventListener('click',()=>{message.textContent=service.value?'En un sitio real, el siguiente paso consultaría la agenda autorizada para '+service.value.toLowerCase()+'. Aquí no se muestra disponibilidad ni se guarda información.':'Selecciona primero un motivo ilustrativo.'});
dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
const toggle=document.querySelector('.mobile-toggle');
const nav=document.getElementById('nav');
function closeMenu(){nav?.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');toggle?.setAttribute('aria-label','Abrir menú')}
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';nav?.classList.toggle('is-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Cerrar menú':'Abrir menú')});
nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});
})();