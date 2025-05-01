import { Component } from "../component";
import { router } from "./router";

export class RouterLink extends Component {
  protected override componentDidMount() {
    this.shadowRoot!.querySelector("div")!.addEventListener("click", (e) => {
      e.preventDefault();
      const href = this.getAttribute("href");
      if (!href) throw new Error("Missing required href attribute");
      router.actions.navigateTo(href);
    });
  }

  protected render() {
    return `<div><slot></slot></div>`;
  }
}

customElements.define("router-link", RouterLink);
