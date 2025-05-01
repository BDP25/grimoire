import L from "leaflet";

export function mapCenterToPointsAndZoom(
  points: L.LatLngExpression[],
  map: L.Map
): void {
  const bounds = L.latLngBounds(points);
  const center = bounds.getCenter();

  map.fitBounds(bounds);
  const zoom = Math.max(map.getZoom() - 1, 0);

  map.setView(center, zoom);
}
