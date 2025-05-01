import { atom } from "xoid";
import { h, Component } from "../../framework";
import { TourGetResponse } from "../../api/models";
import { client } from "../../api/client";

export class TourDetails extends Component {
  static get observedAttributes() {
    return ["tourId"];
  }

  public tour;

  constructor() {
    super();
    this.tour = atom<TourGetResponse>();
  }

  protected componentDidMount(): void {
    this.fetchTour();
  }

  protected componentInitSubs() {
    return [this.tour.subscribe(() => this.internalRender())];
  }

  protected async fetchTour() {
    const tourId = this.getAttribute("tourId");
    if (!tourId) throw Error("Cannot fetch when tourId is null");
    const tour = await client.tours.getTour(tourId);
    this.tour.set(tour);
  }

  protected render() {
    if (!this.tour.value) {
      return <neon-spinner size="large" />;
    }

    return (
      <div className="flex flex-col text-justify md:w-4/5 md:m-auto">
        <h1 className="text-3xl">{this.tour.value.title}</h1>
        <tour-details-map data-tour={this.tour.value} />
        <tour-details-tab data-tour={this.tour.value} />
      </div>
    );
  }
}

export class TourDetailsTabs extends Component {
  public tour?: TourGetResponse;
  private tab;

  constructor() {
    super();
    this.tab = atom<"description" | "amenities" | "statistics">("description");
  }

  protected componentInitSubs() {
    return [this.tab.subscribe(() => this.internalRender())];
  }

  protected render() {
    let tabContent = <p>Tab not found</p>;
    switch (this.tab.value) {
      case "amenities":
        tabContent = <tour-tab-amenities data-tour={this.tour} />;
        break;
      case "description":
        tabContent = <tour-tab-description data-tour={this.tour} />;
        break;
      case "statistics":
        tabContent = <tour-tab-stats data-tour={this.tour} />;
        break;
    }

    return (
      <div>
        <div className="flex flex-row gap-1 mt-8">
          <neon-button
            color="yellow"
            onClick={() => this.tab.set("description")}
          >
            Description
          </neon-button>
          <neon-button color="red" onClick={() => this.tab.set("amenities")}>
            Amenities
          </neon-button>
          <neon-button color="pink" onClick={() => this.tab.set("statistics")}>
            Statistics
          </neon-button>
        </div>
        <div className="w-full flex flex-col text-justify mb-12">
          {tabContent}
        </div>
      </div>
    );
  }
}

customElements.define("tour-details", TourDetails);
customElements.define("tour-details-tab", TourDetailsTabs);
