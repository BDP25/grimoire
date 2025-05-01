import { h, Component } from "../framework";
import { TourListFilters } from "../api/models";
import { TourList } from "../components/app/tourList";

export class ToursPage extends Component {
  handleFiltersUpdate(e: CustomEvent<TourListFilters>) {
    console.log("handleFiltersUpdate");
    console.log(e.detail);
    const tourList = this.shadowRoot!.querySelector("tour-list") as TourList;
    tourList.filters.set(e.detail);
  }
  handleSearch() {
    console.log("handleSearch");
    const tourList = this.shadowRoot!.querySelector("tour-list") as TourList;
    tourList.fetchTours();
  }

  protected render() {
    return (
      <page-layout>
        <div className="flex flex-col gap-4 text-justify md:w-4/5 xl:w-1/2 md:m-auto">
          <tour-filters
            onFilterUpdate={(e: CustomEvent<TourListFilters>) =>
              this.handleFiltersUpdate(e)
            }
            onSearch={() => this.handleSearch()}
          />
          <tour-list />
        </div>
      </page-layout>
    );
  }
}

customElements.define("tours-page", ToursPage);
