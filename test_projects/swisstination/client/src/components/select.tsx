import { h, Component } from "../framework";

export class NeonSelect extends Component {
  static get observedAttributes() {
    return ["id", "name", "value"];
  }

  public value: any;

  protected render() {
    const currentValue = this.getAttribute("value");
    return (
      <select
        id={this.getAttribute("id") || ""}
        name={this.getAttribute("name") || ""}
        className="border-black border-2 p-2.5 focus:outline-none focus:shadow-[2px_2px_0px_rgba(0,0,0,1)]"
        onInput={(e) => {
          this.value = (e.target as HTMLInputElement).value;
          const event = new Event("input");
          this.dispatchEvent(event);
        }}
      >
        {
          Array.from(this.children).map((child) => {
            if (child.getAttribute("value") == currentValue) {
              child.setAttribute("selected", "");
            } else {
              child.removeAttribute("selected");
            }
            return child;
          }) as any
        }
      </select>
    );
  }
}

customElements.define("neon-select", NeonSelect);
