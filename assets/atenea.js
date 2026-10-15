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
