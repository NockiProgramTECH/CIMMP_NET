

    'use strict';
    const URL_SUBMIT = '/submit-temoignage/';
    

    /* Navbar scroll */
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });

    /* Smooth scroll sur toutes les ancres */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' });
        closeMobileMenu();
      });
    });

    /* Menu mobile */
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const mobileMenu   = document.getElementById('mobileMenu');
    const mobileClose  = document.getElementById('mobileClose');

    function openMobileMenu() {
      mobileMenu.classList.add('open');
      hamburgerBtn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
    function closeMobileMenu() {
      mobileMenu.classList.remove('open');
      hamburgerBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
    hamburgerBtn.addEventListener('click', openMobileMenu);
    mobileClose.addEventListener('click', closeMobileMenu);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobileMenu(); });

    /* Intersection Observer – fade-in */
    const io = new IntersectionObserver(
      entries => entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); io.unobserve(entry.target); }
      }),
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    document.querySelectorAll('.fade-in').forEach(el => io.observe(el));

    /* Formulaire témoignage – validation */
    const form        = document.getElementById('temoignageForm');
    const formSuccess = document.getElementById('formSuccess');
    const submitBtn   = document.getElementById('submitBtn');


function validateField(id, rule) {
  const f = document.getElementById(id);
  const e = document.getElementById(`${id}-error`);
  const ok = rule(f.value.trim());

  f.classList.toggle('error', !ok);
  if (e) e.classList.toggle('visible', !ok);

  return ok;
}

form.addEventListener('submit', function (e) {
  e.preventDefault();

  const ok =
    validateField('prenom', v => v.length > 0) &&
    validateField('nom', v => v.length > 0) &&
    validateField('telephone', v => /^[\d\s+\-]{8,}$/.test(v)) &&
    validateField('categorie', v => v.length > 0) &&
    validateField('message', v => v.length >= 20);

  // ❗ Si invalide → STOP
  if (!ok) return;

  const data = {
    prenom: document.getElementById('prenom').value.trim(),
    nom: document.getElementById('nom').value.trim(),
    telephone: document.getElementById('telephone').value.trim(),
    categorie: document.getElementById('categorie').value.trim(),
    message: document.getElementById('message').value.trim(),
  };

  submitBtn.disabled = true;
  submitBtn.innerHTML = 'Envoi en cours...';

  sendData(data);
});

function sendData(data) {
  const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
  const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

  if (!csrfToken) {
    alert('Erreur de sécurité : token CSRF introuvable. Actualisez la page et réessayez.');
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Envoyer';
    return;
  }

  fetch(URL_SUBMIT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(data),
    credentials: 'same-origin',
  })
    .then(async response => {
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text || response.statusText}`);
      }
      return response.json();
    })
    .then(res => {
      if (res.success) {
        // cacher le formulaire et afficher message de succès
        form.querySelectorAll('input, select, textarea, button').forEach(el => el.disabled = true);
        formSuccess.classList.add('visible');
      } else {
        alert(res.error || 'Erreur serveur lors de l’envoi du témoignage.');
      }
    })
    .catch(error => {
      console.error('Erreur AJAX:', error);
      alert(`Une erreur est survenue : ${error.message}`);
    })
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Envoyer';
    });
}

    /* Effacement erreurs en temps réel */
    ['prenom','nom','categorie'].forEach(id => {
      document.getElementById(id).addEventListener('input', function () {
        if (this.value.trim()) { this.classList.remove('error'); document.getElementById(`${id}-error`)?.classList.remove('visible'); }
      });
    });
    document.getElementById('telephone').addEventListener('input', function () {
      if (/[\d\s+\-]{8,}/.test(this.value.trim())) { this.classList.remove('error'); document.getElementById('telephone-error').classList.remove('visible'); }
    });
    document.getElementById('message').addEventListener('input', function () {
      if (this.value.trim().length >= 20) { this.classList.remove('error'); document.getElementById('message-error').classList.remove('visible'); }
    });



document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('eventModal');
  const closeBtn = modal.querySelector('.close');
  const modalImage = document.getElementById('modalImage');
  const modalName = document.getElementById('modalName');
  const modalDate = document.getElementById('modalDate');
  const modalLieu = document.getElementById('modalLieuSpan');
  const modalDesc = document.getElementById('modalDescription');

  // Fonction d'ouverture
  function openModal(eventData) {
    modalName.textContent = eventData.name;
    modalDate.textContent = eventData.date;
    modalLieu.textContent = eventData.lieu;
    modalDesc.textContent = eventData.description;

    // Gestion de l'image
    if (eventData.image && eventData.image !== '') {
      modalImage.src = eventData.image;
      modalImage.style.display = 'block';
    } else {
      modalImage.style.display = 'none';
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  // Fermeture
  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  // Écoute sur tous les événements
  document.querySelectorAll('.event-item').forEach(function(card) {
    const btnVoir = card.querySelector('.btn-voir');
    if (btnVoir) {
      btnVoir.addEventListener('click', function(e) {
        e.stopPropagation();
        // Récupération des données depuis les attributs data-*
        const eventData = {
          name: card.dataset.eventName,
          date: card.dataset.eventDate,
          lieu: card.dataset.eventLieu,
          description: card.dataset.eventDescription,
          image: card.dataset.eventImage || ''
        };
        openModal(eventData);
      });
    }
  });

  // Fermeture par clic sur la croix
  closeBtn.onclick = function(e) {
    e.stopPropagation();
    closeModal();
  };

  // Fermeture par clic en dehors du contenu
  modal.onclick = function(event) {
    if (event.target === modal) {
      closeModal();
    }
  };

  // Fermeture avec la touche Échap
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
});
