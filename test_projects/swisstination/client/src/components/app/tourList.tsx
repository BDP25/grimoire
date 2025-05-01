import { atom } from "xoid";

import { h, Component } from "../../framework";
import { TourListFilters, TourListResponse } from "../../api/models";
import { client } from "../../api/client";

export class TourList extends Component {
  public tours;
  public filters;

  constructor() {
    super();
    this.tours = atom<TourListResponse[]>();
    this.filters = atom<TourListFilters>({
      order: "desc",
      sort: "likes",
    });
  }

  protected componentDidMount(): void {
    this.fetchTours();
  }

  protected componentInitSubs() {
    return [
      this.tours.subscribe(() => this.internalRender()),
      this.filters.subscribe(() => {
        this.fetchTours();
      }),
    ];
  }

  public async fetchTours() {
    const tours = await client.tours.listTours(this.filters.value!);
    this.tours.set(tours);
  }

  protected render() {
    if (!this.tours.value) {
      return <neon-spinner size="large" />;
    }

    return (
      <div className="w-full flex flex-col gap-4">
        {this.tours.value!.map((tour) => (
          <tour-card data-tour={tour} />
        ))}
      </div>
    );
  }
}

customElements.define("tour-list", TourList);
