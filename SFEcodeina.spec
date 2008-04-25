#
# spec file for package SFEcodeina
#
# includes module(s): codeina
#
# Note that codeina does not seem to work on Solaris.  This may because
# my two patches hack the code in bad ways, or because OpenSSL is not
# present, or perhaps the code needs further work to be functional on
# Solaris.  However, I wanted to make this spec file available so that
# people could build the code and hopefully help get it working.
#
# Note there has not been a codeina tarball release, so downloading
# from the URL will fail.  You need to build a tarball by hand from SVN,
# change the autogen.sh to start with "#!/bin/bash" instead # of
# "#!/bin/sh", and run autogen.sh.  Then run "make dist" to create a
# tarball to build with.
#
# Note that Solaris does not have the OpenSSL module which codeina 
# requires.  Just to get codeina to build, I commented it out of the
# configure.ac file before running autogen.sh.
#
# To access codeina from subversion:
#
# svn co https://core.fluendo.com/gstreamer/svn/codeina/trunk/ codeina
#
%define pythonver 2.4

%include Solaris.inc

Name:		SFEcodeina
Summary:	Codec Installe:w
Version:	0.10.2.1
URL:		http://fedoraproject.org/wiki/Multimedia/Codeina
# Note this URL does not work, there is not yet a codeina release.
# See instructions at the top of the spec-file.
#
Source0:	http://fedoraproject.org/wiki/Multimedia/Codeina/codeina-%{version}.tar.bz2
Patch1:         codeina-01-fixpython.diff
Patch2:         codeina-02-nolsb.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/codeina-%{version}-build
Requires:	SUNWgnome-python-libs
Requires:	SUNWgnome-media
Requires:	SUNWgst-python
Requires:	SFEpyyaml
Requires:	SFEnotify-python
BuildRequires:	SUNWPython-devel >= %{pythonver}
BuildRequires:	SUNWgst-python
BuildRequires:	SFEpyyaml
BuildRequires:	SFEnotify-python

%include default-depend.inc

%description
Codeina informs the user about the value of open formats and can optionally
function as a codec installer for gstreamer applications such as Totem that
currently installs Fluendo codecs.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root
Requires: SUNWgnome-config

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n codeina-%version
%patch1 -p1
%patch2 -p1

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS -I common/m4
autoconf
automake -a -c -f
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-??_??.omf
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/codeina
%{_bindir}/codeina.bin
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/codeina.desktop
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*
%{_datadir}/codeina/*

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/codeina/*
%{_sysconfdir}/xdg/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
#FIXME: Not in 2.22.0:%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%changelog
* Thu Apr 10 2008 - brian.cameron@sun.com
- New spec file. 

