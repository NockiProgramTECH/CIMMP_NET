
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
