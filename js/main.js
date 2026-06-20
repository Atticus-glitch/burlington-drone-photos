document.addEventListener('DOMContentLoaded', () => {

  const header = document.getElementById('header');

  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('scrolled', y > 80);

    document.querySelectorAll('.nav-links a').forEach(link => {
      const section = document.querySelector(link.getAttribute('href'));
      if (!section) return;
      const rect = section.getBoundingClientRect();
      link.classList.toggle('active', rect.top < 200 && rect.bottom > 100);
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = themeToggle.querySelector('i');
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') {
    document.body.classList.add('dark-mode');
    themeIcon.className = 'fas fa-sun';
  }
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    themeIcon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  });

  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');
  });

  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    });
  });

  const slides = document.querySelectorAll('.hero-slide');
  let currentSlide = 0;

  const nextSlide = () => {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('active');
  };

  if (slides.length > 1) {
    setInterval(nextSlide, 5000);
  }

  const revealElements = () => {
    const elements = document.querySelectorAll('.section-header, .pricing-card, .gallery-item, .about-layout > *, .contact-layout > *');
    elements.forEach(el => {
      if (!el.classList.contains('reveal')) {
        el.classList.add('reveal');
      }
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 80) {
        el.classList.add('visible');
      }
    });
  };

  window.addEventListener('scroll', revealElements, { passive: true });
  revealElements();

  const form = document.getElementById('contactForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const original = btn.innerHTML;
    btn.innerHTML = '<span>Sending...</span><i class="fas fa-spinner fa-pulse"></i>';
    btn.disabled = true;

    try {
      const fd = new FormData(form);
      await fetch(form.action, { method: 'POST', body: new URLSearchParams(fd) });
      btn.innerHTML = '<span>Thanks! I\'ll Be in Touch Soon</span><i class="fas fa-check"></i>';
      btn.style.background = '#0ea776';
      form.reset();
    } catch {
      btn.innerHTML = '<span>Something went wrong. Email me directly at atticus.a@zohomail.com</span><i class="fas fa-envelope"></i>';
      btn.style.background = '#dc2626';
    }

    setTimeout(() => {
      btn.innerHTML = original;
      btn.style.background = '';
      btn.disabled = false;
    }, 4000);
  });

});
