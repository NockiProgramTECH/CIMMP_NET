
    /* ----------------------------------------------------------
       MODAL – OUVERTURE & FERMETURE
    ---------------------------------------------------------- */
    const overlay    = document.getElementById('modalOverlay');
    const modalClose = document.getElementById('modalClose');

    function openModal(id) {
      const d = predications[id];
      if (!d) return;

      // Image & hero
      document.getElementById('modalImg').src = d.img;
      document.getElementById('modalImg').alt = d.title;
      document.getElementById('modalCat').innerHTML = d.cat;
      document.getElementById('modalTitle').textContent = d.title;
      document.getElementById('modalMeta').innerHTML = d.meta.map(m =>
        `<div class="modal-meta-tag"><i class="fa-solid ${m.icon}"></i> ${m.text}</div>`
      ).join('');

      // Résumé
      const summaryEl = document.getElementById('modalSummary');
      summaryEl.innerHTML = `<h3 class="content-block-title"><i class="fa-solid fa-align-left"></i> Résumé du Message</h3>`
        + d.summary.map(p => `<p>${p}</p>`).join('');

      // Points clés
      document.getElementById('keyPointsList').innerHTML = d.points.map((p, i) =>
        `<div class="key-point">
           <div class="key-point-num">${String(i+1).padStart(2,'0')}</div>
           <p>${p}</p>
         </div>`
      ).join('');

      // Application
      document.getElementById('appList').innerHTML = d.app.map(a =>
        `<div class="application-item"><i class="fa-solid ${a.icon}"></i><p>${a.text}</p></div>`
      ).join('');

      // Verset principal
      document.getElementById('modalVerseRef').innerHTML  = `<i class="fa-solid fa-book-bible"></i> ${d.verseRef}`;
      document.getElementById('modalVerseText').innerHTML =
        `<i class="fa-solid fa-quote-left" style="color:var(--accent-yellow);margin-right:5px;font-size:0.75rem;"></i>${d.verseText}<i class="fa-solid fa-quote-right" style="color:var(--accent-yellow);margin-left:5px;font-size:0.75rem;"></i>`;
      document.getElementById('modalVerseContext').textContent = d.verseCtx;

      // Versets secondaires
      document.getElementById('versesList').innerHTML = d.verses.map(v =>
        `<div class="verse-mini">
           <div class="verse-mini-ref"><i class="fa-solid fa-bookmark"></i> ${v.ref}</div>
           <p class="verse-mini-text">${v.text}</p>
         </div>`
      ).join('');

      // Infos rapides
      document.getElementById('quickInfoList').innerHTML = d.quickInfo.map(q =>
        `<div class="quick-info-row">
           <i class="fa-solid ${q.icon}"></i>
           <div><div class="qi-label">${q.label}</div><div class="qi-val">${q.val}</div></div>
         </div>`
      ).join('');

      // Évaluation
      document.getElementById('modalRatingNum').textContent = d.rating.toFixed(1);
      document.getElementById('modalRatingStars').innerHTML = Array.from({length:5}, (_,i) =>
        `<i class="fa-${i < d.ratingStars ? 'solid' : 'regular'} fa-star"></i>`
      ).join('');
      document.getElementById('modalRatingText').textContent = d.ratingText;

      // Ouvrir
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      overlay.scrollTop = 0;
    }

    function closeModal() {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    modalClose.addEventListener('click', closeModal);
    overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

    // Clic sur les cartes
    document.querySelectorAll('.pred-card').forEach(card => {
      function activate() { openModal(parseInt(card.dataset.id)); }
      card.addEventListener('click', activate);
      card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(); } });
    });

    /* ----------------------------------------------------------
       FILTRE DES CATÉGORIES
    ---------------------------------------------------------- */
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        // (Filtre visuel simple – dans une app réelle, on filtrerait les cartes)
      });
    });

    /* ----------------------------------------------------------
       INTERSECTION OBSERVER – FADE-IN
    ---------------------------------------------------------- */
    const io = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } }),
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    document.querySelectorAll('.fade-in').forEach(el => io.observe(el));

    /* ----------------------------------------------------------
       MENU MOBILE
    ---------------------------------------------------------- */
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const mobileMenu   = document.getElementById('mobileMenu');
    const mobileClose2 = document.getElementById('mobileClose');

    hamburgerBtn.addEventListener('click', () => {
      mobileMenu.classList.add('open');
      hamburgerBtn.setAttribute('aria-expanded','true');
      document.body.style.overflow = 'hidden';
    });
    mobileClose2.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      hamburgerBtn.setAttribute('aria-expanded','false');
      document.body.style.overflow = '';
    });
    document.querySelectorAll('.mobile-menu a').forEach(a => {
      a.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
