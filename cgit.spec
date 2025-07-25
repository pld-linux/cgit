Summary:	cgit - a fast webinterface to git
Summary(pl.UTF-8):	cgit - szybki interfejs WWW do gita
Name:		cgit
Version:	0.10.2
Release:	1
License:	GPL v2
Group:		Development/Tools
Source0:	http://git.zx2c4.com/cgit/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	6682d597f6e3e76645a254c7be537bd3
Source1:	%{name}.conf
Source2:	%{name}-repo.conf
Source3:	%{name}-apache.conf
Patch0:		%{name}-system-git.patch
Patch1:		%{name}-git-2.0.3.patch
URL:		http://git.zx2c4.com/cgit/about/
BuildRequires:	git-core-devel >= 2.0.3
BuildRequires:	lua52-devel
BuildRequires:	openssl-devel
BuildConflicts:	zlib-devel = 1.2.5-1
Requires:	webapps
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		webapp		cgit
%define		webappdir	%{_sysconfdir}/webapps/%{webapp}
%define		appdir		%{_datadir}/%{webapp}
%define		cgibindir	%{_prefix}/lib/cgi-bin

%define         _noautoreqfiles %{_libdir}/cgit/filters

%description
Cgit is a CGI application implemented in C: it's basically (yet)
another git command, used to generate HTML. Cgit is not forking: all
git operations are performed by linking with libgit.a. It uses a
built-in cache: the generated HTML is stored on disk for the benefit
of later requests.

%description -l pl.UTF-8
Cgit to napisana w C aplikacja CGI - zasadniczo jest to (kolejny)
interfejs do gita, generujący kod HTML. Cgit jest aplikacją
nieforkującą - wszystkie operacje na repozytoriach wykonywane są z
użyciem biblioteki. Aplikacja ta korzysta z cache - wygenerowany kod
HTML zapisany jest na dysku dla kolejnych żądań.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
cp  %{_includedir}/git-core/{Makefile,config.*} git

%build
%{__make} \
	V=1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/git-core" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	LUA_PKGCONFIG=lua5.2 \
	CGIT_CONFIG="%{webappdir}/%{webapp}.conf" \
	CGIT_SCRIPT_PATH="%{cgibindir}"

%install
rm -rf $RPM_BUILD_ROOT

# The same CFLAGS as in %build  stage has to be passed to avoid
# "new build flags" logic in Makefile
%{__make} install \
	V=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	CFLAGS="%{rpmcflags} -I/usr/include/git-core" \
	CGIT_CONFIG="%{webappdir}/%{webapp}.conf" \
	CGIT_DATA_PATH="%{appdir}" \
	CGIT_SCRIPT_PATH="%{cgibindir}"

# cache
install -d $RPM_BUILD_ROOT/var/cache/cgit

# webapp stuff
install -d $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/apache.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{webapp}

%triggerin -- apache-base
%webapp_register httpd %{webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{webapp}

%files
%defattr(644,root,root,755)
%doc README cgitrc.5.txt
%dir %{webappdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/cgit.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/cgit-repo.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{webappdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{webappdir}/httpd.conf
%attr(755,root,root) %{cgibindir}/cgit.cgi
%attr(770,root,http) /var/cache/cgit
%{appdir}
%dir %{_prefix}/lib/cgit
%dir %{_prefix}/lib/cgit/filters
%attr(755,root,root) %{_prefix}/lib/cgit/filters/about-formatting.sh
%attr(755,root,root) %{_prefix}/lib/cgit/filters/commit-links.sh
%attr(655,root,root) %{_prefix}/lib/cgit/filters/email-gravatar.lua
%attr(755,root,root) %{_prefix}/lib/cgit/filters/email-gravatar.py
%attr(655,root,root) %{_prefix}/lib/cgit/filters/email-libravatar.lua
%attr(655,root,root) %{_prefix}/lib/cgit/filters/simple-authentication.lua
%attr(755,root,root) %{_prefix}/lib/cgit/filters/syntax-highlighting.py
%attr(755,root,root) %{_prefix}/lib/cgit/filters/syntax-highlighting.sh
%dir %{_prefix}/lib/cgit/filters/html-converters
%attr(755,root,root) %{_prefix}/lib/cgit/filters/html-converters/man2html
%attr(755,root,root) %{_prefix}/lib/cgit/filters/html-converters/md2html
%attr(755,root,root) %{_prefix}/lib/cgit/filters/html-converters/rst2html
%attr(755,root,root) %{_prefix}/lib/cgit/filters/html-converters/txt2html
%dir %{_prefix}/lib/cgit/filters/html-converters/resources
%attr(755,root,root) %{_prefix}/lib/cgit/filters/html-converters/resources/markdown.pl
%attr(655,root,root) %{_prefix}/lib/cgit/filters/html-converters/resources/rst-template.txt
