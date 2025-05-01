import { h, Component } from "../framework";

export class NeonButton extends Component {
  static get observedAttributes() {
    return ["color", "variant"];
  }

  protected render() {
    const color = this.getAttribute("color") || "cyan";
    const variant = this.getAttribute("variant") || "default";
    return (
      <button
        className={`btn ${
          variant == "rounded" ? "btn--rounded" : ""
        } bg-${color}-200 hover:bg-${color}-300 active:bg-${color}-400`}
      >
        <slot></slot>
      </button>
    );
  }
}

customElements.define("neon-button", NeonButton);
