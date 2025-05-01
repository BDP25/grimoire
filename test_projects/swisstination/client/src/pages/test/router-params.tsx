import { h, Component, router } from "../../framework";

export class RouterParamsPage extends Component {
  private stateDestructor?: () => void;

  protected componentDidMount(): void {
    this.stateDestructor = router.subscribe(() => this.internalRender());
  }

  protected componentWillUnmount(): void {
    this.stateDestructor!();
  }

  protected render() {
    if (!router.value.params["id"]) {
      return (
        <page-layout>
          <p>Hello you have entered no route params</p>
        </page-layout>
      );
    }
    return (
      <page-layout>
        <p>Hello you are on page {router.value.params["id"]}</p>
      </page-layout>
    );
  }
}

customElements.define("test-router-state", RouterParamsPage);
