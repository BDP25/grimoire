import { h, router, Component } from "../framework";

export class HomePage extends Component {
  protected componentDidMount(): void {
    this.shadowRoot!.querySelector("neon-button")!.addEventListener(
      "click",
      () => {
        router.actions.navigateTo("/tours");
      }
    );
  }

  protected render() {
    return (
      <page-layout>
        <div className="flex flex-col items-start justify-between md:items-center  md:mt-8">
          <h1 className="text-6xl hero-font md:text-8xl">
            Welcome to Swisstination
          </h1>
          <p className="text-2xl hero-font md:text-4xl">
            A community-driven platform that connects travelers with Swiss
            locals.
          </p>
          <div className="w-full flex flex-col items-center justify-center md:flex-row md:gap-24">
            <div className="flex justify-center mt-6">
              <neon-button color="yellow">
                Start exploring Switzerland!
              </neon-button>
            </div>
            <div className="flex justify-center mt-8">
              <img src="/dora.png" alt="Dora" width="200" />
            </div>
          </div>
        </div>
      </page-layout>
    );
  }
}

customElements.define("home-page", HomePage);
