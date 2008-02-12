#*******************************#
#*******************************#
#  FIXME: builds but won't run  #
#*******************************#
#*******************************#

#
# spec file for package SFEnvu
#
# includes module(s): nvu
#

%include Solaris.inc

Name:          SFEnvu
Summary:       Web authoring system based on Mozilla Composer
Version:       1.0
Source:        %{sf_download}/portablenvu/nvu-%{version}-sources.tar.bz2 
URL:           http://www.nvu.com/
Patch1:        nvu-01-moz_objdir.diff
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWzip
BuildRequires: SUNWgtar

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n %name-%version -c
cd mozilla
%patch1 -p1

sed -e 's/5\.10/5.11/g' -e 's/5_10/5_11/g' -e 's/2_10/2_11/' \
      security/coreconf/SunOS5.10.mk \
    > security/coreconf/SunOS5.11.mk
sed -e 's/5\.10/5.11/g' -e 's/5_10/5_11/g' -e 's/2_10/2_11/' \
      security/coreconf/SunOS5.10_i86pc.mk \
    > security/coreconf/SunOS5.11_i86pc.mk

%build
cd mozilla

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

export LDFLAGS="-z ignore -L%{_libdir} -L/usr/sfw/lib -R'\$\$ORIGIN:\$\$ORIGIN/..' -R%{_libdir}/mps"
export CFLAGS="-xlibmil"
export CXXFLAGS="-norunpath -xlibmil -xlibmopt -features=tmplife -lCrun -lCstd"
%ifarch sparc
export CFLAGS="$CFLAGS -xO5"
export CXXFLAGS="$CXXFLAGS -xO5"
%else
export CFLAGS="$CFLAGS -xO3"
export CXXFLAGS="$CXXFLAGS -xO3"
%endif

cat << "EOF" > .mozconfig
MOZILLA_OFFICIAL=1
export MOZILLA_OFFICIAL

BUILD_OFFICIAL=1
export BUILD_OFFICIAL

MOZ_STANDALONE_COMPOSER=1
export MOZ_STANDALONE_COMPOSER

mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options MOZ_STANDALONE_COMPOSER=1

ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --mandir=%{_mandir}
ac_add_options --with-default-mozilla-five-home=/usr/lib/nvu

ac_add_options --enable-optimize
ac_add_options --disable-debug

ac_add_options  --disable-svg
ac_add_options  --without-system-mng
ac_add_options  --without-system-png
ac_add_options  --disable-ldap
ac_add_options  --disable-mailnews
ac_add_options  --disable-installer
ac_add_options  --disable-activex
ac_add_options  --disable-activex-scripting
ac_add_options  --disable-tests
ac_add_options  --disable-oji
ac_add_options  --disable-necko-disk-cache
ac_add_options  --enable-single-profile
ac_add_options  --disable-profilesharing
ac_add_options  --enable-extensions=wallet,xml-rpc,xmlextras,pref,universalchardet,editor/cascades,spellcheck
ac_add_options  --enable-necko-protocols=http,ftp,file,jar,viewsource,res,data
ac_add_options  --disable-pedantic
ac_add_options  --disable-short-wchar
ac_add_options  --enable-xprint
ac_add_options  --enable-strip-libs
ac_add_options  --enable-crypto
ac_add_options  --disable-mathml
ac_add_options  --with-system-zlib
ac_add_options  --enable-toolkit=gtk2
ac_add_options  --enable-default-toolkit=gtk2
ac_add_options  --enable-xft
ac_add_options  --disable-freetype2

ac_add_options --enable-image-decoders=default,-xbm
EOF

BUILD_OFFICIAL=1
MOZILLA_OFFICIAL=1
MOZ_STANDALONE_COMPOSER=1
MOZ_PKG_FORMAT=BZ2
export BUILD_OFFICIAL MOZILLA_OFFICIAL MOZ_STANDALONE_COMPOSED MOZ_PKG_FORMAT

make -f client.mk build

%install
/bin/rm -rf $RPM_BUILD_ROOT

cd mozilla
BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 \
    DESTDIR=$RPM_BUILD_ROOT \
    make install

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


%files 
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/nvu
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/nvu-1.0

%files devel
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/nvu-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/idl
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Fri Jul  7 2006 - laca@sun.com
- renamed to SFEnvu
* Fri Feb  3 2006 - damien.carbery@sun.com
- Initial version.
