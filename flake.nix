{
  description = "Use prebuild anysnake2-musl";

  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs?rev=7e9b0dff974c89e070da1ad85713ff3c20b0ca97";

    };
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      defaultPackage.x86_64-linux = pkgs.stdenv.mkDerivation rec {
        name = "anysnake";
        version = "1.14.0";
        src = pkgs.fetchurl {
          url =
            "https://github.com/TyberiusPrime/anysnake2/releases/download/${version}/anysnake2_${version}_x86_64-unknown-linux-musl.tar.gz";
          sha256 = "sha256-0a+JcG5yoAQOku/AD3xg3Yt0ijPXhP5sVNAqDwOA6Tg=";
        };
        sourceRoot = ".";
        installPhase = ''
          mkdir $out/bin -p
          cp /build/anysnake2 $out/bin/
        '';
      };
    };
}
