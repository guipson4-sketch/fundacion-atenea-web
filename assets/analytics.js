// Google Analytics 4 (se carga solo si build.py define GA_ID). Eventos de conversión:
// generate_lead (formularios), begin_checkout (donación en línea), contact (clic en correo), donate_click.
(function(){
  var s=document.currentScript, id=s&&s.getAttribute('data-ga'); if(!id) return;
  window.dataLayer=window.dataLayer||[];
  window.gtag=function(){dataLayer.push(arguments)};
  gtag('js',new Date()); gtag('config',id,{anonymize_ip:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a'); if(!a) return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('mailto:')===0) gtag('event','contact',{method:'email',link_url:h.slice(7)});
    else if(h.indexOf('#donar')>-1) gtag('event','donate_click',{link_text:(a.textContent||'').trim().slice(0,40)});
  });
})();
