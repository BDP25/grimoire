import { h, Component } from "../framework";

export class PageLayout extends Component {
  protected render() {
    return (
      <div>
        <page-navbar></page-navbar>
        <div className="w-full min-h-screen h-auto pt-24 px-6 md:pt-32 md:px-12 bg-cyan-200">
          <slot></slot>
        </div>
      </div>
    );
  }
}

customElements.define("page-layout", PageLayout);
