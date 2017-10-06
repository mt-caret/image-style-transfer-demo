with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "image-style-transfer-demo";
  version = "0.0.1";

  src = ./.;

  installPhase = ''
    mkdir -p $out/bin
    cp -r ./* $out/bin
    patchShebangs $out/bin/app.py
  '';

  propagatedBuildInputs = [
    (pkgs.python35.withPackages (ps: [
      ps.scipy
      ps.flask
      ps.gunicorn
      ps.tensorflow
      ps.pillow
      ps.redis
      (ps.buildPythonPackage rec {
        name = "${pname}-${version}";
        pname = "rq";
        version = "0.8.2";
        propagatedBuildInputs = [ ps.click ps.redis ];
        src = ps.fetchPypi {
          inherit pname version;
          sha256 = "1xl9idic5q06zggnbss8i3ighjkla0pndhvca11vawrh3in3b4qx";
        };
      })
    ]))
    pkgs.redis
  ];

  meta = {
    homepage = https://github.com/mt-caret/image-style-transfer-demo;
    license = licenses.mit;
  };
}
