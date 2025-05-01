import { Atom, atom } from "xoid";

import { h, Component } from "../../framework";

export class ButtonStatePage extends Component {
  private counter: Atom<number>;
  private stateDestructor?: () => void;

  constructor() {
    super();

    this.counter = atom(0);
    this.onClickButton = this.onClickButton.bind(this);
  }

  protected componentDidMount(): void {
    this.stateDestructor = this.counter.subscribe(() => this.internalRender());
  }

  protected componentWillUnmount(): void {
    this.shadowRoot!.querySelector("neon-button")!.removeEventListener(
      "click",
      this.onClickButton
    );
    this.stateDestructor!();
  }

  onClickButton() {
    console.log("Clicked");
    this.counter.update((state) => state + 1);
  }

  protected render() {
    const btn = <neon-button>Click me</neon-button>;
    btn.addEventListener("click", this.onClickButton);
    return (
      <page-layout>
        {this.counter.value == 0
          ? "No clicks so fare"
          : "Button clicked " + this.counter.value + " times"}
        {btn}
      </page-layout>
    );
  }
}

customElements.define("test-btn-state-page", ButtonStatePage);
