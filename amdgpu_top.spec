Name:           amdgpu_top
Version:        0.10.5
Release:        1%{?dist}
Summary:        Tool to displays AMDGPU usage and performance counters

License:        MIT
URL:            https://github.com/Umio-Yasuno/amdgpu_top
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  rust >= 1.70
BuildRequires:  cargo
BuildRequires:  libdrm-devel >= 2.4.110
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_amdgpu)
BuildRequires:  gcc

# Runtime dependencies
Requires:       libdrm >= 2.4.110
Requires:       libdrm-amdgpu

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

%package tui
Summary:        TUI-only version of amdgpu_top (without GUI)
Requires:       libdrm >= 2.4.110
Requires:       libdrm-amdgpu

%description tui
This package contains the TUI-only version of amdgpu_top without GUI 
dependencies, suitable for headless systems and minimal installations.

%prep
%autosetup -n %{name}-%{version}

%build
# Build full version with all features
cargo build --release --locked

# Build TUI-only version
cargo build --release --locked --no-default-features --features="tui,json" --bin amdgpu_top
mv target/release/amdgpu_top target/release/amdgpu_top-tui

# Rebuild full version
cargo build --release --locked

%install
# Install main binary
install -Dm755 target/release/amdgpu_top %{buildroot}%{_bindir}/amdgpu_top

# Install TUI-only binary
install -Dm755 target/release/amdgpu_top-tui %{buildroot}%{_bindir}/amdgpu_top-tui

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
%{_datadir}/metainfo/io.github.umio_yasuno.amdgpu_top.metainfo.xml
%{_mandir}/man1/amdgpu_top.1*

%files tui
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/amdgpu_top-tui
%{_datadir}/applications/amdgpu_top-tui.desktop

%changelog
* Mon Aug 19 2025 Petar Petrov <petar@example.com> - 0.10.5-1
- Initial COPR package for Fedora 42 and EPEL
- Added TUI-only subpackage for minimal installations
- Support for x86_64 and aarch64 architectures