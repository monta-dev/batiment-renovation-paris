import { getBarOptions, getDonutOptions, donutColors } from '../configChart.js';
import { renderList, updatePageTitle, setActiveMenu } from '../utils/ui.js';

export const TypesController = {
  /**
   * Initializes the Types Dashboard view.
   * @param {Object} data
   */
  init(data, config = {}) {
    console.log('🛠️ [TypesController] Initializing...');

    if (!config.isOverview) {
      updatePageTitle('Types de Rénovation');
      setActiveMenu(1);
      this.adjustLayout();
    }

    this.renderStats(data.types, config);
  },

  adjustLayout() {
    // Modify UI Structure for singular chart view
    const socialChart = document.getElementById('socialChart');
    if (socialChart) socialChart.parentElement.style.display = 'none';

    const socialDonut = document.getElementById('socialDonut');
    if (socialDonut) socialDonut.parentElement.parentElement.parentElement.style.display = 'none';
  },

  renderStats(data, config = {}) {
    const ids = {
      bar: config.bar || 'privateChart',
      donut: config.donut || 'privateDonut',
      list: config.list || 'privateListContainer'
    };
    // Process Data
    const typeItems = data.map((d, i) => ({
      name: d.type,
      value: d.count,
      percent: -1,
      color: donutColors[i % donutColors.length]
    }));

    const total = typeItems.reduce((acc, curr) => acc + curr.value, 0);
    typeItems.forEach((item) => (item.percent = Math.round((item.value / total) * 100 * 10) / 10));

    // Render Main Bar Chart - Reusing privateChart container
    const barData = typeItems.map((d) => ({ name: d.name, total: d.value, renovated: d.value }));

    if (document.querySelector(`#${ids.bar}`)) {
      new ApexCharts(
        document.querySelector(`#${ids.bar}`),
        getBarOptions(barData, 'Types de Rénovation (Volume)')
      ).render();
    }

    // Render Donut
    if (document.querySelector(`#${ids.donut}`)) {
      new ApexCharts(
        document.querySelector(`#${ids.donut}`),
        getDonutOptions(typeItems, 'TYPES')
      ).render();
    }

    // Render List
    renderList(ids.list, typeItems);
  }
};
