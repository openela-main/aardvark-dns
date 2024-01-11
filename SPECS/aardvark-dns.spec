# debuginfo doesn't work yet
%global debug_package %{nil}

Epoch: 2
Name: aardvark-dns
Version: 1.7.0
License: ASL 2.0 and BSD and MIT
Release: 1%{?dist}
ExclusiveArch: %{rust_arches}
Summary: Authoritative DNS server for A/AAAA container records
URL: https://github.com/containers/aardvark-dns
Source0: %{url}/archive/v%{version}.tar.gz
Source1: %{url}/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
BuildRequires: cargo
BuildRequires: git-core
BuildRequires: make
BuildRequires: rust-srpm-macros
Conflicts: netavark < %{epoch}:%{version}

%description
%{summary}

Forwards other request to configured resolvers.
Read more about configuration in `src/backend/mod.rs`.

%prep
%autosetup -Sgit
tar fx %{SOURCE1}
mkdir -p .cargo

cat >.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

[net]
offline = true
EOF

%build
%{__make} build

%install
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%files
%license LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}

%changelog
* Fri Jul 07 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.7.0
- Related: #2176063

* Wed Apr 12 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.6.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.6.0
- Related: #2176063

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-2
- build always offline
- Related: #2124478

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.5.0
- Related: #2124478

* Thu Dec 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.4.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.4.0
- Related: #2124478

* Wed Nov 16 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.3.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.3.0
- Related: #2124478

* Tue Oct 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.2.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.2.0
- Related: #2124478

* Wed Aug 24 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-4
- remove windows binaries and regenerate vendor tarball
- Related: #2061316

* Tue Aug 23 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-3
- conflict with older versions than aardvark-dns itself
- Related: #2061316

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-2
- add Epoch to preserve upgrade path
- Related: #2061316

* Wed Aug 3 2022 Jindrich Novy <jnovy@redhat.com> 1.1.0-1
- initial import
- Related: #2061316
