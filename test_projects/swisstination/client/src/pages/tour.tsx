import { h, router, Component } from "../framework";

export class TourDetailPage extends Component {
  protected render() {
    const tourId = router.value.params.id;

    if (!tourId) {
      // TODO: Make better 404 page...
      return <p>404 Not found</p>;
    }

    return (
      <page-layout>
        <tour-details tourId={tourId} />
      </page-layout>
    );
  }
}

customElements.define("tour-page", TourDetailPage);
