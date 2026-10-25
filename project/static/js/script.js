(function () {
  const navbar = document.querySelector(".navbar");
  const toggle = document.getElementById("nav-toggle");
  const mobile = document.getElementById("nav-mobile");
  if (!navbar || !toggle || !mobile) return;

  window.addEventListener(
    "scroll",
    () => {
      navbar.classList.toggle("scrolled", window.scrollY > 20);
    }, {
      passive: true,
    },
  );

  toggle.addEventListener("click", () => {
    const isOpen = mobile.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen);
    toggle.innerHTML = isOpen ?
      '<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="5" x2="15" y2="15"/><line x1="5" y1="15" x2="15" y2="5"/></svg>' :
      '<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="17" y2="6"/><line x1="3" y1="10" x2="17" y2="10"/><line x1="3" y1="14" x2="14" y2="14"/></svg>';
  });

  mobile.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobile.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.innerHTML =
        '<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="17" y2="6"/><line x1="3" y1="10" x2="17" y2="10"/><line x1="3" y1="14" x2="14" y2="14"/></svg>';
    });
  });
})();

(function () {
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document
        .querySelectorAll(".filter-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const filter = btn.dataset.filter;
      document
        .querySelectorAll("#vehicles-grid [data-usage]")
        .forEach((card) => {
          card.style.display =
            filter === "الكل" || card.dataset.usage === filter ? "" : "none";
        });
    });
  });
})();

(function () {
  const input = document.getElementById("member-search");
  if (!input) return;
  const cards = document.querySelectorAll("#members-grid .member-card");
  let emptyMsg = null;

  input.addEventListener("input", () => {
    const q = input.value.trim();
    let visible = 0;
    cards.forEach((card) => {
      const text =
        card.querySelector(".member-card__name").textContent +
        card.querySelector(".member-card__rank").textContent;
      const show = !q || text.includes(q);
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });
    if (!emptyMsg) {
      emptyMsg = document.createElement("div");
      emptyMsg.className = "members-empty";
      emptyMsg.textContent = "لا توجد نتائج للبحث";
      document.getElementById("members-grid").appendChild(emptyMsg);
    }
    emptyMsg.style.display = visible === 0 ? "" : "none";
  });
})();

(function () {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
    },
  );
  document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
})();

// TOAST
document.querySelectorAll("[data-toast]").forEach((toast) => {
  const duration = toast.dataset.duration || 4000;

  setTimeout(() => {
    toast.style.animation = "toastOut 0.25s ease forwards";
    toast.style.pointerEvents = "none";

    setTimeout(() => {
      toast.remove();
    }, 300);
  }, duration);
});

// USER MENU (Discord account dropdown)
(function () {
  const btn = document.querySelector("[data-user-menu-toggle]");
  const menu = document.querySelector("[data-user-menu-dropdown]");
  if (!btn || !menu) return;

  const setOpen = (open) => {
    menu.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", String(open));
    menu.setAttribute("aria-hidden", String(!open));
  };

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    setOpen(!menu.classList.contains("open"));
  });
  document.addEventListener("click", (e) => {
    if (!menu.contains(e.target)) setOpen(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      setOpen(false);
      btn.focus();
    }
  });
})();
