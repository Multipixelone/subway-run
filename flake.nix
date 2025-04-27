{
  description = "Multipixelone subway tracker";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      # use git commit as version (i don't like this impl but i'll be brave)
      version = toString (self.shortRev or self.dirtyShortRev or self.lastModified or "unknown");
      pkgs = nixpkgs.legacyPackages.${system};
      # python definitions & modules
      pythonPackages = pkgs.python3Packages;
      pythonModules = [
        (pkgs.callPackage ./nyct-gtfs.nix {inherit pythonPackages;})
      ];

      # packages
      subway-run = pkgs.callPackage ./subway-run.nix {inherit pythonModules pythonPackages version;};

      # devEnv
      env = pkgs.mkShell {
        venvDir = "./.venv";
        buildInputs = [
          pythonModules
          pythonPackages.python
          pythonPackages.venvShellHook
          pkgs.autoPatchelfHook
        ];
        name = "subway";
        DIRENV_LOG_FORMAT = "";
      };
    in {
      packages = {
        subway-run = subway-run;
        default = self.packages.${system}.subway-run;
      };
      devShells.default = env;
    });
}
