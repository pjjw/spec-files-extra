#
#
#

Summary:	Rockin' asteroids game
Name:		Maelstrom
Version:	3.0.6
Release:	6
License:	GPL for code, artwork and sounds can be redistributed only with Maelstrom
Group:		X11/Applications/Games
Source0:	http://www.devolution.com/~slouken/projects/Maelstrom/src/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Patch0:		%{name}-00-cheaters.diff
Patch1:		%{name}-01-dirs.diff
Patch2:		%{name}-02-amfix.diff
Patch3:		%{name}-03-sec.diff
Patch4:		%{name}-04-configure.diff
URL:		http://www.devolution.com/~slouken/projects/Maelstrom/
BuildRequires:	SDL_net-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Maelstrom is a rockin' asteroids game ported from the Macintosh
Originally written by Andrew Welch of Ambrosia Software, and ported to
UNIX and then SDL by Sam Lantinga <slouken@devolution.com>.

%prep
%setup	-q
# everlasting shield, more shots available, all-in-one equipment and
# reversed bonus in time function ;)
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
touch NEWS AUTHORS ChangeLog

%build
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

libtoolize -f -c
aclocal
autoconf -f
automake -f -a -c
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
	    --datadir=%{_datadir}		\
	    --localstatedir=%{_localstatedir}	\
	    --enable-shared
%{__make}

%install
%define		_gamedir	%{_datadir}/Maelstrom
%define		_desktopdir	%{_datadir}/applications

install -d $RPM_BUILD_ROOT{%{_localstatedir}/games,%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_gamedir}/Images/Makefile*
rm -f Docs/Makefile*

# /usr is read-only
mv -f $RPM_BUILD_ROOT%{_gamedir}/Maelstrom-Scores $RPM_BUILD_ROOT/var/games
(
  cd $RPM_BUILD_ROOT%{_gamedir}
  ln -sf Maelstrom-Scores ../../%{_gamedir}/Maelstrom-Scores
)

# not needed (examples for internal Mac library)
# and playwave conflicts with SDL_mixer
rm -f $RPM_BUILD_ROOT%{_bindir}/{macres,playwave,snd2wav}

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Converted from the Linux spec
* PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

Revision 1.24  2007/03/13 09:51:25  sparky
- place # SourceN-md5: just after SourceN:

Revision 1.23  2007/02/12 21:23:44  glen
- tabs in preamble

Revision 1.22  2007/02/12 00:48:33  baggins
- converted to UTF-8

Revision 1.21  2006/10/17 18:19:13  qboosh
- cleanup
- score file writable for games group only
- release 6

Revision 1.20  2005/12/04 23:10:17  glen
- adapterized (sorted %verify flags)

Revision 1.19  2005/04/25 18:57:34  tiwek
- update patch

Revision 1.18  2004/07/04 00:23:00  havner
- wrrr

Revision 1.17  2004/06/20 21:36:19  arekm
- fix specflags (quotation here is buggy)

Revision 1.16  2004/03/16 16:08:11  undefine
- pt_BR translations from conectiva

Revision 1.15  2003/12/03 13:38:40  gotar
- _applnkdir -> _desktopdir

Revision 1.14  2003/06/28 19:36:24  gotar
- -fomit-frame-pointer on ia32

Revision 1.13  2003/06/22 20:37:04  gotar
- added some useful comment

Revision 1.12  2003/06/19 19:54:00  radek
- release 3: fixed .desktop

Revision 1.11  2003/06/04 18:01:29  radek
- fixed URLs, added md5 checksum

Revision 1.10  2003/05/26 16:24:19  malekith
- massive attack: adding Source-md5

Revision 1.9  2003/05/25 05:45:21  misi3k
- massive attack s/pld.org.pl/pld-linux.org/

Revision 1.8  2003/05/21 16:29:48  misi3k
- rel 2
- added sec patch (Maelstrom Local Buffer Overflow)

Revision 1.7  2003/02/08 00:02:58  gotar
- upgraded to 3.0.6 (fixes)

Revision 1.6  2003/01/19 18:45:14  qboosh
- typo in Group

Revision 1.5  2003/01/18 22:53:34  juandon
- removed two lines with define

Revision 1.4  2002/10/20 07:56:03  gotar
- changed URLs to local

Revision 1.3  2002/09/10 20:02:46  kloczek
- cleanups.

Revision 1.2  2002/06/27 21:53:14  qboosh
- fixed FHS compl.: added dirs patch, moved data to %%{_datadir}/Maelstrom,
  scores to /var/games
- amfix patch to allow rebuild ac/am
- resolved conflict with SDL_mixer
- release 2

Revision 1.1  2002/06/19 23:07:40  gotar
- initial release, STBR.
