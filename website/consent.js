/* consent.js – Cookie-Banner + Google Analytics/Ads mit Einwilligung (Consent Mode v2).
   Auf jeder Seite im <head> einbinden:  <script src="consent.js"></script>
   Google-Ads-ID und Conversion-Label später unten in C eintragen ("ads", "adsLabel"). */
window.dataLayer=window.dataLayer||[];
if(typeof window.gtag!=='function'){window.gtag=function(){dataLayer.push(arguments);};}
gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});
gtag('set','ads_data_redaction',true);gtag('set','url_passthrough',false);

(function(){
var CSS=".cm{position:fixed;left:0;right:0;bottom:0;z-index:200;display:flex;justify-content:center;padding:0 12px calc(12px + env(safe-area-inset-bottom));pointer-events:none;opacity:0;transform:translateY(16px);transition:opacity 280ms var(--ease-out,cubic-bezier(.23,1,.32,1)),transform 280ms var(--ease-out,cubic-bezier(.23,1,.32,1))}\n.cm[hidden]{display:none}\n.cm.on{opacity:1;transform:none}\n.cm-card{pointer-events:auto;width:100%;max-width:780px;max-height:86svh;overflow-y:auto;overscroll-behavior:contain;background:var(--navy2,#0f2238);color:var(--text,#eaf1f8);border:1px solid var(--line,rgba(255,255,255,.14));border-radius:20px;padding:22px 20px;box-shadow:0 18px 60px rgba(0,0,0,.55);font:400 14px/1.55 var(--sans,system-ui,sans-serif)}\n.cm-card:focus{outline:none}\n.cm h2{font:600 22px/1.2 var(--serif,Georgia,serif);margin:0 0 8px;color:var(--text,#fff)}\n.cm p{margin:0 0 10px;color:var(--muted,#9fb2c6)}\n.cm a{color:var(--cyan,#4fd8ff);text-underline-offset:3px}\n.cm-row{display:grid;gap:8px;margin-top:14px}\n@media(min-width:620px){.cm-row{grid-template-columns:repeat(3,1fr)}}\n.cm-btn{appearance:none;font:600 15px/1 var(--sans,system-ui,sans-serif);min-height:48px;padding:0 16px;border-radius:14px;border:1px solid var(--gold,#d9b46a);background:transparent;color:var(--text,#fff);cursor:pointer;transition:transform 160ms var(--ease-out,cubic-bezier(.23,1,.32,1)),background-color 160ms var(--ease-out,cubic-bezier(.23,1,.32,1))}\n.cm-btn:active{transform:scale(.97)}\n.cm-btn:focus-visible,.cm-sw input:focus-visible+i,.cm-lnk:focus-visible{outline:2px solid var(--cyan,#4fd8ff);outline-offset:3px}\n@media(hover:hover) and (pointer:fine){.cm-btn:hover{background:rgba(217,180,106,.14)}}\n.cm-opt{border-top:1px solid var(--line,rgba(255,255,255,.14));padding:14px 0 4px;margin-top:10px}\n.cm-opt:first-of-type{margin-top:6px}\n.cm-h{display:flex;align-items:center;justify-content:space-between;gap:14px}\n.cm-h b{font-weight:600;color:var(--text,#fff);font-size:15px}\n.cm-opt p{margin:6px 0 8px;font-size:13px}\n.cm-meta{font-size:12px;color:var(--muted,#9fb2c6);opacity:.9}\n.cm-sw{position:relative;flex:none;width:52px;height:30px;display:inline-block;cursor:pointer}\n.cm-sw input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:pointer;z-index:1}\n.cm-sw i{position:absolute;inset:0;border-radius:99px;background:rgba(255,255,255,.16);border:1px solid var(--line,rgba(255,255,255,.2));transition:background-color 200ms var(--ease-out,cubic-bezier(.23,1,.32,1))}\n.cm-sw i::after{content:\"\";position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;transition:transform 200ms var(--ease-out,cubic-bezier(.23,1,.32,1))}\n.cm-sw input:checked+i{background:var(--cyan,#4fd8ff)}\n.cm-sw input:checked+i::after{transform:translateX(22px);background:#06182a}\n.cm-sw input:disabled{cursor:not-allowed}.cm-sw input:disabled+i{opacity:.55}\n.cm-lnk{appearance:none;background:none;border:0;padding:0;margin:0;font:inherit;color:inherit;text-decoration:underline;text-underline-offset:3px;cursor:pointer}\nfooter .cm-lnk{color:var(--muted)}\n@media(prefers-reduced-motion:reduce){.cm,.cm-btn,.cm-sw i,.cm-sw i::after{transition:none}}";
var HTML="<div class=\"cm\" id=\"cm\" hidden>\n <div class=\"cm-card\" role=\"dialog\" aria-labelledby=\"cm-t\" aria-describedby=\"cm-d\" tabindex=\"-1\" id=\"cm-card\">\n  <div id=\"cm-l1\">\n   <h2 id=\"cm-t\">Deine Daten, deine Entscheidung</h2>\n   <p id=\"cm-d\">Diese Seite funktioniert auch ohne Tracking. Mit deiner Einwilligung messe ich zusätzlich, wie sie genutzt wird (Google Analytics), und schalte Werbung bei Google. Dabei können Daten an Anbieter in den USA übermittelt werden. Du entscheidest selbst und kannst jede Auswahl jederzeit über „Cookie-Einstellungen“ im Seitenende ändern oder widerrufen.</p>\n   <p style=\"margin:0\"><a href=\"datenschutz.html\">Datenschutzerklärung</a> · <a href=\"impressum.html\">Impressum</a></p>\n   <div class=\"cm-row\">\n    <button type=\"button\" class=\"cm-btn\" data-cm=\"none\">Alle ablehnen</button>\n    <button type=\"button\" class=\"cm-btn\" data-cm=\"settings\">Einstellungen</button>\n    <button type=\"button\" class=\"cm-btn\" data-cm=\"all\">Alle akzeptieren</button>\n   </div>\n  </div>\n  <div id=\"cm-l2\" hidden>\n   <h2>Cookie-Einstellungen</h2>\n   <p>Wähle, was du erlaubst. Nichts davon ist vorausgewählt, außer dem, was die Seite zum Funktionieren braucht.</p>\n   <div class=\"cm-opt\">\n    <div class=\"cm-h\"><b>Notwendig</b><span class=\"cm-sw\"><input type=\"checkbox\" checked disabled aria-label=\"Notwendig, immer aktiv\"><i></i></span></div>\n    <p>Speichert deine Cookie-Entscheidung und sorgt dafür, dass die Seite sicher und fehlerfrei läuft. Ohne diese Technik ist die Seite nicht nutzbar, deshalb ist sie immer aktiv.</p>\n    <div class=\"cm-meta\">Speicherung der Entscheidung im Browser (ms_consent), bis zu 6 Monate.</div>\n   </div>\n   <div class=\"cm-opt\">\n    <div class=\"cm-h\"><b>Statistik (Google Analytics 4)</b><label class=\"cm-sw\"><input type=\"checkbox\" id=\"cm-stat\" aria-label=\"Statistik erlauben\"><i></i></label></div>\n    <p>Zeigt mir, welche Seiten gelesen werden und woher Besucher kommen, damit ich die Seite verbessern kann.</p>\n    <div class=\"cm-meta\">Anbieter: Google Ireland Limited / Google LLC (USA). Cookies _ga, _ga_*, bis zu 2 Jahre.</div>\n   </div>\n   <div class=\"cm-opt\">\n    <div class=\"cm-h\"><b>Werbung Google (Google Ads)</b><label class=\"cm-sw\"><input type=\"checkbox\" id=\"cm-gads\" aria-label=\"Google Ads erlauben\"><i></i></label></div>\n    <p>Misst, ob eine Google-Anzeige zu einer Anfrage geführt hat, und ermöglicht Werbung für Besucher dieser Seite (Remarketing).</p>\n    <div class=\"cm-meta\">Anbieter: Google Ireland Limited / Google LLC (USA). Cookies _gcl_*, bis zu 90 Tage.</div>\n   </div>\n   <p style=\"margin:14px 0 0;font-size:12px\">Terminbuchung (Calendly), WhatsApp und das Bewertungstool (Immoinvent) laden erst, wenn du sie selbst öffnest. Dann gelten deren Datenschutzhinweise. Mehr dazu in der <a href=\"datenschutz.html\">Datenschutzerklärung</a>.</p>\n   <div class=\"cm-row\">\n    <button type=\"button\" class=\"cm-btn\" data-cm=\"none\">Alle ablehnen</button>\n    <button type=\"button\" class=\"cm-btn\" data-cm=\"save\">Auswahl speichern</button>\n    <button type=\"button\" class=\"cm-btn\" data-cm=\"all\">Alle akzeptieren</button>\n   </div>\n  </div>\n </div>\n</div>";
function init(){
  if(document.getElementById('cm'))return;
  var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
  document.body.insertAdjacentHTML('beforeend',HTML);
  if(!document.querySelector('[data-cm-open]')){
    var f=document.querySelector('footer .wrap')||document.querySelector('footer')||document.body;
    f.insertAdjacentHTML('beforeend','<p style="margin:14px 0 0;font-size:13px"><button type="button" class="cm-lnk" data-cm-open>Cookie-Einstellungen</button></p>');
  }
  run();
}
function run(){
(function(){
  var C={"ga4": "G-VQ73DJ6CFV", "ads": "", "adsLabel": "", "ver": 2, "days": 180}, KEY='ms_consent', mem=null, applied={stat:false,gads:false}, loaded=false, opener=null;
  var $=function(i){return document.getElementById(i);};
  function now(){return Date.now();}
  function read(){
    var raw=null;try{raw=localStorage.getItem(KEY);}catch(e){}
    var s=null;try{s=raw?JSON.parse(raw):mem;}catch(e){s=mem;}
    if(!s||s.v!==C.ver||!s.ts||now()-s.ts>C.days*864e5)return null;
    return s;
  }
  function write(s){mem=s;try{localStorage.setItem(KEY,JSON.stringify(s));}catch(e){}}
  function script(src,cb){var el=document.createElement('script');el.async=true;el.src=src;if(cb)el.onload=cb;document.head.appendChild(el);}

  function delCookies(){
    var host=location.hostname,parts=host.split('.'),doms=[host,'.'+host];
    for(var i=1;i<parts.length-1;i++)doms.push('.'+parts.slice(i).join('.'));
    document.cookie.split(';').forEach(function(c){
      var n=c.split('=')[0].trim();
      if(/^(_ga|_gid|_gat|_gcl_|_gac_|_fbp|_fbc|FPAU|FPGCLAW|FPLC)/.test(n)){
        doms.forEach(function(d){document.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain='+d;});
        document.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
      }
    });
  }

  function loadGoogle(s){
    var first=(s.stat&&C.ga4)?C.ga4:((s.gads&&C.ads)?C.ads:'');
    if(!first)return;
    if(!loaded){loaded=true;gtag('js',new Date());script('https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(first));}
    if(s.stat&&C.ga4&&!applied.stat){gtag('config',C.ga4);applied.stat=true;}
    if(s.gads&&C.ads&&!applied.gads){gtag('config',C.ads);applied.gads=true;}
  }

  function apply(s,prev){
    gtag('consent','update',{
      analytics_storage:s.stat?'granted':'denied',
      ad_storage:s.gads?'granted':'denied',
      ad_user_data:s.gads?'granted':'denied',
      ad_personalization:s.gads?'granted':'denied'
    });
    if(prev&&((prev.stat&&!s.stat)||(prev.gads&&!s.gads))){delCookies();location.reload();return;}
    if(s.stat||s.gads)loadGoogle(s);
    window.MSConsent.state=s;
  }

  function show(layer){
    var cm=$('cm');cm.hidden=false;
    $('cm-l1').hidden=layer!==1;$('cm-l2').hidden=layer!==2;
    var s=read()||{stat:false,gads:false};
    $('cm-stat').checked=!!s.stat;$('cm-gads').checked=!!s.gads;
    requestAnimationFrame(function(){cm.classList.add('on');});
  }
  function hide(){
    var cm=$('cm');cm.classList.remove('on');
    setTimeout(function(){cm.hidden=true;},300);
    if(opener&&opener.focus){try{opener.focus();}catch(e){}}opener=null;
  }
  function decide(kind){
    var prev=read(),s={v:C.ver,ts:now(),stat:false,gads:false};
    if(kind==='all'){s.stat=s.gads=true;}
    else if(kind==='save'){s.stat=$('cm-stat').checked;s.gads=$('cm-gads').checked;}
    write(s);hide();apply(s,prev);
  }

  window.MSConsent={
    state:null,
    open:function(){opener=document.activeElement;show(2);setTimeout(function(){$('cm-card').focus();},50);}
  };

  document.addEventListener('click',function(e){
    var t=e.target.closest?e.target.closest('[data-cm],[data-cm-open]'):null;
    if(t){
      if(t.hasAttribute('data-cm-open')){e.preventDefault();window.MSConsent.open();return;}
      var k=t.getAttribute('data-cm');
      if(k==='settings'){$('cm-l1').hidden=true;$('cm-l2').hidden=false;$('cm-card').focus();return;}
      decide(k);return;
    }
    var a=e.target.closest?e.target.closest('a[href]'):null;if(!a)return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('calendly.com')>-1)track('termin');
    else if(h.indexOf('wa.me')>-1)track('whatsapp');
    else if(h.indexOf('wert-radar')>-1)track('wertradar');
  },true);

  function track(name){
    var s=window.MSConsent.state;if(!s)return;
    try{
      if(s.stat&&C.ga4&&window.gtag)gtag('event',name+'_klick');
      if(s.gads&&C.ads&&C.adsLabel&&name!=='wertradar'&&window.gtag)gtag('event','conversion',{send_to:C.ads+'/'+C.adsLabel});
    }catch(e){}
  }
  window.msTrack=track;

  var s0=read();
  if(s0){apply(s0,null);}else{show(1);}
})();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
