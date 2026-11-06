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

  document.querySelectorAll(".program-card, .values-pair article, .gallery figure, .steps li, .notice, .timeline li, .welcome > div, .approach > div, .program-detail > *, .archive-list li, .directory > div")
    .forEach(element => observer.observe(element));
}
