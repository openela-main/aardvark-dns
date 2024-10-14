# debuginfo doesn't work yet
%global debug_package %{nil}

%global aardvark_dns_branch v1.10.1-rhel
%global aardvark_dns_commit0 3d0fec1eb11bfe722ed645c5717425195d4d481f
%global aardvark_dns_shortcommit0 %(c=%{aardvark_dns_commit0}; echo ${c:0:7})

Epoch: 2
Name: aardvark-dns
Version: 1.10.1
License: ASL 2.0 and BSD and MIT
Release: 2%{?dist}
ExclusiveArch: %{rust_arches}
Summary: Authoritative DNS server for A/AAAA container records
URL: https://github.com/containers/aardvark-dns
%if 0%{?aardvark_dns_branch:1}
Source0: https://github.com/containers/aardvark-dns/tarball/%{aardvark_dns_commit0}/%{aardvark_dns_branch}-%{aardvark_dns_shortcommit0}.tar.gz
%else
Source0: https://github.com/containers/aardvark-dns/archive/%{aardvark_dns_commit0}/aardvark-dns-%{aardvark_dns_branch}-%{aardvark_dns_shortcommit0}.tar.gz
%endif
Source1: https://github.com/containers/aardvark-dns/releases/download/%{aardvark_dns_version}/aardvark-dns-%{aardvark_dns_branch}-vendor.tar.gz
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
tar fx %{SOURCE0}
%if 0%{?aardvark_dns_branch:1}
pushd containers-aardvark-dns-%{aardvark_dns_shortcommit0}
%else
pushd aardvark-dns-%{aardvark_dns_commit0}
%endif
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
%if 0%{?aardvark_dns_branch:1}
pushd containers-aardvark-dns-%{aardvark_dns_shortcommit0}
%else
pushd aardvark-dns-%{aardvark_dns_commit0}
%endif
%__scm_setup_git -q
%make_build build
popd

%install
%if 0%{?aardvark_dns_branch:1}
pushd containers-aardvark-dns-%{aardvark_dns_shortcommit0}
%else
pushd aardvark-dns-%{aardvark_dns_commit0}
%endif
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
popd

%files
%if 0%{?aardvark_dns_branch:1}
%license containers-aardvark-dns-%{aardvark_dns_shortcommit0}/LICENSE
%else
%license aardvark-dns-%{aardvark_dns_commit0}/LICENSE
%endif
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}

%changelog
* Wed Sep 25 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.1-2
- build off the RHEL maintenance branch
- Resolves: RHEL-59129

* Thu Jan 25 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.10.0
- Related: Jira:RHEL-2110

* Thu Dec 07 2023 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.9.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.9.0
- Related: Jira:RHEL-2110

* Fri Sep 29 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.8.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.8.0
- Related: Jira:RHEL-2110

* Mon Jul 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.7.0
- Related: #2176055

* Thu May 11 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.6.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.6.0
- Related: #2176055

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-2
- always stay offline during build
- Related: #2123641

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.5.0
- Related: #2123641

* Thu Dec 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.4.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.4.0
- Related: #2123641

* Mon Nov 14 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.3.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.3.0
- Related: #2123641

* Wed Sep 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.2.0-1
- update to https://github.com/containers/aardvark-dns/releases/tag/v1.2.0
- Related: #2116481
* Wed Aug 24 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-4
- remove windows binaries and regenerate vendor tarball
- Related: #2061390

* Tue Aug 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-3
- add gating.yaml
- Related: #2061390

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-2
- bump Epoch to preserve upgrade path
- Related: #2061390

* Wed Aug 3 2022 Jindrich Novy <jnovy@redhat.com> 1.1.0-1
- initial import
- Related: #2061390
