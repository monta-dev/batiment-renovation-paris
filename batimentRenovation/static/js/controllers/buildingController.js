import { getBarOptions, getDonutOptions, donutColors } from '../configChart.js';
import { renderList, updatePageTitle, setActiveMenu } from '../utils/ui.js';

export const BuildingController = {
  /**
   * Initializes the Building Dashboard view.
   * @param {Object} data - The full dataset (we'll extract buildings).
   */
  init(data, config = {}) {
    console.log('🏗️ [BuildingController] Initializing...');

    // 1. Set Headings & Menu (only if not in dashboard overview)
    if (!config.isOverview) {
      updatePageTitle('Bâtiments Rénovés');
      setActiveMenu(0);
    }

    // 2. Render content
    this.renderStats(data.buildings, config);
  },

  renderStats(data, config = {}) {
    const ids = {
      privateBar: config.privateBar || 'privateChart',
      socialBar: config.socialBar || 'socialChart',
      privateDonut: config.privateDonut || 'privateDonut',
      socialDonut: config.socialDonut || 'socialDonut',
      privateList: config.privateList || 'privateListContainer',
      socialList: config.socialList || 'socialListContainer'
    };
    // Transform DTO to Chart format
    const privateData = data.map((d) => ({
      name: d.name,
      total: d.total,
      renovated: d.private_renovated
    }));
    const socialData = data.map((d) => ({
      name: d.name,
      total: d.total * 0.4,
      renovated: d.social_renovated
    }));

    // Render Bar Charts
    if (document.querySelector(`#${ids.privateBar}`)) {
      new ApexCharts(
        document.querySelector(`#${ids.privateBar}`),
        getBarOptions(privateData, 'Logement Privé')
      ).render();
    }

    if (document.querySelector(`#${ids.socialBar}`)) {
      new ApexCharts(
        document.querySelector(`#${ids.socialBar}`),
        getBarOptions(socialData, 'Logement Social')
      ).render();
    }

    // Prepare & Render Donut Data
    const generatePieData = (dataset) =>
      dataset.map((d, i) => ({
        name: d.name,
        value: d.renovated,
        percent:
          Math.round((d.renovated / dataset.reduce((a, b) => a + b.renovated, 0)) * 100 * 10) / 10,
        color: donutColors[i % 20]
      }));

    const pieDataPrivate = generatePieData(privateData);
    const pieDataSocial = generatePieData(socialData);

    if (document.querySelector(`#${ids.privateDonut}`)) {
      new ApexCharts(
        document.querySelector(`#${ids.privateDonut}`),
        getDonutOptions(pieDataPrivate, 'PRIVÉ')
      ).render();
    }

    if (document.querySelector(`#${ids.socialDonut}`)) {
      new ApexCharts(
        document.querySelector(`#${ids.socialDonut}`),
        getDonutOptions(pieDataSocial, 'SOCIAL')
      ).render();
    }

    // Render Lists
    renderList(ids.privateList, pieDataPrivate.slice(0, 20));
    renderList(ids.socialList, pieDataSocial.slice(0, 20));
  }
};
