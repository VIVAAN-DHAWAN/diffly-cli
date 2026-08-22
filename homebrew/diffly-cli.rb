class DifflyCli < Formula
  desc "Deterministic triage for large GitHub pull requests"
  homepage "https://github.com/VIVAAN-DHAWAN/diffly-cli"
  url "https://github.com/VIVAAN-DHAWAN/diffly-cli/releases/download/v0.4.0/diffly_cli-0.4.0.tar.gz"
  sha256 "8823266f2755196933141edaa72b269f33d873ac09bd637925a2923550e99877"
  license "MIT"

  depends_on "python@3.13"

  def install
    python3 = Formula["python@3.13"].opt_bin/"python3.13"
    venv = libexec/"venv"
    system python3, "-m", "venv", venv
    venv_pip = venv/"bin/pip"
    system venv_pip, "install", "--upgrade", "pip"
    system venv_pip, "install", buildpath
    bin.install_symlink venv/"bin/diffly"
    bin.install_symlink venv/"bin/diffly-cli"
  end

  test do
    assert_match "diffly", shell_output("#{bin}/diffly version")
  end
end
