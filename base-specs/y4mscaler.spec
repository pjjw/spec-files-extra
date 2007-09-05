#
# spec file for package y4mscaler
#
# includes module(s): y4mscaler
#

%define src_ver 9.0
%define src_name y4mscaler
%define src_url http://www.mir.com/DMG/Software

Name:		y4mscaler
Summary:	video scaler
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}-src.tgz
Patch1:		y4mscaler-01-makefile.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export COPT="%cxx_optflags"
export LDFLAGS="%_ldflags"

make

%install
export PREFIX=%{_prefix}
export BINDIR=%{_bindir}
export MANDIR=%{_mandir}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Sep  5 2007 - dougs@truemail.co.th
- Initial base spec file
