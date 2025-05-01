import { h, Component } from "../../framework";
import { TourListFilters } from "../../api/models";
import { atom } from "xoid";
import { debounce } from "../../utils/io";

const filterOrderColumn = [
  { value: "likes", label: "Likes" },
  { value: "duration", label: "Duration" },
  { value: "title", label: "Title" },
];

const filterTags = [
  { value: "adventure", label: "Adventure" },
  { value: "history", label: "History" },
  { value: "nature", label: "Nature" },
  { value: "culture", label: "Culture" },
];

export class TourFilters extends Component {
  private filters;

  constructor() {
    super();
    this.filters = atom<TourListFilters>({
      order: "desc",
      sort: "likes",
      search: "",
    });
  }

  protected componentInitSubs() {
    return [
      this.filters.subscribe(() => {
        this.handleFilterUpdate();
      }),
    ];
  }

  private handleFilterUpdate() {
    const event = new CustomEvent<TourListFilters>("filterupdate", {
      detail: this.filters.value,
    });
    this.dispatchEvent(event);
  }
  private handleSearchButton() {
    const event = new Event("search");
    this.dispatchEvent(event);
  }

  private mergeFilters(partialNewFilters: TourListFilters) {
    this.filters.update((state: TourListFilters) => ({
      ...state,
      ...partialNewFilters,
    }));
  }

  private debounceSearch = debounce((search: string) => {
    this.mergeFilters({
      search,
    });
  });

  protected render() {
    return (
      <form className="w-full flex flex-col mb-8 p-8 bg-pink-200 border-2 border-black rounded-md">
        <div className="flex flex-col flex-wrap justify-between gap-4">
          <input
            id="search"
            type="text"
            placeholder="Search for tours..."
            className="h-12 px-4 border-2 border-black rounded-md focus:outline-none focus:border-black hover:border-black"
            value={this.filters.value.search}
            onInput={(e: any) => {
              this.debounceSearch(e.target.value);
            }}
          />
          <div className="flex flex-row flex-wrap justfiy-between gap-4">
            <neon-select
              id="sort"
              name="sort"
              onInput={(e: any) =>
                this.mergeFilters({
                  sort: e.target.value,
                })
              }
              value={this.filters.value.sort}
            >
              {filterOrderColumn.map((option) => (
                <option value={option.value}>{option.label}</option>
              ))}
            </neon-select>
            <neon-select
              id="order"
              name="order"
              onInput={(e: any) =>
                this.mergeFilters({
                  order: e.target.value,
                })
              }
              value={this.filters.value.order}
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </neon-select>
          </div>
          <neon-button
            type="submit"
            className="ms-auto"
            onClick={() => this.handleSearchButton()}
          >
            Search
          </neon-button>
        </div>
      </form>
    );
  }
}

customElements.define("tour-filters", TourFilters);
