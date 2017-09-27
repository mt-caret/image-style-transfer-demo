with import <nixpkgs> {};

(pkgs.python35.buildEnv.override {
  extraLibs = with pkgs.python35Packages; [
    flask
    tensorflow
  ];
}).env
