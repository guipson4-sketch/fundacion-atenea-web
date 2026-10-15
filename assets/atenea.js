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

  // Formularios: en esta versión no hay servidor; se arma un correo.
  var MAIL='contacto@fundacionatenea.org';
  document.querySelectorAll('form[data-mail]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var st=f.querySelector('[role=status]');
      if(!f.checkValidity()){
        if(st){st.textContent='Completa los campos obligatorios.';st.style.color='#C81E73'}
        f.reportValidity(); return;
      }
      var lines=[];
      new FormData(f).forEach(function(v,k){ if(k!=='ok') lines.push(k+': '+v) });
      var subject=f.getAttribute('data-mail');
      var m=f.querySelector('input[name=motivo]:checked'); if(m) subject=m.value;
      location.href='mailto:'+MAIL+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(lines.join('\n'));
      if(st){st.textContent='Abriendo tu aplicación de correo…';st.style.color=''}
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
