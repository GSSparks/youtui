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
            python.pkgs.yt_dlp
            mpv
            fzf
          ];

          # optionally you can set PYTHONPATH or other environment vars
          shellHook = ''
            export PYTHONPATH=${toString ./.}
          '';
        };

        packages = {
          youtui = pkgs.stdenv.mkDerivation {
            pname = "youtui";
            version = "0.1.0";  # update as needed

            src = ./.;

            nativeBuildInputs = [ pkgs.python3 ];
            propagatedBuildInputs = [
              python.pkgs.yt_dlp
              mpv
              fzf
            ];

            # Since this is a Python script, we can just “install” the script
            installPhase = ''
              mkdir -p $out/bin
              cp youtui.py $out/bin/youtui
              wrapProgram $out/bin/youtui \
                --set PYTHONPATH "${python.sitePackages}"
            '';

            meta = with pkgs.lib; {
              description = "YouTube in your terminal via mpv / fzf";
              license = licenses.mit;
              maintainers = [ ];
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
