{ nixpkgs ? import ./nixpkgs.nix { }
}:

with nixpkgs;

stdenv.mkDerivation {
  name = "analisys-nix-shell";
  buildInputs = with python3Packages; [ python3 setuptools requests hexbytes eth-keys eth-rlp ];
}
