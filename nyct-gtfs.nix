{
  pythonPackages,
  fetchFromGitHub,
}:
pythonPackages.buildPythonPackage rec {
  pname = "nyct-gtfs";
  version = "ef6feab94eab1869dce81452c4b53ac8c5db31c0";

  src = fetchFromGitHub {
    owner = "Andrew-Dickinson";
    repo = "nyct-gtfs";
    rev = version;
    sha256 = "sha256-tjOltMYJPT9xxe3ycVGoVL54t/e2TiJdEJnPkMqyXJY=";
  };

  build-system = [pythonPackages.setuptools];

  pythonImportsCheck = ["nyct_gtfs"];

  doCheck = false;
  # TODO: fix checks
  preCheck = ''
    cd $src/tests
  '';
  # preCheck = ''
  #   substituteInPlace tests/test_feed_parse.py \
  #     --replace-fail test_data/a_division.nyct.gtfsrt $src/tests/test_data/a_division.nyct.gtfsrt
  # substituteInPlace tests/test_feed_parse_cpp.py \
  #   --replace-fail "test_data/a_division.nyct.gtfsrt" "${src}/tests/test_data/a_division.nyct.gtfsrt"
  # substituteInPlace tests/gtfs_parse_test_local.py \
  #   --replace-fail "test_data/2_delay.nyct.gtfsrt" "${src}/tests/test_data/2_delay.nyct.gtfsrt"
  # '';

  propagatedBuildInputs = [
    pythonPackages.requests
    pythonPackages.protobuf
    pythonPackages.httpx
  ];

  nativeCheckInputs = [
    pythonPackages.pytestCheckHook
  ];
}
