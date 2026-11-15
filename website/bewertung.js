(function(){
  var form=document.querySelector('[data-lead-form]'); if(!form) return;
  var steps=[].slice.call(form.querySelectorAll('.lead-step'));
  var bar=form.querySelector('[data-lead-bar]'), err=form.querySelector('[data-lead-error]');
  var time=form.querySelector('[data-lead-time]'); if(time) time.value=String(Date.now());
  var cur=0;
  function show(i){cur=i;steps.forEach(function(s,n){s.classList.toggle('is-active',n===i)});if(bar)bar.style.width=((i+1)/steps.length*100)+'%';err.textContent='';
    var f=steps[i].querySelector('input:not([type=radio]),select');if(f&&i>0)f.focus({preventScroll:true});}
  function valid(i){var bad=[].slice.call(steps[i].querySelectorAll('[required]')).filter(function(el){
      if(el.type==='radio'){return !steps[i].querySelector('input[name="'+el.name+'"]:checked');}
      if(el.type==='checkbox'){return !el.checked;}
      if(el.type==='email'){return !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value.trim());}
      return !el.value.trim();});
    if(bad.length){err.textContent='Bitte fülle die markierten Felder aus.';bad.forEach(function(el){el.classList.add('is-invalid');el.addEventListener('input',function(){el.classList.remove('is-invalid')},{once:true})});return false;}
    return true;}
  form.addEventListener('change',function(e){if(e.target.name==='objektart'&&cur===0)show(1);});
  form.addEventListener('click',function(e){
    if(e.target.matches('[data-lead-next]')&&valid(cur))show(cur+1);
    if(e.target.matches('[data-lead-back]'))show(Math.max(0,cur-1));});
  form.addEventListener('submit',function(e){if(!valid(cur)){e.preventDefault();return;}
    if(typeof gtag==='function')gtag('event','form_submit_lead');});
  form.classList.add("is-js"); show(0);
  var m=/[?&]fehler=(\d)/.exec(location.search); if(m){show(2); err.textContent=m[1]==="2"?"Der Versand hat leider nicht geklappt. Bitte schreib mir per WhatsApp oder versuche es erneut.":"Bitte prüfe deine Angaben – einige Pflichtfelder fehlen.";}
})();
