#
# spec file for package SFExmms2
#
# includes module(s): xmms2
#

%include Solaris.inc

%define src_name xmms2
%define src_url	 http://nchc.dl.sourceforge.net/sourceforge/%{src_name}

Name:                    SFExmms2
Summary:                 Client/server based media player system
Version:                 0.4DrKosmos
Source:                  %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:                  xmms2-01-ruby.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibsamplerate-devel
Requires: SFElibsamplerate
BuildRequires: SFEcurl-devel
Requires: SFEcurl
BuildRequires: SFElibao-devel
Requires: SFElibao
BuildRequires: SFElibmpcdec-devel
Requires: SFElibmpcdec
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFElibdiscid-devel
Requires: SFElibdiscid
BuildRequires: SFEffmpeg-devel
Requires: SFEffmpeg
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFElibmad
Requires: SFEruby
Requires: SUNWsqlite
BuildRequires: SUNWsqlite-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
unset CC CFLAGS CXX CXXFLAGS
export LINKFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
./waf	--prefix=%{_prefix}		\
	--with-mandir=%{_mandir}	\
	--destdir=$RPM_BUILD_ROOT	\
	configure

./waf build

%install
rm -rf $RPM_BUILD_ROOT
./waf --destdir=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
mv $RPM_BUILD_ROOT/usr/perl5/site_perl $RPM_BUILD_ROOT/usr/perl5/vendor_perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/xmms2
%{_libdir}/ruby
%{_libdir}/python2.*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xmms2
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_mandir}
%{_prefix}/perl5

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Bumped version to 0.4DrKosmos, add SUNWsqlite dep, add patch to
- build ruby plugin against ruby 1.9.0 (Ruby plugin patch submitted upstream).
* Sun Dec 30 2007 - markwright@internode.on.net
- Bump to 2.0.4DrKosmos
* Mon Jul 30 2007 - dougs@truemail.co.th
- initial
