Name:           amdgpu_top
Version:        0.10.5
Release:        4%{?dist}
Summary:        Tool to displays AMDGPU usage and performance counters

%global debug_package %{nil}

License:        MIT
URL:            https://github.com/Umio-Yasuno/amdgpu_top
Source0:        https://github.com/perosredo/amdgpu_top/archive/refs/tags/v%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

%if 0%{?fedora}
BuildRequires:  rust >= 1.70
BuildRequires:  cargo
%endif
%if 0%{?epel}
BuildRequires:  rust >= 1.70
BuildRequires:  cargo
%endif
BuildRequires:  libdrm-devel >= 2.4.110
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_amdgpu)
BuildRequires:  gcc
BuildRequires:  clang

# Runtime dependencies
Requires:       libdrm >= 2.4.110

%description
amdgpu_top is a tool that displays AMD GPU utilization, similar to nvidia-smi
or intel_gpu_top. The tool displays information gathered from performance 
counters (GRBM, GRBM2), sensors, fdinfo, gpu_metrics and AMDGPU driver.

Features:
- Simple TUI mode (like nvidia-smi, rocm-smi)
- Full TUI mode with detailed monitoring
- GUI mode with graphical interface
- JSON output for automation/scripting
- Process monitoring and memory usage tracking
- Performance counter access
- GPU metrics and sensor data

%prep
%autosetup

%build
# Build with all features enabled
cargo build --release --locked --no-default-features --features="libdrm_link,tui,gui,json"

%install
# Install main binary
install -Dm755 target/release/amdgpu_top %{buildroot}%{_bindir}/amdgpu_top

# Install desktop files
install -Dm644 assets/amdgpu_top.desktop %{buildroot}%{_datadir}/applications/amdgpu_top.desktop
install -Dm644 assets/amdgpu_top-tui.desktop %{buildroot}%{_datadir}/applications/amdgpu_top-tui.desktop

# Install metainfo
install -Dm644 assets/io.github.umio_yasuno.amdgpu_top.metainfo.xml %{buildroot}%{_datadir}/metainfo/io.github.umio_yasuno.amdgpu_top.metainfo.xml

# Install man page if it exists
if [ -f docs/amdgpu_top.1 ]; then
    install -Dm644 docs/amdgpu_top.1 %{buildroot}%{_mandir}/man1/amdgpu_top.1
fi

%files
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/amdgpu_top
%{_datadir}/applications/amdgpu_top.desktop
%{_datadir}/applications/amdgpu_top-tui.desktop
%{_datadir}/metainfo/io.github.umio_yasuno.amdgpu_top.metainfo.xml
%{_mandir}/man1/amdgpu_top.1*

%changelog
* Tue Aug 20 2024 ps <ps@nunya> - 0.10.5-3
- Remove libdrm-amdgpu from Requires as it doesn't exist as separate package
- libdrm_amdgpu.so is provided by main libdrm package

* Tue Aug 20 2024 ps <ps@nunya> - 0.10.5-2
- Fixed build by removing non-existent amdgpu_top-tui binary and subpackage
- The upstream project builds a single binary with all features integrated

* Mon Aug 19 2024 ps <ps@nunya> - 0.10.5-1
- Initial COPR package for Fedora 42 and EPEL
- Support for x86_64 and aarch64 architectures