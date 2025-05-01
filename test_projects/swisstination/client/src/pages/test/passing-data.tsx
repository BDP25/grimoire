import { atom } from "xoid";
import { h, Component, router } from "../../framework";

class Consumer extends Component {
  public counter?: number;

  protected render() {
    return <p>Child: {this.counter}</p>;
  }
}

export class PasingDataPage extends Component {
  private counter;

  constructor() {
    super();
    this.counter = atom(0);
  }

  protected componentInitSubs(): (() => void)[] {
    return [this.counter.subscribe(() => this.internalRender())];
  }

  protected render() {
    return (
      <page-layout>
        <neon-button onClick={() => this.counter.update((state) => state + 1)}>
          Click me
        </neon-button>
        <p>Parent: {this.counter.value}</p>
        <test-passing-data-consumer data-counter={this.counter.value} />
      </page-layout>
    );
  }
}

customElements.define("test-passing-data-page", PasingDataPage);
customElements.define("test-passing-data-consumer", Consumer);
