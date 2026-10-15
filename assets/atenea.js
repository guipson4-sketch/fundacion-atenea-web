// Fundación Atenea · comportamiento compartido (sin animaciones)
(function(){
  // Mosaico del logo: cuadros estáticos en la paleta de la marca
  var pal=['#C81E73','#EE827C','#F3BC81','#F6E08A','#A3CDF5','#69184B','#8A2BB0'];
  document.querySelectorAll('.tiles').forEach(function(el){
    var s=parseInt(el.getAttribute('data-seed')||'7',10);
    function r(){s=(s*9301+49297)%233280;return s/233280}
    var n=parseInt(el.getAttribute('data-n')||'64',10);
    for(var i=0;i<n;i++){
      var t=document.createElement('i'), v=r();
      if(v>=.45){t.style.background=pal[Math.floor(r()*pal.length)];t.style.opacity=(.35+r()*.65).toFixed(2)}
      el.appendChild(t);
    }
  });

  // Formularios: se guardan en Netlify Forms (panel + aviso por correo).
  // Si el envío falla (p. ej. al abrir el archivo localmente), se ofrece el correo como respaldo.
  var MAIL='contacto@ateneapiuraperu.org';
  document.querySelectorAll('form[data-mail]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var st=f.querySelector('[role=status]'), btn=f.querySelector('button[type=submit]');
      if(!f.checkValidity()){
        if(st){st.textContent='Completa los campos obligatorios.';st.style.color='#D6287F'}
        f.reportValidity(); return;
      }
      var data=new FormData(f);
      if(btn) btn.disabled=true;
      if(st){st.textContent='Enviando…';st.style.color=''}
      fetch('/api/form',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data).toString()})
        .then(function(r){
          if(!r.ok) throw new Error(r.status);
          f.reset();
          if(st){st.textContent='¡Gracias! Recibimos tu mensaje y te responderemos pronto.';st.style.color='#1F7A4D'}
        })
        .catch(function(){
          var lines=[]; data.forEach(function(v,k){ if(['form-name','bot-field','autorizo'].indexOf(k)<0) lines.push(k+': '+v) });
          var subject=f.getAttribute('data-mail'), m=f.querySelector('input[name=motivo]:checked'); if(m) subject=m.value;
          location.href='mailto:'+MAIL+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(lines.join('\n'));
          if(st){st.textContent='Abriendo tu aplicación de correo…'}
        })
        .finally(function(){ if(btn) btn.disabled=false });
    });
  });

  // Donaciones en línea (Mercado Pago vía /api/donar)
  document.querySelectorAll('.donate-form').forEach(function(f){
    var otro=f.querySelector('.otro');
    f.addEventListener('change',function(){ var c=f.querySelector('input[name=monto]:checked'); otro.hidden=!(c&&c.value==='otro') });
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var st=f.querySelector('[role=status]'), btn=f.querySelector('button');
      var c=f.querySelector('input[name=monto]:checked'), monto=c&&c.value==='otro'?f.otro.value:(c&&c.value);
      if(!monto||Number(monto)<5){ st.textContent='Elige o escribe un monto desde S/ 5.'; st.style.color='#D6287F'; return }
      btn.disabled=true; st.textContent='Conectando con la pasarela segura…'; st.style.color='';
      fetch('/api/donar',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({monto:monto,nombre:f.nombre.value,email:f.email.value})})
        .then(function(r){return r.json().catch(function(){return {}}).then(function(d){return {ok:r.ok,d:d}})})
        .then(function(x){ if(x.ok&&x.d.url){location.href=x.d.url;return} st.textContent=(x.d&&x.d.error)||'No pudimos iniciar el pago. Intenta de nuevo o dona por Yape.'; st.style.color='#D6287F'; btn.disabled=false })
        .catch(function(){ st.textContent='Sin conexión. Intenta de nuevo o dona por Yape.'; st.style.color='#D6287F'; btn.disabled=false });
    });
  });
})();

// Asistente de soporte (Gemini vía función del servidor /api/chat)
(function(){
  var WA='https://wa.me/51900000000';
  var open=document.createElement('button');
  open.className='bot-open'; open.type='button';
  open.setAttribute('aria-haspopup','dialog');
  open.innerHTML='<i></i><span>¿Dudas? Pregúntale a Atenea</span>';
  open.setAttribute('aria-label','Abrir asistente de soporte');
  var box=document.createElement('section');
  box.className='bot'; box.hidden=true; box.setAttribute('role','dialog'); box.setAttribute('aria-label','Asistente de soporte');
  box.innerHTML='<div class="bot-h"><div><b>Asistente Atenea</b><small>Respuestas automáticas · Para tu caso, escríbenos</small></div><button class="bot-x" type="button" aria-label="Cerrar">×</button></div>'+
    '<div class="bot-log" aria-live="polite"></div>'+
    '<div class="bot-q"></div>'+
    '<form class="bot-f"><label class="skip" for="bot-in">Tu pregunta</label><textarea id="bot-in" rows="1" maxlength="800" placeholder="Escribe tu pregunta…"></textarea><button type="submit">Enviar</button></form>'+
    '<p class="bot-n">No compartas datos personales, de salud ni detalles de tu caso: este chat usa IA de Google. ¿En peligro? Llama a la Línea 100. <a href="'+WA+'">Hablar con una persona</a></p>';
  document.body.appendChild(open); document.body.appendChild(box);
  var log=box.querySelector('.bot-log'), form=box.querySelector('form'), input=box.querySelector('textarea'),
      send=form.querySelector('button'), quick=box.querySelector('.bot-q');
  var history=[];
  try{history=JSON.parse(sessionStorage.getItem('atenea-chat')||'[]')}catch(e){}
  function save(){try{sessionStorage.setItem('atenea-chat',JSON.stringify(history.slice(-20)))}catch(e){}}
  function add(role,text){var d=document.createElement('div');d.className='msg '+role;d.textContent=text;log.appendChild(d);log.scrollTop=log.scrollHeight;return d}
  function render(){
    log.innerHTML='';
    add('model','Hola, soy el asistente de la Fundación Atenea. Puedo contarte sobre nuestros programas, cómo pedir ayuda, donar o ser voluntaria/o. ¿En qué te ayudo?');
    history.forEach(function(m){add(m.role,m.text)});
    quick.hidden=history.length>0;
  }
  ['¿Cómo pido ayuda?','¿Cómo puedo donar?','Quiero ser voluntaria','¿Qué hace el programa de niñez?'].forEach(function(q){
    var b=document.createElement('button');b.type='button';b.textContent=q;b.onclick=function(){ask(q)};quick.appendChild(b);
  });
  function ask(text){
    text=text.trim(); if(!text||send.disabled) return;
    quick.hidden=true; history.push({role:'user',text:text}); add('user',text); save();
    input.value=''; send.disabled=true;
    var w=add('model wait','Escribiendo…');
    fetch('/api/chat',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({messages:history})})
      .then(function(r){return r.json().catch(function(){return {}}).then(function(d){return {ok:r.ok,d:d}})})
      .then(function(x){
        w.remove();
        if(x.ok&&x.d.reply){history.push({role:'model',text:x.d.reply});add('model',x.d.reply);save()}
        else{history.pop();save();add('err',(x.d&&x.d.error)||'El asistente no está disponible. Escríbenos por WhatsApp al +51 900 000 000.')}
      })
      .catch(function(){w.remove();history.pop();save();add('err','Sin conexión con el asistente. Escríbenos por WhatsApp al +51 900 000 000.')})
      .finally(function(){send.disabled=false;input.focus()});
  }
  form.addEventListener('submit',function(e){e.preventDefault();ask(input.value)});
  input.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();ask(input.value)}});
  function show(v){box.hidden=!v;open.hidden=v;if(v){render();input.focus()}else open.focus()}
  open.onclick=function(){show(true)};
  box.querySelector('.bot-x').onclick=function(){show(false)};
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!box.hidden)show(false)});
})();

// Animaciones al hacer scroll: aparición escalonada, imágenes que se asientan y cifras que cuentan.
(function(){
  var top=document.querySelector('.top');
  if(top){var f=function(){top.classList.toggle('scrolled',window.scrollY>8)};f();window.addEventListener('scroll',f,{passive:true})}
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('anim');
  var sel=['.shead','.statement','.facts > div','.pcard','.cols > .col','.steps > .step','.moms > .mom','.team > .member',
    '.rows > .row','.log .lr','.arts > .art','.trust > div','.dip > *','.pull','.band .wrap > *','.cta h2','.cta .btns',
    '.split > .l','.split > .r','.faq details','.kv > div','.list li','.phero .meta','.foot .big'];
  var els=[];
  sel.forEach(function(s){document.querySelectorAll(s).forEach(function(el){
    if(el.closest('.fb')||el.classList.contains('rv')) return;
    var sib=Array.prototype.indexOf.call(el.parentNode.children,el);
    el.style.setProperty('--d',Math.min(sib,6)*90+'ms');
    el.classList.add('rv'); els.push(el);
  })});
  document.querySelectorAll('.pimg,.dip .tall').forEach(function(el){el.classList.add('rv-img');els.push(el)});
  // cifras: 28,1 % · 4 578 · S/ 120
  function count(el){
    var raw=el.textContent, m=raw.match(/[\d\s.,]*\d/); if(!m) return;
    var num=m[0], dec=(num.split(',')[1]||'').length, val=parseFloat(num.replace(/\s/g,'').replace(/\./g,'').replace(',','.'));
    if(!isFinite(val)) return;
    var t0=null, dur=1400;
    function fmt(v){var s=v.toFixed(dec).split('.');s[0]=s[0].replace(/\B(?=(\d{3})+(?!\d))/g,' ');return s.join(',')}
    function step(t){t0=t0||t;var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);el.textContent=raw.replace(num,fmt(val*e));if(p<1)requestAnimationFrame(step);else el.textContent=raw}
    requestAnimationFrame(step);
  }
  var io=new IntersectionObserver(function(entries){entries.forEach(function(en){
    if(!en.isIntersecting) return;
    var el=en.target; el.classList.add('in'); io.unobserve(el);
    el.querySelectorAll && el.querySelectorAll('.facts strong, strong').forEach(function(s){if(s.closest('.facts'))count(s)});
  })},{rootMargin:'0px 0px -8% 0px',threshold:.12});
  els.forEach(function(el){io.observe(el)});
  // red de seguridad: nada queda oculto si algo falla
  setTimeout(function(){els.forEach(function(el){if(el.getBoundingClientRect().top<innerHeight)el.classList.add('in')})},1500);
})();
