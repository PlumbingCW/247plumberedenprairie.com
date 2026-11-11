(function(){
  document.documentElement.classList.remove('nojs');
  var t=document.getElementById('mob-toggle'),d=document.getElementById('mob-drawer'),o=document.getElementById('mob-overlay'),c=document.getElementById('drawer-close');
  function openD(){d.removeAttribute('hidden');o.classList.add('visible');t.setAttribute('aria-expanded','true');t.setAttribute('aria-label','Close navigation menu');document.documentElement.style.overflow='hidden';}
  function closeD(){d.setAttribute('hidden','');o.classList.remove('visible');t.setAttribute('aria-expanded','false');t.setAttribute('aria-label','Open navigation menu');document.documentElement.style.overflow='';}
  if(t&&d&&o){
    t.addEventListener('click',function(){t.getAttribute('aria-expanded')==='true'?closeD():openD();});
    if(c)c.addEventListener('click',closeD);
    o.addEventListener('click',closeD);
    d.querySelectorAll('a').forEach(function(a){a.addEventListener('click',closeD);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')closeD();});
    window.addEventListener('resize',function(){if(window.innerWidth>768)closeD();});
  }
  document.querySelectorAll('.faq-q button').forEach(function(b){
    b.addEventListener('click',function(){
      var item=b.closest('.faq-item');
      var open=item.classList.toggle('open');
      b.setAttribute('aria-expanded',open?'true':'false');
    });
  });
})();
