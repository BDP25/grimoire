{ pkgs, lib, config, inputs, ... }:

{
  packages = [ pkgs.git ];

  languages = {
    nix.enable = true;
    python = {
      enable = true;
      poetry.enable = true;
      poetry.activate.enable = true;
      poetry.install.enable = true;
    };
    javascript.enable = true;
  };

  pre-commit.hooks.vitest = {
    enable = true;
    name = "vitest";
    entry = "npm run test -- run";
    files = "\\.(ts|js|tsx|jsx)$";
    pass_filenames = false;
  };

  pre-commit.hooks = {
    ruff.enable = true;
    ruff-format.enable = true;
  };
}
