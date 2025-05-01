import { h, Component } from "../../framework";
import { client } from "../../api/client";

import { atom } from "xoid";

import { TourGetResponse, UserProfileResponse } from "../../api/models";

export class TourTabDescription extends Component {
  public tour?: TourGetResponse;
  private author;

  constructor() {
    super();
    this.author = atom<{ user: UserProfileResponse; avatar: string }>();
  }

  protected componentInitSubs() {
    return [this.author.subscribe(() => this.internalRender())];
  }

  async fetchAuthor() {
    if (!this.tour?.creatorId) return;
    const author = await client.users.getUserById(this.tour.creatorId);
    const avatar = client.users.getAvatarURI(author);
    this.author.set({ user: author, avatar: avatar });
  }

  async init() {
    await this.fetchAuthor();
  }

  protected render() {
    const bgColor = "yellow";
    return (
      <div className={`bg-${bgColor}-200 p-8`}>
        <h2 className="text-xl pb-4">Description</h2>
        <p>{this.tour!.description}</p>
        <div className="flex flex-row justify-start items-center gap-4 mt-12">
          <img
            className="rounded-full h-16 w-16"
            src={this.author.value?.avatar}
            alt="author avatar"
          />
          <div className="flex flex-col">
            <span className="font-bold">
              {this.author.value?.user.username}
            </span>
            <span>{this.author.value?.user.bio}</span>
          </div>
        </div>
      </div>
    );
  }
}

customElements.define("tour-tab-description", TourTabDescription);
