import { htmlToNode } from "../client/src/framework";

export type CardProps = {
  image?: string;
  subtitle?: string;
  title?: string;
  text?: string;
  onClick?: () => void;
};

export const createCard = ({
  image,
  subtitle,
  title,
  text,
  onClick,
}: CardProps) => {
  const elmFigure = image
    ? `<figure class="card-figure">
        <img
        src="${image}"
        alt="thumbnail"
        class="w-full h-full object-cover"
        />
    </figure>`
    : "";
  const elmSubtitle = subtitle
    ? `<p class="card-subtitle">${subtitle}</p>`
    : "";
  const elmTitle = title ? `<h1 class="card-title">${title}</h1>` : "";
  const elmText = text ? `<p class="card-text">${text}</p>` : "";

  const card = htmlToNode(`<neon-card>
      <div slot="figure">
        ${elmFigure}
      </div>
      <div slot="content">
          <div className="absolute top-2 right-2 w-12 h-12 bg-red-500 rounded-full border-4 border-black"></div>
          ${elmSubtitle}
          ${elmTitle}
          ${elmText}
      </div>
    </neon-card>`);

  if (onClick) card.addEventListener("click", onClick);
  return card;
};
