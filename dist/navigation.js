document.documentElement.classList.add("js");

const menu = document.querySelector("#menu");
const nav = document.querySelector("#primary");
const groups = [...nav.querySelectorAll("details")];
const mobile = matchMedia("(max-width: 940px)");

function setMenu(open) {
  menu.setAttribute("aria-expanded", String(open));
  nav.classList.toggle("open", open);
  if (!open) groups.forEach(group => { group.open = false; });
}

menu.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
mobile.addEventListener("change", () => setMenu(false));

groups.forEach(group => {
  group.addEventListener("toggle", () => {
    if (group.open) groups.filter(other => other !== group).forEach(other => { other.open = false; });
  });
});

document.addEventListener("click", event => {
  if (!nav.contains(event.target) && !menu.contains(event.target)) setMenu(false);
});

document.addEventListener("keydown", event => {
  if (event.key !== "Escape") return;
  const group = groups.find(item => item.open);
  if (group) {
    group.open = false;
    group.querySelector("summary").focus();
  } else if (mobile.matches && nav.classList.contains("open")) {
    setMenu(false);
    menu.focus();
  }
});

const gallery = document.querySelector(".hero-visual");
if (gallery) {
  const slides = [...gallery.querySelectorAll(".hero-slide")];
  const controls = gallery.querySelector(".hero-buttons");
  const caption = gallery.querySelector("#hero-caption");
  let active = 0;

  function advance(offset) {
    slides[active].hidden = true;
    active = (active + offset + slides.length) % slides.length;
    slides[active].hidden = false;
    caption.textContent = `${active + 1} / ${slides.length} · ${slides[active].dataset.caption}`;
  }

  const [previous, next] = controls.querySelectorAll("button");
  previous.addEventListener("click", () => advance(-1));
  next.addEventListener("click", () => advance(1));
  controls.hidden = false;
  advance(0);
}

const motion = matchMedia("(prefers-reduced-motion: no-preference)");
if (motion.matches && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add("arrived");
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.15 });

  document.querySelectorAll(".section-intro h2, .section-intro > p, .program-card, .values-pair article, .moment-card, .steps li, .notice, .timeline li, .story-layout > *, .performance-layout > *, .program-detail > *, .archive-list li, .directory > div")
    .forEach(element => observer.observe(element));
}

// Reading progress is decorative and respects reduced-motion preferences.
if (motion.matches) {
  const hero = document.querySelector(".hero");
  const frame = document.querySelector(".hero-visual");
  if (hero && frame) {
    const progress = document.querySelector(".reading-progress");
    if (progress) {
      let ticking = false;
      addEventListener("scroll", () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const total = document.documentElement.scrollHeight - innerHeight;
          progress.style.setProperty("--read-progress", total > 0 ? Math.min(1,scrollY / total) : 0);
          ticking = false;
        });
      }, { passive:true });
    }
  }
}

const filters = document.querySelector(".gallery-filters");
const cards = [...document.querySelectorAll(".all-moments .moment-card")];
if (filters) {
  const count = document.querySelector(".gallery-count");
  function filterPhotos(category) {
    filters.querySelectorAll("button").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.filter === category));
    });
    cards.forEach(card => { card.hidden = category !== "All moments" && card.dataset.category !== category; });
    const shown = cards.filter(card => !card.hidden).length;
    count.textContent = `${shown} ${shown === 1 ? "moment" : "moments"}${category === "All moments" ? " from our community" : ` · ${category}`}`;
  }
  filters.querySelectorAll("button").forEach(button => button.addEventListener("click", () => filterPhotos(button.dataset.filter)));
  filters.hidden = false;
  filterPhotos("All moments");
}

const viewer = document.querySelector(".photo-dialog");
const photoLinks = [...document.querySelectorAll(".photo-open")];
if (viewer && typeof viewer.showModal === "function") {
  const image = viewer.querySelector("#viewer-image");
  const caption = viewer.querySelector("#viewer-caption");
  const source = viewer.querySelector("#viewer-source");
  let selected = null;
  let returnFocus = null;
  let previousOverflow = "";

  function showPhoto(link) {
    selected = link;
    image.src = link.href;
    image.alt = link.querySelector("img").alt;
    caption.textContent = link.dataset.caption;
    source.href = link.dataset.source;
  }
  function move(offset) {
    const visible = photoLinks.filter(link => !link.closest("figure").hidden);
    showPhoto(visible[(visible.indexOf(selected) + offset + visible.length) % visible.length]);
  }
  photoLinks.forEach(link => link.addEventListener("click", event => {
    // Preserve normal new-tab and download link behavior.
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    returnFocus = link;
    showPhoto(link);
    previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    viewer.showModal();
    viewer.querySelector("[data-viewer-close]").focus();
  }));
  viewer.querySelector("[data-viewer-close]").addEventListener("click", () => viewer.close());
  viewer.querySelector("[data-viewer-prev]").addEventListener("click", () => move(-1));
  viewer.querySelector("[data-viewer-next]").addEventListener("click", () => move(1));
  viewer.addEventListener("keydown", event => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      move(event.key === "ArrowLeft" ? -1 : 1);
    }
  });
  viewer.addEventListener("click", event => {
    if (event.target === viewer) {
      const rect = viewer.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) viewer.close();
    }
  });
  viewer.addEventListener("close", () => {
    document.body.style.overflow = previousOverflow;
    returnFocus?.focus();
  });
}
