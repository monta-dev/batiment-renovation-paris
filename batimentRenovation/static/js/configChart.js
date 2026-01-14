// Configuration for ApexCharts and Visual Styles

export const donutColors = [
  '#3B82F6',
  '#10B981',
  '#F59E0B',
  '#EF4444',
  '#8B5CF6',
  '#EC4899',
  '#6366F1',
  '#14B8A6',
  '#F97316',
  '#06B6D4',
  '#84CC16',
  '#D946EF',
  '#4F46E5',
  '#0EA5E9',
  '#2563EB',
  '#065F46',
  '#991B1B',
  '#7C3AED',
  '#BE185D',
  '#4338CA'
];

export const getBarOptions = (data, title) => ({
  series: [
    {
      name: "L'ensemble des logements",
      data: data.map((d) => d.total)
    },
    {
      name: 'Nombre de logements rénovés',
      data: data.map((d) => d.renovated)
    }
  ],
  chart: {
    type: 'bar',
    height: 380,
    toolbar: { show: false },
    background: 'transparent',
    fontFamily: 'Inter, sans-serif'
  },
  colors: ['#87CEEB', '#C4B5FD'],
  plotOptions: { bar: { horizontal: false, columnWidth: '12px', borderRadius: 4 } },
  dataLabels: { enabled: false },
  xaxis: {
    categories: data.map((d) => d.name),
    axisBorder: { show: false },
    axisTicks: { show: false },
    labels: { style: { colors: '#94A3B8', fontSize: '10px', fontWeight: 600 } }
  },
  yaxis: { labels: { style: { colors: '#94A3B8', fontSize: '10px' } } },
  grid: { borderColor: 'rgba(0,0,0,0.05)', strokeDashArray: 4 },
  legend: {
    position: 'bottom',
    horizontalAlign: 'center',
    fontSize: '12px',
    fontWeight: 500,
    markers: { radius: 12, offsetX: -4 },
    itemMargin: { horizontal: 20, vertical: 10 }
  },
  title: { text: title, align: 'left', style: { fontSize: '14px', color: '#64748B' } }
});

export const getDonutOptions = (data, centerLabel) => ({
  series: data.map((d) => d.value),
  chart: { type: 'donut', height: 350 },
  labels: data.map((d) => d.name),
  colors: donutColors,
  dataLabels: { enabled: false },
  legend: { show: false },
  stroke: { show: true, width: 4, colors: ['#fff'] },
  plotOptions: {
    pie: { donut: { size: '65%', background: 'transparent' } }
  },
  tooltip: { y: { formatter: (val) => val.toLocaleString() } }
});
