import type { Preview } from "@storybook/html";

import "../client/src/main";
import "../client/src/css/styles.css";

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
