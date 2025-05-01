import { h, Component } from "../framework";

export class NeonCard extends Component {
  static get observedAttributes() {
    return ["label", "color"];
  }

  protected render() {
    return (
      <article className="card">
        {/* 
        TODO: this adds a line as border below the figure (bug)
        currently not used so lets comment it out
        
        <div className="card-figure">
          <slot name="figure"></slot>
        </div> */}
        <div className="card-content">
          <slot name="content"></slot>
        </div>
      </article>
    );
  }
}

customElements.define("neon-card", NeonCard);
