import { client } from "../api/client";
import { app } from "../context/app";
import { h, Component } from "../framework";

export class LoginPage extends Component {
  protected render() {
    const page = (
      <page-layout>
        <div className="w-full max-w-md mx-auto">
          <form className="bg-white rounded-lg overflow-hidden">
            <div className="p-8 space-y-4">
              <h2 className="text-4xl font-bold text-center text-black mb-6">
                Login
              </h2>

              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700"
                >
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  className="w-full px-4 py-3 border-2 border-black rounded-md text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter your email"
                />
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700"
                >
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  required
                  className="w-full px-4 py-3 border-2 border-black rounded-md text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter your password"
                />
              </div>

              <button
                type="submit"
                className="w-full !mt-8 bg-black hover:bg-gray-800 text-white font-bold py-3 px-4 rounded-md transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black"
              >
                Log In
              </button>
            </div>

            <div className="px-8 py-6 bg-yellow-300 text-black text-center">
              <p className="text-sm">
                Don't have an account?{" "}
                <router-link href="/signup">
                  <a className="font-bold hover:underline">Signup</a>
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </page-layout>
    );

    page.querySelector("form")!.addEventListener("submit", async (e) => {
      // Prevent reloading site
      e.preventDefault();

      // TODO: Fix issue with compiler not detecting value property
      const email = page.querySelector("input#email")!.value;
      const password = page.querySelector("input#password")!.value;

      try {
        await app.actions.login(email, password);
      } catch (ex) {
        console.error(ex);
      }

      console.log("Login success!");
    });

    return page;
  }
}

customElements.define("login-page", LoginPage);
