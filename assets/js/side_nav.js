// Side navigation: active dot tracking + scroll-reveal animations
document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.scroll-section');
  const dots = document.querySelectorAll('.side-nav-dot');

  if (!sections.length) return;

  // Scroll-reveal: fade in sections as they enter viewport
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  sections.forEach(s => revealObserver.observe(s));

  // Active dot tracking with debounce
  let lastActiveId = null;
  let debounceTimer = null;

  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const newId = entry.target.id;
        if (newId === lastActiveId) return;

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          lastActiveId = newId;
          dots.forEach(d => d.classList.remove('active'));
          const active = document.querySelector(
            `.side-nav-dot[href="#${newId}"]`
          );
          if (active) active.classList.add('active');
        }, 80);
      }
    });
  }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 });

  sections.forEach(s => navObserver.observe(s));

  // Smooth scroll on dot click
  dots.forEach(dot => {
    dot.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(dot.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
