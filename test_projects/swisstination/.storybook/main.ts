import type { StorybookConfig } from "@storybook/html-vite";

import { mergeConfig } from "vite";
import projectConfig from "../vite.config";

const config: StorybookConfig = {
  stories: [
    "../stories/**/*.mdx",
    "../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)",
  ],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@chromatic-com/storybook",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/html-vite",
    options: {},
  },
  staticDirs: ["../client/public"],
  core: {
    builder: "@storybook/builder-vite",
  },
  async viteFinal(config, { configType }) {
    return mergeConfig(config, projectConfig);
  },
};
export default config;
