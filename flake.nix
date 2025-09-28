{
  description = "Flake for youtui — YouTube in your terminal";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;  # or pin a version, e.g. python38
      in {
        devShell = pkgs.mkShell {
          name = "youtui-dev-shell";

          buildInputs = with pkgs; [
            python
            yt-dlp
            mpv
            fzf
          ];

          # optionally you can set PYTHONPATH or other environment vars
          shellHook = ''
            export PYTHONPATH=${toString ./.}
          '';
        };

        packages = {
          youtui = pkgs.python3Packages.buildPythonApplication {
            pname = "youtui";
            version = "0.1.0";
            src = ./.;

            format = "other"; # <-- tells nix not to expect setup.py/pyproject

            propagatedBuildInputs = with pkgs.python3Packages; [
                yt-dlp
            ];

            nativeBuildInputs = [
                pkgs.makeWrapper
            ];

            installPhase = ''
                mkdir -p $out/bin
                cp youtui.py $out/bin/youtui
                chmod +x $out/bin/youtui
                wrapProgram $out/bin/youtui \
                --prefix PATH : ${pkgs.lib.makeBinPath [ pkgs.mpv pkgs.fzf ]}
            '';

            meta = with pkgs.lib; {
                description = "YouTube in your terminal via mpv / fzf";
                license = licenses.mit;
                platforms = platforms.unix;
            };
          };
        };

        # optionally provide a default “app” or overlay
        defaultPackage = self.outputs.packages.${system}.youtui;
        defaultApp = {
          type = "app";
          program = "${self.outputs.packages.${system}.youtui}/bin/youtui";
        };
      });
}
