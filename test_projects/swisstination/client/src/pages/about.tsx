import { h, Component } from "../framework";

interface SocialMediaLink {
  name: string;
  icon: string;
  url: string;
}

export class AboutPage extends Component {
  protected readonly socialMediaLinks: SocialMediaLink[] = [
    {
      name: "X",
      icon: "/icons/x.svg",
      url: "https://x.com/swisstination",
    },
    {
      name: "Instagram",
      icon: "/icons/instagram.svg",
      url: "https://instagram.com/swisstination",
    },
    {
      name: "TikTok",
      icon: "/icons/tiktok.svg",
      url: "https://tiktok.com/@swisstination",
    },
    {
      name: "Facebook",
      icon: "/icons/facebook.svg",
      url: "https://facebook.com/swisstination",
    },
  ];

  protected render() {
    return (
      <page-layout>
        <div className="flex flex-col gap-4 text-justify md:w-1/2 md:m-auto">
          <h1 className="text-3xl">About Swisstination</h1>
          <p>
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
            nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
            erat, sed diam voluptua.
          </p>
          <img src="/icons/nc-reviewing.svg" />
          <p>
            At vero eos et accusam et justo duo dolores et ea rebum. Stet clita
            kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
            amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed
            diam nonumy eirmod tempor invidunt ut labore et dolore magna
            aliquyam erat, sed diam voluptua.
          </p>
          <div className="flex justify-center mt-6">
            <neon-button color="pink">Subscribe to the Newsletter!</neon-button>
          </div>
          <div className="flex flex-row justify-center my-6">
            {this.socialMediaLinks.map((link) => (
              <a
                href={link.url}
                className="mr-4 transition ease-in-out delay-150 duration-300 hover:scale-110 hover:-translate-y-1"
                rel="noopener noreferrer nofollow"
                target="_blank"
              >
                <img src={link.icon} alt={link.name} className="w-6 h-6" />
              </a>
            ))}
          </div>
        </div>
      </page-layout>
    );
  }
}

customElements.define("about-page", AboutPage);
