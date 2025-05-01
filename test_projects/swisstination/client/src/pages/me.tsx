import { Destructor } from "xoid";
import { app } from "../context/app";
import { h, router, Component } from "../framework";
import { client } from "../api/client";

export class MePage extends Component {
  private appDestructor?: Destructor;

  protected componentDidMount(): void {
    this.appDestructor = app.subscribe(() => {
      this.internalRender();
    });
  }

  protected componentWillUnmount(): void {
    this.appDestructor!();
  }

  logoutUser() {
    app.actions.logout();
    router.actions.navigateTo("/home");
  }

  authenticateUser(route: string) {
    router.actions.navigateTo(route);
  }

  protected render() {
    if (!app.value.currentUser) {
      return (
        <page-layout>
          <div className="w-full flex flex-col justify-center items-center mt-12">
            <h1 className="text-xl card-subtitle">
              Whoops..., you must login first!
            </h1>
            <div className="flex flex-row justify-center gap-12 items-center">
              <neon-button
                color="green"
                onClick={() => this.authenticateUser("/signup")}
              >
                Signup
              </neon-button>
              <neon-button
                color="yellow"
                onClick={() => this.authenticateUser("/login")}
              >
                Login
              </neon-button>
            </div>
          </div>
        </page-layout>
      );
    }
    return (
      <page-layout>
        <div className="max-w-4xl mx-auto py-8 px-4">
          <neon-card color="yellow">
            <div slot="content">
              <div className="w-7 h-7 rounded"></div>
              <div className="card-subtitle flex flex-row justify-start items-center gap-8">
                <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-black">
                  <img
                    src={client.users.getAvatarURI(app.value.currentUser)}
                    alt="User avatar"
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex flex-col">
                  <h1 className="text-3xl font-bold">
                    {app.value.currentUser?.username}
                  </h1>
                  <span>
                    Member since:{" "}
                    {new Date(
                      app.value.currentUser?.date_joined ?? ""
                    ).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <p className="text-gray-700">
                <span className="font-medium">Location:</span>{" "}
                {app.value.currentUser?.location ?? "Not provided"}
              </p>
              <p className="text-gray-700">
                <span className="font-medium">Bio:</span>{" "}
                {app.value.currentUser?.bio ?? "No bio available"}
              </p>
              <div className="w-full flex flex-row gap-4 items-center justify-between mt-12">
                <neon-button color="yellow">Edit Profile</neon-button>
                <neon-button color="red" onClick={this.logoutUser}>
                  Logout
                </neon-button>
              </div>
            </div>
          </neon-card>
        </div>
      </page-layout>
    );
  }
}

customElements.define("me-page", MePage);
