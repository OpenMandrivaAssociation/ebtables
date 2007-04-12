%define	name	ebtables
%define version 2.0.8
%define rcrel rc2
%define release %mkrel 0.%{rcrel}.2

Summary:	A filtering tool for a bridging firewall
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}-v%{version}-%{rcrel}.tar.bz2
Group:		System/Kernel and hardware
URL:		http://ebtables.sourceforge.net/
License:	GPL
#BuildRequires:  kernel-source >= 2.6.0
Requires:	kernel >= 2.6.0
BuildRoot:	%{_tmppath}/%{name}-v%{version}-root

%description
The ebtables program is a filtering tool for a bridging firewall.
The filtering is focussed on the Link Layer Ethernet frame fields.
Apart from filtering, it also gives the ability to alter the
Ethernet MAC addresses and implement a brouter. 

%prep

%setup -q -n %{name}-v%{version}-%{rcrel}

%build

#make CFLAGS="%{optflags} -fPIC" LIBDIR=/%{_lib}
%make CFLAGS="%{optflags}" static

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}/sbin
#install -d %{buildroot}/%{_lib}/ebtables

install -m644 ebtables.8 %{buildroot}%{_mandir}/man8/
install -m644 ethertypes %{buildroot}%{_sysconfdir}/
#install -m755 ebtables %{buildroot}/sbin/
install -m755 static %{buildroot}/sbin/ebtables
#install -m644 libebtc.so %{buildroot}/%{_lib}/ebtables/
#install -m644 extensions/*.so %{buildroot}/%{_lib}/ebtables/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc ChangeLog INSTALL THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ethertypes
%attr(0755,root,root) /sbin/ebtables
%attr(0644,root,root) %{_mandir}/man8/ebtables.8*
#attr(0755,root,root) %dir /%{_lib}/ebtables
#attr(0644,root,root) /%{_lib}/ebtables/*.so

