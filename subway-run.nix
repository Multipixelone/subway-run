{
  pythonPackages,
  pythonModules,
  version,
}:
pythonPackages.buildPythonApplication rec {
  inherit version;
  pname = "subway-run";
  format = "other";
  src = ./.;

  propagatedBuildInputs = pythonModules;

  dontUnpack = true;
  doCheck = false;
  pytestCheckHook = false;

  installPhase = ''
    install -Dm755 ${src}/scripts/subway-run.py $out/bin/${pname}
    sed -i '1s|^|#!/usr/bin/env python3\n|' $out/bin/${pname}
  '';
  meta.mainProgram = "subway-run";
}
