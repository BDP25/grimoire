import { h, Component, router } from "../framework";

export class Navbar extends Component {
  protected render() {
    const page = (
      <div>
        <nav className="fixed w-full bg-white z-50">
          <div className="my-2 px-4 md:px-6">
            <div className="flex justify-between h-16">
              <div className="flex-shrink-0 flex items-center">
                <a
                  href="/"
                  className="text-3xl font-bold hero-font text-red-400"
                >
                  Swisstination
                </a>
              </div>
              <div className="hidden md:flex items-center space-x-4">
                <router-link href="/home">
                  <a className="text-black hover:border-b-2 hover:border-black">
                    Home
                  </a>
                </router-link>
                <router-link href="/tours">
                  <a className="text-black hover:border-b-2 hover:border-black">
                    Tours
                  </a>
                </router-link>
                <router-link href="/about">
                  <a className="text-black hover:border-b-2 hover:border-black">
                    About
                  </a>
                </router-link>
                <login-button />
              </div>
              <div className="flex justify-end items-center space-x-2 md:hidden">
                <login-button />
                <button id="menu-btn" className="btn w-10 h-10 p-2">
                  <img
                    src="/icons/ni-list.svg"
                    alt="menu"
                    className="w-6 h-6"
                  />
                </button>
              </div>
            </div>
          </div>
        </nav>
        <div
          id="overlay"
          className="fixed inset-0 bg-gray-800 opacity-25 hidden z-40"
        ></div>
        <div
          id="mobile-sidebar"
          className="fixed inset-y-0 left-0 w-5/6 bg-white shadow-lg transform -translate-x-full transition-transform duration-300 ease-in-out z-50"
        >
          <div className="p-4">
            <button id="close-btn" className="text-gray-700 focus:outline-none">
              <img src="/icons/ni-x.svg" alt="close" className="w-8 h-8" />
            </button>
            <div className="mt-6 flex flex-col items-center justify-center space-y-4">
              <router-link href="/home">
                <a className="text-black hover:border-b-2 hover:border-black">
                  Home
                </a>
              </router-link>
              <router-link href="/tours">
                <a className="text-black hover:border-b-2 hover:border-black">
                  Tours
                </a>
              </router-link>
              <router-link href="/about">
                <a className="text-black hover:border-b-2 hover:border-black">
                  About
                </a>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    );

    const menuBtn = page.querySelector("#menu-btn")!;
    const closeBtn = page.querySelector("#close-btn")!;
    const mobileSidebar = page.querySelector("#mobile-sidebar")!;
    const overlay = page.querySelector("#overlay")!;
    const links = page.querySelectorAll(".link");

    function openSidebar() {
      mobileSidebar.classList.remove("-translate-x-full");
      overlay.classList.remove("hidden");
    }
    function closeSidebar() {
      mobileSidebar.classList.add("-translate-x-full");
      overlay.classList.add("hidden");
    }

    menuBtn.addEventListener("click", () => openSidebar());
    closeBtn.addEventListener("click", () => closeSidebar());
    overlay.addEventListener("click", () => closeSidebar());

    links.forEach((link) => {
      link.addEventListener("click", () => closeSidebar());
    });

    return page;
  }
}

customElements.define("page-navbar", Navbar);
