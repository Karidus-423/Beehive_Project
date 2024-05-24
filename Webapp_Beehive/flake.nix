{
  description = "Beehive Project Python Environment Flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
	flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (system:
  let
	name = "Bee-Env";
	system = "x86_64-linux";
	pkgs = nixpkgs.legacyPackages.${system};
  in
  {
	devShells.default = (pkgs.buildFHSEnv {
    inherit name;

    targetPkgs = pkgs: (with pkgs; [
		python3
		python311Packages.pip
		nodePackages_latest.pyright
    ]);
	runScript = "zsh";
  })
  .env;
  });
}
