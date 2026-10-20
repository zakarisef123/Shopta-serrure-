(function(){
  // Assureurs : liste générée dans assets/js/assureurs.js
  var insurers = window.ASSUREURS || [];
  function initials(n){
    if (/^[A-Z0-9]{2,3}$/.test(n)) return n;
    if (/^[A-Z0-9]{4,5}$/.test(n)) return n.slice(0,2);
    return n.replace(/[^A-Za-zÀ-ÿ ]/g," ").split(" ").filter(Boolean).map(function(w){return w[0]}).join("").slice(0,2).toUpperCase();
  }
  function fallbackChip(i){
    var el = document.createElement("span"), lg = document.createElement("span"), ic = document.createElement("i"), img = new Image();
    el.className = "ins"; lg.className = "lg";
    ic.style.setProperty("--c", i.c); ic.textContent = initials(i.n);
    img.alt = ""; img.loading = "lazy"; img.decoding = "async"; img.referrerPolicy = "no-referrer";
    img.onload = function(){ if (img.naturalWidth > 16) lg.classList.add("ok"); };
    img.src = "https://www.google.com/s2/favicons?sz=128&domain=" + i.d;
    lg.appendChild(ic); lg.appendChild(img);
    el.appendChild(lg);
    el.appendChild(document.createTextNode(i.n));
    el.title = i.n;
    return el;
  }
  function chip(i){
    if (!i.logo) return fallbackChip(i);
    var el = document.createElement("span"), img = new Image();
    el.className = "ins has-logo"; el.title = i.n;
    img.alt = i.n; img.decoding = "async"; img.src = i.logo;
    img.onerror = function(){ el.replaceWith(fallbackChip(i)); };
    el.appendChild(img);
    if (i.label) el.appendChild(document.createTextNode(i.n));
    return el;
  }
  // les assureurs avec logo fourni passent en premier
  insurers = insurers.filter(function(i){return i.logo}).concat(insurers.filter(function(i){return !i.logo}));
  var half = Math.ceil(insurers.length/2);
  [insurers.slice(0,half), insurers.slice(half)].forEach(function(list, idx){
    var track = document.querySelector('.marquee[data-row="'+(idx+1)+'"] .track');
    if (!track) return;
    // deux copies pour une boucle continue
    for (var k=0;k<2;k++) list.forEach(function(i){
      var c = chip(i);
      if (k===1) c.setAttribute("aria-hidden","true");
      track.appendChild(c);
    });
  });

  document.querySelectorAll(".zones-tabs button").forEach(function(b){
    b.addEventListener("click",function(){
      document.querySelectorAll(".zones-tabs button").forEach(function(x){x.setAttribute("aria-selected","false")});
      document.querySelectorAll(".zone-panel").forEach(function(x){x.classList.remove("active")});
      b.setAttribute("aria-selected","true");
      var p=document.getElementById(b.dataset.zone); p.classList.add("active");
    });
  });

  // Header au scroll
  var header = document.querySelector("header.site");
  window.addEventListener("scroll",function(){ header.classList.toggle("scrolled", window.scrollY > 10); },{passive:true});

  // Menu mobile
  var burger = document.querySelector(".burger"), mnav = document.getElementById("mnav");
  burger.addEventListener("click",function(){
    var open = mnav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
  });
  mnav.querySelectorAll("a").forEach(function(a){ a.addEventListener("click",function(){ mnav.classList.remove("open"); burger.setAttribute("aria-expanded","false"); }); });

  // Apparition au scroll
  if ("IntersectionObserver" in window){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); io.unobserve(e.target);} }); },{threshold:.12, rootMargin:"0px 0px -40px 0px"});
    document.querySelectorAll(".reveal").forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function(el){ el.classList.add("in"); });
  }

  // Suivi des clics d'appel / WhatsApp
  document.querySelectorAll("[data-track]").forEach(function(a){
    a.addEventListener("click",function(){ if (window.gtag) gtag("event", a.dataset.track.indexOf("wa")===0 ? "whatsapp_click" : "phone_click", {location:a.dataset.track}); });
  });

  // Formulaire -> WhatsApp
  var form = document.getElementById("contact-form");
  if (form) form.addEventListener("submit",function(e){
    e.preventDefault();
    var f = e.target.elements, name = f.name.value.trim(), tel = f.tel.value.trim();
    if (!name){ f.name.focus(); f.name.style.borderColor="#ef4444"; return; }
    if (!tel){ f.tel.focus(); f.tel.style.borderColor="#ef4444"; return; }
    var txt = "Bonjour Shopta Serrure,\n\nNom : "+name+"\nTéléphone : "+tel+"\nBesoin : "+f.type.value+(f.city.value?"\nVille : "+f.city.value:"")+(f.msg.value?"\n\n"+f.msg.value:"");
    if (window.gtag) gtag("event","generate_lead",{type:f.type.value});
    window.open("https://wa.me/33620546693?text="+encodeURIComponent(txt),"_blank","noopener");
  });

  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
