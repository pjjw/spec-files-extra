#
#
#

Name:		adns
Summary:	Advanced, easy to use, asynchronous-capable DNS client library
Version:	1.4
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	ftp://ftp.chiark.greenend.org.uk/users/ian/adns/%{name}-%{version}.tar.gz
# Source0-md5:	88bc7bbf3f62a8d4fb186b8f72ead853
Patch0:		%{name}-01-destdir.diff
Patch1:		adns-02-configure.diff
URL:		http://www.chiark.greenend.org.uk/~ian/adns/
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
adns is a resolver library for C (and C++) programs. In contrast with
the existing interfaces, gethostbyname et al and libresolv, it has the
following features:
- It is reasonably easy to use for simple programs which just want to
  translate names to addresses, look up MX records, etc.
- It can be used in an asynchronous, non-blocking, manner. Many
  queries can be handled simultaneously.
- Responses are decoded automatically into a natural representation
  for a C program - there is no need to deal with DNS packet formats.
- Sanity checking (eg, name syntax checking, reverse/forward
  correspondence, CNAME pointing to CNAME) is performed automatically.
- Time-to-live, CNAME and other similar information is returned in an
  easy-to-use form, without getting in the way.
- There is no global state in the library; resolver state is an opaque
  data structure which the client creates explicitly. A program can have
  several instances of the resolver.
- Errors are reported to the application in a way that distinguishes
  the various causes of failure properly.
- Understands conventional resolv.conf, but this can overridden by
  environment variables.
- Flexibility. For example, the application can tell adns to: ignore
  environment variables (for setuid programs), disable sanity checks eg
  to return arbitrary data, override or ignore resolv.conf in favour of
  supplied configuration, etc.
- Believed to be correct ! For example, will correctly back off to TCP
  in case of long replies or queries, or to other nameservers if several
  are available. It has sensible handling of bad responses etc.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"
# aclocal.m4 is only local, don't run aclocal
%{__autoconf} -f
./configure --prefix=%{_prefix}                 \
            --libdir=%{_libdir}                 \
            --bindir=%{_bindir}                 \
            --includedir=%{_includedir}         \
            --datadir=%{_datadir}               \
            --localstatedir=%{_localstatedir}   \
            --enable-dynamic			\
            --enable-shared			\
	    --disable-static
make

%install
make install \
	DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libadns.so.*.* libadns.so

%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Converted from the Linux spec
* PLD Team <feedback@pld-linux.org>
* All persons listed below can be reached at <cvs_login>@pld-linux.org

* Revision 1.32  2007/02/12 21:23:46  glen
* tabs in preamble

* Revision 1.31  2007/02/12 00:48:36  baggins
- converted to UTF-8

* Revision 1.30  2006/11/16 19:36:17  qboosh
- updated to 1.4

* Revision 1.29  2006/08/22 10:25:29  glen
- rel 3

* Revision 1.28  2006/08/20 13:18:53  qboosh
- fixed libadns.so symlink, release 2

* Revision 1.27  2006/07/27 15:45:21  tommat
- up to 1.3
- removed already aplied patches

* Revision 1.26  2004/10/24 19:57:19  paladine
- spaces->tabs
- cleanups

* Revision 1.25  2004/08/20 10:09:53  pluto
- ready for AC.
- release 4.

Revision 1.24  2004/08/18 22:56:51  pluto
- license updated.

Revision 1.23  2004/05/24 20:56:32  pluto
- gcc 3.4 fix.

Revision 1.22  2004/04/03 06:33:22  qboosh
- release 3

Revision 1.21  2004/03/29 19:02:49  qboosh
- strict internal deps, don't run aclocal (only broke build)

Revision 1.20  2003/11/23 22:36:56  speedy
- release 2, ac

Revision 1.19  2003/09/22 12:36:17  trojan
- updated to 1.1

Revision 1.18  2003/08/09 18:21:51  snurf
- fixed typo in pl desc

Revision 1.17  2003/08/06 16:05:02  kloczek
- może wrescie ktoś wykasuje to konto ?

Revision 1.16  2003/05/26 16:24:19  malekith
- massive attack: adding Source-md5

Revision 1.15  2003/05/25 05:45:24  misi3k
- massive attack s/pld.org.pl/pld-linux.org/

Revision 1.14  2002/12/12 01:33:17  blues
- spelling fixes by Tomasz "Witek" Wittner <wittt_@poczta.onet.pl>

Revision 1.13  2002/10/09 13:14:16  kloczek
- use more macros, some cosmetics, added missing "rm -f missing" and use new %doc

Revision 1.12  2002/09/07 11:06:20  kloczek
- release 4: use new %doc.

Revision 1.11  2002/05/21 23:12:40  kloczek
- perl -pi -e "s/^automake -a -c -f --foreing/\%\{__automake\}/; \
             s/^automake -a -c -f/\%\{__automake\}/; \
     s/^autoconf/\%\{__autoconf\}/"

Revision 1.10  2002/04/25 15:41:56  arturs
- fixed a small typo

Revision 1.9  2002/02/23 01:13:37  kloczek
- adapterized.

Revision 1.8  2002/02/22 23:28:40  kloczek
- removed all Group fields translations (our rpm now can handle translating
  Group field using gettext).

Revision 1.7  2002/02/13 22:45:09  ankry
- added desc from KSI; adapterized
- release 3

Revision 1.6  2002/01/18 02:12:18  kloczek
- perl -pi -e "s/pld-list\@pld.org.pl/feedback\@pld.org.pl/"

Revision 1.5  2001/12/02 14:11:04  kloczek
- release 2.

Revision 1.4  2001/11/21 13:33:03  qboosh
- pl translations, equal subpackages requires

Revision 1.3  2001/11/19 02:14:54  kloczek
- fixed %description for prog.

Revision 1.2  2001/11/19 02:14:04  kloczek
- first PLD release.
  Based on MDK spec.
