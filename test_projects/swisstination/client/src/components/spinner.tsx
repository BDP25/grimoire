import { h, Component } from "../framework";

const sizeClasses: { [key: string]: any } = {
  small: "w-8 h-8",
  medium: "w-16 h-16",
  large: "w-24 h-24",
};

export class NeonSpinner extends Component {
  static get observedAttributes() {
    return ["size", "color", "backgroundColor"];
  }

  protected render() {
    const size = this.getAttribute("size") || "medium";
    const color = this.getAttribute("color") || "#FF6B6B";
    const backgroundColor = this.getAttribute("backgroundColor") || "#4ECDC4";
    return (
      <div className="relative inline-block">
        <div
          className={`${sizeClasses[size]} bg-white border-4 border-black transform rotate-3 animate-pulse`}
          style={{
            backgroundColor,
            boxShadow: "8px 8px 0px 0px rgba(0,0,0,1)",
          }}
        >
          <div
            className={`${sizeClasses[size]} absolute inset-0 border-4 border-black transform -rotate-6 animate-spin`}
            style={{ borderColor: color, borderRightColor: "transparent" }}
          ></div>
        </div>
      </div>
    );
  }
}

customElements.define("neon-spinner", NeonSpinner);
