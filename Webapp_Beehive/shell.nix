{pkgs, ...}: let
  name = "BeeEnv";
in
  (pkgs.buildFHSEnv {
    # The name of the environment and the wrapper executable.
    inherit name;
    # Packages to be installed for the main host's architecture
    targetPkgs = pkgs: (with pkgs; [
		python3
		python311Packages.pip
		nodePackages_latest.pyright
    ]);
	runScript = "zsh";
  })
  .env
