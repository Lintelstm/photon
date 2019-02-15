Name:           WALinuxAgent
Summary:        The Windows Azure Linux Agent
Version:        2.2.35
Release:        2%{?dist}
License:        Apache License Version 2.0
Group:          System/Daemons
Url:            https://github.com/Azure/WALinuxAgent
Source0:        %{name}-%{version}.tar.gz
Patch0:         photondistroadd.patch
%define sha1 WALinuxAgent=2cebed7efab54adb634c97519900f7a1de55403a
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-xml
BuildRequires:  systemd
BuildRequires:  python-distro
Requires:       python2
Requires:       python2-libs
Requires:       python-xml
Requires:       python-pyasn1
Requires:       openssh
Requires:       openssl
Requires:       (util-linux or toybox)
Requires:       /bin/sed
Requires:       /bin/grep
Requires:       sudo
Requires:       iptables
Requires:       systemd
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The Windows Azure Linux Agent supports the provisioning and running of Linux
VMs in the Windows Azure cloud. This package should be installed on Linux disk
images that are built to run in the Windows Azure environment.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%pre -p /bin/sh

%build
python2 setup.py build -b py2

%install
python2 -tt setup.py build -b py2 install --prefix=%{_prefix} --lnx-distro='photonos' --root=%{buildroot} --force
mkdir -p  %{buildroot}/%{_localstatedir}/log
mkdir -p -m 0700 %{buildroot}/%{_sharedstatedir}/waagent
touch %{buildroot}/%{_localstatedir}/log/waagent.log

%check
python2 setup.py check && python2 setup.py test

%post
%systemd_post waagent.service

%preun
%systemd_preun waagent.service

%postun
%systemd_postun_with_restart waagent.service


%files
/usr/lib/systemd/system/*
%defattr(0644,root,root,0755)
%doc Changelog
%attr(0755,root,root) %{_bindir}/waagent
%attr(0755,root,root) %{_bindir}/waagent2.0
%config %{_sysconfdir}/waagent.conf
%ghost %{_localstatedir}/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent
/usr/lib/python2.7/site-packages/*

%changelog
* Fri Feb 15 2019 Tapas Kundu <tkundu@vmware.com> 2.2.35-2
- Bump up release to build with latest python-distro
* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> 2.2.35-1
- Update to 2.2.35
* Wed Feb 28 2018 Anish Swaminathan <anishs@vmware.com> 2.2.22-1
- Update to 2.2.22
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.14-2
- Requires /bin/grep, /bin/sed and util-linux or toybox
* Thu Jul 13 2017 Anish Swaminathan <anishs@vmware.com> 2.2.14-1
- Update to 2.2.14
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.18-4
- Use python2 explicitly to build
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.18-3
- GA - Bump release of all rpms
* Tue May 10 2016 Anish Swaminathan <anishs@vmware.com> 2.0.18-2
- Edit post scripts
* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 2.0.18-1
- Update to 2.0.18
* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.0.14-3
- Removed redundant requires 
* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum
* Fri Mar 13 2015 - mbassiouny@vmware.com
- Initial packaging
