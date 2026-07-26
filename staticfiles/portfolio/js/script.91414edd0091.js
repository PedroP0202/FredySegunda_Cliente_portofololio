/* ═══════════════════════════════════════════════════════════════
   FREDY SEGUNDA — PORTFOLIO
   JavaScript Premium — UI/UX Redesign 2025/2026
   ─────────────────────────────────────────────
   LÓGICA PRESERVADA (não alterada):
   · triggerUpload()
   · loadMedia()
   · openLightbox()
   · closeLightbox()
   · Admin Mode (double-click logo)
   · Keyboard ESC lightbox close
   ═══════════════════════════════════════════════════════════════ */

/* ════════════════════════════════════
   LÓGICA ORIGINAL — PRESERVADA
   ════════════════════════════════════ */

function triggerUpload(id){
  if (document.body.classList.contains('admin-mode')) {
    document.getElementById(id).click();
  }
}

function loadMedia(input, placeholderId, lbId){
  const file = input.files[0];
  if(!file) return;
  const url = URL.createObjectURL(file);
  const ph = document.getElementById(placeholderId);
  const isVideo = file.type.startsWith('video/');
  const slot = ph ? ph.closest('.media-slot, .reel-item') : null;

  if(ph){
    if(isVideo){
      const v = document.createElement('video');
      v.src = url;
      v.autoplay = true;
      v.muted = true;
      v.loop = true;
      v.playsInline = true;
      v.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;';
      ph.replaceWith(v);
    } else {
      const img = document.createElement('img');
      img.src = url;
      img.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;';
      ph.replaceWith(img);
    }
  }

  if(slot){
    slot.dataset.mediaUrl = url;
    slot.dataset.mediaType = isVideo ? 'video' : 'image';
    slot.addEventListener('click', function(e){
      if(e.target.tagName === 'INPUT') return;
      openLightbox(this.dataset.mediaUrl, this.dataset.mediaType);
    }, {once: false});
  }
}

function openLightbox(url, type){
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lb-img');
  const vid = document.getElementById('lb-vid');
  if(type === 'video'){
    vid.src = url;
    vid.style.display = 'block';
    img.style.display = 'none';
  } else {
    img.src = url;
    img.style.display = 'block';
    vid.style.display = 'none';
    vid.src = '';
  }
  lb.classList.add('open');
}

function closeLightbox(e){
  if(e.target.id === 'lightbox'){
    document.getElementById('lightbox').classList.remove('open');
    document.getElementById('lb-vid').pause();
  }
}

document.addEventListener('keydown', function(e){
  if(e.key === 'Escape'){
    document.getElementById('lightbox').classList.remove('open');
    document.getElementById('lb-vid').pause();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.logo');
  if (logo) {
    logo.addEventListener('dblclick', () => {
      const pwd = prompt("Password para modo edição:");
      if (pwd === "admin123") {
        document.body.classList.add('admin-mode');
        alert("Modo de edição ativado!");
      }
    });
  }
});

/* ════════════════════════════════════
   PREMIUM INTERACTIONS — REDESIGN 2025
   ════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ──────────────────────────────────
     1. SCROLL PROGRESS BAR
     ────────────────────────────────── */
  const progressBar = document.getElementById('scroll-progress');
  if (progressBar) {
    const updateProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = progress + '%';
    };
    window.addEventListener('scroll', updateProgress, { passive: true });
  }

  /* ──────────────────────────────────
     2. NAV GLASSMORPHISM ON SCROLL
     ────────────────────────────────── */
  const nav = document.querySelector('nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });
  }

  /* ──────────────────────────────────
     3. ACTIVE NAV LINK (Intersection Observer)
     ────────────────────────────────── */
  const sections = document.querySelectorAll('section[id], div[id]');
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

  if (navLinks.length > 0 && sections.length > 0) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + id) {
              link.classList.add('active');
            }
          });
        }
      });
    }, { threshold: 0.3, rootMargin: '-10% 0px -60% 0px' });

    sections.forEach(sec => sectionObserver.observe(sec));
  }

  /* ──────────────────────────────────
     4. MOBILE HAMBURGER MENU
     ────────────────────────────────── */
  const hamburger = document.querySelector('.nav-hamburger');
  const mobileNav = document.querySelector('.nav-mobile');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      const isOpen = hamburger.classList.toggle('open');
      mobileNav.classList.toggle('open', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    mobileNav.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ──────────────────────────────────
     5. CUSTOM CURSOR (Enhanced)
     ────────────────────────────────── */
  const cursor = document.querySelector('.cursor');
  const follower = document.querySelector('.cursor-follower');

  if (cursor && follower && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let mouseX = 0, mouseY = 0;
    let followerX = 0, followerY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = mouseX + 'px';
      cursor.style.top = mouseY + 'px';
    }, { passive: true });

    if (typeof gsap !== 'undefined') {
      gsap.to({}, {
        duration: 0.01,
        repeat: -1,
        onRepeat: () => {
          followerX += (mouseX - followerX) * 0.12;
          followerY += (mouseY - followerY) * 0.12;
          follower.style.left = followerX + 'px';
          follower.style.top = followerY + 'px';
        }
      });
    } else {
      document.addEventListener('mousemove', (e) => {
        follower.style.left = e.clientX + 'px';
        follower.style.top = e.clientY + 'px';
      }, { passive: true });
    }

    // Hover states
    const hoverEls = document.querySelectorAll('a, button, .media-slot, .reel-item, .logo, .sec-sub, .f-link, .nav-link');
    hoverEls.forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.classList.add('hover-active');
        follower.classList.add('hover-active');
      });
      el.addEventListener('mouseleave', () => {
        cursor.classList.remove('hover-active');
        follower.classList.remove('hover-active');
      });
    });
  }

  /* ──────────────────────────────────
     6. SPOTLIGHT CURSOR (Glow following mouse)
     ────────────────────────────────── */
  const spotlight = document.getElementById('spotlight');
  if (spotlight) {
    let spotX = window.innerWidth / 2;
    let spotY = window.innerHeight / 2;
    let targetX = spotX, targetY = spotY;

    document.addEventListener('mousemove', (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
    }, { passive: true });

    const animateSpotlight = () => {
      spotX += (targetX - spotX) * 0.06;
      spotY += (targetY - spotY) * 0.06;
      spotlight.style.left = spotX + 'px';
      spotlight.style.top = spotY + 'px';
      requestAnimationFrame(animateSpotlight);
    };
    animateSpotlight();

    // Fade out spotlight on mouse leave
    document.addEventListener('mouseleave', () => { spotlight.style.opacity = '0'; });
    document.addEventListener('mouseenter', () => { spotlight.style.opacity = '1'; });
  }

  /* ──────────────────────────────────
     7. MAGNETIC ELEMENTS
     ────────────────────────────────── */
  if (typeof gsap !== 'undefined') {
    const magneticEls = document.querySelectorAll('.magnetic-item, .btn-main, .btn-sec, .btn-dark, .logo');
    magneticEls.forEach(el => {
      el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        const isBig = el.classList.contains('media-slot');
        const factor = isBig ? 0.03 : 0.15;

        gsap.to(el, {
          x: x * factor,
          y: y * factor,
          duration: 0.3,
          ease: 'power2.out'
        });
      });

      el.addEventListener('mouseleave', () => {
        gsap.to(el, {
          x: 0,
          y: 0,
          duration: 0.7,
          ease: 'elastic.out(1, 0.3)'
        });
      });
    });
  }

  /* ──────────────────────────────────
     8. RIPPLE EFFECT ON BUTTONS
     ────────────────────────────────── */
  const rippleButtons = document.querySelectorAll('.btn-main, .btn-sec, .btn-dark');
  rippleButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const size = Math.max(rect.width, rect.height) * 2;

      const ripple = document.createElement('span');
      ripple.className = 'ripple-circle';
      ripple.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${x - size / 2}px;
        top: ${y - size / 2}px;
        position: absolute;
      `;
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 700);
    });
  });

  /* ──────────────────────────────────
     9. TILT CARDS (3D hover effect)
     ────────────────────────────────── */
  const tiltCards = document.querySelectorAll('.media-slot, .reel-item, .process-item');
  const isTouchDevice = window.matchMedia('(hover: none)').matches;

  if (!isTouchDevice) {
    tiltCards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        const rotX = y * -4;
        const rotY = x * 6;

        card.style.transform = `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale3d(1.01, 1.01, 1.01)`;
        card.style.transition = 'transform 0.1s ease';
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
      });
    });
  }

  /* ──────────────────────────────────
     10. ANIMATED COUNTERS (Hero stats)
     ────────────────────────────────── */
  const statNumbers = document.querySelectorAll('.stat-n');
  let countersAnimated = false;

  const animateCounter = (el) => {
    const text = el.textContent.trim();
    const match = text.match(/(\d+)(\+?)/);
    if (!match) return;

    const target = parseInt(match[1], 10);
    const suffix = match[2] || '';
    const duration = 1400;
    const startTime = performance.now();

    const update = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(eased * target);
      el.textContent = current + suffix;
      if (progress < 1) requestAnimationFrame(update);
    };

    requestAnimationFrame(update);
  };

  // Trigger when stats are in view
  const statsEl = document.querySelector('.hero-stats');
  if (statsEl) {
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !countersAnimated) {
          countersAnimated = true;
          statNumbers.forEach((el, i) => {
            setTimeout(() => animateCounter(el), i * 150);
          });
          statsObserver.disconnect();
        }
      });
    }, { threshold: 0.5 });
    statsObserver.observe(statsEl);
  }

  /* ──────────────────────────────────
     11. GSAP ANIMATIONS
     ────────────────────────────────── */
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Hero entrance — staggered
    const heroTimeline = gsap.timeline({ delay: 0.1 });
    heroTimeline
      .from('.hero-eyebrow', {
        y: 20, opacity: 0, duration: 0.7, ease: 'power3.out'
      })
      .from('.hero-title', {
        y: 40, opacity: 0, duration: 1, ease: 'power3.out'
      }, '-=0.4')
      .from('.hero-stats', {
        y: 20, opacity: 0, duration: 0.7, ease: 'power3.out'
      }, '-=0.5')
      .from('.avail', {
        y: 16, opacity: 0, duration: 0.6, ease: 'power3.out'
      }, '-=0.7')
      .from('.hero-desc', {
        y: 16, opacity: 0, duration: 0.6, ease: 'power3.out'
      }, '-=0.4')
      .from('.btn-main, .btn-sec', {
        y: 16, opacity: 0, duration: 0.6, stagger: 0.1, ease: 'power3.out'
      }, '-=0.3');

    // Scroll reveal for sections
    gsap.utils.toArray('.gsap-reveal').forEach(el => {
      gsap.from(el, {
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          toggleActions: 'play none none reverse'
        },
        y: 50,
        opacity: 0,
        duration: 0.9,
        ease: 'power3.out'
      });
    });

    // Reel strip stagger
    gsap.from('.reel-item', {
      scrollTrigger: {
        trigger: '.reel-strip',
        start: 'top 90%',
        toggleActions: 'play none none reverse'
      },
      y: 30,
      opacity: 0,
      duration: 0.6,
      stagger: 0.08,
      ease: 'power2.out'
    });

    // Section headers
    gsap.utils.toArray('.sec-header, .reel-header').forEach(el => {
      gsap.from(el, {
        scrollTrigger: {
          trigger: el,
          start: 'top 90%',
          toggleActions: 'play none none reverse'
        },
        y: 20,
        opacity: 0,
        duration: 0.7,
        ease: 'power3.out'
      });
    });

    // Skills bars
    gsap.from('.fill', {
      scrollTrigger: {
        trigger: '.skills-strip',
        start: 'top 85%'
      },
      width: '0%',
      duration: 1.4,
      ease: 'power3.out',
      stagger: 0.08
    });

    // Process items stagger
    gsap.from('.process-item', {
      scrollTrigger: {
        trigger: '.skills-strip',
        start: 'top 80%',
        toggleActions: 'play none none reverse'
      },
      y: 20,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: 'power2.out'
    });

    // CTA block
    gsap.from('.cta-block > div', {
      scrollTrigger: {
        trigger: '.cta-block',
        start: 'top 85%',
        toggleActions: 'play none none reverse'
      },
      y: 30,
      opacity: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: 'power3.out'
    });

    // Grid items stagger
    gsap.utils.toArray('.grid-3 .media-slot, .grid-2-asym .media-slot').forEach((el, i) => {
      gsap.from(el, {
        scrollTrigger: {
          trigger: el,
          start: 'top 90%',
          toggleActions: 'play none none reverse'
        },
        y: 30,
        opacity: 0,
        duration: 0.7,
        delay: (i % 3) * 0.08,
        ease: 'power3.out'
      });
    });

    // Parallax on hero content
    gsap.to('.hero-left', {
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: true
      },
      y: 60,
      ease: 'none'
    });

    gsap.to('.hero-right', {
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: true
      },
      y: 40,
      ease: 'none'
    });

    // Blob parallax
    gsap.to('.hero-blob-1', {
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: true
      },
      y: -80,
      ease: 'none'
    });

    gsap.to('.hero-blob-2', {
      scrollTrigger: {
        trigger: '.hero',
        start: 'top top',
        end: 'bottom top',
        scrub: true
      },
      y: -40,
      ease: 'none'
    });

  } else {
    // Fallback without GSAP: simple class-based reveal
    const revealEls = document.querySelectorAll('.gsap-reveal, .gsap-hero');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, { threshold: 0.1 });

    revealEls.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
      observer.observe(el);
    });
  }

  /* ──────────────────────────────────
     12. SMOOTH SCROLL for anchor links
     ────────────────────────────────── */
  document.querySelectorAll('a[href^="#"], .sec-sub, .nav-link[href^="#"]').forEach(el => {
    el.addEventListener('click', function(e) {
      const href = this.getAttribute('href') || this.getAttribute('onclick');
      if (!href || !href.startsWith('#')) return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const navHeight = document.querySelector('nav')?.offsetHeight || 70;
        const top = target.getBoundingClientRect().top + window.scrollY - navHeight;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  /* ──────────────────────────────────
     13. SKILL BARS — glow on hover
     ────────────────────────────────── */
  document.querySelectorAll('.skill-row').forEach(row => {
    const fill = row.querySelector('.fill');
    if (!fill) return;
    row.addEventListener('mouseenter', () => {
      fill.style.boxShadow = '0 0 14px rgba(76, 117, 238, 0.7)';
    });
    row.addEventListener('mouseleave', () => {
      fill.style.boxShadow = '0 0 8px rgba(76, 117, 238, 0.5)';
    });
  });

  /* ──────────────────────────────────
     14. FOOTER LINKS hover glow
     ────────────────────────────────── */
  document.querySelectorAll('.f-link').forEach(link => {
    link.addEventListener('mouseenter', () => {
      link.style.textShadow = '0 0 12px rgba(76, 117, 238, 0.5)';
    });
    link.addEventListener('mouseleave', () => {
      link.style.textShadow = '';
    });
  });

});
