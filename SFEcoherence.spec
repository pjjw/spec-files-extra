#
# spec file for package SUNWcoherence
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc


Name:                    SFEcoherence
Summary:                 DLNA/UPnP framework for the digital living 
URL:                     http://coherence.beebits.net
Version:                 0.5.8
Source:                  http://coherence.beebits.net/download/Coherence-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n Coherence-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/Coherence-%{version}-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/coherence/*
%{_libdir}/python%{pythonver}/misc/*

%changelog
* Thu Oct 09 2008 - jijun.yu@sun.com
- Initial version.
