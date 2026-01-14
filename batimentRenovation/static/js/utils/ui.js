/**
 * UI Utility Functions
 * Handles DOM manipulations shared across controllers.
 */

/**
 * Updates the main page title (h1 in header).
 * @param {string} title - The new title to display.
 */
export function updatePageTitle(title) {
    const titleEl = document.querySelector('header h1');
    if (titleEl) titleEl.textContent = title;
}

/**
 * Hides sidebar sections that do not match the current page type.
 * @param {string} pageType - The active page identifier ('batiment', 'types', 'dpe').
 */
export function setSidebarVisibility(pageType) {
  const sections = document.querySelectorAll('.accordion-section');

  // If we are on the global dashboard, show everything
  if (pageType === 'dashboard') {
    sections.forEach((s) => (s.style.display = 'block'));
    return;
  }

  sections.forEach((section, index) => {
    // Logic: 0=Batiments, 1=Types, 2=DPE
    const typeIndexMap = {
      batiment: 0,
      types: 1,
      dpe: 2
    };

    const targetIndex = typeIndexMap[pageType];

    if (index !== targetIndex && targetIndex !== undefined) {
      section.style.display = 'none';
    } else {
      section.style.display = 'block';
    }
  });
}

/**
 * Expands the active menu item and its submenu.
 * @param {number} index - Index of the menu item to activate.
 */
export function setActiveMenu(index) {
    const sections = document.querySelectorAll('.accordion-section');
    sections.forEach((section, i) => {
        const btn = section.querySelector('.accordion-btn');
        const submenu = section.querySelector('.submenu');
        const chevron = btn?.querySelector('.material-symbols-outlined:last-child');

        if (i === index) {
            btn?.classList.add('open');
            submenu?.classList.remove('hidden');
            chevron?.classList.add('rotate-180');
        }
    });
}

/**
 * Renders a list of items with colored dots (legend style).
 * @param {string} containerId - The ID of the container element.
 * @param {Array} data - Array of objects {name, percent, color}.
 */
export function renderList(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';
    const mid = Math.ceil(data.length / 2);
    const col1 = data.slice(0, mid);
    const col2 = data.slice(mid);

    const createCol = (items) => {
        const col = document.createElement('div');
        col.className = 'list-column';
        items.forEach((item) => {
            col.innerHTML += `
                  <div class="list-row">
                      <div class="dot" style="background-color: ${item.color};"></div>
                      <div class="row-content">
                          <span class="row-name">${item.name}</span>
                          <span class="row-percent">${item.percent}%</span>
                      </div>
                  </div>
              `;
        });
        return col;
    };
    container.appendChild(createCol(col1));
    container.appendChild(createCol(col2));
}

/**
 * Initializes accordion interactions.
 */
export function initInteractions() {
    document.querySelectorAll('.accordion-btn').forEach((btn) => {
        // Remove existing listeners to avoid duplicates if re-init (though usually called once)
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        newBtn.addEventListener('click', () => {
            const section = newBtn.parentElement;
            const submenu = newBtn.nextElementSibling;
            const chevron = newBtn.querySelector('.material-symbols-outlined:last-child');
            if (submenu) {
                const isOpen = !submenu.classList.contains('hidden');
                submenu.classList.toggle('hidden', isOpen);
                chevron.classList.toggle('rotate-180', !isOpen);
                newBtn.classList.toggle('open', !isOpen);
            }
        });
    });
}
