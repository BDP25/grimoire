import { Destructor } from "xoid";
import { Component } from "../component";
import { router } from "./router";

export class RouterActivePage extends Component {
  private routerDestructor?: Destructor;

  protected componentDidMount(): void {
    this.routerDestructor = router.subscribe(() => {
      this.internalRender();
    });
  }

  protected componentWillUnmount(): void {
    this.routerDestructor!();
  }

  protected render() {
    return router.value.activeRoute.html;
  }
}

customElements.define("router-active-page", RouterActivePage);
