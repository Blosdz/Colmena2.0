import { semanticBand } from './chartColors.js';

/** Banda dominante (mayor %) de un resultado de constructo. */
export function dominantBand(result) {
  if (!result?.bands?.length) return null;
  return result.bands.reduce((best, band) => ((band.pct || 0) > (best.pct || 0) ? band : best), result.bands[0]);
}

/** % de la banda semánticamente "desfavorable" (alto riesgo) de un resultado. */
export function unfavorablePct(result) {
  return result.bands?.find((band) => semanticBand(band.label) === 'unfavorable')?.pct || 0;
}
