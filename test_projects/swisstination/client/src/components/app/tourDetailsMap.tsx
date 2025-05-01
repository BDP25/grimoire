import L from "leaflet";
import "leaflet-routing-machine";
import "leaflet/dist/leaflet.css";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";

import { h, Component } from "../../framework";
import { TourGetResponse } from "../../api/models";
import { mapCenterToPointsAndZoom } from "../../utils/geo";

export class TourDetailsMap extends Component {
  // Attributes
  public tour?: TourGetResponse;

  // State
  private map?: L.Map;
  private watchId?: number;
  private userMarker?: L.Marker;

  protected componentDidMount(): void {
    if (!this.tour) throw new Error("Tour not defined!");

    this.initMap();
    this.initGeolocation();
  }

  private initMap() {
    const mapContainer = this.shadowRoot?.querySelector("#map") as HTMLElement;
    if (!mapContainer)
      throw new Error("Could not find map container in shadowdom");

    const map = L.map(mapContainer);
    const points = this.tour!.destination.map((dest) => {
      if (!dest.amenity?.lat || !dest.amenity?.lon) return null;
      return new L.LatLng(
        parseFloat(dest.amenity.lat),
        parseFloat(dest.amenity.lon)
      );
    }).filter((v) => v != null);

    mapCenterToPointsAndZoom(points, map);

    // Add routing
    (L as any).Routing.control({
      waypoints: points,
      createMarker: function (
        _i: number,
        waypoint: L.Routing.Waypoint,
        _n: number
      ) {
        return L.marker(waypoint.latLng);
      },
      router: new L.Routing.OSRMv1({
        serviceUrl: "https://router.project-osrm.org/route/v1",
        profile: "foot"
      }),
      lineOptions: {
        styles: [{ color: "#f76363", weight: 4 }],
        extendToWaypoints: true,
        missingRouteTolerance: 10
      },
      routeWhileDragging: false,
      addWaypoints: false,
      show: false
    }).addTo(map);

    // Add copy right
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        'Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add user marker
    this.userMarker = L.marker([0, 0], {
      icon: L.icon({
        iconUrl: "/icons/pointer.svg",
        iconSize: [35, 35],
        iconAnchor: [12, 41]
      })
    }).addTo(map);

    this.map = map;
  }

  private initGeolocation() {
    if (!navigator.geolocation)
      throw new Error("Browser does not support geolocation");

    this.watchId = navigator.geolocation.watchPosition(
      (position) => this.handlePostionUpdate(position),
      (err) => {
        console.log("Geolocation error: ", err);
      },
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 2000
      }
    );
  }

  handlePostionUpdate(position: GeolocationPosition) {
    const { latitude, longitude } = position.coords;
    console.log("new: ", latitude, longitude);
    this.userMarker!.setLatLng([latitude, longitude]);
  }

  protected componentWillUnmount(): void {
    if (this.watchId) navigator.geolocation.clearWatch(this.watchId);
  }

  protected render() {
    return <div id="map" className="w-full h-96 z-0 mt-4"></div>;
  }
}

customElements.define("tour-details-map", TourDetailsMap);
