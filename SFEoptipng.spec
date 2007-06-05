#
# spec file for package SFEoptipng.spec
#
# includes module(s): optipng
#
%include Solaris.inc

%define src_name	optipng
%define src_url		http://switch.dl.sourceforge.net/%{src_name}

Name:                   SFEoptipng
Summary:                Advanced PNG Format File Optimizer
Version:                0.5.5
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

cd src
sed -e '/^prefix=/s+=.*$+=%{_prefix}+' \
    -e '/^mandir=/s+=.*$+=%{_mandir}+' \
    -e '/^CC.*=/d' -e '/^CFLAGS.*=/d' -e '/^LDFLAGS.*=/d' \
    -e '/^ZLIB.*=/s+=.*$+= -lz+' \
    -e '/^PNGLIB.*=/s+=.*$+= -lpng -lm+' \
    -e '/^PNGLIB.*=/s+=.*$+= -lpng -lm+' \
    -e '/^LIBS.*=/s+\$([PGNZ]*DIR)/++g' \
    -e '/^\$(OPTIPNG):/s+\$(LIBS)+$(PNGXDIR)/$(PNGXLIB)+' \
    -e 's/-I\$([PGNZ]*DIR)//g' \
    -e '/^.(PNGXDIR)..(PNGXLIB):/s/:.*$/:/' \
    scripts/unix-std.mak > scripts/unix-solaris.mak
ln -s scripts/unix-solaris.mak Makefile

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd src

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make

%install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%changelog
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
