import { Destructor } from "xoid";
import { h, Component, router } from "../framework";
import { app } from "../context/app";
import { client } from "../api/client";

export class LoginButton extends Component {
  private appDestructor?: Destructor;

  constructor() {
    super();
    this.handleLoginOnClick = this.handleLoginOnClick.bind(this);
  }

  handleLoginOnClick() {
    router.actions.navigateTo("/login");
  }

  handleProfileMeClick() {
    router.actions.navigateTo("/me");
  }

  protected componentDidMount(): void {
    this.appDestructor = app.subscribe(() => {
      this.internalRender();
    });
  }

  protected componentWillUnmount(): void {
    this.appDestructor!();
  }

  protected render() {
    if (!app.value.currentUser) {
      return (
        <button
          id="login-btn"
          className="btn h-10 w-20 bg-cyan-200 hover:bg-cyan-300 active:bg-cyan-400"
          onClick={this.handleLoginOnClick}
        >
          Login
        </button>
      );
    }
    return (
      <button
        id="me-view"
        className="flex items-center gap-3 btn btn h-10 p-2"
        onClick={this.handleProfileMeClick}
      >
        <div className="w-7 h-7 rounded-full overflow-hidden border-2 border-black">
          <img
            src={client.users.getAvatarURI(app.value.currentUser)}
            alt="User avatar"
            className="w-full h-full object-cover"
          />
        </div>
        <span className="text-black">{app.value.currentUser.username}</span>
      </button>
    );
  }
}

customElements.define("login-button", LoginButton);
