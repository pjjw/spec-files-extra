#
# spec file for package SFEpyopenssl
#
# includes module(s): openssl
#

%include Solaris.inc
Name:                    SFEpyopenssl
Summary:                 Python Interface to the OpenSSL library
URL:                     http://pyopenssl.sourceforge.net/
Version:                 0.7
Source:                  http://internap.dl.sourceforge.net/sourceforge/pyopenssl/pyOpenSSL-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n pyOpenSSL-%version

%build
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=%{buildroot}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/OpenSSL/*

%changelog
* Mon Apr 28 2008 - brian.cameron@sun.com
- Created
