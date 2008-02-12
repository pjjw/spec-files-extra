#
# spec file for package SFExdialog.spec
#
# includes module(s): xdialog
#
%include Solaris.inc

%define src_name	Xdialog
%define src_url		http://xdialog.free.fr

Name:                   SFExdialog
Summary:                Xdialog is a X11 drop in replacement for cdialog
Version:                2.3.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWgnome-base-libs-devel
Requires:	SUNWgnome-base-libs

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

libtoolize --force

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --with-gtk2

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Mon Apr 30 2007 - dougs@truemail.co.th
- Fixed src_url and Summary
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
