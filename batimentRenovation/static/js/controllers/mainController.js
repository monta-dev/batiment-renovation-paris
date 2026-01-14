// Main Front Controller - SPA Architecture with Integrated Filters
import { fetchDashboardData } from '../apiFetch.js';
import { AuthService } from '../services/authService.js';
import { BuildingController } from './buildingController.js';
import { TypesController } from './typesController.js';
import { DpeController } from './dpeController.js';

class FrontController {
  constructor() {
    this.data = null;
  }

  async init() {
    console.log('🚀 [SPA] Booting Single Page Dashboard');

    try {
      if (!AuthService.isAuthenticated()) return;

      this.data = await fetchDashboardData();
      this.renderAll();
      this.setupNavigation();

      // Default view
      this.switchView('overview');
    } catch (error) {
      console.error('❌ [FrontController] Failure:', error);
    }
  }

  renderAll() {
    BuildingController.init(this.data, { isOverview: true });
    TypesController.init(this.data, {
      isOverview: true,
      bar: 'typesBar',
      donut: 'typesDonut',
      list: 'typesList'
    });
    DpeController.init(this.data, {
      isOverview: true,
      bar: 'dpeBar',
      donut: 'dpeDonut',
      list: 'dpeList'
    });
  }

  setupNavigation() {
    // 1. Manage Sidebar Navigation & Accordions
    const sidebar = document.getElementById('sidebarNav');

    sidebar.addEventListener('click', (e) => {
      const btn = e.target.closest('.accordion-btn, .nav-item');
      if (!btn) return;

      e.preventDefault();
      const view = btn.getAttribute('data-view');

      if (view) {
        this.switchView(view);
        this.updateActiveStyles(btn);
      }
    });

    // 2. Manage Submenu Filtering (Mock functionality)
    document.querySelectorAll('.submenu-item').forEach((item) => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        // Visual toggle for filter
        item.parentElement
          .querySelectorAll('.submenu-item')
          .forEach((el) => el.classList.remove('selected'));
        item.classList.add('selected');
        console.log(`🔍 [Filter] Applied: ${item.textContent}`);
      });
    });
  }

  updateActiveStyles(activeBtn) {
    // Reset all
    document.querySelectorAll('.nav-item, .accordion-btn').forEach((el) => {
      el.classList.remove('active', 'open');
      const sub = el.nextElementSibling;
      if (sub && sub.classList.contains('submenu')) sub.classList.add('hidden');
    });

    // Activate current
    activeBtn.classList.add('active');
    if (activeBtn.classList.contains('accordion-btn')) {
      activeBtn.classList.add('open');
      const submenu = activeBtn.nextElementSibling;
      if (submenu) submenu.classList.remove('hidden');
    }
  }

  switchView(viewType) {
    const sections = document.querySelectorAll('.view-section');
    const title = document.getElementById('viewTitle');
    const subtitle = document.getElementById('viewSubtitle');

    if (viewType === 'overview') {
      sections.forEach((s) => (s.style.display = 'block'));
      title.textContent = 'Tableau de Bord Global';
      subtitle.textContent = 'Synthèse Interactive';
    } else {
      sections.forEach((s) => {
        s.style.display = s.id === `section-${viewType}` ? 'block' : 'none';
      });
      const labels = { batiment: 'Bâtiments', types: 'Types', dpe: 'DPE' };
      title.textContent = labels[viewType] || 'Détails';
      subtitle.textContent = 'Filtres actifs appliqués';
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
    setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new FrontController().init();
});
