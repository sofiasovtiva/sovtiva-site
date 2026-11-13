/* Sovtiva Editorial 04 — progressive article finder. No calls or tracking. */
(() => {
 'use strict';
 const tools=document.getElementById('discovery-tools'),search=document.getElementById('discovery-search'),
 count=document.getElementById('discovery-count'),surprise=document.getElementById('discovery-surprise'),
 empty=document.getElementById('discovery-empty');
 if(!tools||!search||!count||!surprise||!empty)return;
 const ids=['latest','guides','ai-services','partner-desk'];
 const sections=ids.map(id=>document.getElementById(id)).filter(Boolean);
 const cards=sections.flatMap(section=>Array.from(section.querySelectorAll('.cards .card')).map(card=>({
  card,group:section.id,text:(card.textContent||'').toLocaleLowerCase(),
  link:card.querySelector('a[href^="/journal/"]')
 })));
 if(!cards.length)return;
 const buttons=Array.from(tools.querySelectorAll('[data-journal-filter]'));
 let active='all',visible=[];
 function update(){
  const q=search.value.trim().toLocaleLowerCase();
  visible=cards.filter(item=>{
   const match=(active==='all'||item.group===active)&&(!q||item.text.includes(q));
   item.card.hidden=!match; return match;
  });
  sections.forEach(s=>s.hidden=!visible.some(item=>item.group===s.id));
  count.textContent=visible.length+(visible.length===1?' story':' stories')+' to explore';
  empty.hidden=visible.length!==0;
  surprise.disabled=!visible.some(item=>item.link);
 }
 tools.hidden=false;
 buttons.forEach(b=>b.addEventListener('click',()=>{
  active=b.dataset.journalFilter;
  buttons.forEach(other=>other.setAttribute('aria-pressed',String(other===b)));
  update();
 }));
 search.addEventListener('input',update);
 search.addEventListener('keydown',e=>{if(e.key==='Escape'){search.value='';update();}});
 surprise.addEventListener('click',()=>{
  const hits=visible.filter(item=>item.link);
  if(!hits.length)return;
  window.location.assign(hits[Math.floor(Math.random()*hits.length)].link.href);
 });
 update();
})();