#
# spec file for package seahorse
#

Name:		seahorse
Version: 	2.22.0
Release: 	0
Summary: 	GNOME2 interface for gnupg
License: 	GPL
Group: 		Applications/Cryptography
URL:		http://live.gnome.org/Seahorse
Source: 	http://ftp.gnome.org/pub/GNOME/sources/seahorse/2.22/%{name}-%{version}.tar.gz
Patch1:		%{name}-01-cryptui.diff
Patch2:		%{name}-02-open.diff
Patch3:		%{name}-03-ldap.diff
Patch4:		%{name}-04-paths.diff
BuildRoot: 	%{_tmppath}/%{name}-%{version}-build

%description
Seahorse is a gnome2 interface for gnupg.
It uses gpgme as the backend.

%prep
%setup -q 
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
autoreconf -sfi
./configure --prefix=%{_prefix}  \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir} \
	    --enable-hkp   \
	    --disable-update-mime-database     \
	    --disable-update-desktop        \
	    --disable-scrollkeeper

make 

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*
%{_libdir}/bonobo/*.so
%{_libdir}/bonobo/servers/*
%{_libdir}/gedit-2/plugins/*.so
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/omf/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/gnome/help/%{name}
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/mime/packages/*
%{_datadir}/mime-info/*
%{_sysconfdir}/gconf/schemas/*

%doc AUTHORS COPYING NEWS README TODO

%changelog
* Fri Mar 14 2008 jijun.yu@sun.com
- Bump to 2.22.0

* Tue Dec 18 2007 jijun.yu@sun.com
- Bump to 2.21.4

* Wed Oct 26 2004 Nate Nielsen <nielsen@memberwebs.com>
- Remove *.a and *.la from RPM_BUILD_ROOT
- Remove updated mime database from RPM_BUILD_ROOT

* Wed Oct 13 2004 Nate Nielsen <nielsen@memberwebs.com>
- Added new mime info 

* Tue Oct 12 2004 Nate Nielsen <nielsen@memberwebs.com>
- Added the gedit plugin to the default manifest

* Fri May 02 2003 Yanko Kaneti <yaneti@declera.com>
- Add some new files to the manifest

* Wed Jan 15 2002 Jean Schurger <yshark@schurger.org>
- Scrollkeeper stuff
- locales install by %find_lang
- secure use of rm -rf

* Tue Jan 14 2002 Yanko Kaneti <yaneti@declera.com>
- First spec
