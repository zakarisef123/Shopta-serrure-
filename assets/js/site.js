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
  setTimeout(function(){ document.querySelectorAll(".reveal:not(.in)").forEach(function(el){ el.classList.add("in"); }); }, 3000);

  // Conversions Google Ads (actives si ads_id est renseigné dans _src/build.py)
  function adsConv(kind){
    var to = (window.ADS_CONV || {})[kind];
    if (to && window.gtag) gtag("event","conversion",{send_to:to, value:1.0, currency:"EUR"});
  }
  // Événements Google Tag Manager : clic_appel, clic_whatsapp, envoi_formulaire
  function gtmEvent(name, data){
    window.dataLayer = window.dataLayer || [];
    var e = {event: name, page_path: location.pathname};
    for (var k in data) e[k] = data[k];
    window.dataLayer.push(e);
  }
  // Tous les liens tel: et WhatsApp, même sans data-track (contenu des pages)
  document.querySelectorAll('a[href^="tel:"]:not([data-track]),a[href^="https://wa.me"]:not([data-track])').forEach(function(a){
    a.addEventListener("click",function(){
      var wa = a.href.indexOf("wa.me")>-1;
      if (window.gtag) gtag("event", wa ? "whatsapp_click" : "phone_click", {location:"inline"});
      adsConv(wa ? "wa" : "call");
      gtmEvent(wa ? "clic_whatsapp" : "clic_appel", {emplacement:"contenu", lien:a.getAttribute("href")});
    });
  });

  // Suivi des clics d'appel / WhatsApp
  document.querySelectorAll("[data-track]").forEach(function(a){
    a.addEventListener("click",function(){
      var wa = a.dataset.track.indexOf("wa")===0;
      if (window.gtag) gtag("event", wa ? "whatsapp_click" : "phone_click", {location:a.dataset.track});
      adsConv(wa ? "wa" : "call");
      gtmEvent(wa ? "clic_whatsapp" : "clic_appel", {emplacement:a.dataset.track, lien:a.getAttribute("href")});
    });
  });

  // Formulaires de contact (Netlify Forms) : envoi sans quitter la page
  document.querySelectorAll("form.lead-form").forEach(function(form){
    form.addEventListener("submit", function(e){
      e.preventDefault();
      if (!form.reportValidity()) return;
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true; btn.dataset.label = btn.innerHTML; btn.textContent = "Envoi en cours…";
      fetch("/", {method:"POST", headers:{"Content-Type":"application/x-www-form-urlencoded"},
                  body:new URLSearchParams(new FormData(form)).toString()})
        .then(function(r){
          if (!r.ok) throw new Error(r.status);
          if (window.gtag) gtag("event","generate_lead",{service:form.service.value, page:form.page.value});
          adsConv("form");
          gtmEvent("envoi_formulaire", {service:form.service.value, emplacement:form.page.value});
          form.reset();
          form.querySelector(".form-ok").hidden = false;
          btn.innerHTML = btn.dataset.label; btn.disabled = false;
        })
        .catch(function(){ form.submit(); });
    });
  });

  // Carrousel d'avis : flèches + défilement automatique
  document.querySelectorAll("[data-carousel]").forEach(function(c){
    var track = c.querySelector(".car-track"), prev = c.querySelector(".prev"), next = c.querySelector(".next");
    function step(){ var r = track.querySelector(".review"); return r ? r.getBoundingClientRect().width + 20 : 300; }
    function update(){
      prev.disabled = track.scrollLeft < 5;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 5;
    }
    prev.addEventListener("click", function(){ track.scrollBy({left:-step()}); });
    next.addEventListener("click", function(){ track.scrollBy({left:step()}); });
    track.addEventListener("scroll", update, {passive:true}); update();
    var paused = false;
    ["mouseenter","touchstart","focusin"].forEach(function(ev){ c.addEventListener(ev, function(){ paused = true; }, {passive:true}); });
    c.addEventListener("mouseleave", function(){ paused = false; });
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) setInterval(function(){
      if (paused || document.hidden) return;
      if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 5) track.scrollTo({left:0}); else track.scrollBy({left:step()});
    }, 5000);
  });

  // Grille tarifaire : onglets Journée / Soirée / Nuit, présélection selon l'heure
  document.querySelectorAll("[data-tarifs]").forEach(function(card){
    var tabs = card.querySelectorAll(".tp-tabs button"), now = card.querySelector(".tp-now");
    function show(slot){
      tabs.forEach(function(t){ t.setAttribute("aria-selected", t.dataset.slot === slot ? "true" : "false"); });
      card.querySelectorAll(".tp-val[data-slot]").forEach(function(v){ v.hidden = v.dataset.slot !== slot; });
    }
    tabs.forEach(function(t){ t.addEventListener("click", function(){ show(t.dataset.slot); }); });
    var h = new Date().getHours(), slot = h >= 8 && h < 18 ? "jour" : (h >= 18 && h < 22 ? "soir" : "nuit");
    show(slot);
    var labels = {jour:"journée", soir:"soirée", nuit:"nuit"};
    now.textContent = "Il est " + h + "h : vous voyez le tarif de " + labels[slot] + ".";
    now.hidden = false;
  });

  // Bandeau de consentement (CNIL) : choix mémorisé 6 mois
  var consent = document.getElementById("consent");
  if (consent) {
    if (!window.SS_CONSENT) consent.hidden = false;
    consent.querySelectorAll("[data-consent]").forEach(function(b){
      b.addEventListener("click", function(){
        var v = b.dataset.consent;
        try { localStorage.setItem("ss_consent", JSON.stringify({v:v, t:Date.now()})); } catch(e) {}
        window.SS_CONSENT = v;
        if (v === "granted" && window.ssLoadTags) window.ssLoadTags();
        if (v === "denied" && window.ssTagsLoaded) location.reload();
        consent.hidden = true;
      });
    });
    document.querySelectorAll("[data-open-consent]").forEach(function(b){
      b.addEventListener("click", function(){ consent.hidden = false; });
    });
  }

  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
