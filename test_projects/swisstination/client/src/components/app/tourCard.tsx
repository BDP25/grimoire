import { h, Component, router, formatDuration } from "../../framework";
import { TourGetResponse } from "../../api/models";
import { client } from "../../api/client";

export class TourCard extends Component {
  // Attributes
  public tour?: TourGetResponse;

  async likeTour() {
    await client.tours.likeTour(this.tour!._id);
    // TODO: ui handle when already liked

    // Inplace update to prevent needing refetching
    this.tour!.likes += 1;
    this.internalRender();
  }

  async dislikeTour() {
    await client.tours.dislikeTour(this.tour!._id);
    // TODO: ui handle when already disliked

    // Inplace update to prevent needing refetching
    this.tour!.likes -= 1;
    this.internalRender();
  }

  protected render() {
    return (
      <neon-card>
        <div slot="content">
          <div className="card-subtitle flex flex-row justify-between">
            <span>{formatDuration(this.tour!.duration)}</span>
            <span>{this.tour!.tags.join(", ")}</span>
          </div>
          <h2 className="card-title">{this.tour!.title}</h2>
          <p className="text-justify">{this.tour!.description}</p>
          <div className="w-full flex align-center justify-between mt-8">
            <neon-button
              color="yellow"
              onClick={() =>
                router.actions.navigateTo(`/tour/${this.tour!._id}`)
              }
            >
              View Tour
            </neon-button>
            <div className="flex flex-row gap-4 items-center md:gap-6">
              <neon-button color="green" onClick={() => this.likeTour()}>
                <img
                  src="/icons/ni-arrow-up.svg"
                  alt="like"
                  className="w-4 h-4"
                />
              </neon-button>
              <div className="hero-font text-2xl">{this.tour!.likes}</div>
              <neon-button color="red" onClick={() => this.dislikeTour()}>
                <img
                  src="/icons/ni-arrow-down.svg"
                  alt="dislike"
                  className="w-4 h-4"
                />
              </neon-button>
            </div>
          </div>
        </div>
      </neon-card>
    );
  }
}

customElements.define("tour-card", TourCard);
