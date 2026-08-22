class DifflyCli < Formula
  include Language::Python::Virtualenv

  desc "Deterministic triage for large GitHub pull requests"
  homepage "https://github.com/VIVAAN-DHAWAN/diffly-cli"
  url "https://github.com/VIVAAN-DHAWAN/diffly-cli/releases/download/v0.4.0/diffly_cli-0.4.0.tar.gz"
  sha256 "8823266f2755196933141edaa72b269f33d873ac09bd637925a2923550e99877"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources(using: "python@3.13")
  end

  test do
    assert_match "diffly", shell_output("#{bin}/diffly version")
  end
end
