Summary:	Remote Server Monitoring and Management and KVM-over-IP
Name:		ipmiview
Version:	2.9.2
Release:	0.1
License:	unknown
Group:		Applications/System
Source0:	ftp://ftp.supermicro.com/utility/IPMIView/Jar/IPMIView20-Class_v%{version}_Build111110.zip
# Source0-md5:	561c4091e1062868ddf73e863ca051de
URL:		http://www.supermicro.com/
BuildRequires:	file
Requires:	jre-X11
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Remote Server Monitoring and Management and KVM-over-IP GUI.

%prep
%setup -q -c

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}}

want=32-bit
%ifarch %{x8664}
want=64-bit
%endif

for f in *.so; do
	file "$f" | grep -qi "${want}" && install -m755 "$f" $RPM_BUILD_ROOT%{_libdir}/%{name}
done

install *.jar *.jnilib $RPM_BUILD_ROOT%{_libdir}/%{name}

cat > $RPM_BUILD_ROOT%{_bindir}/ipmiview << 'EOF'
#!/bin/sh
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ipmiview"
[ ! -d "$CONFIG_DIR" ] && mkdir -p "$CONFIG_DIR"
cd "$CONFIG_DIR"
exec java -Djava.library.path=%{_libdir}/%{name} -jar %{_libdir}/%{name}/IPMIView20.jar
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/trapview << 'EOF'
#!/bin/sh
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ipmiview"
[ ! -d "$CONFIG_DIR" ] && mkdir -p "$CONFIG_DIR"
cd "$CONFIG_DIR"
exec java -Djava.library.path=%{_libdir}/%{name} -jar %{_libdir}/%{name}/TrapView.jar
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt *.pdf
%attr(755,root,root) %{_bindir}/ipmiview
%attr(755,root,root) %{_bindir}/trapview
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.jar
%{_libdir}/%{name}/*.jnilib
%attr(755,root,root) %{_libdir}/%{name}/*.so
