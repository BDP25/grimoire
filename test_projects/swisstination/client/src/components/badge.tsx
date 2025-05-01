import { h, Component } from "../framework";

export class NeonBadge extends Component {
  static get observedAttributes() {
    return ["label", "color"];
  }

  protected render() {
    const label = this.getAttribute("label") || "";
    const color = this.getAttribute("color") || "cyan";
    return (
      <div className={`badge bg-${color}-100 text-${color}-800`}>{label}</div>
    );
  }
}

customElements.define("neon-badge", NeonBadge);
