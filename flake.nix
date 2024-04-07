{
  description = "Beehive Project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    python-ver.url ="github:nixos/nixpkgs/10b813040df67c4039086db0f6eaf65c536886c6";
	pip2nix.url = "github:nix-community/pip2nix";
  };

  outputs = { self, nixpkgs, mach-nix,... }@inputs:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

  in
  {
	packages.${system}.default = pkgs.stdenv.mkDerivation{};
    devShells.x86_64-linux.default = pkgs.mkShell {
      nativeBuildInputs = with pkgs; [
        inputs.python-ver.legacyPackages.${system}.python3
      ];
    };

  };
}


