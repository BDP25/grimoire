import { h, Component } from "../../framework";
import { TourGetResponse } from "../../api/models";

export class TourTabAmenities extends Component {
  // Attributes
  public tour?: TourGetResponse;

  protected render() {
    const bgColor = "red";
    if (!this.tour?.destination) {
      return (
        <div className={`bg-${bgColor}-200 p-8`}>
          <p>No amenities attached to this tour!</p>
        </div>
      );
    }

    return (
      <div className={`bg-${bgColor}-200 p-8`}>
        <h2 className="text-xl pb-4">Amenities</h2>
        <ol className="list-decimal ps-8">
          {this.tour!.destination.map((dest) => (
            <li className="[&:not(:last-child)]:pb-8">
              <h3 className="text-lg">{dest.title}</h3>
              <p className="w-5/6">{dest.description}</p>
            </li>
          ))}
        </ol>
      </div>
    );
  }
}

customElements.define("tour-tab-amenities", TourTabAmenities);
