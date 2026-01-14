// Data Fetching Service with Caching Strategy

const CACHE_KEY = 'RENOVATION_DASHBOARD_DATA';
const CACHE_DURATION = 2 * 60 * 60 * 1000; // 2 hours in ms

/**
 * Fetches all necessary dashboard data from distinct sources.
 * Uses LocalStorage for caching to minimize network requests.
 * @param {boolean} forceRefresh - If true, ignores cache and fetches fresh data.
 * @returns {Promise<Object>} Object containing all datasets (buildings, types, dpe).
 */
export async function fetchDashboardData(forceRefresh = false) {
  console.log(`🚀 [apiFetch] Requesting Data... (Force Refresh: ${forceRefresh})`);

  // 1. Check Cache
  if (!forceRefresh) {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      try {
        const { timestamp, data } = JSON.parse(cached);
        const now = Date.now();
        if (now - timestamp < CACHE_DURATION) {
          console.log('✅ [apiFetch] Returning valid CACHED data');
          return data;
        } else {
          console.log('⚠️ [apiFetch] Cache expired');
        }
      } catch (e) {
        console.warn('⚠️ [apiFetch] Cache corrupted, fetching fresh data');
      }
    }
  }

  // 2. Fetch from Network
  console.log('🌐 [apiFetch] Fetching from network...');

  // We use Promise.allSettled to ensure that if one fails, others can still proceed.
  // However, for the app to work "completely", we'd ideally want all.
  // But per requirements, we'll try to handle partial failures gracefully if needed,
  // though for now we'll assume we want to construct a full object.

  const results = await Promise.allSettled([
    fetch('data/stats_batiments.json').then((r) =>
      r.ok ? r.json() : Promise.reject('Components Error')
    ),
    fetch('data/stats_types.json').then((r) => (r.ok ? r.json() : Promise.reject('Types Error'))),
    fetch('data/stats_dpe.json').then((r) => (r.ok ? r.json() : Promise.reject('DPE Error')))
  ]);

  // 3. Process Results
  const [buildingsResult, typesResult, dpeResult] = results;

  const finalData = {
    buildings: buildingsResult.status === 'fulfilled' ? buildingsResult.value : [],
    types: typesResult.status === 'fulfilled' ? typesResult.value : [],
    dpe: dpeResult.status === 'fulfilled' ? dpeResult.value : []
  };

  // Log failures if any
  if (buildingsResult.status === 'rejected') console.error('❌ Failed to fetch Buildings data');
  if (typesResult.status === 'rejected') console.error('❌ Failed to fetch Types data');
  if (dpeResult.status === 'rejected') console.error('❌ Failed to fetch DPE data');

  // 4. Save to Cache (only if we have at least some data)
  if (finalData.buildings.length || finalData.types.length || finalData.dpe.length) {
    try {
      const cacheObject = {
        timestamp: Date.now(),
        data: finalData
      };
      localStorage.setItem(CACHE_KEY, JSON.stringify(cacheObject));
      console.log('💾 [apiFetch] Data saved to cache');
    } catch (e) {
      console.error('❌ [apiFetch] Failed to save to localStorage (Quota exceeded?)', e);
    }
  }

  return finalData;
}
